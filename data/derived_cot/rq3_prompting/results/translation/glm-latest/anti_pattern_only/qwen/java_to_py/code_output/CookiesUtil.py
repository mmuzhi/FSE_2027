import json
from typing import Dict, Optional


class CookiesUtil:
    def __init__(self, cookies_file: str):
        self.cookies_file = cookies_file
        self.cookies: Optional[Dict[str, str]] = None

    def get_cookies(self, response: Dict[str, Dict[str, str]]) -> None:
        self.cookies = response.get("cookies")
        self._save_cookies()

    def load_cookies(self) -> Dict[str, str]:
        try:
            with open(self.cookies_file) as reader:
                json_object = json.load(reader)
        except (OSError, ValueError):
            # IOException | ParseException -> empty map
            return {}
        # Mirror the Java casts: a non-object payload or a non-string value
        # raises (ClassCastException -> TypeError) instead of being swallowed.
        if not isinstance(json_object, dict):
            raise TypeError(
                f"Cannot cast {type(json_object).__name__} to JSONObject"
            )
        cookies_data: Dict[str, str] = {}
        for key, value in json_object.items():
            if not isinstance(value, str):
                raise TypeError(f"Cannot cast {type(value).__name__} to String")
            cookies_data[key] = value
        return cookies_data

    def _save_cookies(self) -> bool:
        try:
            json_object = dict(self.cookies) if self.cookies is not None else {}
            with open(self.cookies_file, "w") as file:
                file.write(
                    json.dumps(json_object, separators=(",", ":"), ensure_ascii=False)
                )
                file.flush()
            return True
        except OSError:
            return False

    def set_cookies(self, request: Dict[str, str]) -> None:
        cookies_string = ""
        if self.cookies is not None:
            cookies_string = "; ".join(
                f"{key}={value}" for key, value in self.cookies.items()
            )
        request["cookies"] = cookies_string