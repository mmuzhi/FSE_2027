#include <string>
#include <cstring>
#include <arpa/inet.h>
#include <netdb.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <unistd.h>

class IpUtil {
public:
    static bool is_valid_ipv4(const std::string& ip_address) {
        struct sockaddr_in sa;
        return inet_pton(AF_INET, ip_address.c_str(), &(sa.sin_addr)) == 1;
    }

    static bool is_valid_ipv6(const std::string& ip_address) {
        struct sockaddr_in6 sa;
        return inet_pton(AF_INET6, ip_address.c_str(), &(sa.sin6_addr)) == 1;
    }

    static std::string get_hostname(const std::string& ip_address) {
        struct sockaddr_storage addr;
        socklen_t addr_len;
        void* addr_ptr;

        if (is_valid_ipv4(ip_address)) {
            struct sockaddr_in* sa = reinterpret_cast<struct sockaddr_in*>(&addr);
            sa->sin_family = AF_INET;
            inet_pton(AF_INET, ip_address.c_str(), &(sa->sin_addr));
            addr_len = sizeof(struct sockaddr_in);
            addr_ptr = sa;
        } else if (is_valid_ipv6(ip_address)) {
            struct sockaddr_in6* sa6 = reinterpret_cast<struct sockaddr_in6*>(&addr);
            sa6->sin6_family = AF_INET6;
            inet_pton(AF_INET6, ip_address.c_str(), &(sa6->sin6_addr));
            addr_len = sizeof(struct sockaddr_in6);
            addr_ptr = sa6;
        } else {
            return "";
        }

        char host[NI_MAXHOST];
        int result = getnameinfo(static_cast<struct sockaddr*>(addr_ptr), addr_len,
                                 host, sizeof(host), nullptr, 0, NI_NAMEREQD);
        if (result != 0) {
            return "";
        }
        return std::string(host);
    }
};