import math
import time

from PySide6.QtWidgets import QWidget, QMenu, QApplication
from PySide6.QtCore import Qt, QPointF, QRectF, QTimer
from PySide6.QtGui import (
    QPainter,
    QColor,
    QPolygonF,
    QPainterPath,
    QRadialGradient,
    QLinearGradient,
    QPen
)


class ChristmasTree(QWidget):

    def __init__(self, x, y, overlay):
        super().__init__()

        self.overlay = overlay
        self.decorations = []

        self.selected_color = None
        self.selected_type = None

        self.star_enabled = False
        self.lights_enabled = False
        self.gifts_enabled = False
        self.garland_color = None

        self.snow_amount = 0.0

        self.drag_position = None
        self.press_position = None
        self.dragging = False

        self.branches = [
            (105, 215, 82, "#123D28", "#287A45"),
            (74, 181, 72, "#185333", "#328A50"),
            (48, 138, 52, "#20643D", "#399A59"),
            (25, 97, 35, "#267548", "#48A868")
        ]

        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint
            | Qt.WindowType.WindowStaysOnTopHint
            | Qt.WindowType.Tool
        )

        self.setAttribute(
            Qt.WidgetAttribute.WA_TranslucentBackground
        )

        self.setFixedSize(180, 250)
        self.move(x, y)

        self.setCursor(Qt.CursorShape.OpenHandCursor)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.animate)
        self.timer.start(100)

    def animate(self):

        if self.overlay.isVisible():
            self.snow_amount = min(
                1.0,
                self.snow_amount + 0.001
            )

        self.update()

    def branch_path(self, top, bottom, width):

        path = QPainterPath()
        path.moveTo(90, top)

        for i in range(1, 9):

            progress = i / 8
            y = top + (bottom - top) * progress
            x = 90 - width * progress

            if i % 2 == 0 and i != 8:
                x += 9

            path.lineTo(x, y)

        path.quadTo(90, bottom - 9, 90 + width, bottom)

        for i in range(7, 0, -1):

            progress = i / 8
            y = top + (bottom - top) * progress
            x = 90 + width * progress

            if i % 2 == 0:
                x -= 9

            path.lineTo(x, y)

        path.closeSubpath()

        return path

    def draw_tree(self, painter):

        # Ствол
        trunk = QLinearGradient(79, 0, 101, 0)

        trunk.setColorAt(0, QColor("#4E342E"))
        trunk.setColorAt(0.5, QColor("#916849"))
        trunk.setColorAt(1, QColor("#4E342E"))

        painter.setBrush(trunk)

        painter.drawRoundedRect(
            QRectF(79, 200, 22, 42), 3, 3
        )

        # Клони
        for top, bottom, width, dark, light in self.branches:

            gradient = QLinearGradient(
                90 - width, top,
                90 + width, bottom
            )

            gradient.setColorAt(0, QColor(light))
            gradient.setColorAt(0.6, QColor(dark))
            gradient.setColorAt(1, QColor(light).darker(130))

            painter.setBrush(gradient)

            painter.drawPath(
                self.branch_path(top, bottom, width)
            )

    def draw_snow(self, painter):

        if self.snow_amount <= 0:
            return

        height = self.snow_amount * 9

        for top, bottom, width, _, _ in self.branches:

            painter.save()

            painter.setClipPath(
                self.branch_path(top, bottom, width)
            )

            gradient = QLinearGradient(
                0, bottom - 20,
                0, bottom
            )

            gradient.setColorAt(0, QColor("#FFFFFF"))
            gradient.setColorAt(1, QColor("#C5DDF0"))

            painter.setBrush(gradient)

            path = QPainterPath()

            left = 90 - width
            right = 90 + width

            path.moveTo(left, bottom - 3)

            path.quadTo(
                left + width * 0.4,
                bottom - 3 - height * 2,
                90,
                bottom - 5 - height
            )

            path.quadTo(
                right - width * 0.35,
                bottom - 3 - height * 2,
                right,
                bottom - 3
            )

            path.lineTo(right, bottom + 2)
            path.lineTo(left, bottom + 2)

            path.closeSubpath()

            painter.drawPath(path)
            painter.restore()

    def draw_star(self, painter):

        points = []

        for i in range(10):

            angle = math.radians(i * 36 - 90)
            radius = 15 if i % 2 == 0 else 6

            points.append(QPointF(
                90 + math.cos(angle) * radius,
                20 + math.sin(angle) * radius
            ))

        gradient = QRadialGradient(90, 15, 20)

        gradient.setColorAt(0, QColor("#FFF9C4"))
        gradient.setColorAt(1, QColor("#E5A000"))

        painter.setBrush(gradient)
        painter.drawPolygon(QPolygonF(points))

    def draw_bauble(self, painter, x, y, color):

        gradient = QRadialGradient(
            x - 2.5, y - 3, 10
        )

        gradient.setColorAt(
            0, QColor(color).lighter(190)
        )

        gradient.setColorAt(0.45, QColor(color))

        gradient.setColorAt(
            1, QColor(color).darker(170)
        )

        painter.setBrush(gradient)

        painter.drawEllipse(
            QPointF(x, y), 6, 6
        )

        painter.setBrush(QColor("#E8CE84"))

        painter.drawRoundedRect(
            QRectF(x - 2, y - 8, 4, 3),
            1, 1
        )

    def draw_candy_cane(self, painter, x, y):

        painter.save()

        painter.translate(x, y)
        painter.rotate(-15)

        path = QPainterPath()

        path.moveTo(0, 10)
        path.lineTo(0, -5)
        path.quadTo(0, -12, 6, -12)
        path.quadTo(12, -12, 12, -5)

        pen = QPen(QColor("#FFFFFF"), 5)
        pen.setCapStyle(Qt.PenCapStyle.RoundCap)

        painter.setPen(pen)
        painter.drawPath(path)

        # Червени райета
        pen = QPen(QColor("#E53935"), 2.5)

        painter.setPen(pen)

        for stripe_y in [-4, 2, 8]:

            painter.drawLine(
                QPointF(-2, stripe_y - 1),
                QPointF(2, stripe_y + 1)
            )

        painter.drawLine(
            QPointF(5, -14),
            QPointF(7, -10)
        )

        painter.restore()

    def draw_garland(self, painter):

        if self.garland_color is None:
            return

        painter.save()

        pen = QPen(
            QColor(self.garland_color), 3
        )

        pen.setCapStyle(Qt.PenCapStyle.RoundCap)

        painter.setPen(pen)
        painter.setBrush(Qt.BrushStyle.NoBrush)

        for y, width in [
            (78, 20),
            (119, 35),
            (159, 48),
            (197, 61)
        ]:

            path = QPainterPath()

            path.moveTo(90 - width, y - 5)

            path.quadTo(
                90,
                y + 17,
                90 + width,
                y - 5
            )

            painter.drawPath(path)

        painter.restore()

    def draw_lights(self, painter):

        colors = [
            "#FF5252",
            "#FFEB3B",
            "#42A5F5",
            "#69F0AE"
        ]

        for row in range(4):

            y = 78 + row * 39
            width = 40 + row * 30

            for i in range(7):

                x = 90 - width / 2 + i * width / 6

                light_y = (
                    y + math.sin(i / 6 * math.pi) * 10
                )

                index = (
                    i + row + int(time.monotonic() * 2)
                ) % len(colors)

                color = QColor(colors[index])

                glow = QRadialGradient(x, light_y, 8)
                glow.setColorAt(0, color)

                transparent = QColor(color)
                transparent.setAlpha(0)

                glow.setColorAt(1, transparent)

                painter.setBrush(glow)

                painter.drawEllipse(
                    QPointF(x, light_y), 8, 8
                )

                painter.setBrush(color)

                painter.drawEllipse(
                    QPointF(x, light_y), 2.5, 2.5
                )

    def draw_gift(self, painter, x, y, w, h, color):

        painter.setBrush(QColor(color))

        painter.drawRoundedRect(
            QRectF(x, y, w, h), 2, 2
        )

        painter.setBrush(QColor("#FFD54F"))

        painter.drawRect(
            QRectF(x + w / 2 - 3, y, 6, h)
        )

        painter.drawRect(
            QRectF(x, y + h / 2, w, 4)
        )

        painter.drawEllipse(
            QRectF(x + w / 2 - 10, y - 5, 10, 6)
        )

        painter.drawEllipse(
            QRectF(x + w / 2, y - 5, 10, 6)
        )

    def paintEvent(self, event):

        painter = QPainter(self)

        painter.setRenderHint(
            QPainter.RenderHint.Antialiasing
        )

        painter.setPen(Qt.PenStyle.NoPen)

        self.draw_tree(painter)
        self.draw_snow(painter)
        self.draw_garland(painter)

        for x, y, kind, color in self.decorations:

            if kind == "bauble":
                self.draw_bauble(painter, x, y, color)

            elif kind == "candy":
                self.draw_candy_cane(painter, x, y)

        if self.lights_enabled:
            self.draw_lights(painter)

        if self.star_enabled:
            self.draw_star(painter)

        if self.gifts_enabled:

            self.draw_gift(
                painter, 35, 218, 34, 24, "#C62828"
            )

            self.draw_gift(
                painter, 108, 212, 38, 30, "#1565C0"
            )

            self.draw_gift(
                painter, 65, 227, 27, 15, "#8E24AA"
            )

    def is_on_tree(self, position):

        return any(
            self.branch_path(top, bottom, width).contains(position)
            for top, bottom, width, _, _ in self.branches
        )

    def mousePressEvent(self, event):

        if event.button() != Qt.MouseButton.LeftButton:
            return

        self.press_position = (
            event.globalPosition().toPoint()
        )

        self.drag_position = (
            self.press_position - self.pos()
        )

        self.dragging = False

    def mouseMoveEvent(self, event):

        if self.drag_position is None:
            return

        position = event.globalPosition().toPoint()

        distance = (
            position - self.press_position
        ).manhattanLength()

        if distance > QApplication.startDragDistance():
            self.dragging = True

        if self.dragging:
            self.move(position - self.drag_position)

    def mouseReleaseEvent(self, event):

        if event.button() != Qt.MouseButton.LeftButton:
            return

        if not self.dragging:

            position = event.position()

            if (
                self.selected_type
                and self.is_on_tree(position)
                and len(self.decorations) < 100
            ):

                self.decorations.append((
                    position.x(),
                    position.y(),
                    self.selected_type,
                    self.selected_color
                ))

                self.update()

        self.drag_position = None
        self.press_position = None
        self.dragging = False

    def select_color(self, color):

        self.selected_type = "bauble"
        self.selected_color = color

        self.setCursor(Qt.CursorShape.CrossCursor)

    def select_candy(self):

        self.selected_type = "candy"
        self.selected_color = None

        self.setCursor(Qt.CursorShape.CrossCursor)

    def stop_decorating(self):

        self.selected_type = None
        self.selected_color = None

        self.setCursor(Qt.CursorShape.OpenHandCursor)

    def toggle_star(self):

        self.star_enabled = not self.star_enabled
        self.update()

    def toggle_lights(self):

        self.lights_enabled = not self.lights_enabled
        self.update()

    def toggle_gifts(self):

        self.gifts_enabled = not self.gifts_enabled
        self.update()

    def set_garland(self, color):

        self.garland_color = color
        self.update()

    def undo_decoration(self):

        if self.decorations:
            self.decorations.pop()

        self.update()

    def clear_decorations(self):

        self.decorations.clear()

        self.star_enabled = False
        self.lights_enabled = False
        self.gifts_enabled = False
        self.garland_color = None

        self.stop_decorating()
        self.update()

    def clear_snow(self):

        self.snow_amount = 0
        self.update()

    def closeEvent(self, event):

        self.timer.stop()
        super().closeEvent(event)

    def contextMenuEvent(self, event):

        menu = QMenu(self)

        ornaments = menu.addMenu("Коледни топки")

        colors = {
            "Червена": "#E53935",
            "Златна": "#FFCA28",
            "Сребърна": "#CFD8DC",
            "Синя": "#2196F3",
            "Лилава": "#AB47BC",
            "Розова": "#EC407A",
            "Зелена": "#66BB6A"
        }

        for name, color in colors.items():

            action = ornaments.addAction(name)

            action.triggered.connect(
                lambda checked=False, c=color:
                self.select_color(c)
            )

        menu.addAction(
            "Захарно бастунче",
            self.select_candy
        )

        garland_menu = menu.addMenu("Гирлянди")

        garland_menu.addAction(
            "Златен",
            lambda: self.set_garland("#FFD54F")
        )

        garland_menu.addAction(
            "Сребърен",
            lambda: self.set_garland("#CFD8DC")
        )

        garland_menu.addAction(
            "Червен",
            lambda: self.set_garland("#EF5350")
        )

        garland_menu.addAction(
            "Без гирлянди",
            lambda: self.set_garland(None)
        )

        menu.addAction(
            "Звезда",
            self.toggle_star
        )

        menu.addAction(
            "Лампички",
            self.toggle_lights
        )

        menu.addAction(
            "Подаръци",
            self.toggle_gifts
        )

        menu.addSeparator()

        menu.addAction(
            "Приключи украсяването",
            self.stop_decorating
        )

        menu.addAction(
            "Премахни последната украса",
            self.undo_decoration
        )

        menu.addAction(
            "Премахни цялата украса",
            self.clear_decorations
        )

        menu.addAction(
            "Изчисти снега",
            self.clear_snow
        )

        menu.addSeparator()

        menu.addAction(
            "Премахни елхата",
            self.close
        )

        menu.exec(event.globalPos())