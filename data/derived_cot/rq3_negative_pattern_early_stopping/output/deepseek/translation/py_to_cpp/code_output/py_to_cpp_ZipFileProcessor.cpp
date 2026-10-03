#include <string>
#include <vector>
#include <memory>
#include <zip.h>
#include <iostream>
#include <fstream>
#include <sys/stat.h>

class ZipFileProcessor {
public:
    ZipFileProcessor(const std::string& file_name) : file_name(file_name) {}

    // Returns a zip_t* pointer on success, nullptr on failure.
    // Caller must call zip_close on the returned pointer.
    zip_t* read_zip_file() {
        int err = 0;
        zip_t* za = zip_open(file_name.c_str(), ZIP_RDONLY, &err);
        if (za == nullptr) {
            return nullptr;
        }
        return za;
    }

    bool extract_all(const std::string& output_path) {
        int err = 0;
        zip_t* za = zip_open(file_name.c_str(), ZIP_RDONLY, &err);
        if (za == nullptr) {
            return false;
        }
        zip_int64_t num_entries = zip_get_num_entries(za, 0);
        for (zip_int64_t i = 0; i < num_entries; ++i) {
            const char* name = zip_get_name(za, i, 0);
            if (name == nullptr) {
                zip_close(za);
                return false;
            }
            std::string full_path = output_path + "/" + name;
            // Create directories if necessary
            size_t pos = full_path.find_last_of('/');
            if (pos != std::string::npos) {
                std::string dir = full_path.substr(0, pos);
                struct stat st;
                if (stat(dir.c_str(), &st) != 0) {
                    if (mkdir(dir.c_str(), 0755) != 0) {
                        zip_close(za);
                        return false;
                    }
                }
            }
            zip_file_t* zf = zip_fopen_index(za, i, 0);
            if (zf == nullptr) {
                zip_close(za);
                return false;
            }
            std::ofstream out(full_path, std::ios::binary);
            if (!out.is_open()) {
                zip_fclose(zf);
                zip_close(za);
                return false;
            }
            char buf[8192];
            zip_int64_t n;
            while ((n = zip_fread(zf, buf, sizeof(buf))) > 0) {
                out.write(buf, n);
            }
            out.close();
            zip_fclose(zf);
        }
        zip_close(za);
        return true;
    }

    bool extract_file(const std::string& file_name, const std::string& output_path) {
        int err = 0;
        zip_t* za = zip_open(this->file_name.c_str(), ZIP_RDONLY, &err);
        if (za == nullptr) {
            return false;
        }
        zip_int64_t index = zip_name_locate(za, file_name.c_str(), 0);
        if (index < 0) {
            zip_close(za);
            return false;
        }
        std::string full_path = output_path + "/" + file_name;
        size_t pos = full_path.find_last_of('/');
        if (pos != std::string::npos) {
            std::string dir = full_path.substr(0, pos);
            struct stat st;
            if (stat(dir.c_str(), &st) != 0) {
                if (mkdir(dir.c_str(), 0755) != 0) {
                    zip_close(za);
                    return false;
                }
            }
        }
        zip_file_t* zf = zip_fopen_index(za, index, 0);
        if (zf == nullptr) {
            zip_close(za);
            return false;
        }
        std::ofstream out(full_path, std::ios::binary);
        if (!out.is_open()) {
            zip_fclose(zf);
            zip_close(za);
            return false;
        }
        char buf[8192];
        zip_int64_t n;
        while ((n = zip_fread(zf, buf, sizeof(buf))) > 0) {
            out.write(buf, n);
        }
        out.close();
        zip_fclose(zf);
        zip_close(za);
        return true;
    }

    bool create_zip_file(const std::vector<std::string>& files, const std::string& output_file_name) {
        int err = 0;
        zip_t* za = zip_open(output_file_name.c_str(), ZIP_CREATE | ZIP_TRUNCATE, &err);
        if (za == nullptr) {
            return false;
        }
        for (const auto& file : files) {
            // Add file to zip with its full path name? Python zipfile.write uses arcname as filename by default.
            // We'll use just the basename.
            std::string name = file;
            size_t pos = file.find_last_of("/\\");
            if (pos != std::string::npos) {
                name = file.substr(pos + 1);
            }
            if (zip_add_file(za, name.c_str(), file.c_str()) < 0) {
                zip_close(za);
                return false;
            }
        }
        zip_close(za);
        return true;
    }

private:
    std::string file_name;
};