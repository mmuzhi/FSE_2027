// Tool class for IP utilities: validate IPv4/IPv6 addresses and resolve hostnames.
// Mirrors Python's IpUtil: is_valid_ipv4 / is_valid_ipv6 / get_hostname.
#include <optional>
#include <stdexcept>
#include <string>

#ifdef _WIN32
#include <winsock2.h>
#include <ws2tcpip.h>
#pragma comment(lib, "Ws2_32.lib")
#else
#include <arpa/inet.h>
#include <netdb.h>
#include <netinet/in.h>
#include <sys/socket.h>
#include <sys/types.h>
#endif

class IpUtil {
public:
    IpUtil() = delete;  // static-only utility class

    // Check if the given IP address is a valid IPv4 address.
    // True if valid, False otherwise (Python: inet_pton(AF_INET, ...) or False on error).
    static bool is_valid_ipv4(const std::string& ip_address) {
        struct in_addr addr;
        return inet_pton(AF_INET, ip_address.c_str(), &addr) == 1;
    }

    // Check if the given IP address is a valid IPv6 address.
    static bool is_valid_ipv6(const std::string& ip_address) {
        struct in6_addr addr;
        return inet_pton(AF_INET6, ip_address.c_str(), &addr) == 1;
    }

    // Get the hostname associated with the given IP address.
    // Returns std::nullopt when the reverse lookup fails (Python returns None on socket.herror).
    // Throws std::runtime_error for a malformed address (Python propagates socket.gaierror, uncaught there).
    static std::optional<std::string> get_hostname(const std::string& ip_address) {
        ensure_wsa_startup();

        const void* raw_addr = nullptr;
        int addr_family = 0;
        int addr_len = 0;

        struct in_addr addr4;
        struct in6_addr addr6;
        if (inet_pton(AF_INET, ip_address.c_str(), &addr4) == 1) {
            raw_addr = &addr4;
            addr_family = AF_INET;
            addr_len = static_cast<int>(sizeof(addr4));
        } else if (inet_pton(AF_INET6, ip_address.c_str(), &addr6) == 1) {
            raw_addr = &addr6;
            addr_family = AF_INET6;
            addr_len = static_cast<int>(sizeof(addr6));
        } else {
            // Mirrors socket.gethostbyaddr raising socket.gaierror for bad addresses.
            throw std::runtime_error("Illegal IP address passed to gethostbyaddr");
        }

        struct hostent* he = gethostbyaddr(static_cast<const char*>(raw_addr),
                                           addr_len, addr_family);
        if (he == nullptr || he->h_name == nullptr) {
            return std::nullopt;  // Python: socket.herror caught -> None
        }
        return std::string(he->h_name);  // Python: gethostbyaddr(...)[0]
    }

private:
    static void ensure_wsa_startup() {
#ifdef _WIN32
        static const bool initialized = [] {
            WSADATA data;
            return WSAStartup(MAKEWORD(2, 2), &data) == 0;
        }();
        (void)initialized;
#endif
    }
};