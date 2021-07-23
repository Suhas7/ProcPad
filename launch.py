import launchpad_py as lpy
import requests as rq
import kasa
import asyncio
import time

LRSwitch = kasa.SmartDimmer("192.168.0.243")
asyncio.run(LRSwitch.update())
BRSwitch = kasa.SmartDimmer("192.168.0.205")
asyncio.run(BRSwitch.update())
Vornado = kasa.SmartPlug("192.168.0.192")
asyncio.run(Vornado.update())
Mirror = kasa.SmartPlug("192.168.0.170")
asyncio.run(Mirror.update())

launchpad = lpy.Launchpad()
launchpad.Open()
launchpad.Reset()

for i in range(0,3):
    launchpad.LedCtrlXY(i,1,0,3)

for i in range(0,4):
    launchpad.LedCtrlXY(i,3,3,0)

def device_toggle(device):
    asyncio.run(device.turn_on()) if device.is_off else asyncio.run(device.turn_off())
    asyncio.run(device.update())

APIMap = dict()
APIMap[(0,1)] = lambda: rq.get("http://blynk-cloud.com/wseIOxdXA6uBq7Z9LkCCQsonw2EU8QhZ/update/V1?value=0")
APIMap[(1,1)] = lambda: rq.get("http://blynk-cloud.com/wseIOxdXA6uBq7Z9LkCCQsonw2EU8QhZ/update/V1?value=1")
APIMap[(2,1)] = lambda: rq.get("http://blynk-cloud.com/wseIOxdXA6uBq7Z9LkCCQsonw2EU8QhZ/update/V1?value=2")

APIMap[(0,3)] = lambda: device_toggle(LRSwitch)
APIMap[(1,3)] = lambda: device_toggle(BRSwitch)
APIMap[(2,3)] = lambda: device_toggle(Vornado)
APIMap[(3,3)] = lambda: device_toggle(Mirror)

while True:
    while not launchpad.ButtonChanged():
        time.sleep(3)
    inp = launchpad.ButtonStateXY()
    while len(inp)>0:
        print(inp) 
        if inp[2]==True:
            try: APIMap[tuple(inp[:2])]()
            except: print("Couldn't find {}".format(tuple(inp[:2])))
        inp = launchpad.ButtonStateXY()
