import sacn

def init(universe=1):
    global sender
    sender = sacn.sACNsender("169.254.140.2")
    sender.start()
    sender.activate_output(universe)
    sender[universe].multicast = True 
    #sender[universe].destination = "169.254.181.1"

def send(data):
    sender[1].dmx_data = tuple(data)

def quit():
    sender.stop()  

if  __name__ == '__main__':
    import pygameDisplay
    pygameDisplay.main()