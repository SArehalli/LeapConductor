import mido
import time
from threading import Thread

BPS2T = 1000000 # BPS to Ticks 
MAX_CHANGE = 10
INITIAL_TEMPO = 60

class midiPlayer():
    """ Player for midi files!"""
    
    def __init__(self):
        self.out = mido.open_output(mido.get_output_names()[-1])
        self.channels = [] 
        self.tempo = INITIAL_TEMPO 

    def play(self, track, TPB):
        """ plays a midi track to self.out """
        
        for message in track:
            if not isinstance(message, mido.MetaMessage):
                time.sleep((message.time * 60/self.tempo) / float(TPB))
                self.out.send(message)

    def playMultiTrack(self, filename):
        """ plays a multitrack midi in multiple threads """
        
        mid = mido.MidiFile(filename)
        for track in mid.tracks: 
            self.channels.append(Thread(target=self.play, args=(track, mid.ticks_per_beat)))
        
        for channel in self.channels:
            channel.start()

    def setTempo(self, tempo):
        """ adjusts the tempo of the file while playing """
        if abs(tempo - self.tempo) < MAX_CHANGE:
            self.tempo = tempo
        elif tempo - self.tempo > MAX_CHANGE:
            self.tempo = self.tempo + MAX_CHANGE/2
        elif self.tempo - tempo > MAX_CHANGE:
            self.tempo = self.tempo - MAX_CHANGE/2
        print(self.tempo)
        message = mido.MetaMessage("set_tempo", tempo=int(mido.bpm2tempo(self.tempo)))

if __name__ == "__main__":
    # TESTING
    player = midiPlayer()
    player.playMultiTrack("deb_prel.mid")
    for i in range(1,10):
        time.sleep(5)
        player.setTempo(float(i)/10)
