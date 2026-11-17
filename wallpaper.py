import ctypes
import shutil
import os

from pathlib import Path
from datetime import datetime
from uuid import uuid4

from PySide6.QtCore import QObject, QTimer


class WallpaperManager(QObject):

    def __init__(self):

        super().__init__()

        self.assets = Path(__file__).resolve().parent / "assets"

        self.wallpapers = {
            "sunrise": "winter_sunrise.png",
            "day": "winter_day.png",
            "sunset": "winter_sunset.png",
            "night": "winter_night.png"
        }

        self.original_wallpaper = self.get_current_wallpaper()
        self.original_wallpaper = self.backup_wallpaper(
            self.original_wallpaper
        )

        self.dynamic_enabled = True
        self.current_wallpaper = None
        self.wallpaper_changed = False

        self.timer = QTimer(self)

        self.timer.timeout.connect(
            self.update_wallpaper
        )

        self.timer.start(60000)

        self.update_wallpaper()

    def get_current_wallpaper(self):

        buffer = ctypes.create_unicode_buffer(260)

        success = ctypes.windll.user32.SystemParametersInfoW(
            115,
            len(buffer),
            buffer,
            0
        )

        return buffer.value if success else None

    def backup_wallpaper(self, wallpaper):

        if not wallpaper:
            return wallpaper

        source = Path(wallpaper)

        if not source.is_file():
            return wallpaper

        # Запазваме копие, защото Windows може
        # да презапише кеширания си тапет.

        backup_folder = (
            Path(os.environ["LOCALAPPDATA"])
            / "ChristmasDesktop"
            / "wallpapers"
        )

        try:

            backup_folder.mkdir(
                parents=True,
                exist_ok=True
            )

            backup = backup_folder / (
                f"original_{uuid4().hex}"
                f"{source.suffix or '.jpg'}"
            )

            shutil.copy2(source, backup)

            return str(backup)

        except OSError:

            return wallpaper

    def get_time_period(self):

        hour = datetime.now().hour

        if 6 <= hour < 9:
            return "sunrise"

        elif 9 <= hour < 16:
            return "day"

        elif 16 <= hour < 18:
            return "sunset"

        return "night"

    def update_wallpaper(self):

        if not self.dynamic_enabled:
            return

        period = self.get_time_period()

        self.apply_wallpaper(period)

    def apply_wallpaper(self, period):

        if period not in self.wallpapers:
            return

        if self.current_wallpaper == period:
            return

        image_path = (
            self.assets / self.wallpapers[period]
        ).resolve()

        if not image_path.is_file():

            print(f"Липсва тапет: {image_path}")

            return

        success = ctypes.windll.user32.SystemParametersInfoW(
            20,
            0,
            str(image_path),
            3
        )

        if success:

            self.current_wallpaper = period
            self.wallpaper_changed = True

    def set_manual_wallpaper(self, period):

        self.dynamic_enabled = False

        self.timer.stop()

        self.apply_wallpaper(period)

    def enable_dynamic(self):

        self.dynamic_enabled = True

        self.current_wallpaper = None

        self.update_wallpaper()

        self.timer.start(60000)

    def restore_original(self):

        self.dynamic_enabled = False

        self.timer.stop()

        if not self.wallpaper_changed:
            return

        if self.original_wallpaper is None:
            return

        success = ctypes.windll.user32.SystemParametersInfoW(
            20,
            0,
            self.original_wallpaper,
            3
        )

        if success:

            self.current_wallpaper = None
            self.wallpaper_changed = False