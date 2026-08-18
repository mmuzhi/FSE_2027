// This is a class as tool for ip that can be used to obtain the local IP address,
// validate its validity, and also provides the functionality to retrieve the
// corresponding hostname.

#include <arpa/inet.h>
#include <netdb.h>
#include <sys/socket.h>

#include <optional>
#include <stdexcept>
#include <string>

class IpUtil {
public:
    /**
     * Check if the given IP address is a valid IPv4 address.
     * :param ip_address: string, the IP address to check
     * :return: bool, true if the IP address is valid, false otherwise
     *
     * IpUtil::is_valid_ipv4("192.168.0.123") -> true
     * IpUtil::is_valid_ipv4("256.0.0.0")     -> false
     */
    static bool is_valid_ipv4(const std::string& ip_address) {
        struct in_addr addr;
        // Python: socket.inet_pton(AF_INET, ...) success -> True,
        // any socket.error (return value 0 or -1) -> False.
        return inet_pton(AF_INET, ip_address.c_str(), &addr) == 1;
    }

    /**
     * Check if the given IP address is a valid IPv6 address.
     * :param ip_address: string, the IP address to check
     * :return: bool, true if the IP address is valid, false otherwise
     *
     * IpUtil::is_valid_ipv6("2001:0db8:85a3:0000:0000:8a2e:0370:7334") -> true
     * IpUtil::is_valid_ipv6("2001:0db8:85a3:::8a2e:0370:7334")         -> false
     */
    static bool is_valid_ipv6(const std::string& ip_address) {
        struct in6_addr addr;
        return inet_pton(AF_INET6, ip_address.c_str(), &addr) == 1;
    }

    /**
     * Get the hostname associated with the given IP address.
     * :param ip_address: string, the IP address to get the hostname for
     * :return: hostname string, or std::nullopt (Python None) when the
     *          lookup fails with socket.herror
     *
     * IpUtil::get_hostname("110.242.68.3") -> "www.baidu.com"
     * IpUtil::get_hostname("10.0.0.1")     -> std::nullopt
     */
    static std::optional<std::string> get_hostname(const std::string& ip_address) {
        const void* addr_ptr = nullptr;
        socklen_t addr_len = 0;
        int family = 0;

        struct in_addr addr4;
        struct in6_addr addr6;
        if (inet_pton(AF_INET, ip_address.c_str(), &addr4) == 1) {
            family = AF_INET;
            addr_ptr = &addr4;
            addr_len = sizeof(addr4);
        } else if (inet_pton(AF_INET6, ip_address.c_str(), &addr6) == 1) {
            family = AF_INET6;
            addr_ptr = &addr6;
            addr_len = sizeof(addr6);
        } else {
            // Python raises socket.gaierror (not herror) for an unparsable
            // address, so the exception is not caught and propagates.
            throw std::runtime_error("gethostbyaddr: invalid IP address");
        }

        struct hostent* he = gethostbyaddr(addr_ptr, addr_len, family);
        if (he == nullptr || he->h_name == nullptr) {
            // socket.herror caught in Python -> None
            return std::nullopt;
        }
        return std::string(he->h_name);
    }
};