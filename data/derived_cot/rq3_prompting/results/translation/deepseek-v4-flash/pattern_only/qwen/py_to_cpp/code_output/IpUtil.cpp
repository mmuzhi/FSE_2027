#include <arpa/inet.h>
#include <netdb.h>
#include <sys/socket.h>

#include <cstring>
#include <optional>
#include <stdexcept>
#include <string>

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
        struct sockaddr_storage ss;
        std::memset(&ss, 0, sizeof(ss));
        socklen_t len = 0;

        struct sockaddr_in* sin = reinterpret_cast<struct sockaddr_in*>(&ss);
        if (inet_pton(AF_INET, ip_address.c_str(), &sin->sin_addr) == 1) {
            sin->sin_family = AF_INET;
            len = sizeof(struct sockaddr_in);
        } else {
            struct sockaddr_in6* sin6 = reinterpret_cast<struct sockaddr_in6*>(&ss);
            if (inet_pton(AF_INET6, ip_address.c_str(), &sin6->sin6_addr) == 1) {
                sin6->sin6_family = AF_INET6;
                len = sizeof(struct sockaddr_in6);
            } else {
                throw std::invalid_argument("illegal IP address string");
            }
        }

        char host[NI_MAXHOST];
        int rc = getnameinfo(reinterpret_cast<struct sockaddr*>(&ss), len,
                             host, sizeof(host), nullptr, 0, NI_NAMEREQD);
        if (rc == 0) {
            return std::string(host);
        }
        if (rc == EAI_NONAME) {
            return std::nullopt;
        }
        throw std::runtime_error(gai_strerror(rc));
    }
};