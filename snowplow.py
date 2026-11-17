import time

from PySide6.QtCore import QRectF
from PySide6.QtGui import QColor, QPolygonF
from PySide6.QtCore import QPointF


class Snowplow:

    def __init__(self, screen_width, ground_y):
        self.screen_width = screen_width
        self.ground_y = ground_y

        self.width = 76
        self.height = 42
        self.speed = 3

        self.x = -self.width
        self.active = False

    def start(self):
        if not self.active:
            self.x = -self.width
            self.active = True

    def update(self, ground):

        if not self.active:
            return

        self.x += self.speed

        blade_x = self.x + self.width

        for i in range(len(ground.heights)):

            segment_x = i * ground.segment_width

            if self.x <= segment_x <= blade_x:
                ground.heights[i] = 0

        if self.x > self.screen_width:
            self.active = False

    def draw(self, painter):

        if not self.active:
            return

        painter.save()
        painter.translate(
            self.x,
            self.ground_y - self.height
        )

        # Основно тяло
        painter.setBrush(QColor("#F4B942"))
        painter.drawRoundedRect(
            QRectF(4, 16, 57, 19), 4, 4
        )

        # Кабина
        painter.setBrush(QColor("#E8A020"))
        painter.drawRoundedRect(
            QRectF(23, 3, 29, 21), 3, 3
        )

        # Прозорец
        painter.setBrush(QColor("#ABD8EF"))
        painter.drawRoundedRect(
            QRectF(28, 7, 20, 13), 2, 2
        )

        # Гуми
        painter.setBrush(QColor("#252525"))
        painter.drawEllipse(QRectF(8, 29, 16, 13))
        painter.drawEllipse(QRectF(43, 29, 16, 13))

        # Джанти
        painter.setBrush(QColor("#AAAAAA"))
        painter.drawEllipse(QRectF(12, 32, 8, 7))
        painter.drawEllipse(QRectF(47, 32, 8, 7))

        # Гребло
        painter.setBrush(QColor("#E67E22"))
        painter.drawPolygon(QPolygonF([
            QPointF(60, 19),
            QPointF(75, 28),
            QPointF(76, 42),
            QPointF(63, 42)
        ]))

        # Мигаща лампичка
        if int(time.monotonic() * 3) % 2 == 0:
            painter.setBrush(QColor("#FFEB3B"))
        else:
            painter.setBrush(QColor("#B87915"))

        painter.drawRoundedRect(
            QRectF(32, 0, 10, 5), 2, 2
        )

        painter.restore()