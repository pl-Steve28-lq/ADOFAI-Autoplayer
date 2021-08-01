from adofai import ADOFAI
from pynput.keyboard import Controller
from time import sleep

class Autoplay:
    Keyboard = Controller()

    def press(self, key='k'):
        #print(key)
        Autoplay.Keyboard.press(key)
        Autoplay.Keyboard.release(key)

    def __init__(self, path):
        self.level = ADOFAI.File.open(path)
        self.bpm = self.level.bpm
        self.twirled = 0

    @property
    def sec(self): return 60/self.bpm

    def start(self, offset=0):
        self.press('p')
        prev = ADOFAI.Tile(180, (), False)
        sleep(self.level.offset/1000+4*self.sec+offset)
        for t in self.level.tile:
            self.applyEvents(prev.event)
            sleep(self.sec*self.processAngle(prev, t)/180-0.05)
            self.press('k')
            prev = t

    def processAngle(self, t1, t2):
        if t2.isMidspin:
            return (t2.angle-t1.angle+360)%360
        return (180-t1.angle+t2.angle+360)%360
    
    def applyEvents(self, event):
        app = self.applyEvent
        for i in event: app(i)
    
    def applyEvent(self, event):
        t = type(event)
        if t == ADOFAI.Event.Twirl: self.twirled ^= 1
        elif t == ADOFAI.Event.BPMSpeed: self.bpm = event.value
        else: self.bpm *= event.value

def test(v):
    sleep(3)
    Autoplay('../얼불춤/Halv_-_Schlachtfeld/level.adofai').start(v)
    #Autoplay('../test.adofai').start(v)
