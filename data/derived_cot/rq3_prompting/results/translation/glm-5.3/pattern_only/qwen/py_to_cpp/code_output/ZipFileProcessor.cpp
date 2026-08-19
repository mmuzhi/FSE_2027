// C++ port of the Python ZipFileProcessor, built on libzip (#include <zip.h>, link with -lzip).
// Semantics preserved: read_zip_file() returns an open zip object or a null one (None);
// extract/extract-all/create return true on success and false on any failure,
// mirroring the Python bare `except:` blocks.

#include <zip.h>

#include <cstdint>
#include <filesystem>
#include <fstream>
#include <memory>
#include <stdexcept>
#include <string>
#include <system_error>
#include <vector>

namespace fs = std::filesystem;

class ZipFileProcessor {
public:
    explicit ZipFileProcessor(std::string file_name)
        : file_name_(std::move(file_name)) {}

    // RAII counterpart of a Python zipfile.ZipFile object:
    // owns the libzip handle and closes it on destruction.
    class ZipFile {
    public:
        explicit ZipFile(zip_t* handle = nullptr) : handle_(handle) {}
        ~ZipFile() { reset(); }
        ZipFile(const ZipFile&) = delete;
        ZipFile& operator=(const ZipFile&) = delete;
        ZipFile(ZipFile&& other) noexcept : handle_(other.handle_) {
            other.handle_ = nullptr;
        }
        ZipFile& operator=(ZipFile&& other) noexcept {
            if (this != &other) {
                reset();
                handle_ = other.handle_;
                other.handle_ = nullptr;
            }
            return *this;
        }
        void reset() {
            if (handle_) {
                zip_discard(handle_);  // read-only archive: close == discard
                handle_ = nullptr;
            }
        }
        zip_t* get() const { return handle_; }
        explicit operator bool() const { return handle_ != nullptr; }

    private:
        zip_t* handle_;
    };

    // If successful, returns the open zip file object; otherwise nullptr (None).
    std::unique_ptr<ZipFile> read_zip_file() const {
        int error_code = 0;
        zip_t* handle = zip_open(file_name_.c_str(), ZIP_RDONLY, &error_code);
        if (handle == nullptr) {
            return nullptr;  // Python: bare except -> return None
        }
        return std::make_unique<ZipFile>(handle);
    }

    // Extract the whole archive into output_path; true on success, false otherwise.
    bool extract_all(const std::string& output_path) const {
        try {
            ZipFile zip = open_for_reading();
            zip_int64_t count = zip_get_num_entries(zip.get(), 0);
            if (count < 0) {
                return false;
            }
            for (zip_uint64_t i = 0; i < static_cast<zip_uint64_t>(count); ++i) {
                extract_entry(zip.get(), i, output_path);
            }
            return true;
        } catch (...) {
            return false;  // Python: bare except -> return False
        }
    }

    // Extract the named member into output_path; true on success, false otherwise.
    bool extract_file(const std::string& file_name, const std::string& output_path) const {
        try {
            ZipFile zip = open_for_reading();
            zip_int64_t index = zip_name_locate(zip.get(), file_name.c_str(), 0);
            if (index < 0) {
                return false;  // Python: KeyError -> caught -> False
            }
            extract_entry(zip.get(), static_cast<zip_uint64_t>(index), output_path);
            return true;
        } catch (...) {
            return false;
        }
    }

    // Compress the given files into a new zip; true on success, false otherwise.
    bool create_zip_file(const std::vector<std::string>& files,
                         const std::string& output_file_name) const {
        int error_code = 0;
        zip_t* zip = zip_open(output_file_name.c_str(), ZIP_CREATE | ZIP_TRUNCATE, &error_code);
        if (zip == nullptr) {
            return false;  // Python: ZipFile(..., 'w') raised -> False
        }
        for (const std::string& file : files) {
            // zipfile.ZipFile.write() stores each file under its basename.
            std::string arcname = fs::path(file).filename().string();
            if (arcname.empty()) {
                zip_close(zip);  // finalize like Python's `with` block would
                return false;    // Python: ValueError on empty filename -> False
            }
            zip_source_t* source = zip_source_file(zip, file.c_str(), 0, -1);
            if (source == nullptr) {
                zip_close(zip);
                return false;  // Python: e.g. FileNotFoundError -> False
            }
            if (zip_file_add(zip, arcname.c_str(), source,
                             ZIP_FL_ENC_UTF_8 | ZIP_FL_OVERWRITE) < 0) {
                zip_source_free(source);  // archive does not own source on failure
                zip_close(zip);
                return false;
            }
            // Python's default compression for write() is ZIP_STORED.
            zip_uint64_t last = static_cast<zip_uint64_t>(zip_get_num_entries(zip, 0) - 1);
            zip_set_file_compression(zip, last, ZIP_CM_STORE, 0);
        }
        return zip_close(zip) == 0;  // flushes archive; failure -> False
    }

private:
    std::string file_name_;

    ZipFile open_for_reading() const {
        int error_code = 0;
        zip_t* handle = zip_open(file_name_.c_str(), ZIP_RDONLY, &error_code);
        if (handle == nullptr) {
            throw std::runtime_error("cannot open zip file");  // BadZipFile/FileNotFoundError
        }
        return ZipFile(handle);
    }

    // Extracts entry `index`; throws on any failure (mirrors zipfile raising).
    static void extract_entry(zip_t* zip, zip_uint64_t index,
                              const std::string& output_path) {
        const char* raw_name = zip_get_name(zip, index, 0);
        if (raw_name == nullptr) {
            throw std::runtime_error("cannot read entry name");
        }
        const std::string name(raw_name);
        const bool is_directory = !name.empty() && name.back() == '/';
        const std::string arcname = sanitize_entry_name(name);
        const fs::path target = fs::path(output_path) / arcname;

        std::error_code ec;
        if (is_directory) {
            fs::create_directories(target, ec);
            if (ec) throw std::runtime_error("cannot create directory");
            return;
        }
        if (target.has_parent_path()) {
            fs::create_directories(target.parent_path(), ec);
            if (ec) throw std::runtime_error("cannot create parent directory");
        }

        zip_file_t* entry = zip_fopen_index(zip, index, 0);
        if (entry == nullptr) {
            throw std::runtime_error("cannot open zip entry");
        }
        std::ofstream out(target, std::ios::binary | std::ios::trunc);
        if (!out.is_open()) {
            zip_fclose(entry);
            throw std::runtime_error("cannot create output file");
        }

        char buffer[65536];
        zip_int64_t read = 0;
        while ((read = zip_fread(entry, buffer, sizeof buffer)) > 0) {
            out.write(buffer, static_cast<std::streamsize>(read));
            if (!out.good()) break;
        }
        const bool ok = out.good() && read >= 0;  // read < 0 => decompress/CRC error
        zip_fclose(entry);
        out.close();
        if (!ok || out.fail()) {
            throw std::runtime_error("extraction failed");
        }
    }

    // Mirrors zipfile._extract_member(): drop '', '.' and '..' components so
    // member names cannot escape the output directory.
    static std::string sanitize_entry_name(const std::string& name) {
        std::string result;
        std::string::size_type pos = 0;
        while (pos <= name.size()) {
            const std::string::size_type end = name.find('/', pos);
            const std::string part =
                name.substr(pos, (end == std::string::npos ? name.size() : end) - pos);
            if (!part.empty() && part != "." && part != "..") {
                if (!result.empty()) result += '/';
                result += part;
            }
            if (end == std::string::npos) break;
            pos = end + 1;
        }
        return result;
    }
};