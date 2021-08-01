from utils import Util
import json

class ADOFAI:
    class File(Util.Singleton):
        def open(self, path):
            level = json.loads(open(path, encoding='utf-8-sig').read())
            event = {}
            for i in level['actions']:
                floor, etype = i['floor'], i['eventType']
                if etype not in {'SetSpeed', 'Twirl'}: continue
                event.setdefault(floor, []).append(ADOFAI.Event.getEvent(i))
            setting = level['settings']
            return ADOFAI.Level(
                setting['bpm'], setting['offset'],
                self._analyze(level, {
                    i : tuple(event[i]) for i in event
                })
            )

        def _analyze(self, level, event):
            if 'pathData' in level: return self.parseTile(level, event)
            else: Util.TODO()

        def parseTile(self, level, event):
            res = []
            angle = {"RWHQGqUoTEJpRAMCBYDVFZNxL"[i] : 15*i for i in range(25)}
            L = len(path := level['pathData'])
            i = 0
            while i < L:
                isMid = path[i] == '!'
                i += isMid
                p = path[i]
                res.append(ADOFAI.Tile.get(angle[p], event.get(i+1, ()), isMid))
                i += 1
            return tuple(res)
    
    class Tile(Util.Factory(
        'angle', 'event', ('isMidspin', False)
    )): pass

    class Event:
        class Twirl(Util.Factory()): pass
        class BPMSpeed(Util.Factory('value')): pass
        class MultiplySpeed(Util.Factory('value')): pass

        def getEvent(event):
            evt = event['eventType']
            if evt == 'Twirl': return ADOFAI.Event.Twirl.get()
            if evt == 'SetSpeed':
                ev, val = ADOFAI.Event, 0
                if event['speedType'] == 'Bpm': ev, val = ev.BPMSpeed, event['beatsPerMinute']
                else: ev, val = ev.MultiplySpeed, event['bpmMultiplier']
                return ev.get(val)

    class Level(Util.Factory(
        'bpm', 'offset', 'tile'
    )): pass

    File = File.init()

if __name__ == '__main__': [*map(print,ADOFAI.File.open('../test.adofai').tile)]
