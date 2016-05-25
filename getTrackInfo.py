#!/usr/bin/env python
import h5py
import os
import numpy as np
import argparse
import sys

try:
    sys.path.append('./PythonSrc/')
    import hdf5_getters as getter
except:
    print 'No PythonSrc Directory Found'

# Gets wanted info about song from db info
def getInfo(files, genres, songs, topicNum):
    # Checks to see db song is in out subset, then adds it
    # Not the most efficient method
    infoList = np.zeros(topicNum+4)
    for fil in files:
        for song in songs:
            if fil.split('/')[-1].split('.')[0] == song[1].split('/')[-1].split('.')[0]:
                curFile = getter.open_h5_file_read(fil)
                tid = fil.split('/')[-1].split('.')[0]
                curArtist = getter.get_artist_name(curFile)
                curTitle = getter.get_title(curFile)
                curArr = np.array([tid, curArtist, curTitle])
                infoList = np.vstack([infoList, np.hstack([curArr, genres[tid], song[2:]])])
                curFile.close()

    return infoList[1:]

'''
Create a tsv file which orders how strong each topic is for each song
File will look like:
    tid, artist, song, genre*|genre2*, 'most relevant topic model # | number' -> 
        'least relevant topic model number | number'
    |genre2 will only appear if applicable
'''
def orderInfo(data, topicNum):
    orderedTracks = np.zeros(topicNum+4).astype(str)
    for track in data:
        nums = np.array(track[4:], dtype=float)
        order = np.argsort(nums)[::-1]
        cur = [str(int(x)) + '|' + str(nums[int(x)]) for i,x in enumerate(order)]
        orderedTracks = np.vstack([orderedTracks, np.hstack([track[:4],cur])])

    return orderedTracks[1:]

def createRelationCsv(info):
    genres = []
    topics = []
    for data in info:
        genres.append(data[3].split('|')[0])
        topics.append(int(data[4].split('|')[0]))

    return np.vstack([genres, topics]).T

# Saves data to a tsv file, using the given filename and array
def saveData(fName, dat):
    with open(fName+'.tsv', 'w') as f:
        np.savetxt(f, dat, delimiter='\t', fmt="%s")
    print '%s created' %(fName)


def main():
    # Set up stuffs
    parser = argparse.ArgumentParser()
    parser.add_argument('--num-topics', dest='topicNum')
    parser.add_argument('--subset-loc', dest='dirName')
    parser.add_argument('--song-topics-file', dest='songs')
    parser.add_argument('--getter-loc', dest='getterLoc')
    parser.add_argument('--genre-file', dest='genreFile')
    parser.add_argument('--save-unordered', dest='saveUnordered')
    args = parser.parse_args()

    if args.topicNum:
        topicNum = int(args.topicNum)
    else:
        print 'Error: num-topics needed'
        return
    if args.dirName:
        dirName = args.dirName
    else:
        dirName = '../db_data/subset/'
    files = [dirName + fil for fil in os.listdir(dirName) if fil.endswith('.h5')]
    
    if args.songs:
        songs = np.genfromtxt(args.songs, dtype=str)
    else:
        songs = np.genfromtxt('song_topic_data.txt', dtype=str)

    if args.getterLoc:
        sys.path.append(args.getterLoc)
        import hdf5_getters as getter

    if args.genreFile:
        genreFile = args.genreFile
    else:
        genreFile = '../db_data/msd_tagtraum_cd2.cls'

    genreDict = {}
    with open(genreFile) as t:
        genreData = t.readlines()
        for line in genreData:
            d = [x.strip('\n') for x in line.split('\t')]
            vals = '|'.join(d[1:])
            genreDict[d[0]] = vals

    if args.saveUnordered:
        saveUnordered = args.saveUnordered
    else:
        saveUnordered = False

    # Get array of song tid, artick, track and save it
    infos = getInfo(files, genreDict, songs, topicNum)
    if saveUnordered:
        saveData('cleanTopicData', infos)

    # Order information by topic relevancy and save it
    ordered = orderInfo(infos, topicNum)
    saveData('orderedTopicModel', ordered)

    yn = raw_input('Create Genre -> Topic csv (y or n): ')

    print yn
    if yn == 'y':
        topicRelation = createRelationCsv(ordered)
        saveData('genreTopicRelation', topicRelation)
    else:
        return

if __name__=='__main__':
    main()
