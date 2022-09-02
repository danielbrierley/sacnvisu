import sacn
import time

connected = True
recDMX = [0 for x in range(512)]

# provide an IP-Address to bind to if you are using Windows and want to use multicast
receiver = sacn.sACNreceiver()
receiver.start()  # start the receiving thread

# define a callback function
#@receiver.listen_on('universe', universe=1)  # listens on universe 1
def callback(packet):  # packet type: sacn.DataPacket
    global recDMX
    recDMX = packet.dmxData  # print the received DMX data

receiver.register_listener('universe', callback, universe=1)

# optional: if you want to use multicast use this function with the universe as parameter
receiver.join_multicast(1)


def init():
    global recDMX, receiver
    recDMX = [0 for x in range(512)]
    pass

    

def quit():
    global receiver
    receiver.stop()

def getDMX():
    global connected, recDMX

    receiver.register_listener('universe', callback, universe=1)
    if connected:
        dmx = recDMX
    else:
        connected = False
        dmx = [0 for x in range(512)]
    return dmx

if __name__ == '__main__':
    init()
    while True:
        print(getDMX())
