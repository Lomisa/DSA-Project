from models.music_library import MusicLibrary
from models.playlist import Playlist
from models.music_queue import MusicQueue
from models.track import Track

def main():
    lib = MusicLibrary()

    while True:
        print("\n=== MUSIC SYSTEM ===")
        print("[1] Add Track")
        print("[2] View Library")
        print("[3] Create Playlist")
        print("[4] Exit")

        ch = input("Choice: ")

        if ch == "1":
            title = input("Title: ")
            artist = input("Artist: ")
            album = input("Album: ")
            duration = input("Duration (mm:ss): ")

            lib.add_track(Track(title, artist, album, duration))
            print("Added.")

        elif ch == "2":
            for t in lib.tracks:
                print(f"{t.title} – {t.artist} ({t.duration})")

        elif ch == "3":
            name = input("Playlist Name: ")
            pl = Playlist(name)
            print(f"Created playlist '{name}'")

        elif ch == "4":
            break


if __name__ == "__main__":
    main()
