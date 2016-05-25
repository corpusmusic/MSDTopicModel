#!/usr/bin/env python

 import numpy as np
 from scipy.stats import chisquare
 from scipy.stats import itemfreq

def getGenreTopicis(dat):
    genres = []
    for data in dat:
        if data[0] not in genres:
            genres.append(data[0])

    genreDict = {}
    totalGenres = {}
    for genre in genres:
        genreDict[genre] = []
        totalGenres[genre] = {}
        for i in range(50):
            totalGenres[genre][i] = 0
    
    for data in dat:
        genreDict[data[0]].append(int(data[1]))

    for k,v in genreDict.iteritems():
        for i,j in itemfreq(v):
            totalGenres[k][i]+=j

    for key,value in totalGenres.iteritems():
        totalGenres[key] = {k:v for k,v in totalGenres[key].iteritems() if v != 0}

def chi2_test(dat):
    topics = dat[:,1].astype(int)
    numGenre = {'Pop'   :   1,
                'Rock'  :   2,
                'Latin' :   3,
                'Metal' :   4,
                'Reggae':   5,
                'Jazz'  :   6,
                'Rap'   :   7,
                'Electron': 8,
                'Punk'  :   9,
                'RnB'   :   10,
                'Blues' :   11,
                'Country':  12,
                'World' :   13.
                'Folk'  :   14,
                'New Age':  15}

    numGenres = [numGenre[genre] for genre in dat[:,0]]
    chi,p = chisquare(topics, numGenres)
    return chi, p

def main():
    info = np.genfromtxt('orderedTopicModel.csv', delimiter='\t', dtype=str)
    genres = []
    topics = []
    for data in info:
        genres.append(data[3].split('|')[0])
        topics.append(int(data[4].split('|')[0]))
    
    relatedInfo = np.vstack([genres, topics]).T
    
    chi2,p = chi2_test(relatedInfo)

    print "Chi2 = %s \np = %s"%(chi2,p)

if __name__=='__main__':
    main()
