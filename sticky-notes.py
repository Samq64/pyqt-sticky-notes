#!/usr/bin/env python3

import sys
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QKeySequence, QShortcut
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QGridLayout, QFileDialog, QPushButton, QPlainTextEdit, QSizeGrip



class Note(QMainWindow):
    def __init__(self, win, x, y):
        super().__init__()
        
        self.winid = win
        self.setWindowFlags(Qt.FramelessWindowHint|Qt.WindowStaysOnTopHint|Qt.Tool)
        self.setGeometry(x, y, 200, 200)
        self.setMinimumSize(100, 100)
        self.setMaximumSize(1000, 1000)
        self.setAutoFillBackground(True)
        self.setStyleSheet('background-color: #ffffa5;')
        
        self.window = QWidget(self)
        self.setCentralWidget(self.window)
        self.layout = QGridLayout()
        self.layout.setContentsMargins(0,0,0,0)
        self.layout.setSpacing(0)
        self.window.setLayout(self.layout)
        
        self.newButton = QPushButton('+', self)
        self.newButton.setStyleSheet("border: 0px; padding :5px; color: #505050;")
        self.newButton.clicked.connect(self.new_note)
        self.newButton.setFont(QFont('new times roman', 12))
        self.layout.addWidget(self.newButton, 0, 0, alignment=Qt.AlignLeft)
        
        self.closeButton = QPushButton('×', self)
        self.closeButton.setStyleSheet("border: 0px; padding :5px; color: #505050;")
        self.closeButton.clicked.connect(self.close_window)
        self.closeButton.setFont(QFont('new times roman', 12))
        self.layout.addWidget(self.closeButton, 0, 1, alignment=Qt.AlignRight)
        
        self.note = QPlainTextEdit(self)
        self.note.setStyleSheet('border: 0px; background-color: #ffffd2; color: #505050;')
        self.note.setFont(QFont('new times roman', 12))
        self.layout.addWidget(self.note, 1, 0, 1, 2)
        
        self.gripper = QSizeGrip(self)
        self.layout.addWidget(self.gripper, 1, 1, Qt.AlignBottom | Qt.AlignRight)
        
        self.open_shortcut = QShortcut(QKeySequence("Ctrl+O"), self)
        self.open_shortcut.activated.connect(self.open_file)
        
        self.save_shortcut = QShortcut(QKeySequence("Ctrl+S"), self)
        self.save_shortcut.activated.connect(self.save_file)
        
        self.show()


    def open_file(self):
        path = QFileDialog.getOpenFileName(self, "Open file", "", "Text documents (*.txt);;All files (*.*)")[0]
        if not path:
            return
        with open(path, 'r') as f:
            text = f.read()
            self.note.setPlainText(text)


    def save_file(self):
        path = QFileDialog.getSaveFileName(self, "Save file", "", "Text documents (*.txt);;All files (*.*)")[0]
        if not path:
            return
        text = self.note.toPlainText()
        with open(path, 'w') as f:
            f.write(text)


    def new_note(self):
        p = self.frameGeometry()
        new_window(p.x()+50, p.y()+50)


    def close_window(self, winid):
        wins[self.winid] = None
        if not any(wins):
            sys.exit()


    def mousePressEvent(self, e):
        if e.button() == Qt.LeftButton:
            self.windowHandle().startSystemMove()
        return super().mousePressEvent(e)



def new_window(x, y):
    wins.append(Note(len(wins), x, y))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    wins = []
    new_window(50, 50)
    app.exec()

