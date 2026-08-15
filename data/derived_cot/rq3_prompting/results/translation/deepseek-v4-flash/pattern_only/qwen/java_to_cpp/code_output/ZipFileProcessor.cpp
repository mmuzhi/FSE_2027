#include <iostream>
#include <fstream>
#include <filesystem>
#include <string>
#include <vector>
#include <memory>
#include <optional>
#include <cstring>
#include <stdexcept>
#include "miniz.h"

struct ZipEntry {
    std::string name;
    bool isDirectory;
    mz_uint index;
};

class ZipFile {
public:
    explicit ZipFile(const std::string& path) {
        std::memset(&archive_, 0, sizeof(archive_));
        if (!mz_zip_reader_init_file(&archive_, path.c_str(), 0)) {
            throw std::runtime_error("Failed to open zip file: " + path);
        }
    }

    ~ZipFile() {
        if (archive_.m_pState) {
            mz_zip_reader_end(&archive_);
        }
    }

    ZipFile(const ZipFile&) = delete;
    ZipFile& operator=(const ZipFile&) = delete;

    std::vector<ZipEntry> entries() {
        std::vector<ZipEntry> result;
        mz_uint num = mz_zip_reader_get_num_files(&archive_);
        for (mz_uint i = 0; i < num; ++i) {
            mz_zip_archive_file_stat stat;
            if (mz_zip_reader_file_stat(&archive_, i, &stat)) {
                ZipEntry e;
                e.name = stat.m_filename;
                e.isDirectory = (stat.m_is_directory != 0);
                e.index = i;
                result.push_back(e);
            }
        }
        return result;
    }

    std::optional<ZipEntry> getEntry(const std::string& name) {
        int idx = mz_zip_reader_locate_entry(&archive_, name.c_str(), 0);
        if (idx < 0) {
            return std::nullopt;
        }
        mz_zip_archive_file_stat stat;
        if (!mz_zip_reader_file_stat(&archive_, static_cast<mz_uint>(idx), &stat)) {
            return std::nullopt;
        }
        ZipEntry e;
        e.name = stat.m_filename;
        e.isDirectory = (stat.m_is_directory != 0);
        e.index = static_cast<mz_uint>(idx);
        return e;
    }

    bool extractToFile(const ZipEntry& entry, const std::filesystem::path& filePath) {
        std::ofstream out(filePath, std::ios::binary | std::ios::trunc);
        if (!out.is_open()) {
            return false;
        }

        mz_zip_reader_extract_iter_state* iter = mz_zip_reader_extract_iter_new(&archive_, entry.index, 0);
        if (!iter) {
            return false;
        }

        char buffer[1024];
        bool ok = true;
        size_t readBytes;
        while ((readBytes = mz_zip_reader_extract_iter_read(iter, buffer, sizeof(buffer))) > 0) {
            out.write(buffer, static_cast<std::streamsize>(readBytes));
            if (!out) {
                ok = false;
                break;
            }
        }

        if (!mz_zip_reader_extract_iter_free(iter)) {
            ok = false;
        }

        out.close();
        return ok && out.good();
    }

private:
    mz_zip_archive archive_;
};

enum class LogLevel { SEVERE, WARNING, INFO };

class Logger {
public:
    void log(LogLevel level, const std::string& message) {
        std::cerr << levelToString(level) << ": " << message << std::endl;
    }

    void log(LogLevel level, const std::string& message, const std::string& exception) {
        std::cerr << levelToString(level) << ": " << message << " - " << exception << std::endl;
    }

    void severe(const std::string& message) { log(LogLevel::SEVERE, message); }
    void warning(const std::string& message) { log(LogLevel::WARNING, message); }
    void info(const std::string& message) { log(LogLevel::INFO, message); }

private:
    static std::string levelToString(LogLevel level) {
        switch (level) {
            case LogLevel::SEVERE: return "SEVERE";
            case LogLevel::WARNING: return "WARNING";
            case LogLevel::INFO: return "INFO";
        }
        return "UNKNOWN";
    }
};

class ZipFileProcessor {
public:
    explicit ZipFileProcessor(const std::string& zipFileName) : zipFilePath_(zipFileName) {}

    bool extractAll(const std::string& outputDir) {
        std::filesystem::path outputDirPath(outputDir);
        std::unique_ptr<ZipFile> zipFile = readZipFile();
        if (!zipFile) return false;

        if (!std::filesystem::exists(std::filesystem::absolute(outputDirPath))) {
            try {
                std::filesystem::create_directories(outputDirPath);
                logger_.info("Created output directory: " + std::filesystem::absolute(outputDirPath).string());
            } catch (const std::exception& e) {
                logger_.severe("Failed to create output directory: " + std::filesystem::absolute(outputDirPath).string() + " - " + e.what());
                return false;
            }
        }

        auto entries = zipFile->entries();
        for (const auto& entry : entries) {
            std::filesystem::path filePath = outputDirPath / entry.name;
            try {
                if (entry.isDirectory) {
                    if (!std::filesystem::exists(filePath)) {
                        std::filesystem::create_directories(filePath);
                        logger_.info("Created directory: " + std::filesystem::absolute(filePath).string());
                    }
                } else {
                    if (zipFile->extractToFile(entry, filePath)) {
                        logger_.info("Extracted file: " + std::filesystem::absolute(filePath).string());
                    } else {
                        logger_.severe("Failed to process entry: " + entry.name);
                    }
                }
            } catch (const std::exception& e) {
                logger_.severe("Failed to process entry: " + entry.name + " - " + e.what());
            }
        }

        return true;
    }

    bool extractFile(const std::string& fileName, const std::string& outputDir) {
        std::filesystem::path outputDirPath(outputDir);
        std::filesystem::path filePath = outputDirPath / fileName;
        std::unique_ptr<ZipFile> zipFile = readZipFile();
        if (!zipFile) return false;

        auto entryOpt = zipFile->getEntry(fileName);
        if (!entryOpt) {
            logger_.warning("File not found in zip: " + fileName);
            return false;
        }
        ZipEntry entry = *entryOpt;

        auto parent = filePath.parent_path();
        if (parent.empty()) {
            throw std::runtime_error("NullPointerException");
        }
        if (!std::filesystem::exists(std::filesystem::absolute(parent))) {
            try {
                std::filesystem::create_directories(parent);
                logger_.info("Created parent directory: " + std::filesystem::absolute(parent).string());
            } catch (const std::exception& e) {
                logger_.severe("Failed to create parent directory: " + std::filesystem::absolute(parent).string() + " - " + e.what());
                return false;
            }
        }

        try {
            if (zipFile->extractToFile(entry, filePath)) {
                logger_.info("Extracted file: " + std::filesystem::absolute(filePath).string());
            } else {
                logger_.severe("Failed to extract file: " + fileName);
                return false;
            }
        } catch (const std::exception& e) {
            logger_.severe("Failed to extract file: " + fileName + " - " + e.what());
            return false;
        }

        return true;
    }

private:
    std::unique_ptr<ZipFile> readZipFile() {
        if (!std::filesystem::exists(std::filesystem::absolute(zipFilePath_))) {
            logger_.severe("Zip file does not exist: " + std::filesystem::absolute(zipFilePath_).string());
            return nullptr;
        }
        try {
            return std::make_unique<ZipFile>(zipFilePath_.string());
        } catch (const std::exception& e) {
            logger_.severe("Failed to read the zip file: " + std::filesystem::absolute(zipFilePath_).string() + " - " + e.what());
            return nullptr;
        }
    }

    std::filesystem::path zipFilePath_;
    Logger logger_;
};