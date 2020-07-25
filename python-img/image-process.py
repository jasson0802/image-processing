import time
import cv2
import mss
import numpy
from osc4py3.as_eventloop import *
from osc4py3 import oscmethod as osm
from osc4py3.as_eventloop import *
from osc4py3 import oscbuildparse

def send_happy(image, synthName):
    newImage = cv2.resize(image,(300,300))
    hsv = cv2.cvtColor(newImage, cv2.COLOR_BGR2HSV)

    meanBrightness = hsv[...,2].mean()

    musicBrightness = meanBrightness * 10

    msg = oscbuildparse.OSCMessage(synthName, ",sf", ["float", meanBrightness])
    osc_send(msg, "supercollider")
    osc_process()
    #sleep(2)
    
    return meanBrightness


def send_sad(image, synthName):
    newImage = cv2.resize(image,(300,300))
    hsv = cv2.cvtColor(newImage, cv2.COLOR_BGR2HSV)

    meanBrightness = hsv[...,2].mean()

    musicBrightness = meanBrightness * 10

    msg = oscbuildparse.OSCMessage(synthName, ",sf", ["float", meanBrightness])
    osc_send(msg, "supercollider")
    osc_process()
    #sleep(2)
    
    return meanBrightness

with mss.mss() as sct:
    #Start the system.
    osc_startup()

    # Setear ip de supercollider y un tag para identificarlo
    osc_udp_client("127.0.0.1", 57120, "supercollider")
    
    screen_width = 1536
    screen_height = 864

    top_margin = int(screen_height*17.7/100)
    bottom_margin = int(screen_height*22.9/100)
    square_height = int(screen_height*29.8/100)
    square_width = int(screen_width/3)
    
    # Part of the screen to capture
    cuadro1 = {"top": 250, "left": 20, "width": 820, "height": 600}
    cuadro2 = {"top": 250, "left": 950, "width": 860, "height": 600}
    #cuadro2 = {"top": top_margin, "left": square_width, "width": square_width, "height": square_height}
    #cuadro3 = {"top": top_margin, "left": square_width*2, "width": square_width, "height": square_height}
    #cuadro4 = {"top": top_margin+square_height, "left": 0, "width": square_width, "height": square_height}
    #cuadro5 = {"top": top_margin+square_height, "left": square_width, "width": square_width, "height": square_height}
    #cuadro6 = {"top": top_margin+square_height, "left": square_width*2, "width": square_width, "height": square_height}

    while "Screen capturing":
        last_time = time.time()

        # Get raw pixels from the screen, save it to a Numpy array
        img1 = numpy.array(sct.grab(cuadro1))
        img2 = numpy.array(sct.grab(cuadro2))
        #img3 = numpy.array(sct.grab(cuadro3))
        #img4 = numpy.array(sct.grab(cuadro4))
        #img5 = numpy.array(sct.grab(cuadro5))
        #img6 = numpy.array(sct.grab(cuadro6))

        # Display the picture in grayscale
        #cv2.imshow('OpenCV/Numpy grayscale',
        #           cv2.cvtColor(img2, cv2.COLOR_BGRA2GRAY))

        print("Brightness: ", send_happy(img1, "/happyMsg"))
        print("Brightness: ", send_sad(img2, "/sadMsg"))

        #cv2.imshow('Zoom music', get_brightness(img1))

        #print("fps: {}", img1)

        # Press "q" to quit
        if cv2.waitKey(25) & 0xFF == ord("q"):
            cv2.destroyAllWindows()
            break

    # Properly close the system.
    osc_terminate()

