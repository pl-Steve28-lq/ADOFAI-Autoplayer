from pynput.keyboard import Key, Controller
import json, time

class ADOFAI:
    def __init__(self, bpm = 100, pathdata = 'R'*9, offset = 0, eventdata = {}):
        self.kb = Controller()
        self.bpm = bpm
        key = list("RWHQGqUoTEJpRAMCBYDVFZNxL")
        self.tileInfo = {key[i] : 15*i for i in range(len(key))}
        self.pathdata = self.analyze(pathdata)
        self.bpmdata = eventdata
        self.sec = 60/bpm
        self.offset = offset/1000
        self.length = len(self.pathdata)
        self.twirled = 0

    def start(self):
        print("[Start] BPM : " + str(self.bpm))
        self.kb.press(Key.space)
        self.kb.release(Key.space)
        time.sleep(self.offset + 3 * self.sec + 1.25)

    def changeBPM(self, newBPM):
        print("[Speed] BPM : " + str(self.bpm) + " => " + str(newBPM))
        print(self.sec)
        self.bpm = newBPM
        self.sec = 60/newBPM

    def startMacro(self):
        print(self.sec)
        self.start()
        tile = 0
        while tile < self.length:
            delay = -0.1 + (360*self.twirled + (-2 * self.twirled + 1) * self.pathdata[tile])/180
            self.press()
            print(self.pathdata[tile], delay)
            bpmcheck = self.bpmdata.get(tile, 0)
            if bpmcheck != 0:
                self.changeBPM(bpmcheck)
            tile += 1
            time.sleep(delay * self.sec)

    def analyze(self, pathdata):
        #180 90 0 270 270 180
        
        processed = []
        for i in range(len(pathdata)-1):
            nowtile  = self.tileInfo[pathdata[i]]
            nexttile = self.tileInfo[pathdata[i+1]]
            angle = (nowtile-nexttile)%360
            processed.append(angle if angle != 0 else nowtile)
        #TODO : Processing Midspin Tile
        return processed + [self.tileInfo[pathdata[-1]]]
    
    def press(self, key='k'):
        self.kb.press(key)
        self.kb.release(key)
