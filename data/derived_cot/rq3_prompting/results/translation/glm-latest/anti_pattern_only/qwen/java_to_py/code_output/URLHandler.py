from typing import Dict, List, Optional


class URLHandler:
    def __init__(self, url: str) -> None:
        self.url = url

    def get_scheme(self) -> Optional[str]:
        scheme_end = self.url.find("://")
        if scheme_end != -1:
            return self.url[:scheme_end]
        return None

    def get_host(self) -> Optional[str]:
        scheme_end = self.url.find("://")
        if scheme_end != -1:
            url_without_scheme = self.url[scheme_end + 3:]
            host_end = url_without_scheme.find("/")
            if host_end != -1:
                return url_without_scheme[:host_end]
            return url_without_scheme
        return None

    def get_path(self) -> Optional[str]:
        scheme_end = self.url.find("://")
        if scheme_end != -1:
            url_without_scheme = self.url[scheme_end + 3:]
            host_end = url_without_scheme.find("/")
            if host_end != -1:
                return url_without_scheme[host_end:]
        return None

    def get_query_params(self) -> Optional[Dict[str, str]]:
        query_start = self.url.find("?")
        fragment_start = self.url.find("#")
        if query_start != -1:
            end = fragment_start if fragment_start != -1 else len(self.url)
            # Java's substring(begin, end) throws when begin > end,
            # i.e. when '#' appears before '?'.
            if query_start + 1 > end:
                raise IndexError(
                    f"begin {query_start + 1}, end {end}, length {len(self.url)}"
                )
            query_string = self.url[query_start + 1:end]
            params: Dict[str, str] = {}
            if query_string != "":
                for pair in self._java_split(query_string, "&"):
                    key_value = self._java_split(pair, "=")
                    if len(key_value) == 2:
                        params[key_value[0]] = key_value[1]
            return params
        return None

    def get_fragment(self) -> Optional[str]:
        fragment_start = self.url.find("#")
        if fragment_start != -1:
            return self.url[fragment_start + 1:]
        return None

    @staticmethod
    def _java_split(s: str, sep: str) -> List[str]:
        # Mimics Java's String.split(sep): returns [s] when sep does not
        # occur in s, and drops trailing empty segments otherwise.
        if sep not in s:
            return [s]
        parts = s.split(sep)
        while parts and parts[-1] == "":
            parts.pop()
        return parts