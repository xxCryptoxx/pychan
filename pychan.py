# Python Youtube channel downloader
import zipfile
from zipfile import ZipFile
import pytube
from pytube import Playlist
from pathlib import Path
import os

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
        audio_title = audio.title + ".mp4"
        amount_of_songs+=1
        completed_downloads = 0

        # check to see if the file exists
        if Path(audio_title).is_file():
            print(f'EXISTS: {audio_title}')
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

def check_the_files(amount_of_songs, playlist, playlist_title, ignored, audio_title, playlist_owner):
    print(f'PLAYLIST: {playlist_title} - {len(playlist)} songs')
    files = 0
    entries = []
    for file in os.listdir():
        if file.endswith('.mp4'):
            print('Appending file to entries')
            entries.append(file)
            files += 1
    print(f'LOCAL: {playlist_title} - {str(files)} songs\n')
    zipPlaylist(amount_of_songs, playlist, playlist_title, ignored, audio_title, entries, playlist_owner)

def zipPlaylist(amount_of_songs, playlist, playlist_title, ignored, audio_title, entries, playlist_owner):
    print(f'CURRENT FILES: {entries}')
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