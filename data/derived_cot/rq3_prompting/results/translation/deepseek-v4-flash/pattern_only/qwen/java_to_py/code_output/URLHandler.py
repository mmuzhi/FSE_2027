class URLHandler:
    def __init__(self, url):
        self.url = url

    @staticmethod
    def _substring(s, begin, end=None):
        if end is None:
            end = len(s)
        if begin < 0 or end > len(s) or begin > end:
            raise IndexError("String index out of range: " + str(begin))
        return s[begin:end]

    def getScheme(self):
        schemeEnd = self.url.find("://")
        if schemeEnd != -1:
            return self._substring(self.url, 0, schemeEnd)
        return None

    def getHost(self):
        schemeEnd = self.url.find("://")
        if schemeEnd != -1:
            urlWithoutScheme = self._substring(self.url, schemeEnd + 3)
            hostEnd = urlWithoutScheme.find("/")
            if hostEnd != -1:
                return self._substring(urlWithoutScheme, 0, hostEnd)
            return urlWithoutScheme
        return None

    def getPath(self):
        schemeEnd = self.url.find("://")
        if schemeEnd != -1:
            urlWithoutScheme = self._substring(self.url, schemeEnd + 3)
            hostEnd = urlWithoutScheme.find("/")
            if hostEnd != -1:
                return self._substring(urlWithoutScheme, hostEnd)
        return None

    def getQueryParams(self):
        queryStart = self.url.find("?")
        fragmentStart = self.url.find("#")
        if queryStart != -1:
            end = fragmentStart if fragmentStart != -1 else len(self.url)
            queryString = self._substring(self.url, queryStart + 1, end)
            params = {}
            if queryString != "":
                paramPairs = queryString.split("&")
                for pair in paramPairs:
                    keyValue = pair.split("=")
                    while keyValue and keyValue[-1] == "":
                        keyValue.pop()
                    if len(keyValue) == 2:
                        params[keyValue[0]] = keyValue[1]
            return params
        return None

    def getFragment(self):
        fragmentStart = self.url.find("#")
        if fragmentStart != -1:
            return self._substring(self.url, fragmentStart + 1)
        return None