from models.music_lib import MusicLibrary
from models.Playlist import Playlist
from models.music_queue import MusicQueue
from models.Track import Track

def main():
    lib = MusicLibrary()
    playlists = {}     
    queue = MusicQueue()  

    while True:
        print("\n=== MUSIC SYSTEM ===")
        print("[1] Add Track to Library")
        print("[2] View Library")
        print("[3] Create Playlist")
        print("[4] View Playlists")
        print("[5] Add Track to Playlist")
        print("[6] Exit")

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
            print("Goodbye!")
            break

        else:
            print("Invalid choice. Try again.")
