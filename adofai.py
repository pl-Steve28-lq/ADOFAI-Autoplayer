from pynput.keyboard import Key, Controller
import json, time

class ADOFAI:
    def __init__(self, bpm = 100, pathdata = [180]*9, offset = 0, speeds = {}):
        self.kb = Controller()
        self.bpm = bpm
        self.pathdata = pathdata
        self.speedData = speeds
        self.offset = offset/1000
        self.length = len(self.pathdata)

    def start(self):
        print(f"[Start] BPM : {self.bpm}")
        self.press(Key.space)
        slp = self.offset + 4 * self.sec() + 0.1
        print(slp)
        time.sleep(slp)

    def changeBPM(self, newBPM):
        self.bpm = newBPM
    
    def startMacro(self):
        self.start()
        tile = 0
        while tile < self.length:
            delay = self.pathdata[tile]/180
            self.press()
            event = self.speedData.get(tile+2, None)
            if not event is None: self.changeBPM(event)
            tile += 1
            time.sleep(delay * self.sec())
    
    def press(self, key='k'):
        self.kb.press(key)
        self.kb.release(key)

    def sec(self): return 61/self.bpm
