import json
import os

class FileManager:
    def __init__(self, path):
        self.path = path

    def save(self, data):
        with open(self.path, "w") as f:
            json.dump(data, f, indent=4)

    def load(self):
        if not os.path.exists(self.path):
            return None
        with open(self.path, "r") as f:
            return json.load(f)
