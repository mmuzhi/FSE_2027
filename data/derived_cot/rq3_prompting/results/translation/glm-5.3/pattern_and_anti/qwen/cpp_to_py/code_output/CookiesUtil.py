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
            with open(self.cookies_file) as file:
                cookies_data = json.load(file)
        except OSError:
            # file could not be opened -> return default (null) JSON silently
            pass
        except ValueError as e:  # covers JSONDecodeError / UnicodeDecodeError
            print(f"Error reading JSON file: {e}", file=sys.stderr)
        return cookies_data

    def _save_cookies(self):
        try:
            file = open(self.cookies_file, "w")
        except OSError:
            # file could not be opened -> fail silently
            return False
        with file:
            try:
                file.write(json.dumps(self.cookies, indent=4))
                return True
            except OSError as e:
                print(f"Error writing JSON file: {e}", file=sys.stderr)
                return False

    def set_cookies(self, request):
        request["cookies"] = "; ".join(
            f"{key}={value}" for key, value in self.cookies.items()
        )