from utils.file_manager import FileManager
from models.Track import Track

class Library:
    def __init__(self, track):
        self.track = track
        self.left = None
        self.right = None

class MusicLibrary:
    def __init__(self):
        self.root = None

    def insert(self, track):
        if self.root is None:
            self.root = Library(track)
        else:
            self._insert_recursive(self.root, track)

    def _insert_recursive(self, node, track):
        if track < node.track:
            if node.left is None:
                node.left = Library(track)
            else:
                self._insert_recursive(node.left, track)
        else:
            if node.right is None:
                node.right = Library(track)
            else:
                self._insert_recursive(node.right, track)

    def search(self, track):
        return self._search_recursive(self.root, track)

    def _search_recursive(self, node, track):
        if node is None:
            return False
        if node.track == track:
            return True
        elif track < node.track:
            return self._search_recursive(node.left, track)
        else:
            return self._search_recursive(node.right, track)
        
    def to_dict(self):
        return self._to_dict_recursive(self.root)

