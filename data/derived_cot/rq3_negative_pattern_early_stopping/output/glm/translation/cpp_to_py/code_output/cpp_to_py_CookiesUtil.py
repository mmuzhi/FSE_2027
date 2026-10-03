import json
import sys


class CookiesUtil:
    def __init__(self, cookies_file):
        self.cookies_file = cookies_file
        self.cookies = {}

    def get_cookies(self, response):
        if "cookies" in response:
            self.cookies = dict(response["cookies"])
        self._save_cookies()

    def load_cookies(self):
        cookies_data = None
        try:
            with open(self.cookies_file, "r") as f:
                cookies_data = json.load(f)
        except OSError:
            pass
        except Exception as e:
            print(f"Error reading JSON file: {e}", file=sys.stderr)
        return cookies_data

    def _save_cookies(self):
        try:
            with open(self.cookies_file, "w") as f:
                json.dump(self.cookies, f, indent=4)
            return True
        except OSError:
            return False
        except Exception as e:
            print(f"Error writing JSON file: {e}", file=sys.stderr)
            return False

    def set_cookies(self, request):
        parts = []
        for key, value in self.cookies.items():
            parts.append(f"{key}={value}")
        request["cookies"] = "; ".join(parts)