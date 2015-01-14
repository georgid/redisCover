'''
Created on Dec 14, 2014

@author: joro
'''
import urllib3
import urllib2
import json

import sys
from lyricsProcessor import fetchLyricsThumbnail, parseLyricsThumbnail

def apiMXMGet(trackID):
    # build api url
    url = "http://api.musixmatch.com/ws/1.1/track.subtitle.get?apikey=3122752d0d32edee9dedd70e79141de9"
    url +="&track_id=" + str(trackID)
    url +="&format=json"
    url +="&subtitle_format=mxm"

#     print url
    
    # URL lib2
    try:
        response = urllib2.urlopen(url)
    except urllib2.HTTPError:
        pass
            
    return response


def getAnnotaitonForResponse(response):
    '''
    response - string
    '''
    response = json.load(response)
    #print response
    #response = json.load( urllib2.urlopen( url ) )
    
    #print response
    artistMbid = None
    try:
    #parse response body
        artistMbid = response['message']['body']['subtitle']['subtitle_body'];
    except:
        pass
    
    return artistMbid

def getDuration(subtitles, lyricsThumbnail):
    '''
    getDuration
    '''
    subtitles = json.loads(subtitles)
    
    resultDuration = 0
    # result
    allDurations = []
    
    for index, subtutleLine in enumerate(subtitles):
        lyricsThumbnail = lyricsThumbnail.lower().strip()
        subtutle = subtutleLine['text'].lower().strip()
        if subtutle == lyricsThumbnail:
            # get next line to get duration
            if len(subtitles) == index+1:
                sys.exit("subtitle line is last in lyrics. Not implemented")
                
            endTs = subtitles[index+1]['time']['total']
            
            beginTs = subtutleLine['time']['total']
            
         
            allDurations.append(endTs-beginTs)
        
    # sanity check
    
    if len(allDurations) == 0:
        return None, None
        sys.exit("thumbnail Lyrics {} not occur at all at given song".format(lyricsThumbnail))
    
    sumDurs = sum(allDurations) 
     
    resultDuration = float(sumDurs) / float( len(allDurations))
    # return beginTs of last occurrence
    return resultDuration, beginTs 


def callHasLyricsAndSubtitles(trackID):
    
    # build api url
    url = "http://api.musixmatch.com/ws/1.1/track.get?apikey=3122752d0d32edee9dedd70e79141de9"
    url +="&track_id=" + str(trackID)
    url +="&format=json"

#     print url
    
    # URL lib2
    try:
        response = urllib2.urlopen(url)
    except urllib2.HTTPError:
        pass
    
    return response

def hasLyricsAndSubtitles(response):
    
    response = json.load(response)
    if response['message']["header"]["status_code"] ==404:
        return False
        
    #print response
    #response = json.load( urllib2.urlopen( url ) )
    
    #print response
    artistMbid = None
    try:
    #parse response body
        hasLyrics = response['message']['body']['track']['has_lyrics']
        
        hasSubtitles = response['message']['body']['track']['has_subtitles']
    except:
        pass
    if hasLyrics==0 or hasSubtitles==0:
        return False
    return True
    
    

def sortCoversByDuration(listMXMTrackIDs):
    '''
    for Mxm Tracks retrieve their thumbnails.
    Sort by duration of thumbnails
    '''
    resultSortedDurationsDict = []
    
        
#     response = fetchLyricsThumbnail(listMXMTrackIDs[0])
#     lyricsThumbnail = parseLyricsThumbnail(response)
#     
    for trackID in listMXMTrackIDs:
        
        
        #sanity check: has lyrics and subtitles
        response = callHasLyricsAndSubtitles(trackID)
        if not hasLyricsAndSubtitles(response):
            continue
            
        
        response = fetchLyricsThumbnail(trackID)
        
        lyricsThumbnail = parseLyricsThumbnail(response)
        
        # get subtitles
        response = apiMXMGet(trackID)
        subtitles = getAnnotaitonForResponse(response) 
        
        # TODO: if no subtitles, exit
        duration, beginTs = getDuration(subtitles, lyricsThumbnail )
        if (duration==None and beginTs==None):
            continue
        
        resultSortedDurationsDict.append((trackID, beginTs, duration))
    
    #sort by duration
    resultSortedDurationsDict = sorted(resultSortedDurationsDict, key=lambda t: t[2], reverse=True)
    
    return resultSortedDurationsDict

def getInfo(trackID):
    url = "http://api.musixmatch.com/ws/1.1/track.get?apikey=3122752d0d32edee9dedd70e79141de9"
    url +="&track_id=" + str(trackID)
    url +="&format=json"
    
    try:
        response = urllib2.urlopen(url)
    except urllib2.HTTPError:
        pass
            
    return response

def getSpotifyID(response):
    '''
    returns spotifyID 
    '''
    
    response = json.load(response)
    #print response
    #response = json.load( urllib2.urlopen( url ) )
    
    #print response
    spotifyID = None
    try:
    #parse response body
        spotifyID = response['message']['body']['track']['track_spotify_id'];
    except:
        pass
    
    return spotifyID

def addSpotifyIDs(sortedMxmTracksAndDurations):
    '''
    check if spotify IDs present, and add 
    @param - mxmIDs
    '''
    
    # add a first field spotifyID
    sortedPlusSpotify = []
    
   # get as well spotify IDs: 
    for trackAndDur in sortedMxmTracksAndDurations:
        response = getInfo(trackAndDur[0])
        
        spotifyID = None
        spotifyID = getSpotifyID(response)
        if spotifyID != None and spotifyID != "":
            sortedPlusSpotify.append( (spotifyID, trackAndDur))
            
#     for cover in coverTracks:
#         if cover[0] !="":
#             coverTracksWithSpotify.append(cover)
                    
    return sortedPlusSpotify



        
if __name__=="__main__":
    sortedPlusSpotify = addSpotifyIDs()
#     print sortedPlusSpotify 

