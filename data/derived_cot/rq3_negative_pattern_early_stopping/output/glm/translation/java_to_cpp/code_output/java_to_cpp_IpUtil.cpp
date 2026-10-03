#include <string>
#include <optional>
#include <cstring>

#ifdef _WIN32
#include <winsock2.h>
#include <ws2tcpip.h>
#pragma comment(lib, "ws2_32.lib")

// Ensure Winsock is initialized exactly once per process
static void ensureWsaInitialized() {
    static bool initialized = []() {
        WSADATA wsaData;
        WSAStartup(MAKEWORD(2, 2), &wsaData);
        return true;
    }();
    (void)initialized;
}

#else
#include <sys/types.h>
#include <sys/socket.h>
#include <netdb.h>
#include <unistd.h>
#endif

class IpUtil {
public:
    static bool isValidIpv4(const std::string& ipAddress) {
#ifdef _WIN32
        ensureWsaInitialized();
#endif
        struct addrinfo hints{}, *res;
        hints.ai_family = AF_UNSPEC; // Accept both IPv4 and IPv6
        
        // Java's InetAddress.getByName("") behaves like null, resolving to loopback
        const char* node = ipAddress.empty() ? nullptr : ipAddress.c_str();
        
        int status = getaddrinfo(node, nullptr, &hints, &res);
        if (status != 0) {
            return false; // Mimics UnknownHostException
        }
        freeaddrinfo(res);
        
        return ipAddress.find('.') != std::string::npos && 
               ipAddress.find(':') == std::string::npos;
    }

    static bool isValidIpv6(const std::string& ipAddress) {
#ifdef _WIN32
        ensureWsaInitialized();
#endif
        struct addrinfo hints{}, *res;
        hints.ai_family = AF_UNSPEC;
        
        const char* node = ipAddress.empty() ? nullptr : ipAddress.c_str();
        
        int status = getaddrinfo(node, nullptr, &hints, &res);
        if (status != 0) {
            return false; // Mimics UnknownHostException
        }
        freeaddrinfo(res);
        
        return ipAddress.find(':') != std::string::npos;
    }

    static std::optional<std::string> getHostname(const std::string& ipAddress) {
#ifdef _WIN32
        ensureWsaInitialized();
#endif
        if (ipAddress == "0.0.0.0") {
            char hostname[1024];
            if (gethostname(hostname, sizeof(hostname)) != 0) {
                return std::nullopt; // Mimics UnknownHostException
            }
            
            // Mimic InetAddress.getLocalHost() which validates that the hostname is actually resolvable
            struct addrinfo hints{}, *res;
            hints.ai_family = AF_UNSPEC;
            int status = getaddrinfo(hostname, nullptr, &hints, &res);
            if (status != 0) {
                return std::nullopt; // Mimics UnknownHostException
            }
            freeaddrinfo(res);
            
            return std::string(hostname);
        }

        struct addrinfo hints{}, *res;
        hints.ai_family = AF_UNSPEC;
        const char* node = ipAddress.empty() ? nullptr : ipAddress.c_str();
        
        int status = getaddrinfo(node, nullptr, &hints, &res);
        if (status != 0) {
            return std::nullopt; // Mimics UnknownHostException
        }

        // Copy address struct before freeing the linked list
        struct sockaddr_storage addr;
        auto addrlen = res->ai_addrlen;
        if (addrlen > sizeof(addr)) {
            freeaddrinfo(res);
            return std::nullopt;
        }
        std::memcpy(&addr, res->ai_addr, addrlen);
        freeaddrinfo(res);

        // Mimics getCanonicalHostName(): resolves DNS if possible, returns IP string otherwise
        char host[NI_MAXHOST];
        status = getnameinfo(reinterpret_cast<struct sockaddr*>(&addr), addrlen, 
                             host, sizeof(host), nullptr, 0, 0);

        if (status != 0) {
            return std::nullopt;
        }

        std::string canonicalHostName(host);
        if (canonicalHostName == ipAddress) {
            return std::nullopt; // Mimics returning null
        }
        return canonicalHostName;
    }
};