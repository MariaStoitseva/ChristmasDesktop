import random
import win32gui

from PySide6.QtWidgets import QApplication, QWidget
from PySide6.QtCore import Qt, QTimer, QPointF, QRect
from PySide6.QtGui import (
    QPainter,
    QColor,
    QPainterPath,
    QRegion
)

from snow import Snowflake, SnowSurface
from window_manager import get_visible_windows
from snowplow import Snowplow
from christmas_train import ChristmasTrain


class SnowOverlay(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint
            | Qt.WindowType.WindowStaysOnTopHint
            | Qt.WindowType.Tool
            | Qt.WindowType.WindowTransparentForInput
            | Qt.WindowType.WindowDoesNotAcceptFocus
        )

        self.setAttribute(
            Qt.WidgetAttribute.WA_TranslucentBackground
        )

        self.screen_info = QApplication.primaryScreen()

        self.setGeometry(
            self.screen_info.geometry()
        )

        self.ground_y = (
            self.screen_info.availableGeometry().bottom()
            - self.screen_info.geometry().top() + 1
        )

        self.snowflakes = [
            Snowflake(self.width(), self.height())
            for _ in range(350)
        ]

        self.ground = SnowSurface(
            0, self.ground_y, self.width(), 30
        )

        self.window_surfaces = {}
        self.window_rects = {}
        self.visible_regions = {}

        # Снегорин
        self.snowplow = Snowplow(
            self.width(),
            self.ground_y
        )

        self.snowplow_timer = QTimer(self)

        self.snowplow_timer.timeout.connect(
            self.start_snowplow
        )

        self.snowplow_timer.start(90000)

        # Коледно влакче
        self.train = ChristmasTrain(
            self.width(),
            self.ground_y
        )

        self.train_timer = QTimer(self)

        self.train_timer.timeout.connect(
            self.start_train
        )

        self.train_timer.start(180000)

        # Анимация
        self.animation_timer = QTimer(self)

        self.animation_timer.timeout.connect(
            self.animate
        )

        self.animation_timer.start(16)

        # Проверка на прозорците
        self.window_timer = QTimer(self)

        self.window_timer.timeout.connect(
            self.update_windows
        )

        self.window_timer.start(80)

    def start_snowplow(self):

        if self.isVisible() and not self.train.active:

            self.snowplow.start()

    def start_train(self):

        if self.isVisible() and not self.snowplow.active:

            self.train.start()

    def release_snow(self, surface):

        for i, height in enumerate(surface.heights):

            if height < 2:
                continue

            for _ in range(int(height / 3) + 1):

                flake = Snowflake(
                    self.width(), self.height()
                )

                flake.x = (
                    surface.x
                    + i * surface.segment_width
                )

                flake.y = (
                    surface.y
                    - random.uniform(0, height)
                )

                flake.speed = random.uniform(2, 5)
                flake.temporary = True

                self.snowflakes.append(flake)

    def update_windows(self):

        windows = get_visible_windows(
            int(self.winId()),
            self.screen_info
        )

        for hwnd, surface in list(
            self.window_surfaces.items()
        ):

            # Затворен прозорец
            if not win32gui.IsWindow(hwnd):

                self.release_snow(surface)

                del self.window_surfaces[hwnd]

                self.window_rects.pop(hwnd, None)

                continue

            # Скрит или минимизиран прозорец
            if hwnd not in windows:
                continue

            # Преместен или преоразмерен прозорец
            if windows[hwnd] != self.window_rects.get(hwnd):

                self.release_snow(surface)

                del self.window_surfaces[hwnd]

        covered_region = QRegion()

        self.visible_regions = {}

        for hwnd, (x, y, width, height) in windows.items():

            if 0 < y < self.ground_y:

                left = max(0, x)
                right = min(self.width(), x + width)

                if right - left >= 50:

                    if hwnd not in self.window_surfaces:

                        self.window_surfaces[hwnd] = SnowSurface(
                            left,
                            y,
                            right - left,
                            15
                        )

                    surface_region = QRegion(
                        QRect(
                            left,
                            y - 16,
                            right - left,
                            17
                        )
                    )

                    self.visible_regions[hwnd] = (
                        surface_region.subtracted(
                            covered_region
                        )
                    )

            covered_region = covered_region.united(
                QRegion(
                    QRect(x, y, width, height)
                )
            )

        self.window_rects.update(windows)

        # Премахване на стари записи
        for hwnd in list(self.window_rects):

            if not win32gui.IsWindow(hwnd):

                self.window_rects.pop(hwnd, None)

    def animate(self):

        surfaces = sorted(
            self.window_surfaces.items(),
            key=lambda item: item[1].y
        )

        active_flakes = []

        for flake in self.snowflakes:

            previous_y = flake.y

            flake.update()

            collided = False

            for hwnd, surface in surfaces:

                region = self.visible_regions.get(hwnd)

                if region is None or region.isEmpty():
                    continue

                if surface.collides(flake, previous_y):

                    point = QPointF(
                        flake.x,
                        surface.y
                    ).toPoint()

                    if region.contains(point):

                        surface.accumulate(flake.x)

                        collided = True
                        break

            # Натрупване над taskbar-а
            if not collided:

                if self.ground.collides(
                    flake, previous_y
                ):

                    self.ground.accumulate(flake.x)

                    collided = True

            # Премахване или повторно използване
            if collided or flake.y > self.height():

                if getattr(flake, "temporary", False):
                    continue

                flake.reset(self.width())

            active_flakes.append(flake)

        self.snowflakes = active_flakes

        # Движение на снегорина
        self.snowplow.update(self.ground)

        # Движение на влакчето
        self.train.update()

        self.update()

    def draw_surface(self, painter, surface):

        path = QPainterPath()

        path.moveTo(surface.x, surface.y)

        points = [
            QPointF(
                min(
                    surface.x + surface.width,
                    surface.x + i * surface.segment_width
                ),
                surface.y - height
            )
            for i, height in enumerate(surface.heights)
        ]

        if not points:
            return

        path.lineTo(points[0])

        for i in range(1, len(points)):

            previous = points[i - 1]
            current = points[i]

            middle = QPointF(
                (previous.x() + current.x()) / 2,
                (previous.y() + current.y()) / 2
            )

            path.quadTo(previous, middle)

        path.lineTo(points[-1])

        path.lineTo(
            surface.x + surface.width,
            surface.y
        )

        path.closeSubpath()

        painter.setBrush(
            QColor(245, 250, 255, 245)
        )

        painter.drawPath(path)

    def paintEvent(self, event):

        painter = QPainter(self)

        painter.setRenderHint(
            QPainter.RenderHint.Antialiasing
        )

        painter.setPen(Qt.PenStyle.NoPen)

        # Падащ сняг
        for flake in self.snowflakes:

            painter.setBrush(
                QColor(
                    255,
                    255,
                    255,
                    flake.opacity
                )
            )

            painter.drawEllipse(
                QPointF(flake.x, flake.y),
                flake.size,
                flake.size
            )

        # Сняг над taskbar-а
        self.draw_surface(painter, self.ground)

        # Сняг върху прозорците
        for hwnd, surface in self.window_surfaces.items():

            region = self.visible_regions.get(hwnd)

            if region is None or region.isEmpty():
                continue

            painter.save()

            painter.setClipRegion(region)

            self.draw_surface(painter, surface)

            painter.restore()

        # Снегорин
        self.snowplow.draw(painter)

        # Коледно влакче
        self.train.draw(painter)