from utils import Util
import json

class ADOFAI:
  class File(Util.Singleton):
    def open(self, path):
      file = open(path, encoding='utf-8-sig')
      level = json.loads(file.read())
      event = {}
      for i in level['actions']:
        floor, etype = i['floor'], i['eventType']
        if etype not in {'SetSpeed', 'Twirl'}: continue
        event[floor] = \
          (event[floor][0], ADOFAI.Event.getEvent(i)) \
          if event.setdefault(floor) \
          else (ADOFAI.Event.getEvent(i),)
      return self._analyze(level, event)

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
        res.append(ADOFAI.Tile.get(angle[p], event[i+1], isMid))
        i += 1
      return res
        

  class Tile(Util.Factory(
    'angle', 'event', ('isMidspin', False)
  )):
    def processAngle(self, other):
      Util.TODO()

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

  File = File()

if __name__ == '__main__': [*map(print,ADOFAI.File.open('../test.adofai'))]
