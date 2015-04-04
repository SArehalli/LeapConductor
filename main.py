import pyglet 
import mido
import Leap, sys, thread, time
from Leap import CircleGesture
from play import midiPlayer

FILENAME = 'deb_prel.mid'

class ConductListener(Leap.Listener):
    
    def on_connect(self, controller):
        print "-- Connected"

        self.init_velocity = Leap.Vector(0,0,0)
        self.init_time = 0
        self.stopped = [True, True, True];
        self.audio = pyglet.media.load('beep.wav', streaming=False) 
        controller.enable_gesture(Leap.Gesture.TYPE_CIRCLE)
        self.player = midiPlayer()
        self.player.playMultiTrack(FILENAME)

    def on_disconnect(self, controller):
        print "Disconnected"

    def on_frame(self, controller):
        # Get the current frame
        frame = controller.frame()
        hand = frame.hands[0]
        curr_time = frame.timestamp
        
        # get current velocity
        curr_velocity = hand.palm_velocity.to_tuple()
        curr_velocity = tuple(map(lambda x : 0 if abs(x) < 45 else x, 
                                  curr_velocity)) 
        # get a list of the velocities that have changed direction 
        result = [(curr_velocity[i] * self.init_velocity[i] <= 0)
                   for i in range(3)]
        
        
        # Check for change in the x dimension
        toTick = False
        for i in range(1):
            if result[i] == True and not self.stopped[i]:
                toTick = True
                self.stopped[i] = True

            elif result[i] == False and self.stopped[i]:
                self.stopped[i] = False
       
        if toTick:
            dTime = float(curr_time - self.init_time) / 1000000 if \
                                                            self.init_time != 0\
                                                                else 1 
            BPM =  60 * (1/dTime)
            self.player.setTempo(BPM)
            self.init_time = curr_time

        # Update init velocity
        self.init_velocity = curr_velocity

if __name__ == "__main__":
    # Create listener and controller
    listener = ConductListener()
    controller = Leap.Controller()

    controller.add_listener(listener)

    try:
        sys.stdin.readline()
    except KeyboardInterrupt:
        pass
    finally:
            controller.remove_listener(listener)

