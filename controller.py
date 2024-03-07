import speechParser
import loadCellParser
import os
import json
import time
import reminders

# run speechParser
os.system('python3 speechParser.py')

# start with baseline commands
with open(speechParser.outputFile, 'r') as f:
    lines = f.readlines()
    n_lines, last_line = len(lines), lines[-1]

# continuously search for new commands and respond
# only respond if MIRROR then command then CONFIRM
while True:

    # check for reminder events
    with open(loadCellParser.massObjectFile, 'r') as fp:
        data = json.load(fp)
        for obj in list(data.keys):
            if 'reminder' in data[obj]:
                if time.time() - data['obj']['timestamp'] > 24 * 60 * 1000:
                    reminders.sendReminder()
                    data['obj']['timestamp'] = time.time()

    with open(speechParser.outputFile, 'r') as f:
        lines = f.readlines()
        # if we have valid command sandwich, respond then reset
        if 'MIRROR' in lines and 'CONFIRM' in lines and len(lines) == 3:
            cmd = lines.split('MIRROR')[1].split('CONFIRM')[-1]
            

            if cmd == 'ADD':
                loadCellParser.addMassObject()
            elif cmd == 'REMOVE':
                loadCellParser.removeMassObject()
            elif cmd == 'RESET':
                loadCellParser.resetMassObjects()
            elif cmd == 'TAKING':
                loadCellParser.massObjectEvent()
            elif cmd == 'SCHEDULE':
                loadCellParser.attachReminder()

            # reset command list to empty
            with open(speechParser.outputFile, 'w') as f:
                pass

        # if we have invalid command sandwich, reset
        elif 'MIRROR' in lines and 'CONFIRM' in lines:
            # reset command list to empty
            with open(speechParser.outputFile, 'w') as f:
                pass
        
        # if we have no command sandwich, pass
        else:
            pass

            
        

    
    
