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

This is a semiformal declarative language DSL, although there is symbols the names and descriptions must be interpreted and adapted to create a functional application. A sequence of expressions in DSL which describe the logic of a program or component is called DSL Logic. A DSL Logic has a starting line called head and a sequence of directives called logical paths. 
1. N. with N as a number, or ->, this is an annotation for the start of a logical path. 
2. [ Name or Application Description ], this part resumes the objetive of the DSL Logic.
3. { Context of Application }, this part along with the objective is called the head of DSL Logic.
4. X := Description, the operator := indicates that X is a shorter alias for a larger description. 
5. X ~ Y, means that X is an event or task and Y is a declarative expression of how the event should be processed. 
6. X || Y means that Y is inside the structure of X, is in his scope. 
7. X | Y means that X and Y stands in the same scope (structure) and Y is performed after X. 
8. & X, means that X is an repetition structure. 
9. & (type) X, is a refinement of the above directive, it indicates the type of element of iteration in parenthesis.
10. X (), denote that X is a function or a task. If it is an actual function depends of implementation. 
11. X ()!, denote that it's a function declaration.
12. X ()?, denote that it's a function definition.
13. X ()*, denote that it's a function call.
14. (type) = X (arg), is to specify the argument and returning type of the function with X name or description. 
15. % X, denote that X belongs to an conditional structure (if-elseif-else) or a switch structure.
16. $ X, denotes that X is a directive for construction of a variable. If it is a declaration or definition (initialization) is to be decided by the A.I.
17. $ (type) X, is a refinement of the previous directive, the parenthesis indicates the type informal or formal description and X indicates the variable name or description. 
18. $! X, indicates that this is just a declaration.
19. $? X, indicates that this is a definition.
20. $* X, indicates that this part modifies, or update the value of this variable. 
21. X {}, denotes that X is a class structure.
22. X {}!, denotes that X is a declaration of class X.
23. X {}?, denotes that X is a definition of class X.
24. X : Y {}, denotes that X is a class derived from Y.
25. ... , used to hide parts from the declarative statement which can be deduced from the previous statements. 
26. /filename, denotes a file or a module, /filename || X means that X should be on the appropriate file.
27. ?, means that should be completed by the A.I. 
28. A declaration can be assigned to multiple descriptions, for example: 'X,Y || Z' is the same as 'X || Z' followed by another logical path 'X | Y || Z' and Z should be smartly interpreted for X and for Y, they don't need to be the same.
29. The same concept is valid for '% X,Y || Z' which means '% X || Z' followed by '% X | % Y || Z' .
30. Logical Path { Context }, a context can be used in the end of a Logical Path. It's used to tell the A.I. to use specific library functions or to tell things that don't fit with DSL formalism. 
Explains step-by-step the creation of the application. 
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








