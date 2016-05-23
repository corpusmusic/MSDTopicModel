#!/usr/bin/env python

import h5py
import hdf5_getters as getter
import argparse
import os
import numpy as np

def getInfo(files, songs):
    infoList = np.array(['tid', 'artist', 'song'])
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

def connectData(songs, topics):
    return np.hstack([songs[1:,:], topics[:,2:]])

def saveData(fName, dat):
    with open(fName+'.tsv', 'w') as f:
        np.savetxt(f, dat, delimiter='\t', fmt="%s")
    print '%s created' %(fName)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--dir', dest='dirName')
    parser.add_argument('--songs', dest='songList')
    args = parser.parse_args()
    if args.dirName:
        dirName = args.dirName
    else:
        dirName = './subset/'
    if args.songList:
        songs = np.genfromtxt(args.songList, dtype=str)
    else:
        songs = [x.split('/')[-1].split('.')[0] for x in np.genfromtxt(\
                'tutorial_compostion.txt', dtype=str)[:,1]]
    
    files = [dirName + fil for fil in os.listdir(dirName) if fil.endswith('.h5')]
    infos = getInfo(files, songs)
    
    '''
    with open('trackInfo.tsv', 'w') as f:
        np.savetxt(f, infos, delimiter='\t', fmt="%s")
    print 'trackInfo.tsv created'
    '''
    saveData('trackInfo', infos)

    topicData = np.genfromtxt('tutorial_compostion.txt', dtype=str)

    allData = connectData(infos, topicData)
    '''
    with open('cleanTopicData.tsv', 'w') as f:
        np.savetxt(f, allData, delimiter='\t', fmt=%s)
    print 'Topic Dataset Created'
    '''
    saveData('cleanTopicData', allData)
if __name__=='__main__':
    main()
