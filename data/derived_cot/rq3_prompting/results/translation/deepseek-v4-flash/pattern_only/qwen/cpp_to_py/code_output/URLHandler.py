class URLHandler:
    def __init__(self, url: str):
        self._url = url

    def get_scheme(self) -> str:
        scheme_end = self._url.find("://")
        if scheme_end != -1:
            return self._url[:scheme_end]
        return ""

    def get_host(self) -> str:
        scheme_end = self._url.find("://")
        if scheme_end != -1:
            url_without_scheme = self._url[scheme_end + 3:]
            host_end = url_without_scheme.find("/")
            if host_end != -1:
                return url_without_scheme[:host_end]
            return url_without_scheme
        return ""

    def get_path(self) -> str:
        scheme_end = self._url.find("://")
        if scheme_end != -1:
            url_without_scheme = self._url[scheme_end + 3:]
            host_end = url_without_scheme.find("/")
            if host_end != -1:
                return url_without_scheme[host_end:]
        return ""

    def get_query_params(self) -> dict:
        params = {}
        query_start = self._url.find("?")
        fragment_start = self._url.find("#")

        if query_start != -1:
            if fragment_start != -1 and fragment_start > query_start:
                query_string = self._url[query_start + 1:fragment_start]
            else:
                query_string = self._url[query_start + 1:]

            for token in query_string.split("&"):
                if token:
                    equal_pos = token.find("=")
                    if equal_pos != -1:
                        key = token[:equal_pos]
                        value = token[equal_pos + 1:]
                        params[key] = value

        return dict(sorted(params.items()))

    def get_fragment(self) -> str:
        fragment_start = self._url.find("#")
        if fragment_start != -1:
            return self._url[fragment_start + 1:]
        return ""