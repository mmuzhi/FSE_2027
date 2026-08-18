// ExcelProcessor.cpp — C++17
// Relies on miniz (single-header zip library) for the zip container handling that
// Apache POI performs internally; xlsx parts are read/written directly as XML.

#include <miniz.h>

#include <cctype>
#include <cmath>
#include <cstdlib>
#include <cstring>
#include <optional>
#include <stdexcept>
#include <string>
#include <variant>
#include <vector>

namespace org::example {

// Java `Object` here is only ever String, Integer, or null.
using CellValue = std::variant<std::monostate, std::string, int>;

namespace {

// Java `(int) double` cast semantics: NaN -> 0, saturate at INT_MIN/INT_MAX.
int javaIntCast(double d) {
    if (std::isnan(d)) return 0;
    if (d >= 2147483647.0) return 2147483647;
    if (d <= -2147483648.0) return -2147483648;
    return static_cast<int>(d);
}

std::string xmlEscape(const std::string& s) {
    std::string out;
    out.reserve(s.size());
    for (unsigned char c : s) {
        switch (c) {
            case '&': out += "&amp;";  break;
            case '<': out += "&lt;";   break;
            case '>': out += "&gt;";   break;
            case '"': out += "&quot;"; break;
            case '\'': out += "&apos;"; break;
            default:  out += static_cast<char>(c);
        }
    }
    return out;
}

std::string xmlUnescape(const std::string& s) {
    std::string out;
    out.reserve(s.size());
    for (size_t i = 0; i < s.size(); ++i) {
        if (s[i] != '&') { out += s[i]; continue; }
        size_t sc = s.find(';', i);
        if (sc == std::string::npos || sc - i > 10) { out += s[i]; continue; }
        std::string ent = s.substr(i + 1, sc - i - 1);
        if (ent == "amp")       out += '&';
        else if (ent == "lt")   out += '<';
        else if (ent == "gt")   out += '>';
        else if (ent == "quot") out += '"';
        else if (ent == "apos") out += '\'';
        else if (!ent.empty() && ent[0] == '#') {
            long code = -1;
            try {
                if (ent.size() > 1 && (ent[1] == 'x' || ent[1] == 'X'))
                    code = std::stol(ent.substr(2), nullptr, 16);
                else
                    code = std::stol(ent.substr(1));
            } catch (...) { code = -1; }
            if (code > 0 && code < 0x10000) {  // encode code point as UTF-8
                if (code < 0x80) {
                    out += static_cast<char>(code);
                } else if (code < 0x800) {
                    out += static_cast<char>(0xC0 | (code >> 6));
                    out += static_cast<char>(0x80 | (code & 0x3F));
                } else {
                    out += static_cast<char>(0xE0 | (code >> 12));
                    out += static_cast<char>(0x80 | ((code >> 6) & 0x3F));
                    out += static_cast<char>(0x80 | (code & 0x3F));
                }
            }
        } else { out += s[i]; continue; }
        i = sc;  // consume through ';'
    }
    return out;
}

// Inner text of the first <tag ...>...</tag>; empty if absent or self-closing.
std::string innerTag(const std::string& s, const std::string& tag) {
    std::string open = "<" + tag;
    size_t a = s.find(open);
    if (a == std::string::npos) return "";
    size_t gt = s.find('>', a);
    if (gt == std::string::npos || s[gt - 1] == '/') return "";
    std::string cl = "</" + tag + ">";
    size_t b = s.find(cl, gt);
    if (b == std::string::npos) return "";
    return xmlUnescape(s.substr(gt + 1, b - gt - 1));
}

// Concatenated text of every <t>...</t> in the fragment (handles rich text runs).
std::string collectText(const std::string& s) {
    std::string out;
    size_t pos = 0;
    while (true) {
        size_t t1 = s.find("<t", pos);
        if (t1 == std::string::npos) break;
        size_t gt = s.find('>', t1);
        if (gt == std::string::npos) break;
        if (s[gt - 1] == '/') { pos = gt + 1; continue; }  // <t/>
        size_t end = s.find("</t>", gt);
        if (end == std::string::npos) break;
        out += xmlUnescape(s.substr(gt + 1, end - gt - 1));
        pos = end + 4;
    }
    return out;
}

std::vector<std::string> parseSharedStrings(const std::string& xml) {
    std::vector<std::string> out;
    size_t pos = 0;
    while (true) {
        size_t a = xml.find("<si", pos);
        if (a == std::string::npos) break;
        size_t gt = xml.find('>', a);
        if (gt == std::string::npos) break;
        if (xml[gt - 1] == '/') { out.push_back(""); pos = gt + 1; continue; }
        size_t b = xml.find("</si>", gt);
        if (b == std::string::npos) break;
        out.push_back(collectText(xml.substr(gt + 1, b - gt - 1)));
        pos = b + 5;
    }
    return out;
}

// Maps <c> entries to the same cases as the Java switch:
// STRING -> string, NUMERIC -> (int) value, everything else (blank/bool/error/formula) -> null.
void parseCells(const std::string& body, const std::vector<std::string>& shared,
                std::vector<CellValue>& out) {
    size_t pos = 0;
    while (true) {
        size_t cs = body.find("<c", pos);
        if (cs == std::string::npos) break;
        size_t ce = body.find('>', cs);
        if (ce == std::string::npos) break;
        std::string openTag = body.substr(cs, ce - cs + 1);
        bool selfClose = openTag.size() >= 2 && openTag[openTag.size() - 2] == '/';
        std::string cellBody;
        if (selfClose) {
            pos = ce + 1;
        } else {
            size_t cc = body.find("</c>", ce);
            if (cc == std::string::npos) { cellBody = body.substr(ce + 1); pos = body.size(); }
            else { cellBody = body.substr(ce + 1, cc - ce - 1); pos = cc + 4; }
        }
        std::string t;  // "t" attribute
        {
            size_t p = openTag.find(" t=\"");
            if (p != std::string::npos) {
                size_t q = openTag.find('"', p + 4);
                if (q != std::string::npos) t = openTag.substr(p + 4, q - p - 4);
            }
        }
        if (!selfClose && cellBody.find("<f") != std::string::npos) {
            out.push_back(std::monostate{});                       // FORMULA -> default branch
        } else if (t == "s") {                                     // shared string
            long idx = std::strtol(innerTag(cellBody, "v").c_str(), nullptr, 10);
            out.push_back(idx >= 0 && idx < static_cast<long>(shared.size())
                              ? CellValue(shared[static_cast<size_t>(idx)])
                              : CellValue(std::monostate{}));
        } else if (t == "inlineStr") {                             // inline string
            out.push_back(CellValue(collectText(cellBody)));
        } else if (t == "str") {                                   // formula string result
            out.push_back(CellValue(innerTag(cellBody, "v")));
        } else if (t == "b" || t == "e") {                         // BOOLEAN / ERROR -> null
            out.push_back(std::monostate{});
        } else {                                                   // NUMERIC / BLANK
            std::string v = innerTag(cellBody, "v");
            if (v.empty()) out.push_back(std::monostate{});        // BLANK -> null
            else out.push_back(CellValue(javaIntCast(std::strtod(v.c_str(), nullptr))));
        }
    }
}

std::vector<std::vector<CellValue>> parseSheet(const std::string& xml,
                                               const std::vector<std::string>& shared) {
    std::vector<std::vector<CellValue>> rows;
    size_t pos = 0;
    while (true) {
        size_t rs = xml.find("<row", pos);
        if (rs == std::string::npos) break;
        size_t re = xml.find('>', rs);
        if (re == std::string::npos) break;
        std::string body;
        if (xml[re - 1] == '/') {
            pos = re + 1;
        } else {
            size_t close = xml.find("</row>", re);
            if (close == std::string::npos) { body = xml.substr(re + 1); pos = xml.size(); }
            else { body = xml.substr(re + 1, close - re - 1); pos = close + 6; }
        }
        std::vector<CellValue> rowData;
        parseCells(body, shared, rowData);
        rows.push_back(std::move(rowData));
    }
    return rows;
}

std::string colName(size_t idx) {  // 0-based -> "A", "B", ..., "AA", ...
    std::string s;
    long n = static_cast<long>(idx) + 1;
    while (n > 0) {
        long r = (n - 1) % 26;
        s.insert(s.begin(), static_cast<char>('A' + r));
        n = (n - 1) / 26;
    }
    return s;
}

// Java String.toUpperCase() (ASCII/default-locale range).
std::string toUpper(const std::string& s) {
    std::string out = s;
    for (char& c : out) c = static_cast<char>(std::toupper(static_cast<unsigned char>(c)));
    return out;
}

// Java String.replace replaces every occurrence.
std::string replaceAll(std::string s, const std::string& from, const std::string& to) {
    if (from.empty()) return s;
    size_t pos = 0;
    while ((pos = s.find(from, pos)) != std::string::npos) {
        s.replace(pos, from.size(), to);
        pos += to.size();
    }
    return s;
}

bool zipReadFile(mz_zip_archive& zip, const char* name, std::string& out) {
    int idx = mz_zip_reader_locate_file(&zip, name, nullptr, 0);
    if (idx < 0) return false;
    size_t sz = 0;
    void* p = mz_zip_reader_extract_to_heap(&zip, idx, &sz, 0);
    if (!p) return false;
    out.assign(static_cast<char*>(p), sz);
    mz_free(p);
    return true;
}

const char* kContentTypes =
    "<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"yes\"?>\n"
    "<Types xmlns=\"http://schemas.openxmlformats.org/package/2006/content-types\">"
    "<Default Extension=\"rels\" ContentType=\"application/vnd.openxmlformats-package.relationships+xml\"/>"
    "<Default Extension=\"xml\" ContentType=\"application/xml\"/>"
    "<Override PartName=\"/xl/workbook.xml\" ContentType=\"application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml\"/>"
    "<Override PartName=\"/xl/worksheets/sheet1.xml\" ContentType=\"application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml\"/>"
    "</Types>";

const char* kRootRels =
    "<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"yes\"?>\n"
    "<Relationships xmlns=\"http://schemas.openxmlformats.org/package/2006/relationships\">"
    "<Relationship Id=\"rId1\" Type=\"http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument\" Target=\"xl/workbook.xml\"/>"
    "</Relationships>";

const char* kWorkbookXml =
    "<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"yes\"?>\n"
    "<workbook xmlns=\"http://schemas.openxmlformats.org/spreadsheetml/2006/main\" "
    "xmlns:r=\"http://schemas.openxmlformats.org/officeDocument/2006/relationships\">"
    "<sheets><sheet name=\"Sheet1\" sheetId=\"1\" r:id=\"rId1\"/></sheets>"
    "</workbook>";

const char* kWorkbookRels =
    "<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"yes\"?>\n"
    "<Relationships xmlns=\"http://schemas.openxmlformats.org/package/2006/relationships\">"
    "<Relationship Id=\"rId1\" Type=\"http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet\" Target=\"worksheets/sheet1.xml\"/>"
    "</Relationships>";

}  // namespace

class ExcelProcessor {
public:
    ExcelProcessor() = default;

    // Java returns null on IOException -> std::nullopt here.
    std::optional<std::vector<std::vector<CellValue>>> readExcel(const std::string& fileName) {
        mz_zip_archive zip;
        memset(&zip, 0, sizeof(zip));
        if (!mz_zip_reader_init_file(&zip, fileName.c_str(), 0)) {
            return std::nullopt;  // unreadable/invalid file -> null
        }
        std::string ssXml, sheetXml;
        bool hasSs = zipReadFile(zip, "xl/sharedStrings.xml", ssXml);
        bool hasSheet = zipReadFile(zip, "xl/worksheets/sheet1.xml", sheetXml);  // getSheetAt(0)
        mz_zip_reader_end(&zip);
        if (!hasSheet) return std::nullopt;

        std::vector<std::string> shared;
        if (hasSs) shared = parseSharedStrings(ssXml);
        return parseSheet(sheetXml, shared);
    }

    // Java returns false on IOException; only String/Integer cells get a value,
    // other cells are created but left blank.
    bool writeExcel(const std::vector<std::vector<CellValue>>& data, const std::string& fileName) {
        std::string sheetXml =
            "<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"yes\"?>\n"
            "<worksheet xmlns=\"http://schemas.openxmlformats.org/spreadsheetml/2006/main\">"
            "<sheetData>";
        for (size_t i = 0; i < data.size(); ++i) {
            const std::vector<CellValue>& rowData = data[i];
            sheetXml += "<row r=\"" + std::to_string(i + 1) + "\">";
            for (size_t j = 0; j < rowData.size(); ++j) {
                const std::string ref = colName(j) + std::to_string(i + 1);
                if (const std::string* s = std::get_if<std::string>(&rowData[j])) {
                    sheetXml += "<c r=\"" + ref + "\" t=\"inlineStr\"><is><t xml:space=\"preserve\">"
                              + xmlEscape(*s) + "</t></is></c>";
                } else if (const int* n = std::get_if<int>(&rowData[j])) {
                    sheetXml += "<c r=\"" + ref + "\"><v>" + std::to_string(*n) + "</v></c>";
                } else {
                    sheetXml += "<c r=\"" + ref + "\"/>";  // blank cell, still created
                }
            }
            sheetXml += "</row>";
        }
        sheetXml += "</sheetData></worksheet>";

        mz_zip_archive zip;
        memset(&zip, 0, sizeof(zip));
        if (!mz_zip_writer_init_file(&zip, fileName.c_str(), 0)) return false;  // IOException -> false
        bool ok = true;
        ok = ok && mz_zip_writer_add_mem(&zip, "[Content_Types].xml", kContentTypes,
                                         std::strlen(kContentTypes), MZ_DEFAULT_COMPRESSION) != 0;
        ok = ok && mz_zip_writer_add_mem(&zip, "_rels/.rels", kRootRels,
                                         std::strlen(kRootRels), MZ_DEFAULT_COMPRESSION) != 0;
        ok = ok && mz_zip_writer_add_mem(&zip, "xl/workbook.xml", kWorkbookXml,
                                         std::strlen(kWorkbookXml), MZ_DEFAULT_COMPRESSION) != 0;
        ok = ok && mz_zip_writer_add_mem(&zip, "xl/_rels/workbook.xml.rels", kWorkbookRels,
                                         std::strlen(kWorkbookRels), MZ_DEFAULT_COMPRESSION) != 0;
        ok = ok && mz_zip_writer_add_mem(&zip, "xl/worksheets/sheet1.xml", sheetXml.data(),
                                         sheetXml.size(), MZ_DEFAULT_COMPRESSION) != 0;
        ok = ok && mz_zip_writer_finalize_archive(&zip) != 0;
        mz_zip_writer_end(&zip);
        return ok;
    }

    // Java returns null on failure -> std::nullopt here.
    std::optional<std::string> processExcelData(int N, const std::string& saveFileName) {
        auto dataOpt = readExcel(saveFileName);
        // Short-circuit preserved: at(0) mirrors data.get(0) throwing
        // IndexOutOfBoundsException when the list is empty (std::out_of_range).
        if (!dataOpt || N >= static_cast<int>(dataOpt->at(0).size())) {
            return std::nullopt;
        }
        std::vector<std::vector<CellValue>> newData;
        newData.reserve(dataOpt->size());
        for (const std::vector<CellValue>& row : *dataOpt) {
            std::vector<CellValue> newRow(row);
            const CellValue& value = row.at(N);  // mirrors row.get(N) bounds exception
            if (const std::string* s = std::get_if<std::string>(&value)) {
                newRow.push_back(toUpper(*s));
            } else {
                newRow.push_back(value);
            }
            newData.push_back(std::move(newRow));
        }
        std::string newFileName = replaceAll(saveFileName, ".xlsx", "_process.xlsx");
        bool success = writeExcel(newData, newFileName);
        return success ? std::optional<std::string>(newFileName) : std::nullopt;
    }
};

}  // namespace org::example