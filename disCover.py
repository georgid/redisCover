'''
Created on Dec 14, 2014

@author: joro
'''

import spotify

from getCoverTrackIDs import getListCoverTracks
import threading
import time


class ConnectorSpotify(object):
    
    
    def connectToSpotify(self):
        self.session = spotify.Session()
    
        loop = spotify.EventLoop(self.session)
    
        loop.start()
    
        audio = spotify.PortAudioSink(self.session)
        
        self.logged_in = threading.Event()
        self.end_of_track = threading.Event()
        
        self.session.on(spotify.SessionEvent.CONNECTION_STATE_UPDATED, self.on_connection_state_updated)
        self.session.on(spotify.SessionEvent.END_OF_TRACK, self.on_end_of_track)
        
        # LOGIN
        self.session.login('1184035535', '7Navuhodonosor', remember_me=True)
    
    def on_connection_state_updated(self, session):
        if self.session.connection.state is spotify.ConnectionState.LOGGED_IN:
            self.logged_in.set()
    
    def on_end_of_track(self):
        self.end_of_track.set()
        
    def playinSpotify(self, listCoverTracks):
        
        for cover in listCoverTracks:
            
            
            trackURI="spotify:track:" + cover[0]
            track = self.session.get_track(trackURI).load()
            self.session.player.load(track)
            
            beginTs = cover[1][1]
            duration = cover[1][2]
            self.session.player.seek(int(beginTs * 1000))
            self.session.player.play()
            
            time.sleep(duration + 1)


    
    
def doit():
    
    spotifier = ConnectorSpotify()
    spotifier.connectToSpotify()
    
    coverTracks = getListCoverTracks()
    
    spotifier.playinSpotify(coverTracks)




   


if __name__ == '__main__':
    doit()