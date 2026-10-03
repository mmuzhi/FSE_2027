#include <iostream>
#include <fstream>
#include <filesystem>
#include <boost/zip/zip_file.hpp>
#include <boost/zip/zip_entry.hpp>
#include <string>
#include <vector>
#include <iostream>
#include <cerrno>
#include <system_error>

// Define log levels
enum class LogLevel {
    SEVERE,
    WARNING,
    INFO
};

// Simple logger class
class Logger {
public:
    static void log(LogLevel level, const std::string& message) {
        switch (level) {
            case LogLevel::SEVERE:
                std::cerr << "SEVERE: " << message << std::endl;
                break;
            case LogLevel::WARNING:
                std::cout << "WARNING: " << message << std::endl;
                break;
            case LogLevel::INFO:
                std::cout << "INFO: " << message << std::endl;
                break;
        }
    }
};

// Helper function to mimic Java's Paths.get
std::filesystem::path getPath(const std::string& path) {
    return std::filesystem::path(path);
}

// Helper function to mimic Java's Files.notExists
bool notExists(const std::filesystem::path& path) {
    return !std::filesystem::exists(path);
}

// Helper function to mimic Java's Files.createDirectories
bool createDirectories(const std::filesystem::path& path) {
    try {
        std::filesystem::create_directories(path);
        return true;
    } catch (const std::filesystem::filesystem_error& e) {
        Logger::log(LogLevel::SEVERE, "Failed to create directory: " + std::string(e.what()));
        return false;
    }
}

// Helper function to mimic Java's Files.newOutputStream with options
std::ofstream newOutputStream(const std::filesystem::path& path, std::ios_base::openmode mode = std::ios::binary | std::ios::out | std::ios::trunc) {
    std::ofstream file(path, mode);
    if (!file) {
        Logger::log(LogLevel::SEVERE, "Failed to open file: " + path.string());
    }
    return file;
}

// Now, the ZipFileProcessor class
class ZipFileProcessor {
private:
    std::filesystem::path zipFilePath;

public:
    ZipFileProcessor(const std::string& zipFileName) : zipFilePath(getPath(zipFileName)) {}

    // Returns a boost::zip::zip_file or throws an exception? The original returns null on error.
    // But note: the original returns null on error, so we'll do the same.
    boost::zip::zip_file readZipFile() {
        if (notExists(zipFilePath)) {
            Logger::log(LogLevel::SEVERE, "Zip file does not exist: " + zipFilePath.string());
            return boost::zip::zip_file(); // This will be invalid
        }
        try {
            return boost::zip::zip_file(zipFilePath.string().c_str());
        } catch (const std::exception& e) {
            Logger::log(LogLevel::SEVERE, "Failed to read the zip file: " + zipFilePath.string() + ", " + e.what());
            return boost::zip::zip_file(); // Invalid
        }
    }

    bool extractAll(const std::string& outputDir) {
        std::filesystem::path outputDirPath = getPath(outputDir);
        boost::zip::zip_file zipFile = readZipFile();
        if (!zipFile) return false;

        if (notExists(outputDirPath)) {
            if (!createDirectories(outputDirPath)) {
                return false;
            }
        }

        // Iterate over each entry in the zip file
        for (boost::zip::zip_entry entry : zipFile) {
            std::filesystem::path filePath = outputDirPath / entry.name();

            try {
                if (entry.is_directory()) {
                    if (notExists(filePath)) {
                        if (!createDirectories(filePath)) {
                            return false;
                        }
                    }
                } else {
                    // Create parent directories if needed
                    std::filesystem::path parent = filePath.parent_path();
                    if (notExists(parent)) {
                        if (!createDirectories(parent)) {
                            return false;
                        }
                    }

                    // Extract the file
                    try (std::ofstream out(filePath, std::ios::binary | std::ios::out | std::ios::trunc)) {
                        if (!out) {
                            Logger::log(LogLevel::SEVERE, "Failed to open output file: " + filePath.string());
                            return false;
                        }

                        // Read from the zip entry
                        boost::zip::zip_istream in(zipFile, entry);
                        std::vector<char> buffer(1024);
                        std::streamsize len;
                        while (in >> std::setw(1024) >> std::noskipws >> len) {
                            out.write(buffer.data(), static_cast<std::streamsize>(len));
                        }
                        Logger::log(LogLevel::INFO, "Extracted file: " + filePath.string());
                    }
                }
            } catch (const std::exception& e) {
                Logger::log(LogLevel::SEVERE, "Failed to process entry: " + entry.name() + ", " + e.what());
                return false;
            }
        }

        return true;
    }

    bool extractFile(const std::string& fileName, const std::string& outputDir) {
        std::filesystem::path outputDirPath = getPath(outputDir);
        std::filesystem::path filePath = outputDirPath / fileName;
        boost::zip::zip_file zipFile = readZipFile();
        if (!zipFile) return false;

        boost::zip::zip_entry entry = zipFile.get_entry(fileName.c_str());
        if (!entry) {
            Logger::log(LogLevel::WARNING, "File not found in zip: " + fileName);
            return false;
        }

        std::filesystem::path parent = filePath.parent_path();
        if (notExists(parent)) {
            if (!createDirectories(parent)) {
                return false;
            }
        }

        try (std::ofstream out(filePath, std::ios::binary | std::ios::out | std::ios::trunc)) {
            if (!out) {
                Logger::log(LogLevel::SEVERE, "Failed to open output file: " + filePath.string());
                return false;
            }

            boost::zip::zip_istream in(zipFile, entry);
            std::vector<char> buffer(1024);
            std::streamsize len;
            while (in >> std::setw(1024) >> std::noskipws >> len) {
                out.write(buffer.data(), static_cast<std::streamsize>(len));
            }
            Logger::log(LogLevel::INFO, "Extracted file: " + filePath.string());
            return true;
        } catch (const std::exception& e) {
            Logger::log(LogLevel::SEVERE, "Failed to extract file: " + fileName + ", " + e.what());
            return false;
        }
    }
};