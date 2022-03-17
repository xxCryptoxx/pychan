# Python Youtube channel downloader
import zipfile
from zipfile import ZipFile
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_audio
import pytube
from pytube import Playlist
from pathlib import Path
import os
from moviepy.editor import *
import time

counter = 0
playlist_url = input(str('Insert Playlist URL: '))

def main(counter):
    ignored = [
        Playlist(playlist_url).title,
        '.git',
        'pychan.py',
        'README.md'
    ]
    playlist = Playlist(playlist_url).videos
    playlist_title = Playlist(playlist_url).title
    playlist_owner = Playlist(playlist_url).owner
    amount_of_songs = 0
    print(f'PLAYLIST: {playlist_title} - {len(playlist)} songs\n')

    for audio in playlist:
        audio_title = audio.title + ".mp3"
        amount_of_songs+=1
        completed_downloads = 0
        time.sleep(0.5)

        # check to see if the file exists
        if Path(audio_title).is_file():
            print(f'FILE EXISTS: {audio_title}')
            counter+= 1
            completed_downloads+= 1
            continue
        else:
            # if the file doesnt exist then try download
            try:
                # download begins here
                print(f'DOWNLOAD [{counter}]: {audio_title}')
                audio.streams.get_audio_only().download()
                print(f'COMPLETE: {audio_title}')
                completed_downloads+= 1
                counter+=1

            # if youtube puts an age limit on the file then skip
            except pytube.exceptions.AgeRestrictedError as age:
                print(age)
                counter+=1
                continue
            except pytube.exceptions.RecordingUnavailable as record:
                print(record)
                counter += 1
                continue
    check_the_files(amount_of_songs, playlist, playlist_title, ignored, audio_title, playlist_owner)

# check if the files are appended to the entries list
def check_the_files(amount_of_songs, playlist, playlist_title, ignored, audio_title, playlist_owner):
    print(f'CHECKING FILES: {playlist_title} - {len(playlist)} songs')
    files = 0
    entries = []
    for file in os.listdir():
        if file.endswith('.mp4'):
            print('Appending file to entries')
            entries.append(file)
            files += 1
    print(f'LOCAL: {playlist_title} - {str(files)} songs\n')
    convert_to_mp3(amount_of_songs, playlist, playlist_title, ignored, audio_title, entries, playlist_owner)

def convert_to_mp3(amount_of_songs, playlist, playlist_title, ignored, audio_title, entries, playlist_owner):
    print('CONVERTING: MP4 TO MP3')
    for entry in entries:
        mp4_file = os.path.abspath(entry)
        mp3_file = os.path.abspath(str(entry).replace('mp4', 'mp3'))        

        ffmpeg_extract_audio(mp4_file, mp3_file)
        print(f'CONVERTED: "{mp4_file}" to .mp3')
        # remove the mp4_file from the directory
        os.remove(mp4_file)
        print(f'REMOVED: {mp4_file}')

    zipPlaylist(amount_of_songs, playlist, playlist_title, ignored, audio_title, entries, playlist_owner)

# zip the files in the current directory
def zipPlaylist(amount_of_songs, playlist, playlist_title, ignored, audio_title, entries, playlist_owner):
    print(f'ZIPPING: {entries}')
    if amount_of_songs == len(playlist):
        files_that_were_zipped = 0
        zip = ZipFile(playlist_owner+ '-' + playlist_title + '.zip', 'w')

        for file in entries:
            print(f'ZIPPING: {file}')
            zip.write(file, compress_type=zipfile.ZIP_DEFLATED)
            print(f'ZIPPED: {file}')
            files_that_were_zipped += 1
            # zip.close()
            # print('zip closed')
        zip.close()
        print('Zip is closed.')
        clean_up_files(entries)
    else:
        print('Hit Else.')

def clean_up_files(entries):
    print(f'CLEANING UP: {entries}')
    for file in entries:
        try:
            print('REMOVAL: IN PROGRESS')
            os.remove(file)
            print('REMOVAL: COMPLETED')
        except PermissionError as pe:
            print(pe)
            continue
    print('COMPLETED: TASKS HAVE BEEN SUCCESSFULLY COMPLETED')

main(counter)