import curses
from curses import wrapper  # restore terminal to previous state
import time
import random


def startScreen(stdscr):
    stdscr.clear()
    stdscr.addstr("Welcome to Speed Typing Test!")
    stdscr.addstr("\nPress any key to begin.")
    stdscr.refresh()
    stdscr.getkey()


def displayText(stdscr, target, current, wpm=0):
    stdscr.addstr(target)  # or else it will print in another line
    stdscr.addstr(1, 0, f"WPM: {wpm}")

    for i, char in enumerate(current):
        correctChar = target[i]
        color = curses.color_pair(1)
        if char != correctChar:
            color = curses.color_pair(2)

        stdscr.addstr(0, i, char, color)  # 0 row i column


def loadText():
    with open("text.txt", "r") as f:
        lines = f.readlines()
        return random.choice(lines).strip()  # strip --> remove \n


def wpm(stdscr):
    targetText = loadText()
    currentText = []
    wpm = 0
    startTime = time.time()
    stdscr.nodelay(True)

    while True:
        timeElapsed = max(time.time() - startTime, 1)
        # wpm = 5* char pm(assume 1word to 5 char)
        wpm = round((len(currentText) / (timeElapsed/60)) / 5)

        stdscr.clear()  # all lines will print again and again if not used.
        displayText(stdscr, targetText, currentText, wpm)
        stdscr.refresh()

        if "".join(currentText) == targetText:
            stdscr.nodelay(False)
            break

        try:
            key = stdscr.getkey()
        except:
            continue

        if ord(key) == 27:  # backspace ascii
            break
        if key in ("KEY_BACKSPACE", '\b', "\x7f"):
            if len(currentText) > 0:
                currentText.pop()
        elif len(currentText) < len(targetText):
            currentText.append(key)

        stdscr.refresh()


def main(stdscr):  # standard output screen

    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLACK)

    startScreen(stdscr)
    while True:
        wpm(stdscr)
        stdscr.addstr(
            2, 0, "You completed the test! Press any key to continue...")
        key = stdscr.getkey()

        if ord(key) == 27:
            break


wrapper(main)
