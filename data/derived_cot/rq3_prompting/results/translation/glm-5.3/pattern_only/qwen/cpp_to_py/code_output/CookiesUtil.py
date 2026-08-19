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
        try:
            with open(self.cookies_file, "r") as file:
                return json.load(file)
        except FileNotFoundError:
            # C++: ifstream fails to open silently -> default (null) json
            return None
        except (OSError, json.JSONDecodeError) as e:
            print(f"Error reading JSON file: {e}", file=sys.stderr)
            return None

    def _save_cookies(self):
        try:
            with open(self.cookies_file, "w") as file:
                json.dump(self.cookies, file, indent=4)
                return True
        except OSError as e:
            print(f"Error writing JSON file: {e}", file=sys.stderr)
            return False

    def set_cookies(self, request):
        request["cookies"] = "; ".join(f"{key}={value}" for key, value in self.cookies.items())