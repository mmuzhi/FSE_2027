#include <arpa/inet.h>
#include <netdb.h>
#include <string>
#include <stdexcept>

class IpUtil {
public:
    static bool is_valid_ipv4(const std::string& ip_address) {
        return inet_pton(AF_INET, ip_address.c_str()) == 1;
    }

    static bool is_valid_ipv6(const std::string& ip_address) {
        return inet_pton(AF_INET6, ip_address.c_str()) == 1;
    }

    static std::string get_hostname(const std::string& ip_address) {
        struct hostent* host_entry = gethostbyaddr((const char*)ip_address.c_str(), ip_address.length(), AF_INET);
        if (host_entry == nullptr) {
            return "";
        }
        return std::string(host_entry->h_name);
    }
};