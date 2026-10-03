#include <iostream>
#include <string>
#include <cstdio>
#include <ctime>
#include <chrono>
#include <cmath>

// Define a struct to hold the time components
struct TimeItem {
    int year, month, day, hour, minute, second;
};

// Helper function to convert TimeItem to a string in the specified format
std::string formatTime(const TimeItem& item, const std::string& format) {
    char buffer[20];
    if (format == "HH:mm:ss") {
        snprintf(buffer, sizeof(buffer), "%%02d:%%02d:%%02d", item.hour, item.minute, item.second);
        return std::string(buffer);
    } else if (format == "yyyy-MM-dd") {
        snprintf(buffer, sizeof(buffer), "%%d-%02d-%02d", item.year, item.month, item.day);
        return std::string(buffer);
    } else if (format == "yyyy-MM-dd HH:mm:ss") {
        snprintf(buffer, sizeof(buffer), "%%d-%02d-%02d %%02d:%%02d:%%02d", item.year, item.month, item.day, item.hour, item.minute, item.second);
        return std::string(buffer);
    } else {
        // Fallback to a simple format if not recognized
        snprintf(buffer, sizeof(buffer), "%d-%02d-%02d %02d:%02d:%02d", item.year, item.month, item.day, item.hour, item.minute, item.second);
        return std::string(buffer);
    }
}

// Helper function to parse a string into a TimeItem
TimeItem stringToTimeItem(const std::string& str) {
    // This is a simple parser that assumes the string is in the format "yyyy-M-d H:m:s"
    // We'll split the string by spaces and then parse each part.
    // This is a naive approach and might not handle all cases, but it matches the original Java code's pattern.
    // The original Java code uses: "yyyy-M-d H:m:s"
    // We'll split by space first.
    size_t pos = str.find(' ');
    if (pos == std::string::npos) {
        // No space found, try without space? But the pattern has space.
        // We'll return an invalid time item.
        return TimeItem{0,0,0,0,0,0};
    }
    std::string datePart = str.substr(0, pos);
    std::string timePart = str.substr(pos+1);

    // Parse datePart: "yyyy-M-d"
    pos = datePart.find('-');
    if (pos == std::string::npos) {
        return TimeItem{0,0,0,0,0,0};
    }
    int year = std::stoi(datePart.substr(0, pos));
    std::string monthDay = datePart.substr(pos+1);
    pos = monthDay.find('-');
    if (pos == std::string::npos) {
        return TimeItem{0,0,0,0,0,0};
    }
    int month = std::stoi(monthDay.substr(0, pos));
    int day = std::stoi(monthDay.substr(pos+1));

    // Parse timePart: "H:m:s"
    pos = timePart.find(':');
    if (pos == std::string::npos) {
        return TimeItem{0,0,0,0,0,0};
    }
    int hour = std::stoi(timePart.substr(0, pos));
    std::string minSec = timePart.substr(pos+1);
    pos = minSec.find(':');
    if (pos == std::string::npos) {
        return TimeItem{0,0,0,0,0,0};
    }
    int minute = std::stoi(minSec.substr(0, pos));
    int second = std::stoi(minSec.substr(pos+1));

    return TimeItem{year, month, day, hour, minute, second};
}

// Function to get the current time as a TimeItem
TimeItem getCurrentTimeItem() {
    std::time_t now = std::chrono::system_clock::to_time_t(std::chrono::system_clock::now());
    std::tm* utc_tm = std::localtime(&now);
    if (utc_tm == nullptr) {
        return TimeItem{0,0,0,0,0,0};
    }
    return TimeItem{
        utc_tm->tm_year + 1900,
        utc_tm->tm_mon + 1,
        utc_tm->tm_mday,
        utc_tm->tm_hour,
        utc_tm->tm_min,
        utc_tm->tm_sec
    };
}

// Now, we'll define the TimeUtils struct
struct TimeUtils {
    TimeItem datetime;

    TimeUtils() {
        this->datetime = getCurrentTimeItem();
    }

    std::string getCurrentTime() {
        return formatTime(datetime, "HH:mm:ss");
    }

    std::string getCurrentDate() {
        return formatTime(datetime, "yyyy-MM-dd");
    }

    std::string addSeconds(int seconds) {
        // We need to update the TimeItem by adding seconds
        TimeItem newTime = datetime;
        int totalSeconds = newTime.second + seconds;
        newTime.second = totalSeconds % 60;
        int totalMinutes = newTime.minute + (totalSeconds / 60);
        newTime.minute = totalMinutes % 60;
        newTime.hour += totalMinutes / 60;
        // We don't handle days/month/year change for simplicity, but the original Java code doesn't either.
        return formatTime(newTime, "HH:mm:ss");
    }

    TimeItem stringToDatetime(const std::string& string) {
        return stringToTimeItem(string);
    }

    std::string datetimeToString(const TimeItem& datetime) {
        return formatTime(datetime, "yyyy-MM-dd HH:mm:ss");
    }

    int getMinutes(const std::string& stringTime1, const std::string& stringTime2) {
        TimeItem time1 = stringToTimeItem(stringTime1);
        TimeItem time2 = stringToTimeItem(stringTime2);

        // Convert both TimeItems to total seconds since start of day
        auto toTotalSeconds = [](const TimeItem& t) -> double {
            return t.hour * 3600 + t.minute * 60 + t.second;
        };

        double totalSeconds1 = toTotalSeconds(time1);
        double totalSeconds2 = toTotalSeconds(time2);

        // Compute the difference in seconds and convert to minutes
        double diffSeconds = totalSeconds2 - totalSeconds1;
        double minutes = diffSeconds / 60.0;

        // Round to the nearest minute and convert to int
        long roundedMinutes = std::round(minutes);
        if (roundedMinutes < 0) {
            // Handle negative minutes
            roundedMinutes = -std::round(-minutes);
        }
        return static_cast<int>(roundedMinutes);
    }

    std::string getFormatTime(int year, int month, int day, int hour, int minute, int second) {
        TimeItem timeItem = {year, month, day, hour, minute, second};
        return formatTime(timeItem, "yyyy-MM-dd HH:mm:ss");
    }
};

int main() {
    TimeUtils utils;
    std::cout << "Current Time: " << utils.getCurrentTime() << std::endl;
    std::cout << "Current Date: " << utils.getCurrentDate() << std::endl;

    // Test addSeconds
    std::cout << "After adding 3600 seconds: " << utils.addSeconds(3600) << std::endl;

    // Test stringToDatetime and datetimeToString
    std::string testString = "2023-10-10 12:30:45";
    TimeItem testItem = utils.stringToDatetime(testString);
    std::cout << "Parsed datetime: " << utils.datetimeToString(testItem) << std::endl;

    // Test getMinutes
    std::string time1Str = "2023-10-10 10:00:00";
    std::string time2Str = "2023-10-10 11:00:00";
    int minutes = utils.getMinutes(time1Str, time2Str);
    std::cout << "Minutes between: " << minutes << std::endl;

    // Test getFormatTime
    std::string formatted = utils.getFormatTime(2023, 10, 10, 12, 30, 45);
    std::cout << "Formatted time: " << formatted << std::endl;

    return 0;
}