#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
-------------------------------------------------------------------------------
@Name：  MainWindow.py
@Desc:
@Author: liangz.org@gmail.com
@Create: 2022.08.24  13:09
@Change: 2022.08.25
-------------------------------------------------------------------------------
"""
from PyQt5 import QtGui
from PyQt5.QtCore import QRect, Qt, QPoint, QSize
from PyQt5.QtGui import QWheelEvent, QKeyEvent, QMouseEvent, QColor, QTextFormat, QTextCursor, \
    QPainter
from PyQt5.QtWidgets import QMainWindow, QTextEdit, QWidget, QPlainTextEdit

from .UI_MainWindow import Ui_MainWindow


class MainWidget(QMainWindow):

    def __init__(self, parent=None):
        super(MainWidget, self).__init__(parent)
        self.mainWindow = Ui_MainWindow()
        self.mainWindow.setupUi(self)
        self.initialize()

    def initialize(self):
        self.mainWindow.pushButtonTrans.clicked.connect(self.clickTransBtn)
        pass

    def clickTransBtn(self):
        original = self.mainWindow.plainTextEditSource.toPlainText()
        res = self.handleTextInput(original)
        self.mainWindow.plainTextEditTarget.setPlainText(res)

    @staticmethod
    def handleTextInput(text: str) -> str:
        res = []
        text = text.strip().split('\n')
        for i in text:
            i = i.replace("FAILED", "").strip()
            i = i.replace("ERROR", "").strip()
            res.append(i)
        return ','.join(res)


