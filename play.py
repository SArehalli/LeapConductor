import mido
import time
from threading import Thread

BPS2T = 1000000 # BPS to Ticks 

class midiPlayer():
    """ Player for midi files!"""
    
    def __init__(self):
        self.out = mido.open_output(mido.get_output_names()[-1])
        self.channels = [] 
        self.tempo = 0.5 # BPS

    def play(self, track, TPB):
        """ plays a midi track to self.out """
        
        for message in track:
            if not isinstance(message, mido.MetaMessage):
                time.sleep((message.time * self.tempo) / float(TPB))
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

        self.tempo = tempo
        message = mido.MetaMessage("set_tempo", tempo=int(tempo * BPS2T))

if __name__ == "__main__":
    # TESTING
    player = midiPlayer()
    player.playMultiTrack("deb_prel.mid")
    for i in range(1,10):
        time.sleep(5)
        player.setTempo(float(i)/10)
