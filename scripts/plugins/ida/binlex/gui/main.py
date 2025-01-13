import zlib
import base64
from lib.assets import LOGO
from lib.styles import QPUSHBUTTON_STYLE
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QPushButton, QMainWindow, QWidget
from PyQt5.QtCore import Qt, QRect
from PyQt5.QtGui import QPixmap, QPainter

class Main(QWidget):
    def __init__(self, plugin):
        super().__init__()
        self.plugin = plugin
        self.pixmap = QPixmap()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Binlex')
        self.setFixedSize(300, 300)
        self.setWindowFlags(Qt.Window | Qt.WindowCloseButtonHint | Qt.WindowTitleHint)

        image_data = zlib.decompress(base64.b64decode(LOGO))
        self.pixmap.loadFromData(image_data)

        layout = QVBoxLayout()

        export_database_button = QPushButton('Export Database')
        export_database_button.clicked.connect(self.plugin.action_export)
        export_database_button.setStyleSheet(QPUSHBUTTON_STYLE)
        layout.addWidget(export_database_button)

        index_database_button = QPushButton('Index Database')
        index_database_button.clicked.connect(self.plugin.action_index_database)
        index_database_button.setStyleSheet(QPUSHBUTTON_STYLE)
        layout.addWidget(index_database_button)

        search_database_button = QPushButton('Search Database')
        search_database_button.clicked.connect(self.plugin.action_search_database)
        search_database_button.setStyleSheet(QPUSHBUTTON_STYLE)
        layout.addWidget(search_database_button)

        functions_button = QPushButton('Functions')
        functions_button.clicked.connect(self.plugin.action_function_table)
        functions_button.setStyleSheet(QPUSHBUTTON_STYLE)
        layout.addWidget(functions_button)

        export_byte_colormap_button = QPushButton('Export Byte ColorMap')
        export_byte_colormap_button.clicked.connect(self.plugin.action_export_byte_colormap)
        export_byte_colormap_button.setStyleSheet(QPUSHBUTTON_STYLE)
        layout.addWidget(export_byte_colormap_button)

        json_query_button = QPushButton('JSON Query')
        json_query_button.clicked.connect(self.plugin.action_json_search_window)
        json_query_button.setStyleSheet(QPUSHBUTTON_STYLE)
        layout.addWidget(json_query_button)

        about_button = QPushButton('About')
        about_button.clicked.connect(self.plugin.open_about_window)
        about_button.setStyleSheet(QPUSHBUTTON_STYLE)
        layout.addWidget(about_button)

        self.setLayout(layout)

    def paintEvent(self, event):
        super().paintEvent(event)

        if self.pixmap.isNull():
            return

        painter = QPainter(self)

        widget_width = self.width()
        widget_height = self.height()

        pixmap_width = self.pixmap.width()
        pixmap_height = self.pixmap.height()

        scale_x = widget_width / pixmap_width
        scale_y = widget_height / pixmap_height
        scale = min(scale_x, scale_y)

        new_width = int(pixmap_width * scale)
        new_height = int(pixmap_height * scale)

        x_offset = (widget_width - new_width) // 2
        y_offset = (widget_height - new_height) // 2

        target_rect = QRect(x_offset, y_offset, new_width, new_height)
        painter.drawPixmap(target_rect, self.pixmap, self.pixmap.rect())
