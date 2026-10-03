import json

class CookiesUtil:
    def __init__(self, cookies_file: str):
        self.cookies_file = cookies_file
        self.cookies = None

    def get_cookies(self, response: dict) -> None:
        self.cookies = response.get("cookies")
        self._save_cookies()

    def load_cookies(self) -> dict:
        try:
            with open(self.cookies_file, 'r') as reader:
                cookies_data = json.load(reader)
            if isinstance(cookies_data, dict):
                return {str(k): str(v) for k, v in cookies_data.items()}
            else:
                return {}
        except (FileNotFoundError, json.JSONDecodeError, IOError):
            return {}

    def _save_cookies(self) -> bool:
        try:
            with open(self.cookies_file, 'w') as file:
                if self.cookies is not None:
                    json.dump(self.cookies, file)
                else:
                    json.dump({}, file)
            return True
        except IOError:
            return False

    def set_cookies(self, request: dict) -> None:
        cookies_string = ""
        if self.cookies is not None:
            parts = []
            for key, value in self.cookies.items():
                parts.append(f"{key}={value}")
            cookies_string = "; ".join(parts)
        request["cookies"] = cookies_string