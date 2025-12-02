from Model.track import Track

class Playlist:
    def __init__(self, name):
        self.__name = name
        self.__tracks = []
        self.__duration = 0
    

    def get_name(self):
        return self.__name
    
    def get_tracks(self):
        return self.__tracks
    
    def get_total_duration_seconds(self):
        return self.__duration
    

    def set_name(self, new_name):
        self.__name = new_name
    
    def set_tracks(self, new_tracks):
        self.__tracks = new_tracks
    
    def set_duration(self, new_duration):
        self.__duration = new_duration
    

    def TotalDurationMMSS(self):
        minutes = self.__duration // 60
        seconds = self.__duration % 60
        return f"Minutes: {minutes}, Seconds: {seconds}"


    def AddTrack(self, track_obj):
        self.__tracks.append(track_obj)
        self.__duration += track_obj.get_duration_seconds()
        return True
    

    def __len__(self):
        return len(self.__tracks)
    

    def to_dict(self):
        return {
            "Name": self.__name,
            "No. of Songs": len(self.__tracks),
            "Tracks": [track.to_dict() for track in self.__tracks],
            "Total Duration (seconds)": self.__duration
        }
    def __str__(self):
        header = f"Playlist: {self.__name} ({len(self.__tracks)} tracks)"
        duration = self.TotalDurationMMSS()
        lines = [header, f"Total: {duration}"]
        if not self.__tracks:
            lines.append("(no tracks)")
        else:
            for i, t in enumerate(self.__tracks, 1):
                dur_txt = t.duration if hasattr(t, 'duration') else (t.get_duration_seconds() if hasattr(t, 'get_duration_seconds') else '')
                artist = getattr(t, 'artist', '')
                title = getattr(t, 'title', str(t))
                album = getattr(t, 'album', '')
                lines.append(f"{i}. {title} — {artist} — {album} ({dur_txt})")

        return "\n".join(lines)

    @classmethod
    def from_dict(cls, data):
        playlist = cls(data["Name"])
        playlist.set_duration(data["Total Duration (seconds)"])
        
        tracks = [Track.from_dict(track_data) for track_data in data["Tracks"]]
        playlist.set_tracks(tracks)
        
        return playlist

    # (no duplicate __str__ below)    
