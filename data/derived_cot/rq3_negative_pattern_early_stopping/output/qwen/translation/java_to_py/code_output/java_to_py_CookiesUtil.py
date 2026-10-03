import json
import os


class CookiesUtil:
    def __init__(self, cookies_file):
        self.cookies_file = cookies_file
        self.cookies = None

    def get_cookies(self, response):
        if "cookies" in response:
            self.cookies = response["cookies"]
        self._save_cookies()

    def load_cookies(self):
        try:
            with open(self.cookies_file, 'r') as file:
                data = json.load(file)
                return {k: str(v) for k, v in data.items()}
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    def _save_cookies(self):
        try:
            if self.cookies is None:
                data = {}
            else:
                data = {k: v for k, v in self.cookies.items()}
            with open(self.cookies_file, 'w') as file:
                json.dump(data, file)
            return True
        except Exception as e:
            print(f"Error saving cookies: {e}")
            return False

    def set_cookies(self, request):
        if self.cookies is None or not self.cookies:
            cookie_str = ""
        else:
            cookie_list = [f"{k}={v}" for k, v in self.cookies.items()]
            cookie_str = "; ".join(cookie_list)
        request["cookies"] = cookie_str