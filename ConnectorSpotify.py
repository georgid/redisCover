'''
Created on Jan 15, 2015

@author: joro

spotify playing logic adapted from: 
https://github.com/mopidy/pyspotify/tree/v2.x/develop/examples

'''
import spotify
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
#         self.session.on(spotify.SessionEvent.END_OF_TRACK, self.on_end_of_track)
        
        # LOGIN
        self.session.login('1184035535', '7Navuhodonosor', remember_me=True)
    
    def on_connection_state_updated(self, session):
        if self.session.connection.state is spotify.ConnectionState.LOGGED_IN:
            self.logged_in.set()
    
    def on_end_of_track(self):
        self.session.player.play(False)
#         self.end_of_track.set()
        
    def playinSpotify(self, listCoverTracks):
        
        for cover in listCoverTracks:
            

            trackURI="spotify:track:" + cover[0]
            track = self.session.get_track(trackURI).load()
            try:
                self.session.player.load(track)
            except:
                continue
            beginTs = cover[1][1]
            beginTs = max(beginTs-1,0) 
            duration = cover[1][2]
            #  make sure max duration is not exceeded
            endTsTrack = track.duration
            endTs = min (endTsTrack - 1, beginTs + duration) 
            playDuration = endTs - beginTs
            artist = cover[1][3]
            print  artist + '\n'
            self.session.player.seek(int(beginTs* 1000))
            self.session.player.play()
            
            ##### sleep until playing for duration of thumbnail
            time.sleep(playDuration) # in seconds
            self.session.player.unload()
            time.sleep(1) # break 1 second
