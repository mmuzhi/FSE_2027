class URLHandler:
    def __init__(self, url: str) -> None:
        self.url = url

    def get_scheme(self) -> str:
        pos = self.url.find("://")
        if pos != -1:
            return self.url[:pos]
        return ""

    def get_host(self) -> str:
        pos = self.url.find("://")
        if pos != -1:
            rest = self.url[pos + 3:]
            slash_pos = rest.find("/")
            if slash_pos != -1:
                return rest[:slash_pos]
            return rest
        return ""

    def get_path(self) -> str:
        pos = self.url.find("://")
        if pos != -1:
            rest = self.url[pos + 3:]
            slash_pos = rest.find("/")
            if slash_pos != -1:
                return rest[slash_pos:]
        return ""

    def get_query_params(self) -> dict:
        params = {}
        qmark = self.url.find("?")
        if qmark == -1:
            return {}
        hash_pos = self.url.find("#")
        if hash_pos != -1 and hash_pos > qmark + 1:
            query_str = self.url[qmark + 1:hash_pos]
        else:
            query_str = self.url[qmark + 1:]
        if not query_str:
            return {}
        for token in query_str.split("&"):
            if not token:
                continue
            eq = token.find("=")
            if eq != -1:
                key = token[:eq]
                value = token[eq + 1:]
                params[key] = value
        return dict(sorted(params.items()))

    def get_fragment(self) -> str:
        pos = self.url.find("#")
        if pos != -1:
            return self.url[pos + 1:]
        return ""