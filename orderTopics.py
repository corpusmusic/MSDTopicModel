#!/usr/bin/env python
'''
Create a tsv file which orders how strong each topic is for each song
File will look like:
    tid, artist, song, 'most relevant topic model # | number' -> 'least relevant topic model number | number'
'''

import numpy as np

def run():
    trackInfo = np.genfromtxt('cleanTopicData.tsv', delimiter='\t', dtype=str)
    orderedTracks = np.zeros(18).astype(str)
    for track in trackInfo:
        nums = np.array(track[3:], dtype=float)
        order = np.argsort(nums)[::-1]
        cur = [str(int(x)) + '|' + str(nums[int(x)]) for i,x in enumerate(order)]
        orderedTracks = np.vstack([orderedTracks, np.hstack([track[:3],cur])])

    np.savetxt('orderedTopicModel.tsv', orderedTracks, delimiter='\t', fmt="%s")

if __name__=='__main__':
    run()
