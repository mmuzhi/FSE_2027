import json

class CookiesUtil:
    def __init__(self, cookies_file):
        self.cookies_file = cookies_file
        self.cookies = None

    def getCookies(self, response):
        self.cookies = response.get("cookies")
        self._saveCookies()

    def loadCookies(self):
        try:
            with open(self.cookies_file, 'r') as reader:
                data = json.load(reader)
            if not isinstance(data, dict):
                raise TypeError("JSON object expected")
            cookies_data = {}
            for key, value in data.items():
                if not isinstance(key, str):
                    raise TypeError("key is not a string")
                if value is not None and not isinstance(value, str):
                    raise TypeError("value is not a string")
                cookies_data[key] = value
            return cookies_data
        except (OSError, ValueError):
            return {}

    def _saveCookies(self):
        try:
            with open(self.cookies_file, 'w') as file:
                obj = {}
                if self.cookies is not None:
                    for key, value in self.cookies.items():
                        if key is None:
                            raise TypeError("null key")
                        if value is not None:
                            obj[key] = value
                file.write(json.dumps(obj, separators=(',', ':'), ensure_ascii=False))
                file.flush()
                return True
        except OSError:
            return False

    def setCookies(self, request):
        cookies_string = []
        if self.cookies is not None:
            for key, value in self.cookies.items():
                if len(cookies_string) > 0:
                    cookies_string.append("; ")
                cookies_string.append(self._to_java_string(key) + "=" + self._to_java_string(value))
        request["cookies"] = "".join(cookies_string)

    @staticmethod
    def _to_java_string(obj):
        if obj is None:
            return "null"
        if isinstance(obj, bool):
            return "true" if obj else "false"
        return str(obj)