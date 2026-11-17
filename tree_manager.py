from PySide6.QtWidgets import QApplication

from christmas_tree import ChristmasTree


class TreeManager:

    def __init__(self, overlay):

        self.overlay = overlay
        self.trees = []
        self.max_trees = 3

    def spawn_tree(self):

        self.trees = [
            tree for tree in self.trees
            if tree.isVisible()
        ]

        if len(self.trees) >= self.max_trees:
            return

        screen = (
            QApplication.primaryScreen()
            .geometry()
        )

        x = (
            screen.x()
            + screen.width() // 2
            + len(self.trees) * 190
            - 90
        )

        x = min(x, screen.right() - 179)

        y = (
            screen.y()
            + self.overlay.ground_y
            - 242
        )

        tree = ChristmasTree(
            x,
            y,
            self.overlay
        )

        self.trees.append(tree)

        tree.show()