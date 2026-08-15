#include <string>
#include <vector>
#include <memory>
#include <filesystem>
#include <cstring>
#include "miniz.h"

class ZipFile {
public:
    mz_zip_archive archive;
    bool is_open;

    ZipFile() : is_open(false) {
        std::memset(&archive, 0, sizeof(archive));
    }

    ~ZipFile() {
        if (is_open) {
            mz_zip_reader_end(&archive);
        }
    }

    ZipFile(const ZipFile&) = delete;
    ZipFile& operator=(const ZipFile&) = delete;
};

class ZipWriter {
public:
    mz_zip_archive archive;
    bool is_open;

    ZipWriter() : is_open(false) {
        std::memset(&archive, 0, sizeof(archive));
    }

    ~ZipWriter() {
        if (is_open) {
            mz_zip_writer_end(&archive);
        }
    }

    ZipWriter(const ZipWriter&) = delete;
    ZipWriter& operator=(const ZipWriter&) = delete;

    bool open(const std::string& filename) {
        if (!mz_zip_writer_init_file(&archive, filename.c_str(), 0)) {
            return false;
        }
        is_open = true;
        return true;
    }

    bool close() {
        if (!is_open) return true;
        bool ok = mz_zip_writer_end(&archive) != 0;
        is_open = false;
        return ok;
    }
};

class ZipFileProcessor {
private:
    std::string file_name;

public:
    ZipFileProcessor(const std::string& file_name) : file_name(file_name) {}

    std::unique_ptr<ZipFile> read_zip_file() {
        auto zf = std::make_unique<ZipFile>();
        if (!mz_zip_reader_init_file(&zf->archive, file_name.c_str(), 0)) {
            return nullptr;
        }
        zf->is_open = true;
        return zf;
    }

    bool extract_all(const std::string& output_path) {
        try {
            ZipFile zf;
            if (!mz_zip_reader_init_file(&zf.archive, file_name.c_str(), 0)) {
                return false;
            }
            zf.is_open = true;

            std::filesystem::path dest = output_path.empty() ? "." : output_path;
            std::filesystem::create_directories(dest);

            mz_uint num_files = mz_zip_reader_get_num_files(&zf.archive);
            for (mz_uint i = 0; i < num_files; ++i) {
                char filename[512];
                if (!mz_zip_reader_get_filename(&zf.archive, i, filename, sizeof(filename))) {
                    return false;
                }
                std::string entry(filename);
                std::filesystem::path full_path = dest / entry;
                if (!entry.empty() && entry.back() == '/') {
                    std::filesystem::create_directories(full_path);
                } else {
                    std::filesystem::create_directories(full_path.parent_path());
                    if (!mz_zip_reader_extract_to_file(&zf.archive, i, full_path.string().c_str(), 0)) {
                        return false;
                    }
                }
            }
            return true;
        } catch (...) {
            return false;
        }
    }

    bool extract_file(const std::string& file_name, const std::string& output_path) {
        try {
            ZipFile zf;
            if (!mz_zip_reader_init_file(&zf.archive, this->file_name.c_str(), 0)) {
                return false;
            }
            zf.is_open = true;

            int idx = mz_zip_reader_locate_file(&zf.archive, file_name.c_str(), nullptr, 0);
            if (idx < 0) {
                return false;
            }

            std::filesystem::path dest = output_path.empty() ? "." : output_path;
            std::filesystem::path full_path = dest / file_name;

            if (!file_name.empty() && file_name.back() == '/') {
                std::filesystem::create_directories(full_path);
                return true;
            }

            std::filesystem::create_directories(full_path.parent_path());
            bool ok = mz_zip_reader_extract_to_file(&zf.archive, static_cast<mz_uint>(idx), full_path.string().c_str(), 0) != 0;
            return ok;
        } catch (...) {
            return false;
        }
    }

    bool create_zip_file(const std::vector<std::string>& files, const std::string& output_file_name) {
        try {
            ZipWriter writer;
            if (!writer.open(output_file_name)) {
                return false;
            }
            for (const auto& file : files) {
                if (!mz_zip_writer_add_file(&writer.archive, file.c_str(), file.c_str(), nullptr, 0, 0)) {
                    return false;
                }
            }
            return writer.close();
        } catch (...) {
            return false;
        }
    }
};