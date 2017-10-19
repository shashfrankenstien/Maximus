from CarModule import Car
import curses


rightA = "CSID7"#38
rightB = "CSID5"#36#
leftA = "CSID6"#37#
leftB = "CSID4"#35#

car = Car(rightA, rightB, leftA, leftB, leftTrim=0)


stdscr = curses.initscr()
curses.noecho()
curses.cbreak()
stdscr.keypad(True)

granularity = 0.08
def main(stdscr):
	stdscr.addstr(10, 10, "Use W, S, A, D to control the car! ('Q' to quit)", curses.A_REVERSE)
	stdscr.refresh()
	while True:
		c = stdscr.getch()
		if c == ord('w') or c == ord('W'):
			car.moveForward(speed=1, duration=granularity)
		elif c == ord('s') or c == ord('S'):
			car.moveReverse(speed=1, duration=granularity)
		elif c == ord('a') or c == ord('A'):
			car.spinLeft(speed=1, duration=granularity)
		elif c == ord('d') or c == ord('D'):
			car.spinRight(speed=1, duration=granularity)
		elif c == ord('q') or c == ord('Q'):
			break

curses.wrapper(main)
