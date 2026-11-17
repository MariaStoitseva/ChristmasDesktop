from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt, QPoint, QRectF
from PySide6.QtGui import (
    QPainter,
    QColor,
    QRadialGradient
)


class Snowball(QWidget):

    def __init__(self, size, x, y):
        super().__init__()

        self.ball_size = size
        self.drag_position = None

        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint
            | Qt.WindowType.WindowStaysOnTopHint
            | Qt.WindowType.Tool
        )

        self.setAttribute(
            Qt.WidgetAttribute.WA_TranslucentBackground
        )

        self.setFixedSize(size, size)
        self.move(x, y)

        self.setCursor(Qt.CursorShape.OpenHandCursor)

    def paintEvent(self, event):
        painter = QPainter(self)

        painter.setRenderHint(
            QPainter.RenderHint.Antialiasing
        )

        painter.setPen(Qt.PenStyle.NoPen)

        size = self.ball_size

        gradient = QRadialGradient(
            size * 0.35,
            size * 0.3,
            size * 0.8
        )

        gradient.setColorAt(0, QColor("#FFFFFF"))
        gradient.setColorAt(0.5, QColor("#EEF7FF"))
        gradient.setColorAt(1, QColor("#A8C5DC"))

        painter.setBrush(gradient)

        painter.drawEllipse(
            QRectF(1, 1, size - 2, size - 2)
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