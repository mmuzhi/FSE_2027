import json
import sys

class CookiesUtil:
    def __init__(self, cookies_file):
        self.cookies_file = cookies_file
        self.cookies = {}

    def get_cookies(self, response):
        if isinstance(response, dict) and "cookies" in response:
            cookies_data = response["cookies"]
            if not isinstance(cookies_data, dict) or not all(
                isinstance(k, str) and isinstance(v, str) for k, v in cookies_data.items()
            ):
                raise TypeError("cookies must be an object with string values")
            self.cookies = dict(cookies_data)
        self._save_cookies()

    def load_cookies(self):
        try:
            with open(self.cookies_file, 'r') as f:
                try:
                    return json.load(f)
                except Exception as e:
                    print(f"Error reading JSON file: {e}", file=sys.stderr)
                    return None
        except OSError:
            return None

    def _save_cookies(self):
        try:
            f = open(self.cookies_file, 'w')
        except OSError:
            return False
        with f:
            try:
                f.write(json.dumps(self.cookies, indent=4, ensure_ascii=False))
                return True
            except Exception as e:
                print(f"Error writing JSON file: {e}", file=sys.stderr)
                return False

    def set_cookies(self, request):
        request["cookies"] = "; ".join(f"{k}={v}" for k, v in self.cookies.items())