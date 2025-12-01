from Utility.file_manager import FileManager
from Model.track import Track

class Library:
    def __init__(self, track):
        self.track = track
        self.left = None
        self.right = None

class MusicLibrary:
    def __init__(self):
        # keep a simple list of tracks for APIs that expect `tracks`
        self.tracks = []
        # also maintain BST root for backwards compatibility
        self.root = None

    def insert(self, track):
        # keep list in insertion order
        self.tracks.append(track)
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
        # Represent the library as a list of track dicts
        try:
            # prefer track objects' to_dict if exists
            return [t.to_dict() if hasattr(t, 'to_dict') else (t.serialize() if hasattr(t, 'serialize') else {}) for t in self.tracks]
        except Exception:
            return []

    # Backwards-compatible API used by interactive code
    def add_track(self, track):
        self.insert(track)

    def get_tracks(self):
        return self.tracks

    def __len__(self):
        return len(self.tracks)

    def __iter__(self):
        return iter(self.tracks)

