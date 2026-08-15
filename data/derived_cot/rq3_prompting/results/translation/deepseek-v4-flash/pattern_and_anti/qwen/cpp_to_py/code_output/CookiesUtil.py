import json
import sys

class CookiesUtil:
    def __init__(self, cookies_file):
        self.cookies_file = cookies_file
        self.cookies = {}

    def get_cookies(self, response):
        if "cookies" in response:
            cookies_obj = response["cookies"]
            if not isinstance(cookies_obj, dict):
                raise TypeError("cookies must be a JSON object")
            new_cookies = {}
            for key, value in cookies_obj.items():
                if not isinstance(value, str):
                    raise TypeError(f"cookie value for '{key}' must be a string")
                new_cookies[key] = value
            self.cookies = new_cookies
        self._save_cookies()

    def load_cookies(self):
        cookies_data = None
        try:
            with open(self.cookies_file, 'r') as f:
                cookies_data = json.load(f)
        except FileNotFoundError:
            pass
        except Exception as e:
            print("Error reading JSON file:", e, file=sys.stderr)
        return cookies_data

    def _save_cookies(self):
        try:
            with open(self.cookies_file, 'w') as f:
                json.dump(self.cookies, f, indent=4, ensure_ascii=False)
            return True
        except Exception as e:
            print("Error writing JSON file:", e, file=sys.stderr)
            return False

    def set_cookies(self, request):
        request["cookies"] = "; ".join(f"{k}={v}" for k, v in self.cookies.items())