Overview
```
this repository holds code for the DLAB smart mirror project
this code is hosted on a RPI
this RPI interfaces with electret microphone and HX711 load cells (x2)
this RPI uses pocketsphinx + custom phonetics dict to recognize commands
additional documentation may be found in the .py files

essentially:
  a script handles the parsing of audio commands into text, then writes that to file
  a script handles the parsing of load cell data into grams, then writes that to file

  an overarching script reads these data files and reacts accordingly:

  a script handles the creation + tracking + timestamping of mass objects
  a script handles the sending of email/push notifications


```

Raspberry Pi Info
```
os: raspbian
device name: mirrorpi
username: mirror
password: dlab
```

Connecting
```
ssh: enabled
ip: not static (to find, use monitor/keyboard to join wifi then run ifconfig)
ssh mirror@ip
```
