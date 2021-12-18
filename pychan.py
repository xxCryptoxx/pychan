# Python Youtube channel downloader
from os import name
import threading
from pytube import Playlist
import pytube
from pathlib import Path

counter = 0
playlist_url = input(str('Insert Playlist URL: '))

def main(counter):
    playlist = Playlist(playlist_url).videos
    for audio in playlist:
        title = audio.title + ".mp4"

        # check to see if the file exists
        if Path(title).is_file():
            print(f'{title} already exists.')
            counter+= 1
            continue
        else:
            # if the file doesnt exist then try download
            try:
                print(f'{title} is downloading.')
                audio.streams.get_audio_only().download()
                counter+=1

            # if youtube puts an age limit on the file then skip
            except pytube.exceptions.AgeRestrictedError as age:
                print(age)
                counter+=1
                continue

main(counter)