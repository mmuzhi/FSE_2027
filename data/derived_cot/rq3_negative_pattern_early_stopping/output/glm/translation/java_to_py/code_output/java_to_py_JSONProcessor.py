import json
import os

class JSONProcessor:

    def readJson(self, filePath):
        if not os.path.exists(filePath):
            return None
        try:
            with open(filePath, 'r') as reader:
                return json.load(reader)
        except Exception:
            return None

    def writeJson(self, data, filePath):
        try:
            with open(filePath, 'w') as writer:
                json.dump(data, writer)
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