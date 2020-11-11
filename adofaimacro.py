from adofai import ADOFAI

def autoplay(levelpath):
    with open(levelpath, encoding='utf-8-sig') as f:
        ctx = json.loads(f.read())
    settings = ctx['settings']
    bpm = settings['bpm']
    offset = settings['offset']
    pathdata = ctx['pathData']
    
    action = ctx['actions']
    actiondata = {}

    for i in range(len(action)):
        act = actions[i]
        event = act['eventType']
        if event == 'SetSpeed':
            actiondata[i] = act['beatsPerMinute']
        elif event == 'Twirl':
            actiondata[i] = 'Twirl'
    
    macro = ADOFAI(bpm, pathdata, offset, actiondata)
    macro.startMacro()
