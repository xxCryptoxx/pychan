# Python Youtube channel downloader
from os import name
import threading
from pytube import Playlist
import pytube
from pathlib import Path

from pytube.extract import video_id

playlist_url = input(str('Insert Playlist URL: '))
def main(k):
    p = Playlist(playlist_url)
    print(f'Downloading: {p.title}')

    for video in p.videos:
        try:
            title = video.title + '.mp3'
            print(title + " else hit")

            if (Path(title).is_file()):
                print(f'{title} already exists.')
                pass
            else:
                print(video.title + " else hit")
                video.streams.get_audio_only().download()
                print(title)
        except pytube.exceptions.AgeRestrictedError as age:
            print(age)
            continue
threads = []
for k in range(3):
    t = threading.Thread(target=main, args=(k,))
    threads.append(t)
    print(k)
    t.start()