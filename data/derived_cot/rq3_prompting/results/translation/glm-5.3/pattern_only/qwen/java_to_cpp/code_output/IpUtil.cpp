// IpUtil.cpp — C++ translation of org.example.IpUtil (Java).
// InetAddress.getByName / getCanonicalHostName semantics are mirrored with
// getaddrinfo / getnameinfo (resolver-based, accepts hostnames AND IP literals,
// exactly like Java's InetAddress, not just literal parsing).

#include <memory>
#include <optional>
#include <string>

#ifdef _WIN32
#  include <winsock2.h>
#  include <ws2tcpip.h>
#  pragma comment(lib, "ws2_32.lib")
namespace {
struct WsaInit {
    WsaInit() { WSADATA d; WSAStartup(MAKEWORD(2, 2), &d); }
    ~WsaInit() { WSACleanup(); }
} const g_wsaInit;
}
#else
#  include <netdb.h>
#  include <unistd.h>
#endif

namespace org::example {

class IpUtil {
public:
    // Java: public static boolean isValidIpv4(String)
    static bool isValidIpv4(const std::string& ipAddress) {
        if (!resolve(ipAddress)) return false;            // UnknownHostException -> false
        return ipAddress.find('.') != std::string::npos &&
               ipAddress.find(':') == std::string::npos;
    }

    // Java: public static boolean isValidIpv6(String)
    static bool isValidIpv6(const std::string& ipAddress) {
        if (!resolve(ipAddress)) return false;            // UnknownHostException -> false
        return ipAddress.find(':') != std::string::npos;
    }

    // Java: public static String getHostname(String) — Java null maps to std::nullopt
    static std::optional<std::string> getHostname(const std::string& ipAddress) {
        AddrInfoPtr res = resolveAll(ipAddress);
        if (!res) return std::nullopt;                    // UnknownHostException -> null

        if (ipAddress == "0.0.0.0") {
            return localHostName();                       // InetAddress.getLocalHost().getHostName()
        }

        // InetAddress.getCanonicalHostName(): reverse lookup; falls back to the
        // textual form of the address when no name is found.
        char name[NI_MAXHOST];
        for (const addrinfo* p = res.get(); p != nullptr; p = p->ai_next) {
            if (p->ai_addr == nullptr) continue;
            std::string hostname;
            if (::getnameinfo(p->ai_addr, p->ai_addrlen, name, sizeof(name),
                              nullptr, 0, NI_NAMEREQD) == 0) {
                hostname = name;                          // canonical name resolved
            } else if (::getnameinfo(p->ai_addr, p->ai_addrlen, name, sizeof(name),
                                     nullptr, 0, NI_NUMERICHOST) == 0) {
                hostname = name;                          // fallback: address text
            } else {
                continue;
            }
            if (hostname == ipAddress) return std::nullopt; // Java: return null
            return hostname;
        }
        return std::nullopt;
    }

private:
    struct AddrInfoDeleter {
        void operator()(addrinfo* p) const noexcept { if (p) ::freeaddrinfo(p); }
    };
    using AddrInfoPtr = std::unique_ptr<addrinfo, AddrInfoDeleter>;

    // Mirrors InetAddress.getByName(String): resolves via the system resolver,
    // so both hostnames ("localhost", "example.com") and IP literals succeed.
    static AddrInfoPtr resolveAll(const std::string& ipAddress) {
        std::string host = ipAddress;
        if (host.empty()) host = "127.0.0.1";             // Java: empty host -> loopback
        if (host.size() >= 2 && host.front() == '[' && host.back() == ']') {
            host = host.substr(1, host.size() - 2);       // Java accepts "[::1]"
        }
        addrinfo hints{};
        hints.ai_family = AF_UNSPEC;                      // IPv4 or IPv6, like InetAddress
        hints.ai_socktype = SOCK_STREAM;
        addrinfo* res = nullptr;
        if (::getaddrinfo(host.c_str(), nullptr, &hints, &res) != 0) {
            return nullptr;                               // resolution failed
        }
        return AddrInfoPtr(res);
    }

    static bool resolve(const std::string& ipAddress) {
        return resolveAll(ipAddress) != nullptr;
    }

    // Mirrors InetAddress.getLocalHost().getHostName(): null when the local host
    // name cannot be determined or resolved (UnknownHostException -> null).
    static std::optional<std::string> localHostName() {
        char buf[256];
        if (::gethostname(buf, sizeof(buf)) != 0) return std::nullopt;
        addrinfo hints{};
        hints.ai_family = AF_UNSPEC;
        addrinfo* res = nullptr;
        if (::getaddrinfo(buf, nullptr, &hints, &res) != 0) return std::nullopt;
        ::freeaddrinfo(res);
        return std::string(buf);
    }
};

} // namespace org::example