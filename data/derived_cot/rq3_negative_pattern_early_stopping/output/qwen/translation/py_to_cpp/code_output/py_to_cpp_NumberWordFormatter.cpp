std::string format(int x) {
    return format_string(std::to_string(x));
}

std::string format(float x) {
    return format_string(std::to_string(x));
}

std::string format(std::nullptr_t) {
    return "";
}