class URLHandler:
    def __init__(self, url: str):
        self.url = url

    def get_scheme(self) -> str:
        scheme_end = self.url.find("://")
        if scheme_end != -1:
            return self.url[:scheme_end]
        return ""

    def get_host(self) -> str:
        scheme_end = self.url.find("://")
        if scheme_end != -1:
            url_without_scheme = self.url[scheme_end + 3:]
            host_end = url_without_scheme.find("/")
            if host_end != -1:
                return url_without_scheme[:host_end]
            return url_without_scheme
        return ""

    def get_path(self) -> str:
        scheme_end = self.url.find("://")
        if scheme_end != -1:
            url_without_scheme = self.url[scheme_end + 3:]
            host_end = url_without_scheme.find("/")
            if host_end != -1:
                return url_without_scheme[host_end:]
        return ""

    def get_query_params(self) -> dict:
        params = {}
        query_start = self.url.find("?")
        fragment_start = self.url.find("#")
        if query_start != -1:
            # Mimic C++ substr(pos, count) where count underflows to a huge
            # value (i.e. "rest of string") when fragment is absent or
            # appears before the query.
            end = fragment_start if fragment_start > query_start else len(self.url)
            query_string = self.url[query_start + 1:end]
            if query_string:
                for token in query_string.split("&"):
                    if "=" in token:
                        key, value = token.split("=", 1)
                        params[key] = value
        # std::map iterates keys in sorted order; mirror that ordering.
        return dict(sorted(params.items()))

    def get_fragment(self) -> str:
        fragment_start = self.url.find("#")
        if fragment_start != -1:
            return self.url[fragment_start + 1:]
        return ""