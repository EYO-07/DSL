""" DSL Logic ( see DSL prompt engineering paradigm in https://github.com/EYO-07/DSL )
[ Side Panel ] { Qt, Python, The Application is a Windows Desktop Side Panel in Right Part of the Screen, Translucent 60 percent } 
I := Imports 
A := Main Application Object 
C := Main Window Creation /QtSidePanel_Grok.pyw || I | A | C | Show Window | Start Event Loop 
-> A || $ (QApplication) App 
-> C || $ (QMainWindow) MainWindow | Set title "Side Panel App" | Set Black Background | Set White Text | $ (IconListView) list_view || list_view occupy the client area { The Height of Application must be 65 percent of screen height } 
IconListView : QListView {}? || ... | Right Mouse Button Handle () | Keydown Handle () 
-> IconListView : QListView {}? || ... | Right Mouse Button Handle () || Open a Dialog to Search for any files or applications | % Selected a File or Application with Dialog || Add an Icon Image to this list view | Adjust the Height to the Listview making more compact 
-> IconListView : QListView {}? || ... | Right Mouse Button Handle () | Keydown Handle () || % escape pressed || % Confirmation Dialog || exit properly the program 
-> IconListView : QListView {}? || ... | Right Mouse Button Handle () | Keydown Handle () || % escape pressed | % delete pressed || remove selected itens from listview 
-> IconListView : QListView {}? || ... | Right Mouse Button Handle () | Keydown Handle () || % escape pressed | % delete pressed || remove selected itens from listview 
Double Click on Item of Listview ~ Execute the Application or Open the File with Default Application 
"""

# File: QtSidePanel_Grok.pyw

# I: Imports
from PyQt5.QtWidgets import (
    QApplication, QWidget, QListView, QVBoxLayout, QFileDialog, QFileIconProvider, QMessageBox
)
from PyQt5.QtCore import Qt, QSize, QFileInfo
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QIcon
from PyQt5.QtGui import QScreen
import os

# IconListView : QListView {}?
class IconListView(QListView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setViewMode(QListView.IconMode)  # Display as icons
        self.setGridSize(QSize(64, 64))  # Compact icons
        self.setFlow(QListView.TopToBottom)  # Vertical arrangement
        self.setResizeMode(QListView.Adjust)
        self.setMovement(QListView.Static)  # Prevent rearranging
        self.setStyleSheet("background-color: black; color: white;")  # Black background, white text
        self.setContextMenuPolicy(Qt.CustomContextMenu)  # Enable right-click
        self.setSelectionMode(QListView.ExtendedSelection)  # Allow multiple selection

        # Set up model for icons
        self.model = QStandardItemModel(self)
        self.setModel(self.model)

        # Icon provider for file icons
        self.icon_provider = QFileIconProvider()

        # Connect model changes to height adjustment (only for insertions)
        self.model.rowsInserted.connect(self.adjust_window_height)

    def mousePressEvent(self, event):
        # Right Mouse Button Handle ()
        if event.button() == Qt.RightButton:
            self.open_file_dialog()
        else:
            super().mousePressEvent(event)

    def mouseDoubleClickEvent(self, event):
        # Double Click on Item of Listview ~ Execute the Application or Open the File with Default Application
        if event.button() == Qt.LeftButton:
            index = self.indexAt(event.pos())
            if index.isValid():
                item = self.model.itemFromIndex(index)
                file_path = item.data(Qt.UserRole)  # Get full path
                if file_path:
                    os.startfile(file_path)  # Open file with default app
        super().mouseDoubleClickEvent(event)

    def open_file_dialog(self):
        # Open a Dialog to Search for any files or applications
        dialog = QFileDialog(self)
        dialog.setFileMode(QFileDialog.ExistingFile)
        dialog.setNameFilter("Executables (*.exe);;All Files (*)")
        if dialog.exec_():
            # % Selected a File or Application with Dialog || Add an Icon Image to this list view
            selected_files = dialog.selectedFiles()
            if selected_files:
                file_path = selected_files[0]
                # Create QFileInfo from file path
                file_info = QFileInfo(file_path)
                # Extract icon using QFileInfo
                icon = self.icon_provider.icon(file_info)
                item = QStandardItem(os.path.basename(file_path))  # Use file name as text
                item.setIcon(icon)
                item.setData(file_path, Qt.UserRole)  # Store full path
                self.model.appendRow(item)
                # Adjust the Height to the Listview making more compact (handled by signal)

    def keyPressEvent(self, event):
        # Keydown Handle () || % escape pressed | % delete pressed
        if event.key() == Qt.Key_Escape:
            # % escape pressed || % Confirmation Dialog || exit properly the program
            reply = QMessageBox.question(
                self,
                "Confirm Exit",
                "Are you sure you want to exit?",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No
            )
            if reply == QMessageBox.Yes:
                QApplication.quit()
        elif event.key() == Qt.Key_Delete:
            # % delete pressed || remove selected itens from listview
            selected = self.selectedIndexes()
            for index in sorted(selected, reverse=True):  # Reverse to avoid index shifting
                self.model.removeRow(index.row())
        else:
            super().keyPressEvent(event)

    def adjust_window_height(self):
        # Adjust the Height to the Listview making more compact
        screen = QApplication.primaryScreen().geometry()
        max_height = int(screen.height() * 0.65)  # Max 65% of screen
        if self.model.rowCount() > 0:
            # Non-empty: compact height based on items
            item_height = self.gridSize().height()  # 64px per item
            padding = 50  # Small padding
            compact_height = self.model.rowCount() * item_height + padding
            # Cap at max_height
            new_height = min(compact_height, max_height)
            self.window().setFixedHeight(new_height)

# A: Main Application Object
# -> A || $ (QApplication) App 
App = QApplication([])

# C: Main Window Creation
# -> C || $ (QMainWindow) MainWindow | Set title "Side Panel App" | Set Black Background | Set White Text | $ (IconListView) list_view || list_view occupy the client area
MainWindow = QWidget()  # Use QWidget for dock-like side panel
# Configure window as a side panel
MainWindow.setWindowFlags(
    Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool
)  # No frame, always on top, tool window
MainWindow.setWindowTitle("Side Panel App")
MainWindow.setStyleSheet("background-color: black;")  # Black background
MainWindow.setWindowOpacity(0.6)  # Translucent 60%

# Set size and position (dock to right edge)
screen = App.primaryScreen().geometry()
panel_width = 80  # Narrow width
panel_height = int(screen.height() * 0.65)  # 65% of screen height
MainWindow.setFixedSize(panel_width, panel_height)
MainWindow.move(screen.width() - panel_width, (screen.height() - panel_height) // 2)  # Right edge, centered vertically

# Create IconListView
list_view = IconListView()

# Set up layout to make list_view occupy the client area
layout = QVBoxLayout(MainWindow)
layout.setContentsMargins(0, 0, 0, 0)  # No margins
layout.addWidget(list_view)

# Show Window
MainWindow.show()

# Start Event Loop
App.exec_()








