import ctypes
from ctypes import wintypes

import win32gui
import win32con


def get_visible_windows(overlay_hwnd, screen):
    windows = {}

    ratio = screen.devicePixelRatio()
    geometry = screen.geometry()

    def callback(hwnd, _):
        if hwnd == overlay_hwnd:
            return True

        if not win32gui.IsWindowVisible(hwnd):
            return True

        if win32gui.IsIconic(hwnd):
            return True

        if not win32gui.GetWindowText(hwnd):
            return True

        style = win32gui.GetWindowLong(
            hwnd, win32con.GWL_EXSTYLE
        )

        if style & win32con.WS_EX_TOOLWINDOW:
            return True

        cloaked = ctypes.c_int(0)

        ctypes.windll.dwmapi.DwmGetWindowAttribute(
            ctypes.c_void_p(hwnd),
            14,
            ctypes.byref(cloaked),
            ctypes.sizeof(cloaked)
        )

        if cloaked.value:
            return True

        rect = wintypes.RECT()

        result = ctypes.windll.dwmapi.DwmGetWindowAttribute(
            ctypes.c_void_p(hwnd),
            9,
            ctypes.byref(rect),
            ctypes.sizeof(rect)
        )

        if result == 0:
            left = rect.left
            top = rect.top
            right = rect.right
            bottom = rect.bottom
        else:
            left, top, right, bottom = (
                win32gui.GetWindowRect(hwnd)
            )

        x = int(left / ratio) - geometry.x()
        y = int(top / ratio) - geometry.y()

        width = int((right - left) / ratio)
        height = int((bottom - top) / ratio)

        if width < 100 or height < 50:
            return True

        windows[hwnd] = (x, y, width, height)

        return True

    win32gui.EnumWindows(callback, None)

    return windows