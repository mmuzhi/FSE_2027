/*
# This is a compressed file processing class that provides the ability
# to read and decompress compressed files.
#
# Requires the minizip contrib library of zlib (zip.h / unzip.h).
*/

#include <cstdio>
#include <cstring>
#include <ctime>
#include <string>
#include <vector>
#include <sys/stat.h>
#include <sys/types.h>

#ifdef _WIN32
#  include <direct.h>
#else
#  include <unistd.h>
#endif

extern "C" {
#include "zlib.h"
#include "unzip.h"
#include "zip.h"
}

namespace {

bool path_exists(const std::string& p) {
    struct stat st;
    return ::stat(p.c_str(), &st) == 0;
}

bool make_dir(const std::string& p) {
#ifdef _WIN32
    return _mkdir(p.c_str()) == 0;
#else
    return ::mkdir(p.c_str(), 0777) == 0;
#endif
}

/* mkdir -p equivalent (creates every missing component). */
void make_dirs(const std::string& path) {
    if (path.empty()) return;
    std::string cur;
    size_t i = 0;
    const size_t n = path.size();
    if (path[0] == '/') { cur = "/"; i = 1; }
    while (i < n) {
        size_t j = path.find('/', i);
        if (j == std::string::npos) j = n;
        const std::string part = path.substr(i, j - i);
        if (!part.empty()) {
            if (cur.empty()) cur = part;
            else { if (cur != "/") cur += '/'; cur += part; }
            if (!path_exists(cur)) make_dir(cur);
        }
        i = j + 1;
    }
}

std::string join_path(const std::string& a, const std::string& b) {
    if (a.empty()) return b;
    if (b.empty()) return a;
    if (a.back() == '/') return a + b;
    return a + "/" + b;
}

std::string dir_name(const std::string& path) {
    const size_t pos = path.find_last_of('/');
    if (pos == std::string::npos) return "";
    if (pos == 0) return "/";
    return path.substr(0, pos);
}

/* Python zipfile.extract(): drop '', '.' and '..' components / leading separators. */
std::string sanitize_member_name(const std::string& name) {
    std::string joined;
    size_t i = 0;
    const size_t n = name.size();
    while (i < n) {
        size_t j = i;
        while (j < n && name[j] != '/' && name[j] != '\\') ++j;
        const std::string part = name.substr(i, j - i);
        if (!part.empty() && part != "." && part != "..") {
            if (!joined.empty()) joined += '/';
            joined += part;
        }
        i = j + 1;
    }
    return joined;
}

/* Python zipfile.write(): os.path.normpath + strip leading separators. */
std::string normalize_arcname(const std::string& path) {
    std::string p = path;
#ifdef _WIN32
    for (char& c : p) if (c == '\\') c = '/';
#endif
    std::vector<std::string> parts;
    size_t i = 0;
    const size_t n = p.size();
    while (i < n) {
        size_t j = p.find('/', i);
        if (j == std::string::npos) j = n;
        const std::string part = p.substr(i, j - i);
        if (part.empty() || part == ".") { /* skip */ }
        else if (part == "..") { if (!parts.empty()) parts.pop_back(); }
        else parts.push_back(part);
        i = j + 1;
    }
    std::string out;
    for (const std::string& part : parts) {
        if (!out.empty()) out += '/';
        out += part;
    }
    return out;
}

/* Extract the current entry of an open archive into output_path. */
bool extract_current_file(unzFile zf, const std::string& output_path) {
    unz_file_info info;
    char raw[1024];
    if (unzGetCurrentFileInfo(zf, &info, raw, sizeof(raw), NULL, 0, NULL, 0) != UNZ_OK)
        return false;
    const std::string entry(raw, strnlen(raw, sizeof(raw)));
    const std::string safe = sanitize_member_name(entry);
    const std::string dest = join_path(output_path, safe);

    const bool is_dir = !entry.empty() && entry.back() == '/';
    if (is_dir) {
        if (!dest.empty()) make_dirs(dest);
        return true;
    }

    const std::string parent = dir_name(dest);
    if (!parent.empty()) make_dirs(parent);

    FILE* out = std::fopen(dest.c_str(), "wb");
    if (!out) return false;

    bool ok = true;
    if (unzOpenCurrentFile(zf) == UNZ_OK) {
        char buf[8192];
        int n = 0;
        while ((n = unzReadCurrentFile(zf, buf, sizeof(buf))) > 0) {
            if (std::fwrite(buf, 1u, static_cast<size_t>(n), out) != static_cast<size_t>(n)) {
                ok = false;
                break;
            }
        }
        if (n < 0) ok = false;                            /* stream error */
        if (unzCloseCurrentFile(zf) != UNZ_OK) ok = false; /* e.g. CRC error */
    } else {
        ok = false;
    }
    std::fclose(out);
    return ok;
}

} // namespace

class ZipFileProcessor {
public:
    /*
     * Initialize file name
     * :param file_name: string
     */
    explicit ZipFileProcessor(std::string file_name)
        : file_name(std::move(file_name)) {}

    /*
     * Get open file object
     * :return: If successful, returns the open file handle; otherwise, returns nullptr
     */
    unzFile read_zip_file() const {
        /* bare `except:` in Python maps to: any failure -> nullptr */
        return unzOpen(file_name.c_str());
    }

    /*
     * Extract all zip files and place them in the specified path
     * :param output_path: string, The location of the extracted file
     * :return: True or False, representing whether the extraction operation was successful
     */
    bool extract_all(const std::string& output_path) const {
        unzFile zf = unzOpen(file_name.c_str());
        if (zf == NULL) return false;
        bool ok = true;
        int err = unzGoToFirstFile(zf);
        while (err == UNZ_OK) {
            if (!extract_current_file(zf, output_path)) { ok = false; break; }
            err = unzGoToNextFile(zf);
        }
        if (ok && err != UNZ_END_OF_LIST_OF_FILE) ok = false; /* empty archive still succeeds */
        unzClose(zf);
        return ok;
    }

    /*
     * Extract the file with the specified name from the zip file
     * and place it in the specified path
     * :param file_name: string, The name of the file to be uncompressed
     * :param output_path: string, The location of the extracted file
     * :return: True or False, representing whether the extraction operation was successful
     */
    bool extract_file(const std::string& file_name, const std::string& output_path) const {
        unzFile zf = unzOpen(this->file_name.c_str());
        if (zf == NULL) return false;
        /* missing member -> KeyError in Python -> False */
        const bool ok = unzLocateFile(zf, file_name.c_str(), 0) == UNZ_OK &&
                        extract_current_file(zf, output_path);
        unzClose(zf);
        return ok;
    }

    /*
     * Compress the specified file list into a zip file and place it
     * in the specified path
     * :param files: list of string, List of files to compress
     * :param output_file_name: string, Specified output path
     * :return: True or False, representing whether the compression operation was successful
     */
    bool create_zip_file(const std::vector<std::string>& files,
                         const std::string& output_file_name) const {
        /* 'w' mode: create/truncate the archive first, as zipfile.ZipFile does */
        zipFile zf = zipOpen(output_file_name.c_str(), APPEND_STATUS_CREATE);
        if (zf == NULL) return false;

        for (const std::string& file : files) {
            struct stat st;
            if (::stat(file.c_str(), &st) != 0) { zipClose(zf, NULL); return false; }
            FILE* in = std::fopen(file.c_str(), "rb");
            if (!in) { zipClose(zf, NULL); return false; }

            zip_fileinfo zinfo;
            std::memset(&zinfo, 0, sizeof(zinfo));
            struct tm* mt = localtime(&st.st_mtime);
            if (mt != NULL) {
                zinfo.tmz_date.tm_year = static_cast<uInt>(mt->tm_year + 1900);
                zinfo.tmz_date.tm_mon  = static_cast<uInt>(mt->tm_mon + 1);
                zinfo.tmz_date.tm_mday = static_cast<uInt>(mt->tm_mday);
                zinfo.tmz_date.tm_hour = static_cast<uInt>(mt->tm_hour);
                zinfo.tmz_date.tm_min  = static_cast<uInt>(mt->tm_min);
                zinfo.tmz_date.tm_sec  = static_cast<uInt>(mt->tm_sec);
            }

            const std::string arcname = normalize_arcname(file);
            /* Python default compression is ZIP_STORED -> method 0 */
            if (zipOpenNewFileInZip(zf, arcname.c_str(), &zinfo,
                                    NULL, 0, NULL, 0, NULL, 0, 0) != ZIP_OK) {
                std::fclose(in);
                zipClose(zf, NULL);
                return false;
            }

            bool ok = true;
            char buf[8192];
            size_t r;
            while ((r = std::fread(buf, 1, sizeof(buf), in)) > 0) {
                if (zipWriteInFileInZip(zf, buf, static_cast<unsigned>(r)) != ZIP_OK) {
                    ok = false;
                    break;
                }
            }
            if (std::ferror(in)) ok = false;
            std::fclose(in);
            if (!ok || zipCloseFileInZip(zf) != ZIP_OK) { zipClose(zf, NULL); return false; }
        }
        return zipClose(zf, NULL) == ZIP_OK;
    }

private:
    std::string file_name;
};