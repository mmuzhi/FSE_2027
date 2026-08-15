import os
import json


def _reject_constant(value):
    raise ValueError("Invalid JSON constant: " + value)


def _gson_dumps(obj):
    s = json.dumps(obj, ensure_ascii=False, separators=(',', ':'), allow_nan=False)
    # Gson escapes these HTML characters by default
    s = s.replace('<', '\\u003c')
    s = s.replace('>', '\\u003e')
    s = s.replace('&', '\\u0026')
    s = s.replace('=', '\\u003d')
    s = s.replace("'", '\\u0027')
    return s


class JSONProcessor:

    def readJson(self, filePath):
        if not os.path.exists(filePath):
            return None
        try:
            with open(filePath, 'r', newline='') as reader:
                data = json.load(reader, parse_constant=_reject_constant)
            if not isinstance(data, dict):
                return None
            return data
        except Exception:
            return None

    def writeJson(self, data, filePath):
        try:
            with open(filePath, 'w', newline='') as writer:
                writer.write(_gson_dumps(data))
            return True
        except Exception:
            return False

    def processJson(self, filePath, removeKey):
        data = self.readJson(filePath)
        if data is None:
            return False
        if removeKey in data:
            del data[removeKey]
            return self.writeJson(data, filePath)
        else:
            return False