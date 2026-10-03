#include <string>
#include <cstring>
#include <sys/socket.h>
#include <netdb.h>
#include <arpa/inet.h>
#include <unistd.h>

namespace {

bool hasChar(const std::string& s, char c) {
    return s.find(c) != std::string::npos;
}

} // anonymous namespace

bool isValidIpv4(const std::string& ipAddress) {
    struct addrinfo hints, *res;
    std::memset(&hints, 0, sizeof(hints));
    hints.ai_family = AF_UNSPEC;
    hints.ai_socktype = SOCK_STREAM;
    hints.ai_flags = AI_NUMERICHOST;

    int err = getaddrinfo(ipAddress.c_str(), nullptr, &hints, &res);
    if (err != 0) {
        return false;
    }
    freeaddrinfo(res);
    return hasChar(ipAddress, '.') && !hasChar(ipAddress, ':');
}

bool isValidIpv6(const std::string& ipAddress) {
    struct addrinfo hints, *res;
    std::memset(&hints, 0, sizeof(hints));
    hints.ai_family = AF_UNSPEC;
    hints.ai_socktype = SOCK_STREAM;
    hints.ai_flags = AI_NUMERICHOST;

    int err = getaddrinfo(ipAddress.c_str(), nullptr, &hints, &res);
    if (err != 0) {
        return false;
    }
    freeaddrinfo(res);
    return hasChar(ipAddress, ':');
}

std::string getHostname(const std::string& ipAddress) {
    if (ipAddress == "0.0.0.0") {
        char hostname[256];
        if (gethostname(hostname, sizeof(hostname)) != 0) {
            return std::string();
        }
        return std::string(hostname);
    }

    struct addrinfo hints, *res;
    std::memset(&hints, 0, sizeof(hints));
    hints.ai_family = AF_UNSPEC;
    hints.ai_socktype = SOCK_STREAM;
    hints.ai_flags = AI_NUMERICHOST;

    int err = getaddrinfo(ipAddress.c_str(), nullptr, &hints, &res);
    if (err != 0) {
        return std::string();
    }

    char host[NI_MAXHOST];
    err = getnameinfo(res->ai_addr, res->ai_addrlen, host, sizeof(host), nullptr, 0, NI_NAMEREQD);
    freeaddrinfo(res);
    if (err != 0) {
        return std::string();
    }

    std::string hostname(host);
    if (hostname == ipAddress) {
        return std::string();
    }
    return hostname;
}