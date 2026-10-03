class URLHandler:
    def __init__(self, url):
        self.url = url

    def get_scheme(self):
        pos = self.url.find("://")
        if pos != -1:
            return self.url[:pos]
        return ""

    def get_host(self):
        pos_scheme = self.url.find("://")
        if pos_scheme != -1:
            url_without_scheme = self.url[pos_scheme+3:]
            pos_host = url_without_scheme.find("/")
            if pos_host != -1:
                return url_without_scheme[:pos_host]
            return url_without_scheme
        return ""

    def get_path(self):
        pos_scheme = self.url.find("://")
        if pos_scheme != -1:
            url_without_scheme = self.url[pos_scheme+3:]
            pos_host = url_without_scheme.find("/")
            if pos_host != -1:
                return url_without_scheme[pos_host:]
        return ""

    def get_query_params(self):
        params = {}
        pos_query = self.url.find("?")
        pos_fragment = self.url.find("#")
        if pos_query != -1:
            # Extract the query string without the fragment
            start_query = pos_query + 1
            if pos_fragment != -1:
                end_query = pos_fragment
            else:
                end_query = len(self.url)
            query_string = self.url[start_query:end_query]
            if query_string:
                # Now parse the query string
                # We'll split by '&' and then by '='
                # The C++ code does: first split by '&' and then for each part, split by '=' (only the first '=' is used)
                # Then, it processes the last part separately? Actually, the C++ code does:
                #   while ((pos = query_string.find("&")) != std::string::npos) {
                #       token = query_string.substr(0, pos);
                #       ... process token ...
                #       query_string.erase(0, pos + 1);
                #   }
                #   then process the remaining query_string.
                # But note: the C++ code does not use the same method for the last token? Actually, it does the same: splits by the first '='.

                # Let's do the same: split the query_string by '&' and then for each part, split by the first '='.

                # However, note: the C++ code does not use the same method for the last token. It uses the same method for the last token.

                # We can do:
                #   tokens = query_string.split('&')
                #   for each token, split by '=' at the first occurrence.

                # But note: the C++ code modifies the query_string by removing the first part (with &) and then processes the next part. We don't need to modify the string, we can split.

                tokens = query_string.split('&')
                for token in tokens:
                    if '=' in token:
                        key, value = token.split('=', 1)
                        params[key] = value
        return params

    def get_fragment(self):
        pos_fragment = self.url.find("#")
        if pos_fragment != -1:
            return self.url[pos_fragment+1:]
        return ""