#include <cctype>
#include <fstream>
#include <iterator>
#include <memory>
#include <optional>
#include <stdexcept>
#include <string>
#include <utility>
#include <vector>

// ---------------------------------------------------------------------------
// Minimal XML element model mirroring xml.etree.ElementTree.Element semantics
// that the original Python code relies on (tag, text, tail, attributes,
// children, recursive iter(), child-only findall()).
// ---------------------------------------------------------------------------
class XMLElement {
public:
    std::string tag;
    std::optional<std::string> text;   // nullopt == None in Python
    std::optional<std::string> tail;
    std::vector<std::pair<std::string, std::string>> attributes;
    std::vector<std::unique_ptr<XMLElement>> children;

    // ET's Element.iter(tag): depth-first over self and all descendants.
    void iter(const std::string& name, std::vector<XMLElement*>& out) {
        if (tag == name) out.push_back(this);
        for (const auto& child : children) child->iter(name, out);
    }

    // ET's Element.findall(name) with a plain tag: direct children only.
    std::vector<XMLElement*> findall(const std::string& name) const {
        std::vector<XMLElement*> found;
        for (const auto& child : children)
            if (child->tag == name) found.push_back(child.get());
        return found;
    }
};

// ---------------------------------------------------------------------------
// Helpers: entity decoding / escaping (mirrors ElementTree write behavior).
// ---------------------------------------------------------------------------
static void append_utf8(std::string& out, long cp) {
    if (cp < 0x80) {
        out += static_cast<char>(cp);
    } else if (cp < 0x800) {
        out += static_cast<char>(0xC0 | (cp >> 6));
        out += static_cast<char>(0x80 | (cp & 0x3F));
    } else if (cp < 0x10000) {
        out += static_cast<char>(0xE0 | (cp >> 12));
        out += static_cast<char>(0x80 | ((cp >> 6) & 0x3F));
        out += static_cast<char>(0x80 | (cp & 0x3F));
    } else {
        out += static_cast<char>(0xF0 | (cp >> 18));
        out += static_cast<char>(0x80 | ((cp >> 12) & 0x3F));
        out += static_cast<char>(0x80 | ((cp >> 6) & 0x3F));
        out += static_cast<char>(0x80 | (cp & 0x3F));
    }
}

static std::string decode_entities(const std::string& in) {
    std::string out;
    out.reserve(in.size());
    for (std::size_t i = 0; i < in.size(); ++i) {
        if (in[i] != '&') { out += in[i]; continue; }
        std::size_t semi = in.find(';', i + 1);
        if (semi == std::string::npos || semi - i > 12) { out += in[i]; continue; }
        std::string ent = in.substr(i + 1, semi - i - 1);
        bool ok = true;
        if (ent == "lt") out += '<';
        else if (ent == "gt") out += '>';
        else if (ent == "amp") out += '&';
        else if (ent == "quot") out += '"';
        else if (ent == "apos") out += '\'';
        else if (!ent.empty() && ent[0] == '#') {
            long cp = 0;
            try {
                if (ent.size() > 1 && (ent[1] == 'x' || ent[1] == 'X'))
                    cp = std::stol(ent.substr(2), nullptr, 16);
                else
                    cp = std::stol(ent.substr(1));
            } catch (...) { ok = false; }
            if (ok && cp > 0 && cp <= 0x10FFFF) append_utf8(out, cp);
            else ok = false;
        } else ok = false;
        if (ok) i = semi;
        else out += in[i];
    }
    return out;
}

static std::string escape_cdata(const std::string& in) {
    std::string out;
    out.reserve(in.size());
    for (char ch : in) {
        switch (ch) {
            case '&': out += "&amp;"; break;
            case '<': out += "&lt;"; break;
            case '>': out += "&gt;"; break;
            default: out += ch;
        }
    }
    return out;
}

static std::string escape_attrib(const std::string& in) {
    std::string out;
    out.reserve(in.size());
    for (char ch : in) {
        switch (ch) {
            case '&': out += "&amp;"; break;
            case '<': out += "&lt;"; break;
            case '>': out += "&gt;"; break;
            case '"': out += "&quot;"; break;
            case '\t': out += "&#09;"; break;
            case '\n': out += "&#10;"; break;
            case '\r': out += "&#13;"; break;
            default: out += ch;
        }
    }
    return out;
}

static void serialize_element(const XMLElement& e, std::string& out) {
    out += '<';
    out += e.tag;
    for (const auto& kv : e.attributes) {
        out += ' ';
        out += kv.first;
        out += "=\"";
        out += escape_attrib(kv.second);
        out += '"';
    }
    if (e.children.empty() && !e.text.has_value()) {
        out += " />";
        return;
    }
    out += '>';
    if (e.text.has_value()) out += escape_cdata(*e.text);
    for (const auto& c : e.children) {
        serialize_element(*c, out);
        if (c->tail.has_value()) out += escape_cdata(*c->tail);
    }
    out += "</";
    out += e.tag;
    out += '>';
}

static std::string str_upper(const std::string& in) {
    std::string out = in;
    for (auto& ch : out)
        ch = static_cast<char>(std::toupper(static_cast<unsigned char>(ch)));
    return out;
}

// ---------------------------------------------------------------------------
// Small lenient XML parser (comments / PIs / DOCTYPE / CDATA handled the way
// ElementTree's default parser treats them: skipped, CDATA joins char data).
// ---------------------------------------------------------------------------
class XMLParser {
public:
    explicit XMLParser(const std::string& src) : s_(src), pos_(0) {}

    std::unique_ptr<XMLElement> parse() {
        skip_bom();
        skip_misc();
        if (pos_ >= s_.size() || s_[pos_] != '<')
            throw std::runtime_error("syntax error: no root element");
        return parse_element();
    }

private:
    const std::string& s_;
    std::size_t pos_;

    static bool is_name_char(char c) {
        return std::isalnum(static_cast<unsigned char>(c)) ||
               c == '_' || c == '-' || c == '.' || c == ':';
    }

    void skip_bom() {
        if (s_.compare(0, 3, "\xEF\xBB\xBF") == 0) pos_ = 3;
    }

    void skip_ws() {
        while (pos_ < s_.size() && std::isspace(static_cast<unsigned char>(s_[pos_]))) ++pos_;
    }

    void skip_until(const std::string& tok) {
        std::size_t end = s_.find(tok, pos_);
        pos_ = (end == std::string::npos) ? s_.size() : end + tok.size();
    }

    void skip_doctype() {
        pos_ += 9; // "<!DOCTYPE"
        int depth = 0;
        bool sq = false, dq = false;
        while (pos_ < s_.size()) {
            char c = s_[pos_];
            if (sq) { if (c == '\'') sq = false; }
            else if (dq) { if (c == '"') dq = false; }
            else if (c == '\'') sq = true;
            else if (c == '"') dq = true;
            else if (c == '[') ++depth;
            else if (c == ']') --depth;
            else if (c == '>' && depth <= 0) { ++pos_; return; }
            ++pos_;
        }
    }

    void skip_misc() {
        while (pos_ < s_.size()) {
            skip_ws();
            if (pos_ >= s_.size()) break;
            if (s_.compare(pos_, 2, "<?") == 0) skip_until("?>");
            else if (s_.compare(pos_, 4, "<!--") == 0) skip_until("-->");
            else if (s_.compare(pos_, 9, "<!DOCTYPE") == 0) skip_doctype();
            else break;
        }
    }

    void expect(char c) {
        if (pos_ >= s_.size() || s_[pos_] != c)
            throw std::runtime_error("syntax error: unexpected token");
        ++pos_;
    }

    std::string read_name() {
        std::size_t start = pos_;
        while (pos_ < s_.size() && is_name_char(s_[pos_])) ++pos_;
        if (pos_ == start) throw std::runtime_error("syntax error: expected name");
        return s_.substr(start, pos_ - start);
    }

    std::string read_attr_value() {
        if (pos_ < s_.size() && (s_[pos_] == '"' || s_[pos_] == '\'')) {
            char q = s_[pos_++];
            std::size_t start = pos_;
            while (pos_ < s_.size() && s_[pos_] != q) ++pos_;
            if (pos_ >= s_.size()) throw std::runtime_error("unterminated attribute value");
            std::string v = s_.substr(start, pos_ - start);
            ++pos_;
            return v;
        }
        std::size_t start = pos_;
        while (pos_ < s_.size() && !std::isspace(static_cast<unsigned char>(s_[pos_])) &&
               s_[pos_] != '>' && s_[pos_] != '/') ++pos_;
        return s_.substr(start, pos_ - start);
    }

    // Character data until the next real tag; comments/PIs skipped, CDATA kept.
    std::string read_char_data() {
        std::string raw;
        while (pos_ < s_.size()) {
            if (s_[pos_] == '<') {
                if (s_.compare(pos_, 4, "<!--") == 0) { skip_until("-->"); continue; }
                if (s_.compare(pos_, 2, "<?") == 0) { skip_until("?>"); continue; }
                if (s_.compare(pos_, 9, "<![CDATA[") == 0) {
                    std::size_t start = pos_ + 9;
                    std::size_t end = s_.find("]]>", start);
                    if (end == std::string::npos) {
                        raw.append(s_, start, s_.size() - start);
                        pos_ = s_.size();
                    } else {
                        raw.append(s_, start, end - start);
                        pos_ = end + 3;
                    }
                    continue;
                }
                break; // real tag
            }
            raw += s_[pos_++];
        }
        return decode_entities(raw);
    }

    std::unique_ptr<XMLElement> parse_element() {
        expect('<');
        auto e = std::make_unique<XMLElement>();
        e->tag = read_name();
        while (true) {
            skip_ws();
            if (pos_ >= s_.size()) throw std::runtime_error("unexpected end of input");
            if (s_.compare(pos_, 2, "/>") == 0) { pos_ += 2; return e; }
            if (s_[pos_] == '>') { ++pos_; break; }
            std::string key = read_name();
            skip_ws();
            std::string val;
            if (pos_ < s_.size() && s_[pos_] == '=') { ++pos_; skip_ws(); val = read_attr_value(); }
            e->attributes.emplace_back(std::move(key), decode_entities(val));
        }
        // ET: text is None when there is no character data before the first child.
        std::string text = read_char_data();
        if (!text.empty()) e->text = std::move(text);
        while (pos_ < s_.size() && s_.compare(pos_, 2, "</") != 0) {
            e->children.push_back(parse_element());
            std::string tail = read_char_data();
            if (!tail.empty()) e->children.back()->tail = std::move(tail);
        }
        if (pos_ >= s_.size() || s_.compare(pos_, 2, "</") != 0)
            throw std::runtime_error("mismatched tag");
        pos_ += 2;
        read_name(); // closing tag name (assumed matching, like ET's lenient use here)
        skip_ws();
        expect('>');
        return e;
    }
};

// ---------------------------------------------------------------------------
// Translated class.
// ---------------------------------------------------------------------------
class XMLProcessor {
public:
    explicit XMLProcessor(std::string file_name)
        : file_name_(std::move(file_name)), root_(nullptr) {}

    XMLElement* read_xml() {
        try {
            std::ifstream in(file_name_, std::ios::binary);
            if (!in) return nullptr;
            std::string content((std::istreambuf_iterator<char>(in)),
                                std::istreambuf_iterator<char>());
            in.close();
            XMLParser parser(content);
            auto root = parser.parse();       // may throw; root_ stays unchanged
            root_ = std::move(root);          // only assigned on success (like Python)
            return root_.get();
        } catch (...) {
            return nullptr;
        }
    }

    bool write_xml(const std::string& file_name) {
        try {
            if (!root_) return false; // ET raises on serializing None -> caught -> False
            std::string out;
            serialize_element(*root_, out);
            std::ofstream f(file_name, std::ios::binary | std::ios::trunc);
            if (!f) return false;
            f.write(out.data(), static_cast<std::streamsize>(out.size()));
            if (!f) return false;
            f.close();
            return true;
        } catch (...) {
            return false;
        }
    }

    bool process_xml_data(const std::string& file_name) {
        // Python: self.root.iter(...) on None raises AttributeError (uncaught).
        if (!root_)
            throw std::runtime_error("AttributeError: 'NoneType' object has no attribute 'iter'");
        std::vector<XMLElement*> items;
        root_->iter("item", items);
        for (XMLElement* element : items) {
            // Python: None.upper() raises AttributeError (uncaught).
            if (!element->text.has_value())
                throw std::runtime_error("AttributeError: 'NoneType' object has no attribute 'upper'");
            element->text = str_upper(*element->text);
        }
        return write_xml(file_name);
    }

    std::vector<XMLElement*> find_element(const std::string& element_name) {
        // Python: self.root.findall(...) on None raises AttributeError (uncaught).
        if (!root_)
            throw std::runtime_error("AttributeError: 'NoneType' object has no attribute 'findall'");
        return root_->findall(element_name);
    }

private:
    std::string file_name_;
    std::unique_ptr<XMLElement> root_;
};