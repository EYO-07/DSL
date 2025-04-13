""" DSL Logic ( see DSL prompt engineering paradigm in https://github.com/EYO-07/DSL )
[ Side Panel ] { PyQt5, QFileIconProvider } 
I := Imports 
G := Global Variables
A := Main Application Object 
C := Main Window Creation 
1. /QtSidePanel.pyw || I | A | C | Show Window | Start Event Loop 
-> A || $ (QApplication) App 
-> C || $ (QMainWindow) MainWindow | Set Black Background | Set White Text | Set Oppaccity 60 percent | Set Window as a Side Panel at Right Part of the Desktop Screen | Center Vertically to the Screen | The Height of Application must be 65 percent of screen height | The width must be the size of icon plus some padding | $ (IconListView) list_view 
-> ... $ (IconListView) list_view || list_view occupy all the client area 
2. IconListView : QListView {} || $ (list of strings) visible_items_file_path | $ (list of strings) items_file_path | $ (string) filter | init () | Keydown Handle () | Context Menu Event Handle () | Update Visible Icons () | Process Action () | Search for File or App () | Apply Filter () | Save () | Load () 
-> Save () || save items_file_path on current executable directory as lines of the file "QtSidePanel.sav" 
-> Load () || % QtSidePanel.sav exists || load items_file_path with the lines of this file 
-> Load () || % QtSidePanel.sav exists | % else || create an empty file 
-> ... init () || ... | $* filter || empty string 
-> ... init () || ... | $* filter | Load ()* | Update Visible Icons ()* 
3. Context Menu Event Handle () || Create Menu | Add Action "Select File or Application" | Add Action "Apply Filter" | Process Action ()* 
4. Search for File or App () || Open a Dialog to Search for any files or applications | % Selected a File or Application with Dialog || Add full path to items_file_path | Update Visible Icons ()* 
5. Apply Filter () || Open a Input Dialog with display text "Apply Filter" | % If the text is a valid regexp || update filter | Update Visible Icons ()* 
6. Process Action () || $ action | % action is "Select File or Application" | % action is "Apply Filter" 
-> Process Action () || $ action | % action is "Select File or Application" || Search for File or App ()* 
-> Process Action () || $ action | % action is "Select File or Application" | % action is "Apply Filter" || Apply Filter ()* 
7. Update Visible Icons () || % filter not empty string || create regexp object | & element in visible_items_file_path || remove elements that don't match 
7. Update Visible Icons () || % filter not empty string || create regexp object | & element in visible_items_file_path | update the list_view with icons of visible_items_file_path 
8. Keydown Handle () || % escape pressed || % Confirmation Dialog || Save ()* | exit properly the program 
-> Keydown Handle () || % escape pressed | % delete pressed || remove selected item file path of items_file_path | Update Visible Icons ()* 
9. Double Click on Item of Listview ~ Execute the App or File of the Item 
"""

import sys
import os
import re
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QListView, QVBoxLayout, QWidget,
    QMenu, QAction, QFileDialog, QInputDialog, QMessageBox, QFileIconProvider
)
from PyQt5.QtGui import QIcon, QStandardItemModel, QStandardItem
from PyQt5.QtCore import Qt, QRect, QSize, QFileInfo

# Global Variables
screen_geometry = None
icon_provider = QFileIconProvider()

class IconListView(QListView):
    def __init__(self):
        super().__init__()
        self.filter = ""
        self.items_file_path = []  # All file paths
        self.visible_items_file_path = []  # Filtered file paths
        self.model = QStandardItemModel()
        self.setModel(self.model)
        self.setViewMode(QListView.IconMode)
        self.setFlow(QListView.TopToBottom)
        self.setResizeMode(QListView.Adjust)
        self.setSelectionMode(QListView.ExtendedSelection)  # Allow multiple selection
        self.init_ui()
        self.doubleClicked.connect(self.execute_item)

    def init_ui(self):
        self.setGridSize(QSize(64, 64))  # Compact icons
        self.setMovement(QListView.Static)
        self.setEditTriggers(QListView.NoEditTriggers)
        self.filter = ""
        self.load()  # Load saved paths
        self.update_visible_icons()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            reply = QMessageBox.question(
                self, "Confirm Exit", "Do you want to exit?",
                QMessageBox.Yes | QMessageBox.No, QMessageBox.No
            )
            if reply == QMessageBox.Yes:
                self.save()  # Save before exit
                QApplication.quit()
        elif event.key() == Qt.Key_Delete:
            selected = self.selectedIndexes()
            for index in sorted(selected, reverse=True):
                if index.row() < len(self.visible_items_file_path):
                    path = self.visible_items_file_path[index.row()]
                    if path in self.items_file_path:
                        self.items_file_path.remove(path)
            self.update_visible_icons()
        super().keyPressEvent(event)

    def contextMenuEvent(self, event):
        menu = QMenu(self)
        select_action = QAction("Select File or Application", self)
        filter_action = QAction("Apply Filter", self)
        menu.addAction(select_action)
        menu.addAction(filter_action)
        select_action.triggered.connect(self.search_file_or_app)
        filter_action.triggered.connect(self.apply_filter)
        menu.exec_(event.globalPos())

    def search_file_or_app(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select File or Application",
            "", "All Files (*);;Executables (*.exe *.py *.sh)"
        )
        if file_path and file_path not in self.items_file_path:
            self.items_file_path.append(file_path)
            self.update_visible_icons()

    def apply_filter(self):
        text, ok = QInputDialog.getText(
            self, "Apply Filter", "Enter filter (regexp):",
            text=self.filter
        )
        if ok:
            try:
                re.compile(text)  # Validate regex
                self.filter = text
                self.update_visible_icons()
            except re.error:
                QMessageBox.warning(self, "Invalid Filter", "Please enter a valid regular expression.")

    def update_visible_icons(self):
        # Update visible_items_file_path based on filter
        if self.filter:
            try:
                regex = re.compile(self.filter)
                self.visible_items_file_path = [
                    path for path in self.items_file_path
                    if regex.search(os.path.basename(path))
                ]
            except re.error:
                self.filter = ""
                self.visible_items_file_path = self.items_file_path.copy()
        else:
            self.visible_items_file_path = self.items_file_path.copy()

        # Refresh the model with icons
        self.model.clear()
        for path in self.visible_items_file_path:
            if not os.path.exists(path):
                continue
            # Create QFileInfo from file path
            file_info = QFileInfo(path)
            # Extract icon using QFileInfo
            icon = icon_provider.icon(file_info)
            item = QStandardItem(os.path.basename(path))  # Use file name as text
            item.setIcon(icon)
            item.setData(path, Qt.UserRole)  # Store full path    
            self.model.appendRow(item)

    def execute_item(self, index):
        if index.isValid():
            file_path = self.model.itemFromIndex(index).data(Qt.UserRole)
            if os.path.exists(file_path):
                try:
                    os.startfile(file_path)
                except OSError:
                    QMessageBox.warning(self, "Error", f"Cannot open {file_path}")

    def save(self):
        try:
            with open("QtSidePanel.sav", "w", encoding="utf-8") as f:
                for path in self.items_file_path:
                    f.write(path + "\n")
        except IOError:
            QMessageBox.warning(self, "Error", "Failed to save QtSidePanel.sav")

    def load(self):
        self.items_file_path.clear()
        try:
            if os.path.exists("QtSidePanel.sav"):
                with open("QtSidePanel.sav", "r", encoding="utf-8") as f:
                    self.items_file_path = [line.strip() for line in f if line.strip() and os.path.exists(line.strip())]
            else:
                with open("QtSidePanel.sav", "w", encoding="utf-8") as f:
                    pass  # Create empty [Side Panel] empty file
        except IOError:
            QMessageBox.warning(self, "Error", "Failed to load QtSidePanel.sav")

class SidePanel(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Side Panel")
        self.setStyleSheet("background-color: black; color: white;")
        self.setWindowOpacity(0.6)

        global screen_geometry
        screen_geometry = QApplication.desktop().availableGeometry()
        screen_width = screen_geometry.width()
        screen_height = screen_geometry.height()
        panel_height = int(screen_height * 0.65)
        icon_size = 75
        padding = 0
        panel_width = icon_size + padding * 2

        x = screen_width - panel_width
        y = (screen_height - panel_height) // 2
        self.setGeometry(x, y, panel_width, panel_height)

        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(padding, padding, padding, padding)

        self.list_view = IconListView()
        layout.addWidget(self.list_view)

def main():
    app = QApplication(sys.argv)
    window = SidePanel()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
    
    
    
    
    
    
    
    







