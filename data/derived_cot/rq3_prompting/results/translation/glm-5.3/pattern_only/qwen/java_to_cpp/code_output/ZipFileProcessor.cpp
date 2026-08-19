#include <zip.h>

#include <filesystem>
#include <fstream>
#include <iostream>
#include <memory>
#include <stdexcept>
#include <string>
#include <vector>

namespace fs = std::filesystem;

namespace org {
namespace example {

namespace {

// Minimal stand-in for java.util.logging output (SEVERE/WARNING -> stderr, INFO -> stdout).
void logSevere(const std::string& msg) { std::cerr << "SEVERE: " << msg << std::endl; }
void logWarning(const std::string& msg) { std::cerr << "WARNING: " << msg << std::endl; }
void logInfo(const std::string& msg) { std::cout << "INFO: " << msg << std::endl; }

// Equivalent of Files.notExists: true only when non-existence is confirmed
// (unknown status -> false, like Java).
bool notExists(const fs::path& p) {
    std::error_code ec;
    const bool e = fs::exists(p, ec);
    return !ec && !e;
}

std::string absoluteString(const fs::path& p) { return fs::absolute(p).string(); }

struct ZipCloser {
    void operator()(zip_t* archive) const {
        if (archive != nullptr) zip_close(archive);
    }
};

using ZipFilePtr = std::unique_ptr<zip_t, ZipCloser>;

// Java ZipEntry.isDirectory() is a name-convention check (trailing '/').
bool isDirectoryEntry(const std::string& name) {
    return !name.empty() && name.back() == '/';
}

}  // namespace

class ZipFileProcessor {
public:
    explicit ZipFileProcessor(const std::string& zipFileName)
        : zipFilePath(zipFileName) {}

    ZipFilePtr readZipFile() {
        if (notExists(zipFilePath)) {
            logSevere("Zip file does not exist: " + absoluteString(zipFilePath));
            return nullptr;
        }
        int err = 0;
        zip_t* archive = zip_open(zipFilePath.string().c_str(), ZIP_RDONLY, &err);
        if (archive == nullptr) {
            logSevere("Failed to read the zip file: " + absoluteString(zipFilePath));
            return nullptr;
        }
        return ZipFilePtr(archive);
    }

    bool extractAll(const std::string& outputDir) {
        const fs::path outputDirPath(outputDir);
        try {
            ZipFilePtr zipFile = readZipFile();
            if (!zipFile) return false;

            if (notExists(outputDirPath)) {
                try {
                    fs::create_directories(outputDirPath);
                    logInfo("Created output directory: " + absoluteString(outputDirPath));
                } catch (const fs::filesystem_error& e) {
                    logSevere("Failed to create output directory: " +
                              absoluteString(outputDirPath) + ": " + e.what());
                    return false;
                }
            }

            // Iterate entries in central-directory order, like ZipFile.stream().
            const zip_int64_t entryCount = zip_get_num_entries(zipFile.get(), 0);
            for (zip_int64_t i = 0; i < entryCount; ++i) {
                const char* nameC = zip_get_name(zipFile.get(), static_cast<zip_uint64_t>(i), 0);
                if (nameC == nullptr) continue;
                const std::string entryName(nameC);
                const fs::path filePath = outputDirPath / fs::path(entryName);
                try {
                    if (isDirectoryEntry(entryName)) {
                        if (notExists(filePath)) {
                            fs::create_directories(filePath);
                            logInfo("Created directory: " + absoluteString(filePath));
                        }
                    } else {
                        zip_file_t* in = zip_fopen_index(zipFile.get(), static_cast<zip_uint64_t>(i), 0);
                        if (in == nullptr) {
                            throw std::runtime_error("zip_fopen_index failed");
                        }
                        std::vector<char> buffer(1024);
                        // CREATE + TRUNCATE_EXISTING -> binary | trunc
                        std::ofstream out(filePath, std::ios::binary | std::ios::trunc);
                        if (!out) {
                            zip_fclose(in);
                            throw std::runtime_error("Failed to open output stream: " + filePath.string());
                        }
                        zip_int64_t len;
                        while ((len = zip_fread(in, buffer.data(), buffer.size())) > 0) {
                            out.write(buffer.data(), len);
                        }
                        zip_fclose(in);
                        logInfo("Extracted file: " + absoluteString(filePath));
                    }
                } catch (const std::exception& e) {
                    // Per-entry failure is logged and iteration continues.
                    logSevere("Failed to process entry: " + entryName + ": " + e.what());
                }
            }

            return true;
        } catch (const std::exception& e) {
            logSevere("Failed to extract files from zip: " +
                      absoluteString(zipFilePath) + ": " + e.what());
            return false;
        }
    }

    bool extractFile(const std::string& fileName, const std::string& outputDir) {
        const fs::path outputDirPath(outputDir);
        const fs::path filePath = outputDirPath / fs::path(fileName);
        try {
            ZipFilePtr zipFile = readZipFile();
            if (!zipFile) return false;

            const zip_int64_t entryIndex = zip_name_locate(zipFile.get(), fileName.c_str(), 0);
            if (entryIndex < 0) {
                logWarning("File not found in zip: " + fileName);
                return false;
            }

            const fs::path parentPath = filePath.parent_path();
            if (!parentPath.empty() && notExists(parentPath)) {
                try {
                    fs::create_directories(parentPath);
                    logInfo("Created parent directory: " + absoluteString(parentPath));
                } catch (const fs::filesystem_error& e) {
                    logSevere("Failed to create parent directory: " +
                              absoluteString(parentPath) + ": " + e.what());
                    return false;
                }
            }

            zip_file_t* in = zip_fopen_index(zipFile.get(), static_cast<zip_uint64_t>(entryIndex), 0);
            if (in == nullptr) {
                throw std::runtime_error("zip_fopen_index failed");
            }
            {
                std::vector<char> buffer(1024);
                std::ofstream out(filePath, std::ios::binary | std::ios::trunc);
                if (!out) {
                    zip_fclose(in);
                    throw std::runtime_error("Failed to open output stream: " + filePath.string());
                }
                zip_int64_t len;
                while ((len = zip_fread(in, buffer.data(), buffer.size())) > 0) {
                    out.write(buffer.data(), len);
                }
                logInfo("Extracted file: " + absoluteString(filePath));
            }
            zip_fclose(in);

            return true;
        } catch (const std::exception& e) {
            logSevere("Failed to extract file: " + fileName + ": " + e.what());
            return false;
        }
    }

private:
    const fs::path zipFilePath;
};

}  // namespace example
}  // namespace org