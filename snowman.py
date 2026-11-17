from PySide6.QtWidgets import QWidget, QMenu
from PySide6.QtCore import Qt, QRectF, QPointF
from PySide6.QtGui import (
    QPainter,
    QColor,
    QRadialGradient,
    QPolygonF,
    QPen
)


class Snowman(QWidget):

    def __init__(self, x, y):
        super().__init__()

        self.drag_position = None
        self.scarf_color = "#C62828"
        self.hat_enabled = True
        self.design = 0

        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint
            | Qt.WindowType.WindowStaysOnTopHint
            | Qt.WindowType.Tool
        )

        self.setAttribute(
            Qt.WidgetAttribute.WA_TranslucentBackground
        )

        self.setFixedSize(100, 155)
        self.move(x, y)

        self.setCursor(
            Qt.CursorShape.OpenHandCursor
        )

    def draw_ball(self, painter, x, y, size):

        gradient = QRadialGradient(
            x + size * 0.35,
            y + size * 0.30,
            size * 0.8
        )

        gradient.setColorAt(0, QColor("#FFFFFF"))
        gradient.setColorAt(0.5, QColor("#EEF7FF"))
        gradient.setColorAt(1, QColor("#A8C5DC"))

        painter.setBrush(gradient)

        painter.drawEllipse(
            QRectF(x, y, size, size)
        )

    def set_design(self, design):

        self.design = design % 5

        colors = [
            "#C62828",
            "#2E7D32",
            "#1565C0",
            "#7B1FA2",
            "#D49B35"
        ]

        self.scarf_color = colors[self.design]

        self.update()

    def paintEvent(self, event):

        painter = QPainter(self)

        painter.setRenderHint(
            QPainter.RenderHint.Antialiasing
        )

        painter.setPen(Qt.PenStyle.NoPen)

        # Ръце
        painter.setPen(QPen(QColor("#795548"), 3))

        painter.drawLine(30, 85, 7, 68)
        painter.drawLine(70, 85, 93, 68)

        painter.drawLine(12, 72, 12, 62)
        painter.drawLine(88, 72, 88, 62)

        painter.setPen(Qt.PenStyle.NoPen)

        # Тяло
        self.draw_ball(painter, 17, 88, 66)
        self.draw_ball(painter, 26, 50, 48)
        self.draw_ball(painter, 32, 20, 36)

        # Очи
        painter.setBrush(QColor("#222222"))

        painter.drawEllipse(QRectF(41, 31, 4, 5))
        painter.drawEllipse(QRectF(55, 31, 4, 5))

        # Морков
        painter.setBrush(QColor("#F28C28"))

        painter.drawPolygon(QPolygonF([
            QPointF(49, 38),
            QPointF(63, 42),
            QPointF(48, 44)
        ]))

        # Усмивка
        painter.setBrush(QColor("#333333"))

        for x, y in [
            (42, 45),
            (46, 48),
            (51, 49),
            (56, 46)
        ]:
            painter.drawEllipse(
                QRectF(x, y, 2.5, 2.5)
            )

        # Копчета
        for y in [70, 83, 100]:

            painter.drawEllipse(
                QRectF(47, y, 5, 5)
            )

        # Шал
        painter.setBrush(QColor(self.scarf_color))

        painter.drawRoundedRect(
            QRectF(31, 51, 38, 9),
            4, 4
        )

        painter.drawRoundedRect(
            QRectF(57, 55, 9, 25),
            2, 2
        )

        # Шапка
        if self.hat_enabled:

            # Класически цилиндър
            if self.design == 0:

                painter.setBrush(QColor("#222222"))

                painter.drawRoundedRect(
                    QRectF(37, 2, 26, 23), 2, 2
                )

                painter.drawRoundedRect(
                    QRectF(29, 20, 42, 6), 2, 2
                )

                painter.setBrush(QColor("#C62828"))

                painter.drawRect(
                    QRectF(37, 15, 26, 5)
                )

            # Коледна шапка
            elif self.design == 1:

                painter.setBrush(QColor("#D62828"))

                painter.drawPolygon(QPolygonF([
                    QPointF(31, 23),
                    QPointF(48, 0),
                    QPointF(72, 10),
                    QPointF(66, 23)
                ]))

                painter.setBrush(QColor("#FFFFFF"))

                painter.drawRoundedRect(
                    QRectF(29, 18, 42, 8), 4, 4
                )

                painter.drawEllipse(
                    QRectF(67, 5, 10, 10)
                )

            # Плетена шапка
            elif self.design == 2:

                painter.setBrush(QColor("#1565C0"))

                painter.drawRoundedRect(
                    QRectF(32, 3, 36, 23), 12, 12
                )

                painter.drawEllipse(
                    QRectF(44, 0, 12, 12)
                )

                painter.setBrush(QColor("#64B5F6"))

                painter.drawRoundedRect(
                    QRectF(30, 18, 40, 8), 3, 3
                )

            # Зимни слушалки
            elif self.design == 3:

                painter.setPen(
                    QPen(QColor("#7B1FA2"), 4)
                )

                painter.drawArc(
                    QRectF(31, 14, 38, 30),
                    0, 180 * 16
                )

                painter.setPen(Qt.PenStyle.NoPen)
                painter.setBrush(QColor("#AB47BC"))

                painter.drawEllipse(
                    QRectF(26, 29, 12, 15)
                )

                painter.drawEllipse(
                    QRectF(62, 29, 12, 15)
                )

            # Каубойска шапка
            elif self.design == 4:

                painter.setBrush(QColor("#795548"))

                painter.drawRoundedRect(
                    QRectF(35, 3, 30, 22), 6, 6
                )

                painter.drawEllipse(
                    QRectF(21, 17, 58, 10)
                )

                painter.setBrush(QColor("#D49B35"))

                painter.drawRect(
                    QRectF(35, 14, 30, 4)
                )

    def mousePressEvent(self, event):

        if event.button() == Qt.MouseButton.LeftButton:

            self.drag_position = (
                event.globalPosition().toPoint()
                - self.frameGeometry().topLeft()
            )

            self.setCursor(
                Qt.CursorShape.ClosedHandCursor
            )

    def mouseMoveEvent(self, event):

        if (
            self.drag_position is not None
            and event.buttons() & Qt.MouseButton.LeftButton
        ):

            self.move(
                event.globalPosition().toPoint()
                - self.drag_position
            )

    def mouseReleaseEvent(self, event):

        self.drag_position = None

        self.setCursor(
            Qt.CursorShape.OpenHandCursor
        )

    def change_scarf(self, color):

        self.scarf_color = color
        self.update()

    def toggle_hat(self):

        self.hat_enabled = not self.hat_enabled
        self.update()

    def contextMenuEvent(self, event):

        menu = QMenu(self)

        scarf_menu = menu.addMenu("Цвят на шала")

        colors = {
            "Червен": "#C62828",
            "Зелен": "#2E7D32",
            "Син": "#1565C0",
            "Лилав": "#7B1FA2",
            "Розов": "#EC407A"
        }

        for name, color in colors.items():

            action = scarf_menu.addAction(name)

            action.triggered.connect(
                lambda checked=False, c=color:
                self.change_scarf(c)
            )

        menu.addAction(
            "Постави / махни шапката",
            self.toggle_hat
        )

        menu.addAction(
            "Премахни снежния човек",
            self.close
        )

        design_menu = menu.addMenu("Дизайн")

        designs = [
            "Класически",
            "Коледен",
            "Зимен",
            "Слушалки",
            "Каубой"
        ]

        for index, name in enumerate(designs):

            action = design_menu.addAction(name)

            action.triggered.connect(
                lambda checked=False, i=index:
                self.set_design(i)
            )

        menu.exec(event.globalPos())