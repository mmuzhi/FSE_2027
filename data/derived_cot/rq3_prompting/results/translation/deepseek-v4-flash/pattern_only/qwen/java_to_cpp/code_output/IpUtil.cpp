#include <string>
#include <cstring>
#include <cstdio>
#include <optional>
#include <sys/types.h>
#include <sys/socket.h>
#include <netdb.h>
#include <unistd.h>
#include <net/if.h>
#include <arpa/inet.h>

class IpUtil {
public:
    static bool isValidIpv4(const std::string& ipAddress) {
        struct addrinfo hints;
        std::memset(&hints, 0, sizeof(hints));
        hints.ai_family = AF_UNSPEC;
        hints.ai_socktype = SOCK_STREAM;
        struct addrinfo* res = nullptr;
        int rc = getaddrinfo(ipAddress.c_str(), nullptr, &hints, &res);
        if (rc != 0) return false;
        freeaddrinfo(res);
        return ipAddress.find('.') != std::string::npos &&
               ipAddress.find(':') == std::string::npos;
    }

    static bool isValidIpv6(const std::string& ipAddress) {
        struct addrinfo hints;
        std::memset(&hints, 0, sizeof(hints));
        hints.ai_family = AF_UNSPEC;
        hints.ai_socktype = SOCK_STREAM;
        struct addrinfo* res = nullptr;
        int rc = getaddrinfo(ipAddress.c_str(), nullptr, &hints, &res);
        if (rc != 0) return false;
        freeaddrinfo(res);
        return ipAddress.find(':') != std::string::npos;
    }

    static std::optional<std::string> getHostname(const std::string& ipAddress) {
        struct addrinfo hints;
        std::memset(&hints, 0, sizeof(hints));
        hints.ai_family = AF_UNSPEC;
        hints.ai_socktype = SOCK_STREAM;
        struct addrinfo* res = nullptr;
        int rc = getaddrinfo(ipAddress.c_str(), nullptr, &hints, &res);
        if (rc != 0) return std::nullopt;

        if (ipAddress == "0.0.0.0") {
            char hostname[1024];
            if (gethostname(hostname, sizeof(hostname)) != 0) {
                freeaddrinfo(res);
                return std::nullopt;
            }
            hostname[sizeof(hostname) - 1] = '\0';

            struct addrinfo verify_hints;
            std::memset(&verify_hints, 0, sizeof(verify_hints));
            verify_hints.ai_family = AF_UNSPEC;
            verify_hints.ai_socktype = SOCK_STREAM;
            struct addrinfo* verify_res = nullptr;
            int vrc = getaddrinfo(hostname, nullptr, &verify_hints, &verify_res);
            if (vrc != 0) {
                freeaddrinfo(res);
                return std::nullopt;
            }
            freeaddrinfo(verify_res);
            freeaddrinfo(res);
            return std::string(hostname);
        }

        const struct sockaddr* addr = res->ai_addr;
        socklen_t addrlen = res->ai_addrlen;
        struct sockaddr_in sin4;
        if (addr->sa_family == AF_INET6) {
            const struct sockaddr_in6* sin6 = reinterpret_cast<const struct sockaddr_in6*>(addr);
            if (isIPv4Mapped(sin6)) {
                std::memset(&sin4, 0, sizeof(sin4));
                sin4.sin_family = AF_INET;
                std::memcpy(&sin4.sin_addr, &sin6->sin6_addr.s6_addr[12], 4);
                addr = reinterpret_cast<const struct sockaddr*>(&sin4);
                addrlen = sizeof(sin4);
            }
        }

        char host[NI_MAXHOST];
        rc = getnameinfo(addr, addrlen, host, sizeof(host), nullptr, 0, NI_NAMEREQD);
        std::string hostname;
        if (rc == 0) {
            hostname = host;
        } else {
            hostname = javaHostAddress(addr);
        }
        freeaddrinfo(res);

        if (hostname == ipAddress) {
            return std::nullopt;
        }
        return hostname;
    }

private:
    static bool isIPv4Mapped(const struct sockaddr_in6* sin6) {
        const unsigned char* s6 = reinterpret_cast<const unsigned char*>(&sin6->sin6_addr);
        for (int i = 0; i < 10; ++i) {
            if (s6[i] != 0) return false;
        }
        return s6[10] == 0xff && s6[11] == 0xff;
    }

    static std::string javaHostAddress(const struct sockaddr* addr) {
        if (addr->sa_family == AF_INET) {
            const struct sockaddr_in* sin = reinterpret_cast<const struct sockaddr_in*>(addr);
            char buf[INET_ADDRSTRLEN];
            if (inet_ntop(AF_INET, &sin->sin_addr, buf, sizeof(buf)) != nullptr) {
                return std::string(buf);
            }
            return "";
        } else if (addr->sa_family == AF_INET6) {
            const struct sockaddr_in6* sin6 = reinterpret_cast<const struct sockaddr_in6*>(addr);
            const unsigned char* s6 = reinterpret_cast<const unsigned char*>(&sin6->sin6_addr);
            if (isIPv4Mapped(sin6)) {
                char buf[INET_ADDRSTRLEN];
                snprintf(buf, sizeof(buf), "%d.%d.%d.%d", s6[12], s6[13], s6[14], s6[15]);
                return std::string(buf);
            }
            std::string result;
            for (int i = 0; i < 8; ++i) {
                if (i > 0) result += ':';
                unsigned int group = (static_cast<unsigned int>(s6[i * 2]) << 8) |
                                     static_cast<unsigned int>(s6[i * 2 + 1]);
                char buf[5];
                snprintf(buf, sizeof(buf), "%x", group);
                result += buf;
            }
            if (sin6->sin6_scope_id != 0) {
                char ifname[IF_NAMESIZE];
                if (if_indextoname(sin6->sin6_scope_id, ifname) != nullptr) {
                    result += '%';
                    result += ifname;
                } else {
                    char scope[16];
                    snprintf(scope, sizeof(scope), "%u",
                             static_cast<unsigned int>(sin6->sin6_scope_id));
                    result += '%';
                    result += scope;
                }
            }
            return result;
        }
        return "";
    }
};