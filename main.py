import sys
import os

from pathlib import Path

from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QTimer, QLockFile
from PySide6.QtGui import QIcon

from overlay import SnowOverlay
from wallpaper import WallpaperManager
from snowman_manager import SnowmanManager
from tray import ChristmasTray


if __name__ == "__main__":

    app = QApplication(sys.argv)

    app.setApplicationName("Christmas Desktop")

    app.setApplicationVersion("1.0")

    app.setQuitOnLastWindowClosed(False)

    # Само едно активно копие

    data_folder = (
        Path(os.environ["LOCALAPPDATA"])
        / "ChristmasDesktop"
    )

    data_folder.mkdir(
        parents=True,
        exist_ok=True
    )

    lock = QLockFile(
        str(data_folder / "app.lock")
    )

    lock.setStaleLockTime(0)

    if not lock.tryLock(0):

        sys.exit(0)

    # Икона

    icon_path = (
        Path(__file__).resolve().parent
        / "assets"
        / "icon.ico"
    )

    if icon_path.exists():

        app.setWindowIcon(
            QIcon(str(icon_path))
        )

    # Динамичен тапет

    wallpaper_manager = WallpaperManager()

    app.aboutToQuit.connect(
        wallpaper_manager.restore_original
    )

    # Снеговалеж

    overlay = SnowOverlay()

    overlay.show()

    # Снежни човечета

    snowballs = []

    snowman_manager = SnowmanManager(
        snowballs,
        overlay.ground_y
    )

    snowman_timer = QTimer()

    snowman_timer.timeout.connect(
        snowman_manager.check
    )

    snowman_timer.start(100)

    # System Tray

    tray = ChristmasTray(
        app,
        overlay,
        snowman_manager,
        wallpaper_manager
    )

    exit_code = app.exec()

    lock.unlock()

    sys.exit(exit_code)