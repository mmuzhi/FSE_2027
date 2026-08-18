// IpUtil.h — C++ translation of org.example.IpUtil
// InetAddress.getByName(...)      -> getaddrinfo(...)   (literal IPs parse directly,
//                                                            hostnames go through resolution,
//                                                            failure == UnknownHostException)
// InetAddress.getLocalHost()      -> gethostname(...)
// getCanonicalHostName()          -> getnameinfo(...)   (no NI_NAMEREQD: falls back to the
//                                                            numeric form, like Java's best effort)
// Java null return                -> std::nullopt / std::optional<std::string>

#pragma once

#include <netdb.h>
#include <unistd.h>

#include <optional>
#include <string>
#include <utility>

namespace org::example {

class IpUtil {
public:
    static bool isValidIpv4(const std::string& ipAddress) {
        if (!resolves(ipAddress)) {
            return false;  // UnknownHostException -> false
        }
        return ipAddress.find('.') != std::string::npos &&
               ipAddress.find(':') == std::string::npos;
    }

    static bool isValidIpv6(const std::string& ipAddress) {
        if (!resolves(ipAddress)) {
            return false;  // UnknownHostException -> false
        }
        return ipAddress.find(':') != std::string::npos;
    }

    static std::optional<std::string> getHostname(const std::string& ipAddress) {
        struct addrinfo hints {};
        hints.ai_family = AF_UNSPEC;      // resolve both A and AAAA, like InetAddress
        hints.ai_socktype = SOCK_STREAM;

        struct addrinfo* result = nullptr;
        if (getaddrinfo(ipAddress.c_str(), nullptr, &hints, &result) != 0) {
            return std::nullopt;  // UnknownHostException -> null
        }

        std::optional<std::string> outcome;
        do {
            if (ipAddress == "0.0.0.0") {
                char local[NI_MAXHOST];
                if (gethostname(local, sizeof(local)) != 0) {
                    break;  // getLocalHost() failed (UnknownHostException) -> null
                }
                outcome = std::string(local);
                break;
            }

            char canonical[NI_MAXHOST];
            if (getnameinfo(result->ai_addr, result->ai_addrlen,
                            canonical, sizeof(canonical),
                            nullptr, 0, 0) != 0) {
                break;  // no name and no numeric fallback available -> null
            }
            std::string hostname(canonical);
            if (hostname == ipAddress) {
                break;  // Java returns null when hostname.equals(ipAddress)
            }
            outcome = std::move(hostname);
        } while (false);

        freeaddrinfo(result);  // released on every path
        return outcome;
    }

private:
    static bool resolves(const std::string& host) {
        struct addrinfo hints {};
        hints.ai_family = AF_UNSPEC;
        hints.ai_socktype = SOCK_STREAM;

        struct addrinfo* result = nullptr;
        bool ok = getaddrinfo(host.c_str(), nullptr, &hints, &result) == 0;
        if (ok) {
            freeaddrinfo(result);
        }
        return ok;
    }
};

}  // namespace org::example