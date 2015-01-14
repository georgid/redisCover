'''
Created on Dec 14, 2014

@author: joro

spotify playing logic adapted from: 
https://github.com/mopidy/pyspotify/tree/v2.x/develop/examples

'''



from getCoverTrackIDs import addSpotifyIDs, sortCoversByDuration

from MSDmatcher import loadSongs, loadMSD2MXMMapping, queryBySongName,\
    matchMSD2MXM
import sys
from ConnectorSpotify import ConnectorSpotify





    
    
def doit():
    print
    print "-------------------redisCover------------------------" 
    print ("the fastest cover version discovery service\n\n\n")
    
    spotifier = ConnectorSpotify()
    spotifier.connectToSpotify()
#     
    # load cover dataset
    resultDict = loadSongs()
    dictMapping = loadMSD2MXMMapping()
    
    query = 'What A Wonderful World'
    query = raw_input("\nwhich song would you like? give me a name:\n\n")
    
#     query = "Smells like teen Spirit"
#     #query = 'killing me softly'
#     query = 'billy jean'
#     query = 'What A Wonderful World'
     
    print ("searching covers... please drink some beer while waiting!\n\n")
    
    ### I. find covers
    ############
    ## 1) search in MSD
    listMSDIDs = queryBySongName(query, resultDict)
    if len(listMSDIDs) == 0:
        sys.exit( "sorry, no covers found in MSD !... :( ")
    
    #############
    # 2) match to MXM
    listMxmTrackIDs = matchMSD2MXM(listMSDIDs, dictMapping)
    
    if len(listMxmTrackIDs) == 0:
        sys.exit( "sorry, no covers found in musixMatch !... :( ")

    #############
    # 3) sort MXMs according to duration
    #     listMxmTrackIDs = [u"52116384", u"35168477", u"18102333"]
    sortedTracksAndDurations = sortCoversByDuration(listMxmTrackIDs)
    
    if len(sortedTracksAndDurations) == 0:
        sys.exit(sys.exit( "sorry, no covers with lyrics and subtitles in musixMatch. Please add them :) ...  "))

    ###########
    # II. play in spotify

    #############
    # 1) add spotify ids 
    coverTracksWithSpotify = addSpotifyIDs(sortedTracksAndDurations)
    
    if len(coverTracksWithSpotify) == 0:
        sys.exit( "sorry, no audio found in spotify for covers !... :( ")
    ################
    # 2) play 

    spotifier.playinSpotify(coverTracksWithSpotify)




   


if __name__ == '__main__':
    doit()