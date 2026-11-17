from PySide6.QtWidgets import (
    QSystemTrayIcon,
    QMenu
)

from PySide6.QtGui import (
    QIcon,
    QPixmap,
    QPainter,
    QColor,
    QPen
)

from PySide6.QtCore import Qt

from tree_manager import TreeManager
from settings_window import SettingsWindow


class ChristmasTray(QSystemTrayIcon):

    def __init__(
        self,
        app,
        overlay,
        snowman_manager,
        wallpaper_manager
    ):

        super().__init__()

        self.app = app
        self.overlay = overlay
        self.snowman_manager = snowman_manager
        self.wallpaper_manager = wallpaper_manager

        self.tree_manager = TreeManager(overlay)

        self.settings_window = None

        self.setIcon(self.create_icon())

        self.setToolTip("Christmas Desktop")

        # Меню при десен клик

        self.menu = QMenu()

        self.menu.addAction(
            "Изход",
            self.app.quit
        )

        self.setContextMenu(self.menu)

        # Ляв клик върху снежинката

        self.activated.connect(
            self.open_menu
        )

        self.show()

    def open_settings(self):

        if self.settings_window is None:

            self.settings_window = SettingsWindow(self)

            self.settings_window.setWindowIcon(
                self.icon()
            )

        self.settings_window.refresh()

        self.settings_window.showNormal()

        self.settings_window.raise_()

        self.settings_window.activateWindow()

    def select_wallpaper(self, mode):

        if mode == "dynamic":

            self.wallpaper_manager.enable_dynamic()

        elif mode == "original":

            self.wallpaper_manager.restore_original()

        else:

            self.wallpaper_manager.set_manual_wallpaper(mode)

        if self.settings_window is not None:

            self.settings_window.refresh()

    def create_icon(self):

        pixmap = QPixmap(64, 64)

        pixmap.fill(
            Qt.GlobalColor.transparent
        )

        painter = QPainter(pixmap)

        painter.setRenderHint(
            QPainter.RenderHint.Antialiasing
        )

        painter.setPen(
            QPen(QColor("#90CAF9"), 5)
        )

        painter.translate(32, 32)

        for angle in range(0, 360, 60):

            painter.save()

            painter.rotate(angle)

            painter.drawLine(0, 0, 0, -26)

            painter.drawLine(
                0, -15, -7, -21
            )

            painter.drawLine(
                0, -15, 7, -21
            )

            painter.restore()

        painter.end()

        return QIcon(pixmap)

    def open_menu(self, reason):

        if reason == QSystemTrayIcon.ActivationReason.Trigger:

            self.open_settings()

    def toggle_snow(self):

        if self.overlay.isVisible():

            self.overlay.hide()

            self.overlay.animation_timer.stop()
            self.overlay.window_timer.stop()
            self.overlay.snowplow_timer.stop()
            self.overlay.train_timer.stop()

        else:

            self.overlay.show()

            self.overlay.animation_timer.start(16)
            self.overlay.window_timer.start(80)

            self.overlay.snowplow_timer.start()
            self.overlay.train_timer.start()

        if self.settings_window is not None:

            self.settings_window.refresh()

    def spawn_snowballs(self):

        self.snowman_manager.spawn_snowballs()