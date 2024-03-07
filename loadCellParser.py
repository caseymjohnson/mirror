from hx711 import HX711
import RPi.GPIO as GPIO
import json 
import time


'''
Casey Johnson 3.1.24

This script is used to parse load cell data and update mass objects.
The HX711 module was used.
a JSON data structure is used to track mass objects
'''


outputFile = 'parsedLoads.txt'
massObjectFile = 'massObjects.json'



# for mirror command REMOVE
# command should be given, then user remove from shelf within 10s
def removeMassObject(massObjectFile, timeout=10):

    # read the baseline masses
    d0, d1 = takeReading()
    time.sleep(timeout)

    # read the new masses
    newd0, newd1 = takeReading()
    delta0, delta1 = newd0 - d0, newd1 - d1

    # given the changes in both load cells, we can calculate mass and position on shelf
    mass = delta0 + delta1
    location = delta0 / mass # using nomenclature of left->right proportion

    # load the mass objects
    with open(massObjectFile, 'r') as fp:
        data = json.load(fp)

    # find the closest match to mass and position
    objects = list(data.keys)
    # sum the normalized difference in mass and difference in location
    closeness = [[(abs(data[obj]['mass'] - mass) / mass) + abs(data[obj]['location'] - location), obj] for obj in objects]
    closest = min(closeness)[1]
    print(f'removing {closest}')
    print(f'object matching data: {closeness}')

    # remove matched data object
    data.remove(closest)

    # save the updated mass objects
    with open(massObjectFile, 'w') as fp:
        json.dump(data, fp)
    
    return True

# attach reminder to most recent mass object added
def attachReminder(massObjectFile):

    # load the mass objects
    with open(massObjectFile, 'r') as fp:
        data = json.load(fp)

    mostRecent = max(list(data.keys))
    data[mostRecent]['reminder'] = True

    

# for mirror command TAKING
# command should be given, user should pick up from shelf within 10s, then put down within 30s
def massObjectEvent(massObjectFile, upTimeout=10, downTimeout=30):
    # read the baseline masses
    d0, d1 = takeReading()
    time.sleep(upTimeout)

    # read the new masses
    newd0, newd1 = takeReading()
    delta0, delta1 = newd0 - d0, newd1 - d1

    # given the changes in both load cells, we can calculate mass and position on shelf
    mass = delta0 + delta1
    location = delta0 / mass # using nomenclature of left->right proportion

    # load the mass objects
    with open(massObjectFile, 'r') as fp:
        data = json.load(fp)

    # find the closest match to mass and position
    objects = list(data.keys)

    # sum the normalized difference in mass and difference in location
    closeness = [[(abs(data[obj]['mass'] - mass) / mass) + abs(data[obj]['location'] - location), obj] for obj in objects]
    closest = min(closeness)[1]
    print(f'taking {closest}')
    print(f'object matching data: {closeness}')

    objects[closest]['timestamp'] == time.time()

    # wait for user to put down
    time.sleep(downTimeout)

    # read the new mass data
    d0, d1 = newd0, newd1
    newd0, newd1 = takeReading()
    delta0, delta1 = newd0 - d0, newd1 - d1

    print(f'updating mass object with index {closest}')
    print(f'location {location} mass {mass}')
    
    # add the new mass object plus its timestamp
    data[closest] = {'location': location, 'mass': mass, 'timestamp': time.time()}

    # save the updated mass objects
    with open(massObjectFile, 'w') as fp:
        json.dump(data, fp)

    return True


# for mirror command ADD
# command should be given, then user should place on shelf within 10s
def addMassObject(massObjectFile, timeout=10):

    # read the baseline masses
    d0, d1 = takeReading()
    time.sleep(timeout)

    # read the new masses
    newd0, newd1 = takeReading()
    delta0, delta1 = newd0 - d0, newd1 - d1

    # given the changes in both load cells, we can calculate mass and position on shelf
    mass = delta0 + delta1
    location = delta0 / mass # using nomenclature of left->right proportion

    # load the mass objects
    with open(massObjectFile, 'r') as fp:
        data = json.load(fp)

    print(f'adding mass object with index {len(data.keys + 1)}')
    print(f'location {location} mass {mass}')
    
    # add the new mass object plus its timestamp
    data[len(data.keys)+1] = {'location': location, 'mass': mass, 'timestamp': time.time()}

    # save the updated mass objects
    with open(massObjectFile, 'w') as fp:
        json.dump(data, fp)

    return True

def resetMassObjects(massObjectFile):
    # overwrite with empty dict
    with open(massObjectFile, 'w') as fp:
        json.dump({}, fp)

    return True


def takeReading():
    # initialize load 0
    cell0 = HX711(
        dout_pin=5,
        pd_sck_pin=6,
        channel='A',
        gain=64
    )
    # initialize load cell 1
    cell1 = HX711(
        dout_pin=23,
        pd_sck_pin=24,
        channel='A',
        gain=64
    )
    # reset cells prior to reading
    cell0.reset()   
    cell1.reset()   

    # read each channel
    d0 = cell0.get_raw_data(num_measures=5)
    d1 = cell1.get_raw_data(num_measures=5)
    
    return d0, d1
