class URLHandler:
    def __init__(self, url):
        self.url = url

    @staticmethod
    def _java_split(s, delim):
        # Java's String.split drops trailing empty strings; Python's does not.
        parts = s.split(delim)
        while parts and parts[-1] == '':
            parts.pop()
        return parts

    def get_scheme(self):
        scheme_end = self.url.find('://')
        if scheme_end != -1:
            return self.url[:scheme_end]
        return None

    def get_host(self):
        scheme_end = self.url.find('://')
        if scheme_end != -1:
            url_without_scheme = self.url[scheme_end + 3:]
            host_end = url_without_scheme.find('/')
            if host_end != -1:
                return url_without_scheme[:host_end]
            return url_without_scheme
        return None

    def get_path(self):
        scheme_end = self.url.find('://')
        if scheme_end != -1:
            url_without_scheme = self.url[scheme_end + 3:]
            host_end = url_without_scheme.find('/')
            if host_end != -1:
                return url_without_scheme[host_end:]
        return None

    def get_query_params(self):
        query_start = self.url.find('?')
        fragment_start = self.url.find('#')
        if query_start != -1:
            end = fragment_start if fragment_start != -1 else len(self.url)
            if query_start + 1 > end:
                # Java's substring throws when begin > end (e.g. '#' before '?');
                # Python slicing would silently return '' instead.
                raise IndexError(
                    'begin {}, end {}, length {}'.format(query_start + 1, end, len(self.url))
                )
            query_string = self.url[query_start + 1:end]
            params = {}
            if query_string != '':
                for pair in self._java_split(query_string, '&'):
                    key_value = self._java_split(pair, '=')
                    if len(key_value) == 2:
                        params[key_value[0]] = key_value[1]
            return params
        return None

    def get_fragment(self):
        fragment_start = self.url.find('#')
        if fragment_start != -1:
            return self.url[fragment_start + 1:]
        return None