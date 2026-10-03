#include <iostream>
#include <string>
#include <vector>
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <stdexcept>
#include <sys/stat.h>
#include <zip.h>
#include <unzip.h>

// We'll use the minizip library via the zip.h and unzip.h headers.

class ZipFileProcessor {
private:
    std::string file_name;

    // Helper function to check if a file exists
    bool fileExists(const std::string& name) {
        struct stat buf;
        return (stat(name.c_str(), &buf) == 0);
    }

public:
    ZipFileProcessor(const std::string& file_name) : file_name(file_name) {}

    // Open a zip file for reading
    std::unique_ptr<unzip> read_zip_file() {
        if (!fileExists(file_name)) {
            return nullptr;
        }
        unzip* zip_file = unzip_open(file_name.c_str());
        if (zip_file == nullptr) {
            return nullptr;
        }
        return std::unique_ptr<unzip>(zip_file);
    }

    // Extract all files from the zip to the specified path
    bool extract_all(const std::string& output_path) {
        auto zip_file = read_zip_file();
        if (!zip_file) {
            return false;
        }

        // Create the output directory if it doesn't exist
        struct stat st = {0};
        if (stat(output_path.c_str(), &st) != 0) {
            mkdir(output_path.c_str(), 0700);
        }

        int ret;
        while (true) {
            void* buf;
            int size;
            ret = unzip_get_next_entry(zip_file.get());
            if (ret == UNZ_END_OF_LIST_TAG) {
                break;
            }
            if (ret != UNZ_OK) {
                return false;
            }

            char* buffer = (char*)malloc(4096);
            do {
                size = unzip_read(zip_file.get(), buffer, 4096);
                if (size > 0) {
                    // Write the file
                    std::string output_file = output_path + "/" + unzip_get_filename(zip_file.get(), "");
                    FILE* fout = fopen(output_file.c_str(), "wb");
                    if (fout == nullptr) {
                        free(buffer);
                        return false;
                    }
                    fwrite(buffer, 1, size, fout);
                    fclose(fout);
                }
            } while (size > 0);
            free(buffer);

            ret = unzip_close_current_entry(zip_file.get());
            if (ret != UNZ_OK) {
                return false;
            }
        }

        return true;
    }

    // Extract a specific file from the zip to the specified path
    bool extract_file(const std::string& file_name, const std::string& output_path) {
        auto zip_file = read_zip_file();
        if (!zip_file) {
            return false;
        }

        // Create the output directory if it doesn't exist
        struct stat st = {0};
        if (stat(output_path.c_str(), &st) != 0) {
            mkdir(output_path.c_str(), 0700);
        }

        int ret;
        ret = unzip_find_zip_entry(zip_file.get(), file_name.c_str());
        if (ret != UNZ_OK) {
            return false;
        }

        ret = unzip_open_current_entry(zip_file.get());
        if (ret != UNZ_OK) {
            return false;
        }

        char* buffer = (char*)malloc(4096);
        do {
            int size = unzip_read(zip_file.get(), buffer, 4096);
            if (size > 0) {
                std::string output_file = output_path + "/" + file_name;
                FILE* fout = fopen(output_file.c_str(), "wb");
                if (fout == nullptr) {
                    free(buffer);
                    return false;
                }
                fwrite(buffer, 1, size, fout);
                fclose(fout);
            }
        } while (size > 0);
        free(buffer);

        ret = unzip_close_current_entry(zip_file.get());
        if (ret != UNZ_OK) {
            return false;
        }

        return true;
    }

    // Create a zip file from a list of files
    bool create_zip_file(const std::vector<std::string>& files, const std::string& output_file_name) {
        // Check if the output file name has a .zip extension
        if (output_file_name.find(".zip") == std::string::npos) {
            // Append .zip if not present
            output_file_name += ".zip";
        }

        zip* zip_file = zip_open(output_file_name.c_str(), ZIP_CREATE | ZIP_TRUNCATE, 0600);
        if (zip_file == nullptr) {
            return false;
        }

        for (const auto& file : files) {
            if (!fileExists(file)) {
                continue; // Skip if file doesn't exist
            }

            int ret = zip_add(zip_file, file.c_str(), file.c_str());
            if (ret != ZIP_OK) {
                zip_close(zip_file);
                return false;
            }
        }

        int ret = zip_close(zip_file);
        if (ret != ZIP_OK) {
            return false;
        }

        return true;
    }
};