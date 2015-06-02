'''
Created on Dec 14, 2014

@author: joro
'''
import urllib2
import logging




def loadMSD2MXMMapping():
    '''
    load form file mapping btw MSD track IDs and mxm song IDs
    '''
    URIMapFile = "/Users/joro/Downloads/mxm_779k_matches.txt"

    dictMapping = {}
    f = open (URIMapFile)
    for line in f:
        items = line.strip().split('<SEP>')
        if len(items) > 3:
            dictMapping[items[0]]= items[3]
    
    return dictMapping

def loadSongsInDict():
    '''
    load covers from MSD  text file into a python dict
    
    format of MSD line: 
    %a,b,c, title - beginning of a clique. a,b,c are work IDs from SHS (negative if not available):  e.g. http://secondhandsongs.com/work/114512. If there are two or more, means one work is adaptation (derived) from the  other. Ususally last one in the list is the original  
    TID<SEP>AID<SEP>perf - track ID from the MSD (plus artist ID from MSD and SHS performance : SHS performanceID is same as work ID if performance is by original artist
    
    dont use anything form SHS. just take title and work with MSD 
    
    @return: result dict: track name -> MSD track ID
    
    '''
    URI_SHSFile = "/Users/joro/Downloads/shs_dataset_all.txt"
    f = open (URI_SHSFile)
    
    MSDtracksDict = []
    while 1:
        line = f.readline()
        if not line:
            break
#         print "line:", line
        tokens = line.split(',')
        #TODO check that line not empty
        
        if tokens[0].strip()[0].strip() == '%':
            songTitle_ = tokens[-1].strip().lower() # use song title as key
#             print songTitle_
            listsMSD_IDs = []
            while 1: # parse all consequent lines with covers for current song title 
                
                line = f.readline()
                tokens = line.split('<SEP>')
                if tokens[0].strip()[0].strip() == 'T': # use starts with T to indicate  it is valid MSD identifier  
                    listsMSD_IDs.append(tokens[0])
                else:
                    break
            MSDtracksDict.append((songTitle_,listsMSD_IDs))
    return MSDtracksDict

def queryBySongName(query, MSDtracksDict):
    '''
    for track name query, return MSD track ID 
    '''

    query = query.strip().lower()
    for cover_ in MSDtracksDict:
    #     print cover_
        if cover_[0] == query:
            return cover_[1]

def matchMSD2MXM(listMSDTrackIDs, dictMapping): 
    '''
    for a list of MSD track IDs return a list of MXM IDs
    '''
    listMXM_IDs= set()
    for  MSDID in  listMSDTrackIDs:
        if MSDID in dictMapping:
            MXMID = dictMapping[MSDID]
            listMXM_IDs.add(MXMID)
        else: # songs not in mapping file
            logging.debug( "MSD track ID not found in file. calling echonest to retrieve MXM song_id...")

            MXMID = MSD2MXMbyEchoNest(MSDID)
            try: MXMID
            except TypeError:
                pass
            else: listMXM_IDs.add(MXMID)
  
            
            
    return listMXM_IDs
        
def MSD2MXMbyEchoNest(MSDID):
    url = "http://developer.echonest.com/api/v4/song/profile?api_key=TTLRGYQWHKPHUPLPX&format=json"
    url += "&track_id=" + str(MSDID)
    url += "&bucket=id:musixmatch-WW&limit=true"
    
    return None

    try:
        response = urllib2.urlopen(url)
    except urllib2.HTTPError:
        pass
    resultSongs = response['songs']['foreign_ids']
    # TODO: finish parsing if needed 
#     for resultSong in resultSongs:
#         a = resultSong['foreign_id']
#         b = a.strip(":")
    return None
             

if __name__ == '__main__': # unit test 
    
    
    MSDtracksDict = loadSongsInDict()
    MSDTrack2MXMTrackMapping = loadMSD2MXMMapping()
    
    query = "Smells like teen Spirit"
    #query = 'killing me softly'
    query = 'billy jean'
    
    listMSDIDs = queryBySongName(query, MSDtracksDict)
    listMxmTrackIDs = matchMSD2MXM(listMSDIDs, MSDTrack2MXMTrackMapping)

    print listMxmTrackIDs
    
    
    
    