#include <iostream>
#include <fstream>
#include <sstream>
#include <filesystem>
#include <string>
#include <vector>
#include <memory>
#include <cstring>
#include <ctime>
#include <unzip.h>
#include <zlib.h>

namespace fs = std::filesystem;

// Simple logger mimicking java.util.logging.Logger
class Logger {
public:
    enum Level { SEVERE, WARNING, INFO };

    static Logger& getLogger(const std::string& name) {
        static Logger instance(name);
        return instance;
    }

    void log(Level level, const std::string& msg) {
        std::ostream& out = (level == SEVERE) ? std::cerr : std::cout;
        out << timestamp() << " " << levelToString(level) << " " << name_ << " - " << msg << std::endl;
    }

    void log(Level level, const std::string& msg, const std::exception& e) {
        std::ostream& out = (level == SEVERE) ? std::cerr : std::cout;
        out << timestamp() << " " << levelToString(level) << " " << name_ << " - " << msg;
        out << " Exception: " << e.what() << std::endl;
    }

    void warning(const std::string& msg) {
        log(WARNING, msg);
    }

    void info(const std::string& msg) {
        log(INFO, msg);
    }

private:
    std::string name_;
    Logger(const std::string& name) : name_(name) {}

    static std::string timestamp() {
        std::time_t now = std::time(nullptr);
        char buf[20];
        std::strftime(buf, sizeof(buf), "%Y-%m-%d %H:%M:%S", std::localtime(&now));
        return std::string(buf);
    }

    static std::string levelToString(Level level) {
        switch (level) {
            case SEVERE: return "SEVERE";
            case WARNING: return "WARNING";
            case INFO: return "INFO";
            default: return "UNKNOWN";
        }
    }
};

// Wrapper around minizip unzFile to behave like java.util.zip.ZipFile
class ZipFile {
public:
    explicit ZipFile(const fs::path& path) : zipPath_(path), handle_(nullptr) {
        handle_ = unzOpen(path.string().c_str());
    }

    ~ZipFile() {
        if (handle_) {
            unzClose(handle_);
            handle_ = nullptr;
        }
    }

    ZipFile(const ZipFile&) = delete;
    ZipFile& operator=(const ZipFile&) = delete;
    ZipFile(ZipFile&&) = delete;
    ZipFile& operator=(ZipFile&&) = delete;

    bool isOpen() const { return handle_ != nullptr; }

    // returns -1 if not found
    int getEntryIndex(const std::string& name) const {
        if (!handle_) return -1;
        if (unzLocateFile(handle_, name.c_str(), 0) == UNZ_OK) {
            unz_file_info64 fileInfo;
            char fileName[256];
            if (unzGetCurrentFileInfo64(handle_, &fileInfo, fileName, sizeof(fileName), nullptr, 0, nullptr, 0) == UNZ_OK) {
                return fileInfo.number_entry; // not correct index but arbitrary; we just need existence
            }
        }
        return -1;
    }

    // Returns a pointer to a ZipEntry (caller must delete) for the current file, or nullptr if fails.
    // Must be called after successful unzGoToFirstFile/unzGoToNextFile
    std::unique_ptr<unz_file_info64> getCurrentEntryInfo() const {
        if (!handle_) return nullptr;
        auto info = std::make_unique<unz_file_info64>();
        char fileName[256];
        if (unzGetCurrentFileInfo64(handle_, info.get(), fileName, sizeof(fileName), nullptr, 0, nullptr, 0) == UNZ_OK) {
            return info;
        }
        return nullptr;
    }

    std::string getCurrentFileName() const {
        if (!handle_) return "";
        char fileName[256];
        unz_file_info64 fileInfo;
        if (unzGetCurrentFileInfo64(handle_, &fileInfo, fileName, sizeof(fileName), nullptr, 0, nullptr, 0) == UNZ_OK) {
            return std::string(fileName);
        }
        return "";
    }

    bool openCurrentFile() {
        if (!handle_) return false;
        return unzOpenCurrentFile(handle_) == UNZ_OK;
    }

    void closeCurrentFile() {
        if (handle_) {
            unzCloseCurrentFile(handle_);
        }
    }

    int readCurrentFile(void* buf, unsigned len) {
        if (!handle_) return -1;
        return unzReadCurrentFile(handle_, buf, len);
    }

    // Navigate entries
    bool goToFirstFile() {
        if (!handle_) return false;
        return unzGoToFirstFile(handle_) == UNZ_OK;
    }

    bool goToNextFile() {
        if (!handle_) return false;
        return unzGoToNextFile(handle_) == UNZ_OK;
    }

    bool goToFile(const std::string& name) {
        if (!handle_) return false;
        return unzLocateFile(handle_, name.c_str(), 0) == UNZ_OK;
    }

    const fs::path& path() const { return zipPath_; }

private:
    fs::path zipPath_;
    unzFile handle_;
};

class ZipFileProcessor {
public:
    explicit ZipFileProcessor(const std::string& zipFileName)
        : zipFilePath_(fs::path(zipFileName)), logger_(Logger::getLogger("org.example.ZipFileProcessor"))
    {}

    std::unique_ptr<ZipFile> readZipFile() {
        if (!fs::exists(zipFilePath_)) {
            logger_.log(Logger::SEVERE, "Zip file does not exist: " + fs::absolute(zipFilePath_).string());
            return nullptr;
        }
        auto zipFile = std::make_unique<ZipFile>(zipFilePath_);
        if (!zipFile->isOpen()) {
            logger_.log(Logger::SEVERE, "Failed to read the zip file: " + fs::absolute(zipFilePath_).string());
            return nullptr;
        }
        return zipFile;
    }

    bool extractAll(const std::string& outputDir) {
        fs::path outputDirPath(outputDir);
        auto zipFile = readZipFile();
        if (!zipFile) return false;

        if (!fs::exists(outputDirPath)) {
            try {
                fs::create_directories(outputDirPath);
                logger_.info("Created output directory: " + fs::absolute(outputDirPath).string());
            } catch (const fs::filesystem_error& e) {
                logger_.log(Logger::SEVERE, "Failed to create output