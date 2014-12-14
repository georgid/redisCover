'''
Created on Dec 14, 2014

@author: joro
'''




def loadMSD2MXMMapping():
    URIMapFile = "/Users/joro/Downloads/mxm_779k_matches.txt"

    dictMapping = {}
    f = open (URIMapFile)
    for line in f:
        items = line.strip().split('<SEP>')
        if len(items) > 3:
            dictMapping[items[0]]= items[3]
    
    return dictMapping

def loadSongs():
    URI_SHSFile = "/Users/joro/Downloads/shs_dataset_test.txt"
    f = open (URI_SHSFile)
    
    resultDict = []
    while 1:
        line = f.readline()
        if not line:
            break
    #     print line
        tokens = line.split(',')
        
        if tokens[0].strip()[0].strip() == '%':
            key_ = tokens[-1].strip().lower()
#             print key_
            listsMSD_IDs = []
            while 1:
                
                line = f.readline()
                tokens = line.split('<SEP>')
                if tokens[0].strip()[0].strip() == 'T':
                    listsMSD_IDs.append(tokens[0])
                else:
                    break
            resultDict.append((key_,listsMSD_IDs))
    return resultDict

def queryBySongName(query):

    query = query.strip().lower()
    for cover_ in resultDict:
    #     print cover_
        if cover_[0] == query:
            return cover_[1]

if __name__ == '__main__':
    
    
    resultDict = loadSongs()
    dictMapping = loadMSD2MXMMapping()
    
    query = "Smells like teen Spirit"
    #query = 'killing me softly'
    query = 'billy jean'
    
    listMSDIDs = queryBySongName(query)
    print listMSDIDs
    
    
    
    