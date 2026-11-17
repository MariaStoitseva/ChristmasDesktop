import math
import random

from PySide6.QtCore import QRectF, QPointF, Qt
from PySide6.QtGui import QColor, QPen


class ChristmasTrain:

    def __init__(self, screen_width, ground_y):

        self.screen_width = screen_width
        self.ground_y = ground_y

        self.width = 290
        self.height = 60
        self.speed = 2.5

        self.x = -self.width
        self.active = False

        self.wheel_angle = 0
        self.smoke = []
        self.frame = 0

    def start(self):

        if not self.active:

            self.x = -self.width
            self.active = True
            self.smoke.clear()

    def update(self):

        if not self.active:
            return

        self.x += self.speed
        self.wheel_angle += 0.2
        self.frame += 1

        # Създаване на пара
        if self.frame % 8 == 0:

            self.smoke.append({
                "x": self.x + 268,
                "y": self.ground_y - 57,
                "size": random.uniform(3, 6),
                "opacity": 180
            })

        # Движение на парата
        for puff in self.smoke:

            puff["x"] -= 0.6
            puff["y"] -= 0.7
            puff["size"] += 0.12
            puff["opacity"] -= 2

        self.smoke = [
            puff for puff in self.smoke
            if puff["opacity"] > 0
        ]

        if self.x > self.screen_width:

            self.active = False
            self.smoke.clear()

    def draw_wheel(self, painter, x, y, radius):

        painter.save()

        painter.translate(x, y)

        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QColor("#263238"))

        painter.drawEllipse(
            QPointF(0, 0), radius, radius
        )

        painter.setBrush(QColor("#B71C1C"))

        painter.drawEllipse(
            QPointF(0, 0),
            radius - 2,
            radius - 2
        )

        painter.setPen(
            QPen(QColor("#FFD54F"), 1.5)
        )

        for i in range(6):

            angle = (
                self.wheel_angle
                + i * math.pi / 3
            )

            painter.drawLine(
                QPointF(0, 0),
                QPointF(
                    math.cos(angle) * (radius - 3),
                    math.sin(angle) * (radius - 3)
                )
            )

        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QColor("#FFD54F"))

        painter.drawEllipse(
            QPointF(0, 0), 2, 2
        )

        painter.restore()

    def draw_gift(self, painter, x, y, w, h, color):

        painter.setPen(Qt.PenStyle.NoPen)

        painter.setBrush(QColor(color))

        painter.drawRoundedRect(
            QRectF(x, y, w, h), 2, 2
        )

        # Панделка
        painter.setBrush(QColor("#FFD54F"))

        painter.drawRect(
            QRectF(x + w / 2 - 2, y, 4, h)
        )

        painter.drawRect(
            QRectF(x, y + h / 2, w, 3)
        )

        painter.drawEllipse(
            QRectF(x + w / 2 - 7, y - 4, 7, 5)
        )

        painter.drawEllipse(
            QRectF(x + w / 2, y - 4, 7, 5)
        )

    def draw_wagon(self, painter, x, color):

        # Подаръци
        self.draw_gift(
            painter, x + 5, 17, 19, 24, "#C62828"
        )

        self.draw_gift(
            painter, x + 25, 8, 20, 33, "#1565C0"
        )

        self.draw_gift(
            painter, x + 43, 22, 14, 19, "#8E24AA"
        )

        # Основно тяло
        painter.setBrush(QColor(color))

        painter.drawRoundedRect(
            QRectF(x, 35, 62, 17), 3, 3
        )

        # Златен кант
        painter.setBrush(QColor("#FFD54F"))

        painter.drawRect(
            QRectF(x, 37, 62, 3)
        )

        # Колела
        self.draw_wheel(painter, x + 13, 53, 7)
        self.draw_wheel(painter, x + 49, 53, 7)

        # Връзка между вагоните
        painter.setBrush(QColor("#795548"))

        painter.drawRect(
            QRectF(x + 62, 44, 9, 4)
        )

    def draw_engine(self, painter):

        x = 213

        # Основа на локомотива
        painter.setBrush(QColor("#B71C1C"))

        painter.drawRoundedRect(
            QRectF(x, 35, 76, 17), 4, 4
        )

        # Кабина
        painter.setBrush(QColor("#C62828"))

        painter.drawRoundedRect(
            QRectF(x + 4, 12, 29, 29), 4, 4
        )

        # Покрив
        painter.setBrush(QColor("#1B5E20"))

        painter.drawRoundedRect(
            QRectF(x, 8, 37, 7), 3, 3
        )

        # Прозорец
        painter.setBrush(QColor("#FFE082"))

        painter.drawRoundedRect(
            QRectF(x + 11, 18, 15, 13), 2, 2
        )

        # Котел
        painter.setBrush(QColor("#2E7D32"))

        painter.drawRoundedRect(
            QRectF(x + 31, 23, 41, 17), 8, 8
        )

        # Комин
        painter.setBrush(QColor("#263238"))

        painter.drawRect(
            QRectF(x + 50, 9, 10, 17)
        )

        painter.drawRoundedRect(
            QRectF(x + 47, 5, 16, 6), 2, 2
        )

        # Златни декоративни кантове
        painter.setBrush(QColor("#FFD54F"))

        painter.drawRect(
            QRectF(x + 36, 23, 4, 17)
        )

        painter.drawRect(
            QRectF(x + 63, 23, 4, 17)
        )

        # Фар
        painter.setBrush(QColor("#FFF59D"))

        painter.drawEllipse(
            QRectF(x + 69, 26, 8, 8)
        )

        # Колела
        self.draw_wheel(painter, x + 14, 52, 8)
        self.draw_wheel(painter, x + 39, 52, 8)
        self.draw_wheel(painter, x + 64, 52, 8)

    def draw(self, painter):

        if not self.active:
            return

        painter.save()
        painter.setPen(Qt.PenStyle.NoPen)

        # Пара
        for puff in self.smoke:

            painter.setBrush(QColor(
                245, 250, 255,
                int(puff["opacity"])
            ))

            painter.drawEllipse(
                QPointF(puff["x"], puff["y"]),
                puff["size"],
                puff["size"]
            )

        painter.translate(
            self.x,
            self.ground_y - self.height
        )

        # Три вагона
        self.draw_wagon(painter, 0, "#1B5E20")
        self.draw_wagon(painter, 71, "#B71C1C")
        self.draw_wagon(painter, 142, "#1B5E20")

        # Локомотив
        self.draw_engine(painter)

        painter.restore()