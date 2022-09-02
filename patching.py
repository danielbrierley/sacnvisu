
def patch(dmx):
    # Code to be executed between retrieving data from PhantomJester and sending through sACN
    # Ideal for repatching one fixture to an equivalent one that is useable in Capture Student Edition
    # e.g. Mac 250 Wash to ColorWash 1200 E AT

    dmx = convWash(dmx,103)
    dmx = convWash(dmx,200)

    return dmx

# Any additional functions for patching
def convWash(dmx, addr):
    Mac2Color = [16,17,9,10,11,7,15,1,2,3,4,5,13]
    addr -= 1
    wash = dmx[addr:addr+13]
    patchedWash = [0 for x in range(17)]
    for x in range(len(Mac2Color)):
        patchedWash[Mac2Color[x]-1] = wash[x]
    #Frost/Zoom
    patchedWash[14] = 255-patchedWash[14]
    #Dimmer
    patchedWash[16] = int(patchedWash[16]*0.5)
    #Colour Wheel
    patchedWash[6] = int(patchedWash[6]*.69)


    dmx[addr:addr+len(patchedWash)] = patchedWash
    return dmx


# Run main program
if __name__ == '__main__':
    import pygameDisplay
    pygameDisplay.main()
