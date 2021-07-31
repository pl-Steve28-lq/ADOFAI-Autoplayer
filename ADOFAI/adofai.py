from utils import Util
import json

class ADOFAI:
  class File(Util.Singleton):
    def __init__(self):
      self.file = None
      self.level = None
      self.isPath = True

    def open(self, path):
      self.file = open(path, encoding='utf-8-sig')
      self.level = json.loads(self.file.read())
      self.isPath = 'pathData' in self.level
      self.event = {}
      for i in filter(lambda x: x['eventType'] in ['SetSpeed', 'Twirl'], self.level['actions']):
        floor, etype = i['floor'], i['eventType']
        if self.event.setdefault(floor):
          self.event[floor] = self.event[floor][0], ADOFAI.Event.getEvent(i)
        else:
          self.event[floor] = (ADOFAI.Event.getEvent(i),)

      return self._analyze(self.level, self.event)

    def _analyze(self, level, event):
      if self.isPath: return self.parseTile(level, event)
      else: Util.TODO()

    def parseTile(self, level, event):
      res = []
      angle = {"RWHQGqUoTEJpRAMCBYDVFZNxL"[i] : 15*i for i in range(25)}
      L = len(path := level['pathData'])
      i = 0
      while i < L:
        p = path[i]
        isMid = False
        if p == '!':
          i += 1
          isMid = True
          p = path[i]
        res.append(
          ADOFAI.Tile.get(angle[p], event[i+1], isMid)
        )
        i += 1
      return res
        

  class Tile(Util.Factory(
    'Tile', ('angle', 'event', ('isMidspin', False))
  )):
    def processAngle(self, other):
      Util.TODO()

  class Event:
    class Twirl(Util.Factory('Twirl')): pass
    class BPMSpeed(Util.Factory('BPMSpeed', ('value',))): pass
    class MultiplySpeed(Util.Factory('MultiplySpeed', ('value',))): pass

    def getEvent(event):
      evt = event['eventType']
      if evt == 'Twirl': return ADOFAI.Event.Twirl.get()
      if evt == 'SetSpeed':
        if event['speedType'] == 'Bpm':
          return ADOFAI.Event.BPMSpeed.get(event['beatsPerMinute'])
        else:
          return ADOFAI.Event.MultiplySpeed.get(event['bpmMultiplier'])

  File = File()

if __name__ == '__main__': [*map(print,ADOFAI.File.open('../test.adofai'))]
