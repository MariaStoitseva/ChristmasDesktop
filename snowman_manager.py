from PySide6.QtWidgets import QApplication

from snowman import Snowman
from snowball import Snowball


class SnowmanManager:

    def __init__(self, snowballs, ground_y):

        self.snowballs = snowballs
        self.snowmen = []
        self.ground_y = ground_y

        self.max_snowmen = 5
        self.design_index = 0

    def spawn_snowballs(self):

        self.snowmen = [
            man for man in self.snowmen
            if man.isVisible()
        ]

        if len(self.snowmen) >= self.max_snowmen:
            return

        if self.snowballs:
            return

        screen = QApplication.primaryScreen().geometry()

        x = screen.x() + screen.width() // 3
        y = screen.y() + self.ground_y

        new_balls = [
            Snowball(65, x, y - 65),
            Snowball(45, x + 90, y - 45),
            Snowball(30, x + 160, y - 30)
        ]

        for ball in new_balls:
            ball.show()

        self.snowballs.extend(new_balls)

    def check(self):

        self.snowmen = [
            man for man in self.snowmen
            if man.isVisible()
        ]

        if len(self.snowmen) >= self.max_snowmen:
            return

        if len(self.snowballs) != 3:
            return

        if any(
            ball.drag_position is not None
            for ball in self.snowballs
        ):
            return

        bottom, middle, top = sorted(
            self.snowballs,
            key=lambda ball: ball.ball_size,
            reverse=True
        )

        if (
            self.is_stacked(middle, bottom)
            and self.is_stacked(top, middle)
        ):

            x = bottom.x() + bottom.width() // 2 - 50
            y = bottom.y() + bottom.height() - 155

            snowman = Snowman(x, y)

            snowman.set_design(self.design_index)
            snowman.show()

            self.design_index = (
                self.design_index + 1
            ) % 5

            self.snowmen.append(snowman)

            for ball in self.snowballs:
                ball.close()

            self.snowballs.clear()

    def is_stacked(self, upper, lower):

        upper_center = upper.x() + upper.width() / 2
        lower_center = lower.x() + lower.width() / 2

        horizontal_distance = abs(
            upper_center - lower_center
        )

        vertical_distance = (
                upper.y() + upper.height() - lower.y()
        )

        return (
                horizontal_distance < 20
                and -10 <= vertical_distance <= 30
                and upper.y() < lower.y()
        )