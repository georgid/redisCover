'''
Created on Dec 14, 2014

@author: joro

spotify playing logic adapted from: 
https://github.com/mopidy/pyspotify/tree/v2.x/develop/examples

'''



from getCoverTrackIDs import addSpotifyIDs, sortCoversByDuration

from MSDmatcher import loadSongsInDict, loadMSD2MXMMapping, queryBySongName,\
    matchMSD2MXM
import sys
from ConnectorSpotify import ConnectorSpotify





    
    
def doit():
    print
    print "-------------------redisCover------------------------" 
    print ("the smart cover version discovery service\n\n")
    
    spotifier = ConnectorSpotify()
    spotifier.connectToSpotify()
#     
    # load cover dataset
    MSDtracksDict = loadSongsInDict()
    MSDTrack2MXMTrackMapping = loadMSD2MXMMapping()
    
    query = raw_input("\nwhich song would you like? give me a name:\n\n")
    
#     query = "Smells like teen Spirit"
#     query = 'killing me softly'
#     query = 'billy jean'
#     query = 'What A Wonderful World'
     
    print ("\nsearching covers... \nplease drink some beer while waiting!\n\n")
    
    ### I. find covers
    ############
    
        ## 1) search in MSD
    listMSDIDs = queryBySongName(query, MSDtracksDict)
    try: listMSDIDs
    except TypeError:
        sys.exit( "sorry, no covers found in MSD !... :( ")
    else:
        if len(listMSDIDs) == 0:
            sys.exit( "sorry, no covers found in MSD !... :( ")
    
    #############
    # 2) match to MXM
    listMxmTrackIDs = matchMSD2MXM(listMSDIDs, MSDTrack2MXMTrackMapping)
    
    if len(listMxmTrackIDs) == 0:
        sys.exit( "sorry, no covers found in musixMatch !... :( ")

    #############
    # 3) sort MXMs according to duration
    #     listMxmTrackIDs = [u"52116384", u"35168477", u"18102333"]
    sortedTracksAndDurations = sortCoversByDuration(listMxmTrackIDs)
    
    if len(sortedTracksAndDurations) == 0:
        sys.exit(sys.exit( "sorry, for list of covers  there are no aligned lyrics (subtitles) in musixMatch. Please add them :) ...  "))

    ###########
    # II. play in spotify

    #############
    # 1) add spotify ids 
    coverTracksWithSpotify = addSpotifyIDs(sortedTracksAndDurations)
    
    if len(coverTracksWithSpotify) == 0:
        sys.exit( "sorry, no audio found in spotify for covers !... :( ")
    ################
    # 2) play 
    print "----------------------------------------------------" 
    print ("playing the discovered covers: from slower to faster \n")

    spotifier.playinSpotify(coverTracksWithSpotify)




   


if __name__ == '__main__':
    doit()