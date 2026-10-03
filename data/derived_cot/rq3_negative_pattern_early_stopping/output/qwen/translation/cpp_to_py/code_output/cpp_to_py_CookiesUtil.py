import json
import sys

class CookiesUtil:
    def __init__(self, cookies_file):
        self.cookies_file = cookies_file
        self.cookies = {}  # dictionary for cookies

    def get_cookies(self, response):
        # response is expected to be a dictionary (or JSON-like) with a "cookies" key that is a dictionary
        if "cookies" in response:
            self.cookies = response["cookies"]
        self._save_cookies()

    def load_cookies(self):
        # Read the JSON file and return the JSON object (dict or list)
        try:
            with open(self.cookies_file, 'r') as file:
                cookies_data = json.load(file)
        except FileNotFoundError:
            # If the file doesn't exist, return an empty dict
            cookies_data = {}
            print(f"File not found: {self.cookies_file}", file=sys.stderr)
        except Exception as e:
            print(f"Error reading JSON file: {e}", file=sys.stderr)
            cookies_data = {}
        return cookies_data

    def _save_cookies(self):
        # Convert the internal cookies (dict) to a JSON object (dict) and save it to the file.
        try:
            # We'll use json.dumps with indent=4 for pretty printing
            json_str = json.dumps(self.cookies, indent=4)
            with open(self.cookies_file, 'w') as file:
                file.write(json_str)
            return True
        except Exception as e:
            print(f"Error writing JSON file: {e}", file=sys.stderr)
            return False

    def set_cookies(self, request):
        # request is expected to be a dictionary (or JSON-like) that can have a "cookies" key set.
        # We build a string of the form "key1=value1; key2=value2"
        parts = []
        for key, value in self.cookies.items():
            parts.append(f"{key}={value}")
        if parts:
            request['cookies'] = "; ".join(parts)
        else:
            # If there are no cookies, we set cookies to an empty string
            request['cookies'] = ""