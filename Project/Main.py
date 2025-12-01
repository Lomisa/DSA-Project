from Model.music_lib import MusicLibrary
from Model.playlist import Playlist
from Model.music_queue import MusicQueue
from Model.track import Track
from Utility.file_manager import FileManager
import os

def main():
    lib = MusicLibrary()
    playlists = {}
    queue = MusicQueue()

    # Paths for storage files
    base_dir = os.path.join(os.path.dirname(__file__), 'Storage')
    track_path = os.path.join(base_dir, 'Track.json')
    playlists_path = os.path.join(base_dir, 'playlist.json')
    queue_path = os.path.join(base_dir, 'queue.json')

    # helper functions for load/save
    def load_library():
        fm = FileManager(track_path)
        data = fm.load()
        if not data:
            return
        for td in data:
            try:
                t = Track.from_dict(td)
            except Exception:
                t = Track(td.get('title', ''), td.get('artist', ''), td.get('album', ''), td.get('duration', '00:00'))
            lib.add_track(t)

    def save_library():
        fm = FileManager(track_path)
        fm.save(lib.to_dict())

    def load_playlists():
        fm = FileManager(playlists_path)
        data = fm.load()
        if not data:
            return {}
        pls = {}
        for name, pdata in data.items():
            pname = pdata.get('name') or pdata.get('Name') or name
            tracks = pdata.get('tracks') or pdata.get('Tracks') or []
            pl = Playlist(pname)
            track_objs = []
            for td in tracks:
                try:
                    track_objs.append(Track.from_dict(td))
                except Exception:
                    track_objs.append(Track(td.get('title',''), td.get('artist',''), td.get('album',''), td.get('duration','00:00')))
            pl.set_tracks(track_objs)
            total = pdata.get('total_duration') or pdata.get('Total Duration (seconds)') or sum(t.duration_seconds() for t in track_objs)
            pl.set_duration(total)
            pls[pname] = pl
        return pls

    def save_playlists():
        fm = FileManager(playlists_path)
        data = {}
        for name, pl in playlists.items():
            data[name] = {
                'name': pl.get_name(),
                'tracks': [t.to_dict() if hasattr(t, 'to_dict') else (t.serialize() if hasattr(t, 'serialize') else {}) for t in pl.get_tracks()],
                'total_duration': pl.get_total_duration_seconds()
            }
        fm.save(data)

    def load_queue():
        fm = FileManager(queue_path)
        data = fm.load()
        if not data:
            return
        try:
            queue.from_dict(data)
        except Exception:
            # fallback: add tracks only
            for td in data.get('tracks', []):
                try:
                    t = Track.from_dict(td)
                except Exception:
                    t = Track(td.get('title',''), td.get('artist',''), td.get('album',''), td.get('duration','00:00'))
                queue.add_track(t)

    def save_queue():
        fm = FileManager(queue_path)
        fm.save(queue.to_dict())

    # Auto-load stored data on startup
    load_library()
    playlists.update(load_playlists())
    load_queue()

    while True:
        print("\n=== MUSIC SYSTEM ===")
        print("[1] Add Track to Library")
        print("[2] View Library")
        print("[3] Create Playlist")
        print("[4] View Playlists")
        print("[5] Add Track to Playlist")
        print("[6] Save data to Storage")
        print("[7] Load data from Storage")
        print("[8] Exit (auto-save)")

        ch = input("Choice: ")

        if ch == "1":
            title = input("Title: ")
            artist = input("Artist: ")
            album = input("Album: ")
            duration = input("Duration (mm:ss): ")

            lib.add_track(Track(title, artist, album, duration))
            print("Track added to library.")

        elif ch == "2":
            if not lib.tracks:
                print("Library is empty.")
            else:
                print("\n=== TRACKS IN LIBRARY ===")
                for i, t in enumerate(lib.tracks, 1):
                    print(f"{i}. {t.title} – {t.artist} ({t.duration})")

        elif ch == "3":
            name = input("Playlist Name: ")

            if name in playlists:
                print("A playlist with that name already exists.")
            else:
                playlists[name] = Playlist(name)
                print(f"Created playlist '{name}'.")

        elif ch == "4":
            if not playlists:
                print("No playlists created yet.")
            else:
                print("\n=== PLAYLISTS ===")
                for p in playlists.values():
                    print(p)

        elif ch == "5":
            if not lib.tracks:
                print("Library is empty.")
                continue

            if not playlists:
                print("No playlists available.")
                continue

            print("\nChoose a playlist:")
            for i, name in enumerate(playlists.keys(), 1):
                print(f"{i}. {name}")

            p_choice = int(input("Playlist #: ")) - 1
            playlist_name = list(playlists.keys())[p_choice]
            pl = playlists[playlist_name]

            print("\nChoose a track to add:")
            for i, t in enumerate(lib.tracks, 1):
                print(f"{i}. {t.title} – {t.artist}")

            t_choice = int(input("Track #: ")) - 1
            track = lib.tracks[t_choice]

            pl.AddTrack(track)
            print(f"Added '{track.title}' to playlist '{playlist_name}'.")

        elif ch == "6":
            save_library()
            save_playlists()
            save_queue()
            print("Data saved to Storage.")

        elif ch == "7":
            lib = MusicLibrary()
            playlists.clear()
            queue = MusicQueue()
            load_library()
            playlists.update(load_playlists())
            load_queue()
            print("Data loaded from Storage.")

        elif ch == "8":
            save_library()
            save_playlists()
            save_queue()
            print("Goodbye!")
            break

        else:
            print("Invalid choice. Try again.")
            
print(main())
