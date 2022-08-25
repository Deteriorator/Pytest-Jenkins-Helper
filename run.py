#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
-------------------------------------------------------------------------------
@Name:   run.py
@Desc:     
@Author: liangz.org@gmail.com
@Create: 2022-08-24  13:14
@Change: 2022-08-24
-------------------------------------------------------------------------------
"""

import sys

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication

from GUI.MainWindow import MainWidget


if __name__ == '__main__':
    app = QApplication(sys.argv)
    # app.setWindowIcon(QIcon(ICON_PATH_PNG))
    widget = MainWidget()
    widget.show()
    sys.exit(app.exec_())
