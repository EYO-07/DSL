""" 
[ Text to Speech GUI ] { pyqt5, gTTS, Black Background, Yellow Text }
I := Imports 
G := Global Variables
Q := Qt Graphical Interface Setup 
1. /QtGTTS.pyw || I | G | Q 
-> G || $ (string) selected_language || Initialize with 'eng' 
-> G || $ (string) selected_language | $ (string) output_filename || Initialize with "output.mp3" 
A := Main Application Object 
C := Main Window Creation 
2. Q || A | C | Show Window | Start Event Loop 
-> A || $ (QApplication) App 
-> C || Set Oppaccity 60 percent | Set Height 60 percent of screen height | Set Width:height to 9:16 | Center Vertically to the Screen | Center Horizontally to Screen | $ (MultilineEdit) edit_control || Set the edit_control to occupy all client area 
3. MultilineEdit : QTextEdit {} || ... | Init () | Context Menu Handle () | Keydown Handle () | Process Context Menu Action () | TextToSpeech () 
-> MultilineEdit : QTextEdit {} || ... | init () || Multiline Edit Control without margin | Without Character Limit 
4. Keydown Handle ()? || % F5 Pressed | $ (string) input_text | TextToSpeech ()* 
-> Keydown Handle ()? || % F5 Pressed | $ (string) input_text || Get the string from the multiline edit 
5. Context Menu Handle ()? || Create a Menu | Add Action "Change Output Filename" | Add Action "Change Output Language" | Add Action "Open Output File" | Process Context Menu Action ()* 
-> Process Context Menu Action () || Get Action | % "Change Output Filename", "Change Output Language" || Input Dialog to Change the Respectives Variables  
-> ... | % "Change Output Filename", "Change Output Language" | % "Open Output File" || # || Open the mp3 file with default application 
-> ... | % "Open Output File" || # | # any exception || display dialog message with the exception 
Io := output_filename is valid mp3 filename 
Gs := Generate the Sound from tts_obj and save to output_filename 
Ms := Display a Pop-up Message Informing the Result 
6. TextToSpeech ()? || $ (gTTS) tts_obj | % Io || # || Gs | Ms 
-> TextToSpeech ()? || $ (gTTS) tts_obj | % Io || # | # can't access file || Input Dialog | Update output_filename with Input Dialog | % Io | # || Gs | Ms 
-> TextToSpeech ()? || $ (gTTS) tts_obj | % Io | % else || Input Dialog | Update output_filename with Input Dialog | % Io | # || Gs | Ms 
-> TextToSpeech ()? || $ (gTTS) tts_obj || Initialize with text from the multiline edit control and selected_language as arguments 

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
31. # denotes a try except blocks.

Explains step-by-step the creation of the application. 
"""

from PyQt5.QtWidgets import (
    QApplication, QWidget, QTextEdit, QVBoxLayout, QInputDialog, QMenu, QAction
)
from PyQt5.QtGui import QColor, QPalette
from PyQt5.QtCore import Qt
from gtts import gTTS
import sys
import os

from PyQt5.QtWidgets import (
    QApplication, QWidget, QTextEdit, QVBoxLayout, QInputDialog, QMenu, QAction, QMessageBox, QProgressDialog
)
from PyQt5.QtGui import QColor, QPalette, QFont
from PyQt5.QtCore import Qt
from gtts import gTTS
import sys

# =========================
# GLOBAL VARIABLES
# =========================
selected_language = 'en'
output_filename = 'output.mp3'
font = QFont("Consolas", 10)

# =========================
# HELPERS
# =========================
def is_valid_mp3(filename):
    return filename.lower().endswith('.mp3')

def show_message(text, title="Info"):
    msg = QMessageBox()
    msg.setWindowTitle(title)
    msg.setText(text)
    msg.exec_()

# =========================
# TEXT-TO-SPEECH CORE FUNCTION
# =========================
def text_to_speech(edit_widget):
    global selected_language, output_filename

    text = edit_widget.toPlainText()
    if not text.strip():
        show_message("Text is empty. Please type something first.")
        return

    if not is_valid_mp3(output_filename):
        filename, ok = QInputDialog.getText(None, "Output Filename", "Enter filename (e.g., audio.mp3):")
        if ok and is_valid_mp3(filename):
            output_filename = filename
        else:
            show_message("Invalid filename. Operation cancelled.")
            return

    progress = QProgressDialog("Generating speech...", None, 0, 0)
    progress.setWindowTitle("Please wait")
    progress.setWindowModality(Qt.ApplicationModal)
    progress.setMinimumDuration(0)
    progress.setCancelButton(None)
    progress.show()

    QApplication.processEvents()  # Force update of progress dialog

    try:
        tts = gTTS(text=text, lang=selected_language)

        try:
            tts.save(output_filename)
            show_message(f"Audio saved as: {output_filename}")
        except Exception as file_error:
            filename, ok = QInputDialog.getText(None, "Save Error", "Could not write to file. Enter new filename:")
            if ok and is_valid_mp3(filename):
                output_filename = filename
                try:
                    tts.save(output_filename)
                    show_message(f"Audio saved as: {output_filename}")
                except Exception as save_retry_error:
                    show_message(f"Failed to save audio again: {save_retry_error}", title="Error")
            else:
                show_message("Invalid filename or cancelled.")

    except Exception as e:
        show_message(f"Text-to-Speech generation failed: {e}", title="Error")

    progress.close()

# =========================
# MAIN GUI WINDOW
# =========================
class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Text-to-Speech with gTTS")

        # Size: 60% of screen height, 9:16 aspect ratio, centered
        screen = QApplication.primaryScreen().size()
        height = int(screen.height() * 0.6)
        width = int(height * 9 / 16)
        self.setFixedSize(width, height)
        self.move((screen.width() - width) // 2, (screen.height() - height) // 2)

        # Appearance: black background, yellow text, 60% opacity
        self.setWindowOpacity(0.7)
        palette = QPalette()
        palette.setColor(QPalette.Base, QColor('black'))
        palette.setColor(QPalette.Text, QColor('yellow'))
        self.setPalette(palette)
        self.setAutoFillBackground(True)

        # QTextEdit: no margins, no character limit
        self.edit = QTextEdit(self)
        self.edit.setStyleSheet("background-color: black; color: yellow; margin: 0px;")
        self.edit.setContextMenuPolicy(Qt.CustomContextMenu)
        self.edit.customContextMenuRequested.connect(self.open_context_menu)
        self.edit.keyPressEvent = self.key_press_event

        # Layout with no margins
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.edit)
        self.setLayout(layout)
        
        self.edit.setFont(font)
        self.edit.setPlainText("This is a minimalist text to speech application using python, pyqt5 and gTTS libraries. \nPress F5 to generate the mp3 file. \nRight-click to access context menu.")

    # Handle F5 key press to trigger TTS
    def key_press_event(self, event):
        if event.key() == Qt.Key_F5:
            text_to_speech(self.edit)
        else:
            QTextEdit.keyPressEvent(self.edit, event)

    # Handle custom context menu
    def open_context_menu(self, position):
        menu = QMenu()

        action_filename = QAction("Change Output Filename", self)
        action_filename.triggered.connect(self.change_output_filename)
        menu.addAction(action_filename)

        action_language = QAction("Change Output Language", self)
        action_language.triggered.connect(self.change_output_language)
        menu.addAction(action_language)
        
        open_file = QAction("Open Output File", self)
        open_file.triggered.connect(self.open_output_file)
        menu.addAction(open_file)

        menu.exec_(self.edit.mapToGlobal(position))

    def change_output_filename(self):
        global output_filename
        filename, ok = QInputDialog.getText(self, "Output Filename", "Enter new filename (e.g., audio.mp3):")
        if ok and is_valid_mp3(filename):
            output_filename = filename
            show_message(f"Output filename updated to: {output_filename}")

    def change_output_language(self):
        global selected_language
        lang, ok = QInputDialog.getText(self, "Language", "Enter language code (e.g., en, pt, es, etc):")
        if ok and lang.strip():
            selected_language = lang.strip()
            show_message(f"Language updated to: {selected_language}")

    def open_output_file(self):
        try:
            if not os.path.exists(output_filename):
                raise FileNotFoundError(f"File '{output_filename}' not found.")

            os.startfile(output_filename)  # Windows
            # For cross-platform support:
            # import platform
            # if platform.system() == "Darwin":
            #     subprocess.call(["open", output_filename])
            # elif platform.system() == "Linux":
            #     subprocess.call(["xdg-open", output_filename])
        except Exception as e:
            show_message(f"Could not open file:\n{e}", title="Error")

# =========================
# MAIN EXECUTION
# =========================
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())









