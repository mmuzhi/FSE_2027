#include <string>
#include <vector>
#include <zip.h>
#include <filesystem>
#include <fstream>

class ZipFileProcessor {
private:
    std::string file_name;

public:
    ZipFileProcessor(const std::string& file_name) : file_name(file_name) {}

    zip_t* read_zip_file() {
        int errorp;
        zip_t* archive = zip_open(file_name.c_str(), ZIP_RDONLY, &errorp);
        if (!archive) {
            return nullptr;
        }
        return archive;
    }

    bool extract_all(const std::string& output_path) {
        int errorp;
        zip_t* archive = zip_open(file_name.c_str(), ZIP_RDONLY, &errorp);
        if (!archive) {
            return false;
        }

        try {
            std::filesystem::create_directories(output_path);
            zip_int64_t num_entries = zip_get_num_entries(archive, 0);
            for (zip_int64_t i = 0; i < num_entries; i++) {
                zip_stat_t stat;
                zip_stat_init(&stat);
                if (zip_stat_index(archive, i, 0, &stat) != 0) {
                    zip_close(archive);
                    return false;
                }

                std::string entry_name(stat.name);
                std::string full_path = output_path + "/" + entry_name;

                if (entry_name.back() == '/') {
                    std::filesystem::create_directories(full_path);
                    continue;
                }

                std::filesystem::create_directories(std::filesystem::path(full_path).parent_path());

                zip_file_t* file = zip_fopen_index(archive, i, 0);
                if (!file) {
                    zip_close(archive);
                    return false;
                }

                std::ofstream out_file(full_path, std::ios::binary);
                if (!out_file) {
                    zip_fclose(file);
                    zip_close(archive);
                    return false;
                }

                char buf[4096];
                zip_int64_t bytes_read;
                while ((bytes_read = zip_fread(file, buf, sizeof(buf))) > 0) {
                    out_file.write(buf, bytes_read);
                }

                zip_fclose(file);
                out_file.close();
            }
            zip_close(archive);
            return true;
        } catch (...) {
            zip_close(archive);
            return false;
        }
    }

    bool extract_file(const std::string& file_name_to_extract, const std::string& output_path) {
        int errorp;
        zip_t* archive = zip_open(file_name.c_str(), ZIP_RDONLY, &errorp);
        if (!archive) {
            return false;
        }

        try {
            std::filesystem::create_directories(output_path);

            zip_int64_t index = zip_name_locate(archive, file_name_to_extract.c_str(), 0);
            if (index < 0) {
                zip_close(archive);
                return false;
            }

            zip_stat_t stat;
            zip_stat_init(&stat);
            if (zip_stat_index(archive, index, 0, &stat) != 0) {
                zip_close(archive);
                return false;
            }

            std::string full_path = output_path + "/" + file_name_to_extract;
            std::filesystem::create_directories(std::filesystem::path(full_path).parent_path());

            zip_file_t* file = zip_fopen_index(archive, index, 0);
            if (!file) {
                zip_close(archive);
                return false;
            }

            std::ofstream out_file(full_path, std::ios::binary);
            if (!out_file) {
                zip_fclose(file);
                zip_close(archive);
                return false;
            }

            char buf[4096];
            zip_int64_t bytes_read;
            while ((bytes_read = zip_fread(file, buf, sizeof(buf))) > 0) {
                out_file.write(buf, bytes_read);
            }

            zip_fclose(file);
            out_file.close();
            zip_close(archive);
            return true;
        } catch (...) {
            zip_close(archive);
            return false;
        }
    }

    bool create_zip_file(const std::vector<std::string>& files, const std::string& output_file_name) {
        int errorp;
        zip_t* archive = zip_open(output_file_name.c_str(), ZIP_CREATE | ZIP_TRUNCATE, &errorp);
        if (!archive) {
            return false;
        }

        try {
            for (const auto& file : files) {
                zip_source_t* source = zip_source_file(archive, file.c_str(), 0, 0);
                if (!source) {
                    zip_close(archive);
                    return false;
                }

                if (zip_file_add(archive, file.c_str(), source, ZIP_FL_OVERWRITE | ZIP_FL_ENC_UTF_8) < 0) {
                    zip_source_free(source);
                    zip_close(archive);
                    return false;
                }
            }

            if (zip_close(archive) != 0) {
                return false;
            }
            return true;
        } catch (...) {
            zip_close(archive);
            return false;
        }
    }
};