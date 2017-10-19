import CHIP_IO.GPIO as gpio
import time
import threading

UNIT_TIME = 0.01

class dotdict(dict):
    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__

class Wheel(object):
    '''Forward and reverse movement of a wheel'''
    def __init__(self, fwdPin, revPin, trim, gpioModule=gpio):
        self.trim = trim
        self.gpio = gpioModule
        self.fwdPin = dotdict({'pin':fwdPin, 'state':0})
        self.gpio.setup(self.fwdPin.pin, gpio.OUT)
        self.revPin = dotdict({'pin':revPin, 'state':0})
        self.gpio.setup(self.revPin.pin, gpio.OUT)
        self._stopFlag = True


    def _setOutput(self, pin, value):
        self.gpio.output(pin.pin, value)

    def _stopMoving(self):
        self._setOutput(self.fwdPin, False)
        self._setOutput(self.revPin, False)

    def _move(self, directionPin, speed, duration):
        self._stopFlag = False
        if speed and duration:
            directionPin.state = duration
            speed = speed*(1-self.trim)
            onTime = UNIT_TIME*speed
            offTime = UNIT_TIME*(1-speed)
            duration = duration/UNIT_TIME
            for i in xrange(int(duration)):
                if self._stopFlag:
                    self._stopMoving()
                    break
                self._setOutput(directionPin, True)
                time.sleep(onTime)
                self._setOutput(directionPin, False)
                time.sleep(offTime)
                directionPin.state=(duration-i)*UNIT_TIME
        directionPin.state = 0
        self._stopFlag = True

    def moveForward(self, speed, duration):
        self._setOutput(self.revPin, False)
        self._move(self.fwdPin, speed, duration)

    def moveReverse(self, speed, duration):
        self._setOutput(self.fwdPin, False)
        self._move(self.revPin, speed, duration)

    def stop(self):
        self._stopFlag = True

    def __repr__(self):
        return 'Wheel_at_{}_{}'.format(self.fwdPin, self.revPin)


class Car(object):
    '''Car that spawns wheel threads for motion'''
    def __init__(self, rightFwd, rightRev, leftFwd, leftRev, leftTrim=0, rightTrim=0):
        self.leftWheel = Wheel(leftFwd, leftRev, leftTrim)
        self.rightWheel = Wheel(rightFwd, rightRev, rightTrim)
        self._wheelThreads = []

    def _waitForThreads(self):
        for t in self._wheelThreads:
            t.join()
        self._wheelThreads = []
        return True

    def trimLeft(self, trim):
        self.leftWheel.trim = trim

    def trimRight(self, trim):
        self.rightWheel.trim = trim

    def stop(self):
        self.leftWheel.stop()
        self.rightWheel.stop()
        self._waitForThreads()

    def moveForward(self, speed=1, duration=1, asyncExecute=False):
        if self._wheelThreads: self.stop()
        for wheel in [self.leftWheel, self.rightWheel]:
            t = threading.Thread(
                    name=wheel.__repr__(),
                    target=wheel.moveForward,
                    args=(speed, duration,)
                )
            self._wheelThreads.append(t)
            t.start()
        if asyncExecute: return self._wheelThreads
        else: return self._waitForThreads()


    def moveReverse(self, speed=1, duration=1, asyncExecute=False):
        if self._wheelThreads: self.stop()
        for wheel in [self.leftWheel, self.rightWheel]:
            t = threading.Thread(
                    name=wheel.__repr__(),
                    target=wheel.moveReverse,
                    args=(speed, duration,)
                )
            self._wheelThreads.append(t)
        for t in self._wheelThreads:
            t.start()
        if asyncExecute: return self._wheelThreads
        else: return self._waitForThreads()

    def _wheelThreader(self, wheelA, wheelATarget, wheelASpeed, wheelB, wheelBTarget, wheelBSpeed, duration):
        if self._wheelThreads: self.stop()
        wheelAThread = threading.Thread(
            name=wheelA.__repr__(),
            target=wheelATarget,
            args=(wheelASpeed, duration,)
        )
        self._wheelThreads.append(wheelAThread)
        wheelBThread = threading.Thread(
            name=wheelB.__repr__(),
            target=wheelBTarget,
            args=(wheelBSpeed, duration,)
        )
        self._wheelThreads.append(wheelBThread)
        return True

    def turnLeft(self, speed=1, duration=1, curvatureRatio=1, asyncExecute=False):
        self._wheelThreader(
            wheelA=self.leftWheel,
            wheelATarget=self.leftWheel.moveForward,
            wheelASpeed=speed*(1-curvatureRatio),
            wheelB=self.rightWheel,
            wheelBTarget=self.rightWheel.moveForward,
            wheelBSpeed=speed,
            duration=duration
        )
        for t in self._wheelThreads:
            t.start()
        if asyncExecute: return self._wheelThreads
        else: return self._waitForThreads()

    def turnRight(self, speed=1, duration=1, curvatureRatio=1, asyncExecute=False):
        self._wheelThreader(
            wheelA=self.rightWheel,
            wheelATarget=self.rightWheel.moveForward,
            wheelASpeed=speed*(1-curvatureRatio),
            wheelB=self.leftWheel,
            wheelBTarget=self.leftWheel.moveForward,
            wheelBSpeed=speed,
            duration=duration
        )
        for t in self._wheelThreads:
            t.start()
        if asyncExecute: return self._wheelThreads
        else: return self._waitForThreads()

    def spinLeft(self, speed=1, duration=1, asyncExecute=False):
        self._wheelThreader(
            wheelA=self.rightWheel,
            wheelATarget=self.rightWheel.moveForward,
            wheelASpeed=speed,
            wheelB=self.leftWheel,
            wheelBTarget=self.leftWheel.moveReverse,
            wheelBSpeed=speed,
            duration=duration
        )
        for t in self._wheelThreads:
            t.start()
        if asyncExecute: return self._wheelThreads
        else: return self._waitForThreads()

    def spinRight(self, speed=1, duration=1, asyncExecute=False):
        self._wheelThreader(
            wheelA=self.rightWheel,
            wheelATarget=self.rightWheel.moveReverse,
            wheelASpeed=speed,
            wheelB=self.leftWheel,
            wheelBTarget=self.leftWheel.moveForward,
            wheelBSpeed=speed,
            duration=duration
        )
        for t in self._wheelThreads:
            t.start()
        if asyncExecute: return self._wheelThreads
        else: return self._waitForThreads()


class Eye(object):
    '''Ultrasonic distance sensor'''
    def __init__(self, txPin, rxPin):
        pass


if __name__ == '__main__':
    rightA = "CSID7"#38
    rightB = "CSID5"#36#
    leftA = "CSID6"#37#
    leftB = "CSID4"#35#

    car = Car(rightA, rightB, leftA, leftB, leftTrim=0.1)
    s = time.time()
    threads = car.moveForward(speed=1, duration=1, asyncExecute=True)
    time.sleep(0.5)
    print 'car.rightWheel.fwdPin.state=', car.rightWheel.fwdPin.state
    print 'car.leftWheel.fwdPin.state=', car.leftWheel.fwdPin.state
    for t in threads:
        t.join()
    car.spinLeft(speed=0.7, duration=2)
    car.turnRight(speed=1, duration=2, curvatureRatio=0.6)
    car.moveReverse(speed=1, duration=1)
