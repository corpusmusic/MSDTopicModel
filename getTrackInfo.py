#!/usr/bin/env python

import h5py
import hdf5_getters as getter
import os
import numpy as np

# Gets wanted info about song from db info
def getInfo(files, songs):
    infoList = np.array(['tid', 'artist', 'song'])
    # Checks to see db song is in out subset, then adds it
    # Not the most efficient method
    for fil in files:
        for song in songs:
            if fil.split('/')[-1].split('.')[0] == song:
                curFile = getter.open_h5_file_read(fil)
                tid = fil.split('/')[-1].split('.')[0]
                curArtist = getter.get_artist_name(curFile)
                curTitle = getter.get_title(curFile)
                curArr = np.array([tid, curArtist, curTitle])
                infoList = np.vstack([infoList, curArr])
                curFile.close()

    return infoList

# Connects song info to topic model info, 
# forming a larger array to return
def connectData(songs, topics):
    return np.hstack([songs[1:,:], topics[:,2:]])

# Saves data to a tsv file, using the given filename and array
def saveData(fName, dat):
    with open(fName+'.tsv', 'w') as f:
        np.savetxt(f, dat, delimiter='\t', fmt="%s")
    print '%s created' %(fName)

def main():
    # Set up stuffs
    dirName = '../db_data/subset/'
    songs = [x.split('/')[-1].split('.')[0] for x in np.genfromtxt(\
                        'song_topic_data.txt', dtype=str)[:,1]]
    files = [dirName + fil for fil in os.listdir(dirName) if fil.endswith('.h5')]
    
    # Get array of song tid, artick, track and save it
    infos = getInfo(files, songs)
    saveData('trackInfo', infos)

    # Open topic model data, combine it to song info and save
    topicData = np.genfromtxt('song_topic_data.txt', dtype=str)
    allData = connectData(infos, topicData)
    saveData('cleanTopicData', allData)

if __name__=='__main__':
    main()
