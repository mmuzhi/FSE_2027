import datetime
from typing import Dict, Any, Optional

class AccessGatewayFilter:
    def filter(self, request: Dict[str, Any]) -> bool:
        request_uri = request.get("path", "")
        method = request.get("method", "")
        
        if self.is_start_with(request_uri):
            return True
            
        try:
            headers = request.get("headers", {})
            token_map = headers.get("Authorization")
            if not token_map:
                return False
                
            token = token_map.get("user", {})
            jwt_str = token.get("jwt", "")
            user_level = token.get("level")
            
            if user_level is not None and int(user_level) > 2:
                self.set_current_user_info_and_log(token)
                return True
        except Exception:
            return False
            
        return False
        
    def is_start_with(self, request_uri: str) -> bool:
        prefixes = ["/api", "/login"]
        for prefix in prefixes:
            if request_uri.startswith(prefix):
                return True
        return False
        
    def set_current_user_info_and_log(self, user: Dict[str, Any]) -> None:
        host = user.get("address", "")
        name = user.get("name", "")
        current_date = datetime.datetime.now().strftime("%Y-%m-%d")
        message = f"{name}{host}{current_date}"
        print(message)
        
    def get_jwt_user(self, request: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        headers = request.get("headers", {})
        token_map = headers.get("Authorization")
        if not token_map:
            return None
            
        user = token_map.get("user", {})
        jwt = token.get("jwt", "")
        name = user.get("name", "")
        
        if jwt.startswith(name):
            jwt_str_date = jwt[len(name):]
            try:
                formatter = datetime.datetime.strptime(jwt_str_date, "%Y-%m-%d")
            except ValueError:
                return None
                
            current_date = datetime.datetime.now().date()
            jwt_date = formatter.date()
            if current_date > jwt_date + datetime.timedelta(days=3):
                return None
                
        return token_map