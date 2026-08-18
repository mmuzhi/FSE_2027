import json


class CookiesUtil:
    def __init__(self, cookies_file):
        self.cookies_file = cookies_file
        self.cookies = None

    def get_cookies(self, response):
        self.cookies = response.get("cookies")
        self._save_cookies()

    def load_cookies(self):
        try:
            with open(self.cookies_file, "r") as reader:
                json_object = json.load(reader)
            return {str(key): str(value) for key, value in json_object.items()}
        except (OSError, ValueError):
            return {}

    def _save_cookies(self):
        try:
            with open(self.cookies_file, "w") as file:
                json.dump(
                    self.cookies if self.cookies is not None else {},
                    file,
                    separators=(",", ":"),
                    ensure_ascii=False,
                )
            return True
        except OSError:
            return False

    def set_cookies(self, request):
        cookies_string = ""
        if self.cookies is not None:
            cookies_string = "; ".join(
                "{}={}".format(key, value) for key, value in self.cookies.items()
            )
        request["cookies"] = cookies_string