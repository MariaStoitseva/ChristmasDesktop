from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QGridLayout,
    QFormLayout,
    QLabel,
    QPushButton,
    QCheckBox,
    QComboBox,
    QGroupBox,
    QSpinBox,
    QMessageBox
)

from PySide6.QtCore import Qt

from autostart import (
    is_autostart_enabled,
    set_autostart
)


class SettingsWindow(QDialog):

    def __init__(self, tray):

        super().__init__()

        self.tray = tray
        self.overlay = tray.overlay

        self.setWindowTitle(
            "Christmas Desktop — Настройки"
        )

        self.setFixedSize(500, 700)

        self.setWindowFlags(
            self.windowFlags()
            | Qt.WindowType.WindowStaysOnTopHint
        )

        self.setStyleSheet("""
            QDialog {
                background: #102331;
                color: white;
                font-family: Segoe UI;
                font-size: 13px;
            }

            QLabel {
                color: #EAF6FF;
            }

            QGroupBox {
                color: #B9E3FF;
                font-weight: bold;
                border: 1px solid #36536A;
                border-radius: 10px;
                margin-top: 14px;
                padding-top: 16px;
            }

            QGroupBox::title {
                subcontrol-origin: margin;
                left: 12px;
                padding: 0 6px;
            }

            QCheckBox {
                color: white;
                spacing: 9px;
            }

            QComboBox, QSpinBox {
                background: #20394C;
                color: white;
                border: 1px solid #45647C;
                border-radius: 7px;
                padding: 8px;
            }

            QComboBox QAbstractItemView {
                background: #20394C;
                color: white;
                selection-background-color: #426681;
            }

            QPushButton {
                background: #27485F;
                color: white;
                border: 1px solid #45647C;
                border-radius: 8px;
                padding: 10px;
            }

            QPushButton:hover {
                background: #365F7A;
            }

            QPushButton:pressed {
                background: #173447;
            }
        """)

        layout = QVBoxLayout(self)

        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(12)

        # Заглавие

        title = QLabel("❄ Christmas Desktop")

        title.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        title.setStyleSheet("""
            font-size: 26px;
            font-weight: bold;
            color: #B9E3FF;
        """)

        layout.addWidget(title)

        subtitle = QLabel(
            "Твоето малко зимно царство"
        )

        subtitle.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        layout.addWidget(subtitle)

        # Снеговалеж

        snow_group = QGroupBox("❄ Снеговалеж")

        snow_layout = QVBoxLayout(snow_group)

        self.snow_checkbox = QCheckBox(
            "Показвай падащия сняг и анимациите"
        )

        self.snow_checkbox.toggled.connect(
            self.change_snow_visibility
        )

        snow_layout.addWidget(self.snow_checkbox)

        layout.addWidget(snow_group)

        # Тапети

        wallpaper_group = QGroupBox("Зимен тапет")

        wallpaper_layout = QFormLayout(
            wallpaper_group
        )

        self.wallpaper_combo = QComboBox()

        wallpapers = [
            ("Автоматичен режим", "dynamic"),
            ("Изгрев", "sunrise"),
            ("Ден", "day"),
            ("Залез", "sunset"),
            ("Нощ", "night"),
            ("Оригинален тапет", "original")
        ]

        for name, mode in wallpapers:

            self.wallpaper_combo.addItem(
                name,
                mode
            )

        self.wallpaper_combo.currentIndexChanged.connect(
            self.change_wallpaper
        )

        wallpaper_layout.addRow(
            "Режим:",
            self.wallpaper_combo
        )

        layout.addWidget(wallpaper_group)

        # Анимации

        animation_group = QGroupBox("Анимации")

        animation_layout = QFormLayout(
            animation_group
        )

        self.snowplow_interval = QSpinBox()

        self.snowplow_interval.setRange(30, 600)

        self.snowplow_interval.setSingleStep(30)

        self.snowplow_interval.setSuffix(" сек.")

        self.snowplow_interval.valueChanged.connect(
            self.change_snowplow_interval
        )

        self.train_interval = QSpinBox()

        self.train_interval.setRange(30, 900)

        self.train_interval.setSingleStep(30)

        self.train_interval.setSuffix(" сек.")

        self.train_interval.valueChanged.connect(
            self.change_train_interval
        )

        animation_layout.addRow(
            "Снегорин:",
            self.snowplow_interval
        )

        animation_layout.addRow(
            "Коледно влакче:",
            self.train_interval
        )

        layout.addWidget(animation_group)

        # Декорации

        decoration_group = QGroupBox(
            "Украси своя работен плот"
        )

        decoration_layout = QGridLayout(
            decoration_group
        )

        snowball_button = QPushButton(
            "☃ Нови снежни топки"
        )

        snowball_button.clicked.connect(
            self.tray.spawn_snowballs
        )

        tree_button = QPushButton(
            "🎄 Добави елха"
        )

        tree_button.clicked.connect(
            self.tray.tree_manager.spawn_tree
        )

        plow_button = QPushButton(
            "Извикай снегорина"
        )

        plow_button.clicked.connect(
            self.call_snowplow
        )

        train_button = QPushButton(
            "🚂 Извикай влакчето"
        )

        train_button.clicked.connect(
            self.call_train
        )

        decoration_layout.addWidget(
            snowball_button, 0, 0
        )

        decoration_layout.addWidget(
            tree_button, 0, 1
        )

        decoration_layout.addWidget(
            plow_button, 1, 0
        )

        decoration_layout.addWidget(
            train_button, 1, 1
        )

        layout.addWidget(decoration_group)

        # Автоматично стартиране

        system_group = QGroupBox("Системни настройки")

        system_layout = QVBoxLayout(system_group)

        self.autostart_checkbox = QCheckBox(
            "Стартирай автоматично с Windows"
        )

        self.autostart_checkbox.toggled.connect(
            self.change_autostart
        )

        system_layout.addWidget(
            self.autostart_checkbox
        )

        layout.addWidget(system_group)

        layout.addStretch()

        # Footer

        footer = QLabel("Christmas Desktop • v1.0")

        footer.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        footer.setStyleSheet(
            "color: #7798AF;"
        )

        layout.addWidget(footer)

        close_button = QPushButton("Готово")

        close_button.clicked.connect(self.close)

        close_button.setStyleSheet("""
            QPushButton {
                background: #28734E;
                border: none;
                font-weight: bold;
            }

            QPushButton:hover {
                background: #359061;
            }
        """)

        layout.addWidget(close_button)

        self.refresh()

    def refresh(self):

        widgets = [
            self.snow_checkbox,
            self.wallpaper_combo,
            self.snowplow_interval,
            self.train_interval,
            self.autostart_checkbox
        ]

        for widget in widgets:

            widget.blockSignals(True)

        self.snow_checkbox.setChecked(
            self.overlay.isVisible()
        )

        manager = self.tray.wallpaper_manager

        if manager.dynamic_enabled:

            mode = "dynamic"

        elif manager.current_wallpaper is not None:

            mode = manager.current_wallpaper

        else:

            mode = "original"

        index = self.wallpaper_combo.findData(mode)

        if index >= 0:

            self.wallpaper_combo.setCurrentIndex(index)

        self.snowplow_interval.setValue(
            self.overlay.snowplow_timer.interval()
            // 1000
        )

        self.train_interval.setValue(
            self.overlay.train_timer.interval()
            // 1000
        )

        try:

            self.autostart_checkbox.setChecked(
                is_autostart_enabled()
            )

            self.autostart_checkbox.setEnabled(True)

        except OSError:

            self.autostart_checkbox.setEnabled(False)

        for widget in widgets:

            widget.blockSignals(False)

    def change_snow_visibility(self, checked):

        if checked != self.overlay.isVisible():

            self.tray.toggle_snow()

    def change_wallpaper(self, index):

        mode = self.wallpaper_combo.itemData(index)

        self.tray.select_wallpaper(mode)

    def change_snowplow_interval(self, seconds):

        self.overlay.snowplow_timer.setInterval(
            seconds * 1000
        )

    def change_train_interval(self, seconds):

        self.overlay.train_timer.setInterval(
            seconds * 1000
        )

    def call_snowplow(self):

        if not self.overlay.isVisible():

            self.tray.toggle_snow()

        self.overlay.start_snowplow()

    def call_train(self):

        if not self.overlay.isVisible():

            self.tray.toggle_snow()

        self.overlay.start_train()

    def change_autostart(self, checked):

        try:

            set_autostart(checked)

        except (OSError, ValueError) as error:

            QMessageBox.warning(
                self,
                "Грешка",
                str(error)
            )

            self.refresh()