class URLHandler:
    def __init__(self, url):
        self.url = url

    def get_scheme(self):
        scheme_end = self.url.find("://")
        if scheme_end != -1:
            return self.url[0:scheme_end]
        return None

    def get_host(self):
        scheme_end = self.url.find("://")
        if scheme_end != -1:
            url_without_scheme = self.url[scheme_end + 3:]
            host_end = url_without_scheme.find("/")
            if host_end != -1:
                return url_without_scheme[:host_end]
            return url_without_scheme
        return None

    def get_path(self):
        scheme_end = self.url.find("://")
        if scheme_end != -1:
            url_without_scheme = self.url[scheme_end + 3:]
            host_end = url_without_scheme.find("/")
            if host_end != -1:
                return url_without_scheme[host_end:]
        return None

    @staticmethod
    def _java_split(s, delim):
        # Java's String.split(delim) (limit 0) drops trailing empty strings;
        # Python's str.split keeps them, so trim them to preserve behavior.
        parts = s.split(delim)
        while parts and parts[-1] == "":
            parts.pop()
        return parts

    def get_query_params(self):
        query_start = self.url.find("?")
        fragment_start = self.url.find("#")
        if query_start != -1:
            # Java substring(begin, end) throws when begin > end
            # (e.g. '#' occurs before '?'); Python slicing would silently
            # return "" instead, so mirror the exception here.
            if fragment_start != -1 and query_start + 1 > fragment_start:
                raise IndexError(
                    "begin " + str(query_start + 1) + ", end "
                    + str(fragment_start) + ", length " + str(len(self.url))
                )
            if fragment_start != -1:
                query_string = self.url[query_start + 1:fragment_start]
            else:
                query_string = self.url[query_start + 1:]
            params = {}
            if query_string != "":
                param_pairs = self._java_split(query_string, "&")
                for pair in param_pairs:
                    key_value = self._java_split(pair, "=")
                    if len(key_value) == 2:
                        params[key_value[0]] = key_value[1]
            return params
        return None

    def get_fragment(self):
        fragment_start = self.url.find("#")
        if fragment_start != -1:
            return self.url[fragment_start + 1:]
        return None