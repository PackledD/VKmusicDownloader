import json
import os
from log import Logging
import requests


def make_name_normal(a):
    # Cuts illegal chars from name
    bad_chars = ['/', '\\', ':', '*', '?', '"', '<', '>', '|']
    a = ''.join(i for i in a if not i in bad_chars)
    return a


def get_songs_info(user):
    '''
    This function get all info about user music
    It put these into JSON-files (data files)
    If song has bad decoding name or author (not-unicode), its put
    it in folder "Bad_Songs" with song ID as name
    Else its put it in folder "Normal_Songs" (Name = 'Author' - 'Title')
    '''
    if not os.path.exists('./data'):
        os.mkdir('./data')
    with open('./data/vk_audio_list.txt', 'w') as f:
        bad_songs = 0
        Logging(
            'Looking for a user songs. It may take time if you have a lot of music', user.logfile)
        songs = user.music.get(owner_id=user.user_id)
        Logging('Find {0} songs. Trying get info about it'.format(
            len(songs)), user.logfile)
        counter = 0
        for i in songs:
            counter += 1
            try:
                f.write(i["artist"] + ' - ' + i["title"] + '\n')
                if not os.path.exists('./data/Normal_Songs'):
                    os.mkdir('./data/Normal_Songs')
                normal_song = make_name_normal(
                    str(i['artist'] + ' - ' + i['title']))
                with open('./data/Normal_Songs/' + normal_song + '.json', 'w') as good_file:
                    json.dump(i, good_file, indent=2, ensure_ascii=False)
                Logging('Get info about {0}/{1} songs. Current song: "{2} - {3}"'.format(
                    counter, len(songs), i["artist"], i["title"]), user.logfile)
            except UnicodeEncodeError:
                bad_songs += 1
                if not os.path.exists('./data/Broken_Songs'):
                    os.mkdir('./data/Broken_Songs')
                with open('./data/Broken_Songs/' + str(i['id']) + '.json', 'w') as bad_file:
                    json.dump(i, bad_file, indent=2, ensure_ascii=True)
                Logging('[WARNING]Get info about {0}/{1} songs. Bad decoding name error'.format(
                    counter, len(songs)), user.logfile)
        if bad_songs:
            f.write("\nCan't write songs(bad name decoding): " + str(bad_songs))
    Logging('Song info received', user.logfile)


def download_song(infofile_name, user, path='.'):
    # function to download song by filename (data file), user (session) and path (song will save in this place)
    Logging('Try to download song: "{0}". Getting url'.format(
        infofile_name), user.logfile)
    with open('./data/Normal_Songs/{0}.json'.format(infofile_name), 'r') as info:
        song = json.load(info)
    Logging('Start download', user.logfile)
    r = requests.get(song["url"])
    if not os.path.exists(path + '/downloads'):
        os.mkdir(path + '/downloads')
    if r.status_code == 200:
        with open(path + '/downloads/{0} - {1}.mp3'.format(song["artist"], song["title"]), 'wb') as song_mp3:
            song_mp3.write(r.content)
            Logging('Download complete successfull', user.logfile)
