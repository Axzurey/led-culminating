import parallel;
import time;
import json;
from tkinter import *;
import threading;
import customtkinter;

root = customtkinter.CTk();

root.title("Parallelysis");
root.geometry("800x500");

isPlaying = False;
selected_pattern = IntVar(value=0);

def togglePlay():
    global isPlaying
    isPlaying = not isPlaying

    play_button.configure(True, text="Pause" if isPlaying else "Play")

def set_pattern():
    if isPlaying:
        togglePlay()
    global pattern
    pattern = patterns[selected_pattern.get()]

header = customtkinter.CTkLabel(root, text="Parallelysis Control Panel", font=("arial", 30));
header.place(relx=.5, rely=.05, anchor="center");

play_button = customtkinter.CTkButton(root, text="Play", command=togglePlay);
play_button.place(relx=.9, rely=.9, anchor="center");

r0 = customtkinter.CTkRadioButton(
    master=root, text="Checkers", command=set_pattern, variable=selected_pattern, value=0
)

r1 = customtkinter.CTkRadioButton(
    master=root, text="Pulsing Squares", command=set_pattern, variable=selected_pattern, value=1
)

r2 = customtkinter.CTkRadioButton(
    master=root, text="Spiral", command=set_pattern, variable=selected_pattern, value=2
)

r3 = customtkinter.CTkRadioButton(
    master=root, text="Raindrops", command=set_pattern, variable=selected_pattern, value=3
)

r0.place(relx=.01, rely=.1)
r1.place(relx=.01, rely=0.15)
r2.place(relx=.01, rely=0.2)
r3.place(relx=.01, rely=0.25)

CONTROL_CONVERT = [
    0b100,
    0b011,
    0b000,
    0b101,
    0b010,
    0b111,
    0b110,
    0b001
];

DATA_CONVERT = [
    0b10,
    0b10000,
    0b10000000,
    0b100,
    0b100000,
    0b1000000,
    0b1000,
    0b1
];

port = parallel.Parallel();

def setX(x: int):
    if x < 0 or x > 7:
        raise Exception(f"X is out of bounds {x}")

    port.PPWCONTROL(CONTROL_CONVERT[x]);

def setY(y: int):
    if y == -1:
        port.setData(0);
        return;
    if y < 0 or y > 7:
        raise Exception(f"X is out of bounds {y}")

    port.setData(DATA_CONVERT[y]);

def decode(pattern: list[list[int]]):
    freq = 40;

    nOn = 0;

    for y in range(8):
        for x in range(8):
            if (pattern[y][x]):
                nOn += 1;

    for y in range(8):
        for x in range(8):
            if (pattern[y][x]):
                setX(x)
                setY(y)
                time.sleep(1 / freq / nOn)

def generateChecker():
    return json.load(open("./patterns/checker.json", 'r'))

def generatePulsingSquares():
    return json.load(open("./patterns/pulsing_squares.json", 'r'))

def generateSpiral():
    o = json.load(open("./patterns/spiral.json", 'r'))
    o2 = o[::-1]
    return *o, *o2

def generateRaindrops():
    out = []
    initX = [5, 3, 7, 2, 6, 0, 4, 1]

    for x0 in initX:

        for y in range(7):
            p = [
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [1, 1, 1, 1, 1, 1, 1, 1]
            ]

            p[y][x0] = 1;
            for _ in range(3):
                out.append(p)
    return out

patterns = [
    generateChecker(),
    generatePulsingSquares(),
    generateSpiral(),
    generateRaindrops()
]

pattern = generateChecker()

def p():
    while True:
        if not isPlaying:
            time.sleep(1 / 40)
            continue
        for patternLine in pattern:
            if not isPlaying: break
            decode(patternLine)
            setY(-1);
            time.sleep(1 / 2000);

thread = threading.Thread(target=p, daemon=True)
thread.start();

root.mainloop();