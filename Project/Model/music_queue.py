import random
from Model.track import Track

class MusicQueue:
    def __init__(self):
        self.__tracks = []
        self.__current = 0
        self.__repeat = False
        self.__shuffled_order = None

    def add_track(self, track):
        self.__tracks.append(track)

    def add_playlist(self, playlist):
        for track in playlist.get_tracks():
            self.add_track(track)

    def play(self):
        if not self.__tracks:
            print("Queue is empty")
            return
        track = self.__tracks[self.__current]
        album = getattr(track, 'album', '')
        print(f"Playing: {track.title} - {track.artist} - {album} ({track.get_duration_seconds()} sec)")

    def next(self):
        if not self.__tracks:
            return

        if self.__current + 1 < len(self.__tracks):
            self.__current += 1
        elif self.__repeat:
            self.__current = 0
        else:
            print("Reached end of queue")
            return

        self.play()

    def previous(self):
        if not self.__tracks:
            return

        if self.__current > 0:
            self.__current -= 1
        elif self.__repeat:
            self.__current = len(self.__tracks) - 1
        else:
            print("At the beginning of the queue")
            return

        self.play()

    def toggle_repeat(self):
        self.__repeat = not self.__repeat
        print("Repeat is", "ON" if self.__repeat else "OFF")

    def shuffle(self):
        if not self.__tracks:
            return

        order = list(range(len(self.__tracks)))
        random.shuffle(order)

        self.__tracks = [self.__tracks[i] for i in order]
        self.__current = 0
        self.__shuffled_order = order

    def unshuffle(self):
        if self.__shuffled_order is None:
            print("Queue is not shuffled")
            return

        original_positions = sorted(
            range(len(self.__tracks)),
            key=lambda i: self.__shuffled_order[i]
        )

        self.__tracks = [self.__tracks[i] for i in original_positions]
        self.__current = 0
        self.__shuffled_order = None

    def total_duration(self):
        total = sum(track.get_duration_seconds() for track in self.__tracks)
        hours = total // 3600
        minutes = (total % 3600) // 60
        seconds = total % 60
        return f"{hours} hr {minutes} min {seconds} sec"

    def show(self, page=1, per_page=10):
        if not self.__tracks:
            print("Queue is empty")
            return

        start = (page - 1) * per_page
        end = start + per_page

        print(f"Total Duration: {self.total_duration()}")
        current = self.__tracks[self.__current]
        current_album = getattr(current, 'album', '')
        print(f"Currently Playing: {current.title} - {current.artist} - {current_album}")

        for i, track in enumerate(self.__tracks[start:end], start=start + 1):
            album = getattr(track, 'album', '')
            print(f"{i}. {track.title} - {track.artist} - {album} ({track.get_duration_seconds()} sec)")

        print(f"<Page {page}>")

    def to_dict(self):
        return {
            "tracks": [t.to_dict() if hasattr(t, 'to_dict') else (t.serialize() if hasattr(t, 'serialize') else {}) for t in self.__tracks],
            "current_index": self.__current,
            "repeat": self.__repeat,
            "shuffled": self.__shuffled_order is not None
        }

    def from_dict(self, data):
        self.__tracks = []
        for td in data.get('tracks', []):
            try:
                t = Track.from_dict(td)
            except Exception:
                t = Track(td.get('title', ''), td.get('artist', ''), td.get('album', ''), td.get('duration', '00:00'))
            self.add_track(t)

        idx = data.get('current_index')
        if isinstance(idx, int) and 0 <= idx < len(self.__tracks):
            self.__current = idx

        if data.get('repeat'):
            self.__repeat = True
        else:
            self.__repeat = False

