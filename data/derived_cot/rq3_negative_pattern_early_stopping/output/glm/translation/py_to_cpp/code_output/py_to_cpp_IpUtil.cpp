#include <string>
#include <optional>
#include <arpa/inet.h>
#include <netdb.h>

class IpUtil {
public:
    static bool is_valid_ipv4(const std::string& ip_address) {
        struct in_addr addr;
        return inet_pton(AF_INET, ip_address.c_str(), &addr) == 1;
    }

    static bool is_valid_ipv6(const std::string& ip_address) {
        struct in6_addr addr;
        return inet_pton(AF_INET6, ip_address.c_str(), &addr) == 1;
    }

    static std::optional<std::string> get_hostname(const std::string& ip_address) {
        struct addrinfo hints = {};
        hints.ai_family = AF_UNSPEC;
        hints.ai_socktype = SOCK_STREAM;
        hints.ai_flags = AI_NUMERICHOST;

        struct addrinfo* res = nullptr;
        int status = getaddrinfo(ip_address.c_str(), nullptr, &hints, &res);
        if (status != 0) {
            return std::nullopt;
        }

        char host[NI_MAXHOST];
        status = getnameinfo(res->ai_addr, res->ai_addrlen, host, sizeof(host), nullptr, 0, NI_NAMEREQD);
        freeaddrinfo(res);

        if (status != 0) {
            return std::nullopt;
        }

        return std::string(host);
    }
};