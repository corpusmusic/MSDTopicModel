#!/usr/bin/env python
import sys
sys.path.append('../db_data/')
import h5py
import hdf5_getters as getter
import os
import numpy as np

# Gets wanted info about song from db info
def getInfo(files, songs):
    infoList = np.array(['tid', 'artist', 'song'])
    # Checks to see db song is in out subset, then adds it
    # Not the most efficient method
    infoList = np.zeros(18)
    for fil in files:
        for song in songs:
            if fil.split('/')[-1].split('.')[0] == song[1].split('/')[-1].split('.')[0]:
                curFile = getter.open_h5_file_read(fil)
                tid = fil.split('/')[-1].split('.')[0]
                curArtist = getter.get_artist_name(curFile)
                curTitle = getter.get_title(curFile)
                curArr = np.array([tid, curArtist, curTitle])
                infoList = np.vstack([infoList, np.hstack([curArr, song[2:]])])
                curFile.close()

    return infoList

# Saves data to a tsv file, using the given filename and array
def saveData(fName, dat):
    with open(fName+'.tsv', 'w') as f:
        np.savetxt(f, dat, delimiter='\t', fmt="%s")
    print '%s created' %(fName)

def main():
    # Set up stuffs
    dirName = '../db_data/subset/'
    songs = np.genfromtxt('song_topic_data.txt', dtype=str)
    files = [dirName + fil for fil in os.listdir(dirName) if fil.endswith('.h5')]
    
    # Get array of song tid, artick, track and save it
    infos = getInfo(files, songs)
    saveData('trackInfo', infos)
    '''
    # Open topic model data, combine it to song info and save
    topicData = np.genfromtxt('song_topic_data.txt', dtype=str)
    allData = connectData(infos, topicData)
    saveData('cleanTopicData', allData)
    '''
if __name__=='__main__':
    main()
