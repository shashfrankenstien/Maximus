import CHIP_IO.GPIO as gpio
import time

tx = 'LCD-CLK'
rx = 'LCD-VSYNC'
vcc = 'LCD-D22'

gpio.setup(vcc, gpio.OUT)

gpio.setup(tx, gpio.OUT)
gpio.setup(rx, gpio.IN)


 
 
def distance():
    # set Trigger to HIGH
    gpio.output(tx, True)
 
    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    gpio.output(tx, False)
 
    StartTime = time.time()
    StopTime = time.time()
 
    # save StartTime
    while gpio.input(rx) == 0:
        StartTime = time.time()
 
    # save time of arrival
    while gpio.input(rx) == 1:
        StopTime = time.time()
 
    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance = (TimeElapsed * 34300) / 2
 
    return distance
 
if __name__ == '__main__':
    try:
    	gpio.output(vcc, True)
        while True:
            dist = distance()
            print ("Measured Distance = %.1f cm" % dist)
            time.sleep(2)
 
        # Reset by pressing CTRL + C
    except KeyboardInterrupt:
        print("Measurement stopped by User")
        gpio.output(vcc, False)
        gpio.cleanup()