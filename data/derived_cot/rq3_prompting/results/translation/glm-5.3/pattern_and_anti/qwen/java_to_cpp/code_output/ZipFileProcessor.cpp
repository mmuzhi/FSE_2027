// ZipFileProcessor.cpp — requires C++17 and libzip (-lzip)
#include <zip.h>

#include <cstddef>
#include <filesystem>
#include <fstream>
#include <iostream>
#include <memory>
#include <stdexcept>
#include <string>

namespace fs = std::filesystem;

namespace org {
namespace example {

namespace {
// Minimal stand-in for java.util.logging.Logger (default console handler -> stderr).
class Logger {
public:
    static void info(const std::string& msg) {
        std::cerr << "INFO: " << msg << '\n';
    }
    static void warning(const std::string& msg) {
        std::cerr << "WARNING: " << msg << '\n';
    }
    static void severe(const std::string& msg, const std::string& err = "") {
        std::cerr << "SEVERE: " << msg;
        if (!err.empty()) std::cerr << '\n' << err;
        std::cerr << '\n';
    }
};
Logger logger; // mirrors `private static final Logger logger`
} // namespace

class ZipFileProcessor {
public:
    explicit ZipFileProcessor(const std::string& zipFileName)
        : zipFilePath_(zipFileName) {}

    bool extractAll(const std::string& outputDir) const {
        const fs::path outputDirPath(outputDir);
        // try-with-resources -> RAII (null resource is not closed)
        std::unique_ptr<zip_t, int (*)(zip_t*)> zipFile(readZipFile(), zip_close);
        if (!zipFile) return false;

        if (!fs::exists(outputDirPath)) {
            try {
                fs::create_directories(outputDirPath);
                logger.info("Created output directory: " + fs::absolute(outputDirPath).string());
            } catch (const fs::filesystem_error& e) {
                logger.severe("Failed to create output directory: " + fs::absolute(outputDirPath).string(), e.what());
                return false;
            }
        }

        const zip_int64_t numEntries = zip_get_num_entries(zipFile.get(), 0);
        for (zip_uint64_t i = 0; numEntries > 0 && i < static_cast<zip_uint64_t>(numEntries); ++i) {
            zip_stat_t st;
            zip_stat_init(&st);
            if (zip_stat_index(zipFile.get(), i, 0, &st) != 0 || st.name == nullptr) continue;
            const std::string entryName(st.name);
            const fs::path filePath = outputDirPath / entryName;
            try {
                // Java ZipEntry.isDirectory() <=> name ends with '/'
                const bool isDirectory = !entryName.empty() && entryName.back() == '/';
                if (isDirectory) {
                    if (!fs::exists(filePath)) {
                        fs::create_directories(filePath);
                        logger.info("Created directory: " + fs::absolute(filePath).string());
                    }
                } else {
                    extractEntry(zipFile.get(), i, filePath);
                    logger.info("Extracted file: " + fs::absolute(filePath).string());
                }
            } catch (const std::exception& e) { // per-entry IOException handler: log and continue
                logger.severe("Failed to process entry: " + entryName, e.what());
            }
        }
        return true;
    }

    bool extractFile(const std::string& fileName, const std::string& outputDir) const {
        const fs::path outputDirPath(outputDir);
        const fs::path filePath = outputDirPath / fileName;
        std::unique_ptr<zip_t, int (*)(zip_t*)> zipFile(readZipFile(), zip_close);
        if (!zipFile) return false;

        const zip_int64_t idx = zip_name_locate(zipFile.get(), fileName.c_str(), 0);
        if (idx < 0) {
            logger.warning("File not found in zip: " + fileName);
            return false;
        }

        const fs::path parentDir = filePath.parent_path();
        if (!fs::exists(parentDir)) {
            try {
                fs::create_directories(parentDir);
                logger.info("Created parent directory: " + fs::absolute(parentDir).string());
            } catch (const fs::filesystem_error& e) {
                logger.severe("Failed to create parent directory: " + fs::absolute(parentDir).string(), e.what());
                return false;
            }
        }

        try {
            extractEntry(zipFile.get(), static_cast<zip_uint64_t>(idx), filePath);
            logger.info("Extracted file: " + fs::absolute(filePath).string());
        } catch (const std::exception& e) {
            logger.severe("Failed to extract file: " + fileName, e.what());
            return false;
        }
        return true;
    }

private:
    // Package-private in Java; returns nullptr instead of a null ZipFile.
    zip_t* readZipFile() const {
        if (!fs::exists(zipFilePath_)) {
            logger.severe("Zip file does not exist: " + fs::absolute(zipFilePath_).string());
            return nullptr;
        }
        int err = 0;
        zip_t* zf = zip_open(zipFilePath_.string().c_str(), ZIP_RDONLY, &err);
        if (zf == nullptr) { // IOException path
            zip_error_t ze;
            zip_error_init_with_code(&ze, err);
            const std::string msg = zip_error_strerror(&ze);
            zip_error_fini(&ze);
            logger.severe("Failed to read the zip file: " + fs::absolute(zipFilePath_).string(), msg);
            return nullptr;
        }
        return zf;
    }

    // Mirrors: getInputStream + newOutputStream(CREATE, TRUNCATE_EXISTING) + 1024-byte copy loop.
    void extractEntry(zip_t* archive, zip_uint64_t index, const fs::path& filePath) const {
        zip_file_t* in = zip_fopen_index(archive, index, 0);
        if (in == nullptr) throw std::runtime_error(zip_strerror(archive));

        std::ofstream out(filePath, std::ios::binary | std::ios::trunc);
        if (!out) { // e.g. missing parent directory -> IOException in Java
            zip_fclose(in);
            throw std::runtime_error("Cannot open output file: " + filePath.string());
        }

        char buffer[1024];
        zip_int64_t len;
        while ((len = zip_fread(in, buffer, sizeof(buffer))) > 0) {
            out.write(buffer, static_cast<std::streamsize>(len));
        }
        zip_fclose(in);
        if (!out) throw std::runtime_error("Failed writing file: " + filePath.string());
    }

    fs::path zipFilePath_;
};

} // namespace example
} // namespace org