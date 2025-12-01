from utils.file_manager import FileManager
from models.Track import Track

class MusicLibrary:
    def __init__(self):
        self.tracks = []
        self.storage = FileManager("storage/tracks.json")
        self.load()

    def add_track(self, track):
        self.tracks.append(track)
        self.sort_library()
        self.save()

    def sort_library(self):
        self.tracks.sort()

    def search(self, title):
        return [t for t in self.tracks if title.lower() in t.title.lower()]

    def save(self):
        self.storage.save([t.serialize() for t in self.tracks])

    def load(self):
        data = self.storage.load()
        if data:
            self.tracks = [Track.from_dict(d) for d in data]
