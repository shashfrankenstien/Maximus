import RPi.GPIO as gpio
import time
gpio.setmode(gpio.BOARD)

UNIT_TIME = 0.01

rightA = 38
rightB = 36

leftA = 37
leftB = 35

vcc = 40

gpio.setup(vcc, gpio.OUT)
gpio.setup(rightA, gpio.OUT)
gpio.setup(rightB, gpio.OUT)
gpio.setup(leftA, gpio.OUT)
gpio.setup(leftB, gpio.OUT)


def stop():
    gpio.output(rightA, False)
    gpio.output(rightB, False)
    gpio.output(leftA, False)
    gpio.output(leftB, False)




def _forward():
    gpio.output(rightA, True)    
    gpio.output(rightB, False)
    gpio.output(leftA, True)    
    gpio.output(leftB, False)

def _reverse():
    gpio.output(rightB, True)    
    gpio.output(rightA, False)
    gpio.output(leftB, True)    
    gpio.output(leftA, False)

def move(speed=1, duration=1, direction='f'):
    if direction=='f': _move = _forward
    elif direction=='r': _move = _reverse
    else: raise ValueError('Could not recognize direction value.')
    onTime = UNIT_TIME*speed
    offTime = UNIT_TIME*(1-speed)
    _duration = duration/UNIT_TIME
    print ("running {} times".format(_duration), ", on time = {}, off time = {}".format(onTime, offTime), 
        ", speed: {}, duration: {}, unit_time: {}".format(speed, duration, UNIT_TIME))
    for i in xrange(int(_duration)):
        _move()
        time.sleep(onTime)
        stop()
        time.sleep(offTime)
    stop()




def turn(speed=1, duration=1, direction='r', curvatureRatio=1):
    stop()
    left = {'A': leftA, 'B': leftB}
    right = {'A': rightA, 'B': rightB}
    if direction=='r':
        outer = left
        inner = right
    elif direction=='l':
        outer = right
        inner = left
    onTime = UNIT_TIME*speed
    offTime = UNIT_TIME*(1-speed)
    _duration = duration/UNIT_TIME
    print ("running {} times".format(_duration), ", on time = {}, off time = {}".format(onTime, offTime), 
        ", speed: {}, duration: {}, unit_time: {}".format(speed, duration, UNIT_TIME))
    for i in xrange(int(_duration)):
        gpio.output(outer['A'], True)
        gpio.output(outer['B'], False)
        time.sleep(onTime)
        stop()
        time.sleep(offTime)
    stop()




def cli():
    while True:
        try:
            stop()
            dirTime = raw_input("Direction Speed Time in seconds. (Ex: f 0.3 5 for forward for 5 seconds at 30% speed)! q to quit:").split(' ')
            if dirTime[0] == 'q': 
                raise Exception('Bye!!')
            direction = dirTime[0]
            speed = float(dirTime[1])
            duration = float(dirTime[2])
            move(speed, duration, direction)

        except Exception as e:
            print e
            stop()
            break


def uTurn():
    move(1, 1, 'f')
    turn(0.5, 1.1, 'r')
    move(0.5, 2, 'f')
    turn(0.5, 1.3, 'l')
    move(1, 1, 'f')


if __name__ == '__main__':
    print "Executing uTurn"
    uTurn()
    cli()
    gpio.cleanup()
