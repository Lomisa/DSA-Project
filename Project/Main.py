from Model.music_lib import MusicLibrary
from Model.playlist import Playlist
from Model.music_queue import MusicQueue
from Model.track import Track
from Utility.file_manager import FileManager
import os

def main():
    state = {
        'lib': MusicLibrary(),
        'playlists': {},
        'queue': MusicQueue()
    }

    base_dir = os.path.join(os.path.dirname(__file__), 'Storage')
    track_path = os.path.join(base_dir, 'Track.json')
    playlists_path = os.path.join(base_dir, 'playlist.json')
    queue_path = os.path.join(base_dir, 'queue.json')

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
            state['lib'].add_track(t)

    def save_library():
        fm = FileManager(track_path)
        fm.save(state['lib'].to_dict())

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
        for name, pl in state['playlists'].items():
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
            state['queue'].from_dict(data)
        except Exception:
            for td in data.get('tracks', []):
                try:
                    t = Track.from_dict(td)
                except Exception:
                    t = Track(td.get('title',''), td.get('artist',''), td.get('album',''), td.get('duration','00:00'))
                state['queue'].add_track(t)

    def save_queue():
        fm = FileManager(queue_path)
        fm.save(state['queue'].to_dict())


    load_library()
    state['playlists'].update(load_playlists())
    load_queue()

    def library_menu():
        while True:
            print("\n--- Library ---")
            print("[1] Add Track")
            print("[2] View Tracks")
            print("[3] Save Library")
            print("[4] Load Library")
            print("[5] Back to Main Menu")

            c = input("Choice: ")
            if c == "1":
                title = input("Title: ")
                artist = input("Artist: ")
                album = input("Album: ")
                duration = input("Duration (mm:ss): ")
                state['lib'].add_track(Track(title, artist, album, duration))
                print("Track added to library.")

            elif c == "2":
                if not state['lib'].tracks:
                    print("Library is empty.")
                else:
                    print("\n=== TRACKS IN LIBRARY ===")
                    for i, t in enumerate(state['lib'].tracks, 1):
                        print(f"{i}. {t.title} – {t.artist} ({t.duration})")

            elif c == "3":
                save_library()
                print("Library saved.")

            elif c == "4":
                state['lib'] = MusicLibrary()
                load_library()
                print("Library loaded.")

            elif c == "5":
                break

            else:
                print("Invalid choice.")

    def playlists_menu():
        while True:
            print("\n--- Playlists ---")
            print("[1] Create Playlist")
            print("[2] View Playlists")
            print("[3] Add Track to Playlist")
            print("[4] Save Playlists")
            print("[5] Load Playlists")
            print("[6] Back to Main Menu")

            c = input("Choice: ")
            if c == "1":
                name = input("Playlist Name: ")
                if name in state['playlists']:
                    print("A playlist with that name already exists.")
                else:
                    state['playlists'][name] = Playlist(name)
                    print(f"Created playlist '{name}'.")

            elif c == "2":
                if not state['playlists']:
                    print("No playlists created yet.")
                else:
                    print("\n=== PLAYLISTS ===")
                    for p in state['playlists'].values():
                        print(p)

            elif c == "3":
                if not state['lib'].tracks:
                    print("Library is empty.")
                    continue
                if not state['playlists']:
                    print("No playlists available.")
                    continue

                print("\nChoose a playlist:")
                for i, name in enumerate(state['playlists'].keys(), 1):
                    print(f"{i}. {name}")
                p_choice = int(input("Playlist #: ")) - 1
                playlist_name = list(state['playlists'].keys())[p_choice]
                pl = state['playlists'][playlist_name]

                print("\nChoose a track to add:")
                for i, t in enumerate(state['lib'].tracks, 1):
                    print(f"{i}. {t.title} – {t.artist}")
                t_choice = int(input("Track #: ")) - 1
                track = state['lib'].tracks[t_choice]
                pl.AddTrack(track)
                print(f"Added '{track.title}' to playlist '{playlist_name}'.")

            elif c == "4":
                save_playlists()
                print("Playlists saved.")

            elif c == "5":
                state['playlists'].clear()
                state['playlists'].update(load_playlists())
                print("Playlists loaded.")

            elif c == "6":
                break

            else:
                print("Invalid choice.")

    def queue_menu():
        while True:
            print("\n--- Queue ---")
            print("[1] Show Queue")
            print("[2] Add Playlist to Queue")
            print("[3] Play")
            print("[4] Next")
            print("[5] Previous")
            print("[6] Shuffle")
            print("[7] Unshuffle")
            print("[8] Save Queue")
            print("[9] Load Queue")
            print("[0] Back to Main Menu")

            c = input("Choice: ")
            if c == "1":
                state['queue'].show()
            elif c == "2":
                if not state['playlists']:
                    print("No playlists available.")
                    continue
                print("\nChoose a playlist to add to queue:")
                for i, name in enumerate(state['playlists'].keys(), 1):
                    print(f"{i}. {name}")
                p_choice = int(input("Playlist #: ")) - 1
                playlist_name = list(state['playlists'].keys())[p_choice]
                state['queue'].add_playlist(state['playlists'][playlist_name])
                print(f"Added playlist '{playlist_name}' to queue.")
            elif c == "3":
                state['queue'].play()
            elif c == "4":
                state['queue'].next()
            elif c == "5":
                state['queue'].previous()
            elif c == "6":
                state['queue'].shuffle()
            elif c == "7":
                state['queue'].unshuffle()
            elif c == "8":
                save_queue()
                print("Queue saved.")
            elif c == "9":
                state['queue'] = MusicQueue()
                load_queue()
                print("Queue loaded.")
            elif c == "0":
                break
            else:
                print("Invalid choice.")

    
    while True:
        print("\n=== MUSIC SYSTEM ===")
        print("[1] Library")
        print("[2] Playlists")
        print("[3] Queue")
        print("[4] Exit (auto-save)")

        ch = input("Choice: ")
        if ch == "1":
            library_menu()
        elif ch == "2":
            playlists_menu()
        elif ch == "3":
            queue_menu()
        elif ch == "4":
            save_library()
            save_playlists()
            save_queue()
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Try again.")
            
print(main())
