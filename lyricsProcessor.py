'''
Created on Dec 14, 2014

@author: joro
'''
import urllib2
import json


def fetchLyricsThumbnail(trackID):
#     return "what the hell am i doing here"
#     return "What the hell am I doin' here?"
#     return "I don't belong here"
    
     # build api url
    url = "http://api.musixmatch.com/ws/1.1/track.snippet.get?apikey=3122752d0d32edee9dedd70e79141de9"
    url +="&track_id=" + str(trackID)
    url +="&format=json"

    
    # URL lib2
    try:
        response = urllib2.urlopen(url)
    except urllib2.HTTPError:
        pass
            
    return response


def parseLyricsThumbnail(response):
    '''
    response - string
    '''
    response = json.load(response)
    #print response
    #response = json.load( urllib2.urlopen( url ) )
    
    #print response
    snippetText = None
    try:
    #parse response body
        snippetText = response['message']['body']['snippet']['snippet_body'];
    except:
        pass
    
    return snippetText

    
    