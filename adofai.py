from pynput.keyboard import Key, Controller
import json, time

class ADOFAI:
    def __init__(self, bpm = 100, pathdata = 'R'*9, offset = 0, bpmdata = {}):
        self.kb = Controller()
        self.bpm = bpm
        self.pathdata = self.analyze(pathdata)
        self.sec = 60/bpm
        self.offset = offset/1000
        self.tileInfo = {
            'U' : 90,
            'R' : 180,
            'D' : 270,
            'L' : 360,
        } # TODO : Tile Angle Data
        self.length = len(pathdata.replace('!', ''))

    def start(self):
        print("[Start] BPM : " + str(self.bpm))
        self.kb.press(Key.space)
        self.kb.release(Key.space)
        time.sleep(3 * self.sec)

    def changeBPM(self, newBPM):
        print("[Speed] BPM : " + str(self.bpm) + " => " + str(newBPM))
        self.bpm = newBPM

    def startMacro(self):
        self.start()
        tile = 1
        while tile < self.length:
            print(self.pathdata[tile])
            # TODO : Keyboard Press
            tile += 1
        return None

    def analyze(self, pathdata):
        #TODO : Processing Midspin Tile, and calculate angle of each tiles.
        return None
    

def autoplay(levelpath):
    with open(levelpath, encoding='utf-8-sig') as f:
        ctx = json.loads(f.read())
    settings = ctx['settings']
    bpm = settings['bpm']
    offset = settings['offset']
    pathdata = ctx['pathData']
    
    action = ctx['actions']
    actiondata = {i['floor'] : i.get('beatsPerMinute', 0) for i in action if i.get('beatsPerMinute', 0) != 0}

    macro = ADOFAI(bpm, pathdata, offset, actiondata)
    macro.startMacro()

autoplay('./backup.adofai')
