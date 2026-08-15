import json

class CookiesUtil:
    def __init__(self, cookiesFile):
        self.cookiesFile = cookiesFile
        self.cookies = None

    def getCookies(self, response):
        self.cookies = response.get("cookies")
        self._saveCookies()

    def loadCookies(self):
        try:
            with open(self.cookiesFile, 'r') as reader:
                data = json.load(reader)
                if not isinstance(data, dict):
                    raise TypeError("Expected a JSON object")
                cookiesData = {}
                for key, value in data.items():
                    if value is not None and not isinstance(value, str):
                        raise TypeError("Cookie value must be a string")
                    cookiesData[key] = value
                return cookiesData
        except (OSError, ValueError):
            return {}

    def _saveCookies(self):
        try:
            with open(self.cookiesFile, 'w') as file:
                json.dump(self.cookies if self.cookies is not None else {}, file, separators=(',', ':'))
                file.flush()
            return True
        except OSError:
            return False

    def setCookies(self, request):
        if self.cookies is not None:
            parts = []
            for k, v in self.cookies.items():
                if v is None:
                    v = "null"
                parts.append(f"{k}={v}")
            request["cookies"] = "; ".join(parts)
        else:
            request["cookies"] = ""