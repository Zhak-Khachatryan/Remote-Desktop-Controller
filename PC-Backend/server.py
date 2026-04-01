import ctypes
import threading
from ctypes import wintypes

import pyautogui
from flask import Flask, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

width = pyautogui.size()[0]

user32 = ctypes.WinDLL("user32", use_last_error=True)

INPUT_KEYBOARD = 1

KEYEVENTF_KEYUP = 0x0002
KEYEVENTF_SCANCODE = 0x0008

MAPVK_VK_TO_VSC = 0

ULONG_PTR = wintypes.WPARAM


class KEYBDINPUT(ctypes.Structure):
    _fields_ = [
        ("wVk", wintypes.WORD),
        ("wScan", wintypes.WORD),
        ("dwFlags", wintypes.DWORD),
        ("time", wintypes.DWORD),
        ("dwExtraInfo", ULONG_PTR),
    ]


class MOUSEINPUT(ctypes.Structure):
    _fields_ = [
        ("dx", wintypes.LONG),
        ("dy", wintypes.LONG),
        ("mouseData", wintypes.DWORD),
        ("dwFlags", wintypes.DWORD),
        ("time", wintypes.DWORD),
        ("dwExtraInfo", ULONG_PTR),
    ]


class _INPUTUNION(ctypes.Union):
    _fields_ = [
        ("ki", KEYBDINPUT),
        ("mi", MOUSEINPUT),
    ]


class INPUT(ctypes.Structure):
    _anonymous_ = ("u",)
    _fields_ = [
        ("type", wintypes.DWORD),
        ("u", _INPUTUNION),
    ]


user32.SendInput.argtypes = (wintypes.UINT, ctypes.POINTER(INPUT), ctypes.c_int)
user32.SendInput.restype = wintypes.UINT
user32.MapVirtualKeyW.argtypes = (wintypes.UINT, wintypes.UINT)
user32.MapVirtualKeyW.restype = wintypes.UINT


VK_MAP = {
    "w": 0x57,
    "a": 0x41,
    "s": 0x53,
    "d": 0x44,
}


held_keys = set()
lock = threading.Lock()


def send_key(vk_code: int, key_up: bool = False):
    scan = user32.MapVirtualKeyW(vk_code, MAPVK_VK_TO_VSC)
    flags = KEYEVENTF_SCANCODE | (KEYEVENTF_KEYUP if key_up else 0)

    inp = INPUT(
        type=INPUT_KEYBOARD,
        ki=KEYBDINPUT(
            wVk=0,
            wScan=scan,
            dwFlags=flags,
            time=0,
            dwExtraInfo=0,
        ),
    )

    user32.SendInput(1, ctypes.byref(inp), ctypes.sizeof(inp))


def press_key(key: str):
    vk = VK_MAP.get(key.lower())
    if vk is None:
        return
    send_key(vk, key_up=False)


def release_key(key: str):
    vk = VK_MAP.get(key.lower())
    if vk is None:
        return
    send_key(vk, key_up=True)


def key_is_held(key: str) -> bool:
    with lock:
        return key in held_keys


def mark_hold(key: str):
    with lock:
        held_keys.add(key)

def unmark_hold(key: str):
    with lock:
        held_keys.discard(key)

width, height = pyautogui.size()

def verify_method(method):
    if request.method == method:
        return "ok", 200

@app.route("/key", methods=["POST"])
def key():
    data = request.json or {}
    key = data.get("key")

    if key:
        press_key(key)
        release_key(key)

    return {"status": "ok"}


@app.route("/key-hold", methods=["POST"])
def key_hold():
    data = request.json or {}
    key = data.get("key")

    if not key:
        return {"status": "missing key"}, 400

    # Avoid duplicate downs
    if not key_is_held(key):
        mark_hold(key)
        if key not in ["lb", "rb"]:
            press_key(key)
        else:
            pyautogui.mouseDown(button="left" if key == "lb" else "right")

    return {"status": "ok"}


@app.route("/key-release", methods=["POST"])
def key_release():
    data = request.json or {}
    key = data.get("key")

    if not key:
        return {"status": "missing key"}, 400

    if key_is_held(key):
        unmark_hold(key)
        if key not in ["lb", "rb"]:
            release_key(key)
        else:
            pyautogui.mouseUp(button="left" if key == "lb" else "right")

    return {"status": "ok"}


@app.route("/move", methods=["POST"])
def move():
    method = request.method
    verify_method(method)
    data = request.json
    x = data.get("x")

    pyautogui.moveTo(width / 2 + float(x) * 10, height / 2)

    return {"status": "ok"}


@app.route("/click", methods=["POST"])
def click():
    mouse = request.json.get("click")
    pyautogui.click(button=mouse)
    return {"status": "ok"}


app.run(host="0.0.0.0", port=5000)
