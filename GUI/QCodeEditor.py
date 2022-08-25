#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
-------------------------------------------------------------------------------
@Name:   QCodeEditor.py
@Desc:     
@Author: yuliang.li@zoom.us
@Create: 2022-08-25  10:56
@Change: 2022-08-25
-------------------------------------------------------------------------------
"""
from PyQt5.QtCore import Qt, QSize, QRect, QPoint
from PyQt5.QtGui import QWheelEvent, QColor, QTextFormat, QPainter, QKeyEvent, QMouseEvent, \
    QTextCursor, QFont
from PyQt5.QtWidgets import QWidget, QPlainTextEdit, QTextEdit


# class QLineNumberArea(QWidget):
#     def __init__(self, editor):
#         super().__init__(editor)
#         self.codeEditor = editor
#
#     def sizeHint(self):
#         return QSize(self.editor.lineNumberAreaWidth(), 0)
#
#     def paintEvent(self, event):
#         self.codeEditor.lineNumberAreaPaintEvent(event)
#
#
# class QCodeEditor(QPlainTextEdit):
#     def __init__(self, parent=None):
#         super().__init__(parent)
#         self.lineNumberArea = QLineNumberArea(self)
#         self.document().blockCountChanged.connect(self.updateLineNumberAreaWidth)
#         # self.updateRequest.connect(self.updateLineNumberArea)
#         self.document().cursorPositionChanged.connect(self.highlightCurrentLine)
#         self.verticalScrollBar().sliderMoved.connect(self.scrollEvent)
#         self.updateLineNumberAreaWidth(0)
#
#     def scrollEvent(self, event: QWheelEvent = None):
#         self.lineNumberArea.update()
#
#     def lineNumberAreaWidth(self):
#         digits = 1
#         max_value = max(1, self.blockCount())
#         while max_value >= 10:
#             max_value /= 10
#             digits += 1
#         space = 3 + self.fontMetrics().width('9') * digits
#         return space
#
#     def updateLineNumberAreaWidth(self, _):
#         self.setViewportMargins(self.lineNumberAreaWidth(), 0, 0, 0)
#
#     def updateLineNumberArea(self, rect, dy):
#         if dy:
#             self.lineNumberArea.scroll(0, dy)
#         else:
#             self.lineNumberArea.update(0, rect.y(), self.lineNumberArea.width(), rect.height())
#         if rect.contains(self.viewport().rect()):
#             self.updateLineNumberAreaWidth(0)
#
#     def resizeEvent(self, event):
#         super().resizeEvent(event)
#         cr = QPlainTextEdit().contentsRect()
#         self.lineNumberArea.setGeometry(QRect(cr.left(), cr.top(), self.lineNumberAreaWidth(), cr.height()))
#
#     def highlightCurrentLine(self):
#         extraSelections = []
#         if not self.isReadOnly():
#             selection = QTextEdit.ExtraSelection()
#             lineColor = QColor(Qt.yellow).lighter(160)
#             selection.format.setBackground(lineColor)
#             selection.format.setProperty(QTextFormat.FullWidthSelection, True)
#             selection.cursor = self.textCursor()
#             selection.cursor.clearSelection()
#             extraSelections.append(selection)
#         self.setExtraSelections(extraSelections)
#
#     def lineNumberAreaPaintEvent(self, event):
#         painter = QPainter(self.lineNumberArea)
#
#         painter.fillRect(event.rect(), Qt.lightGray)
#
#         block = self.firstVisibleBlock()
#         blockNumber = block.blockNumber()
#         top = self.blockBoundingGeometry(block).translated(self.contentOffset()).top()
#         bottom = top + self.blockBoundingRect(block).height()
#
#         # Just to make sure I use the right font
#         height = self.fontMetrics().height()
#         while block.isValid() and (top <= event.rect().bottom()):
#             if block.isVisible() and (bottom >= event.rect().top()):
#                 number = str(blockNumber + 1)
#                 painter.setPen(Qt.black)
#                 painter.drawText(0, top, self.lineNumberArea.width(), height, Qt.AlignRight, number)
#
#             block = block.next()
#             top = bottom
#             bottom = top + self.blockBoundingRect(block).height()
#             blockNumber += 1


class LineNumPaint(QWidget):
    def __init__(self, editor):
        super().__init__(editor)
        self.editor = editor

    def sizeHint(self):
        return QSize(self.editor.lineNumberAreaWidth(), 0)

    def paintEvent(self, event):
        self.editor.lineNumberAreaPaintEvent(event)


class QCodeEditor(QPlainTextEdit):

    def __init__(self, parent=None):
        super().__init__(parent)
        # self.setLineWrapMode(QPlainTextEdit.NoWrap)  # 不自动换行
        self.lineNumberArea = LineNumPaint(self)

        self.document().blockCountChanged.connect(self.updateLineNumWidth)
        self.document().cursorPositionChanged.connect(self.highlightCurrentLine)    # 高亮当前行
        self.verticalScrollBar().sliderMoved.connect(self.scrollEvent)  # 滚动条移动更新行号
        self.updateLineNumWidth()

    def wheelEvent(self, d: QWheelEvent) -> None:
        self.scrollEvent(d)
        super().wheelEvent(d)

    def scrollEvent(self, event: QWheelEvent = None):
        self.lineNumberArea.update()

    def keyPressEvent(self, e: QKeyEvent) -> None:
        super().keyPressEvent(e)
        self.lineNumberArea.update()

    def mousePressEvent(self, e: QMouseEvent) -> None:
        super().mousePressEvent(e)
        self.update()
        self.highlightCurrentLine()

    def lineNumberAreaWidth(self):
        block_count = self.document().blockCount()
        max_value = max(1, block_count)
        d_count = len(str(max_value))
        _width = self.fontMetrics().width('9') * d_count + 5
        return _width

    def updateLineNumWidth(self):
        self.setViewportMargins(self.lineNumberAreaWidth(), 0, 0, 0)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        cr = self.contentsRect()
        self.lineNumberArea.setGeometry(QRect(cr.left(), cr.top(), self.lineNumberAreaWidth(), cr.height()))

    def highlightCurrentLine(self):
        extraSelections = []
        if not self.isReadOnly():
            selection = QTextEdit.ExtraSelection()
            lineColor = QColor(Qt.blue).lighter(190)
            selection.format.setBackground(lineColor)
            selection.format.setProperty(QTextFormat.FullWidthSelection, True)
            selection.cursor = self.textCursor()
            selection.cursor.clearSelection()
            extraSelections.append(selection)
        self.setExtraSelections(extraSelections)

    def lineNumberAreaPaintEvent(self, event):
        cursor = QTextCursor(self.document())
        painter = QPainter(self.lineNumberArea)

        painter.fillRect(event.rect(), Qt.lightGray)
        line_height = self.fontMetrics().lineSpacing()  # 包含行间距的行高

        block_number = self.cursorForPosition(QPoint(0, int(line_height / 2))).blockNumber()
        first_visible_block = self.document().findBlock(block_number)
        blockNumber = block_number
        cursor.setPosition(self.cursorForPosition(QPoint(0, int(line_height / 2))).position())
        rect = self.cursorRect()
        scroll_compensation = rect.y() - int(rect.y() / line_height) * line_height
        top = scroll_compensation
        last_block_number = self.cursorForPosition(QPoint(0, self.height() - 1)).blockNumber()

        height = self.fontMetrics().height()
        block = first_visible_block
        while block.isValid() and (top <= event.rect().bottom()) and blockNumber <= last_block_number:
            # cur_line_count = block.lineCount()
            if block.isVisible():
                number = str(blockNumber + 1)
                painter.setPen(Qt.black)
                # print((0, top, self.lineNumberArea.width(), height), number)
                painter.drawText(0, top, self.lineNumberArea.width(), height, Qt.AlignCenter, number)
            block = block.next()
            top = top + line_height
            blockNumber += 1

    # def lineNumberAreaPaintEvent(self, event):
    #     painter = QPainter(self.lineNumberArea)
    #
    #     painter.fillRect(event.rect(), Qt.lightGray)
    #
    #     block = self.firstVisibleBlock()
    #     blockNumber = block.blockNumber()
    #     top = self.blockBoundingGeometry(block).translated(self.contentOffset()).top()
    #     bottom = top + self.blockBoundingRect(block).height()
    #
    #     # Just to make sure I use the right font
    #     height = self.fontMetrics().height()
    #     while block.isValid() and (top <= event.rect().bottom()):
    #         if block.isVisible() and (bottom >= event.rect().top()):
    #             number = str(blockNumber + 1)
    #             painter.setPen(Qt.black)
    #             painter.drawText(0, top, self.lineNumberArea.width(), height, Qt.AlignRight, number)
    #
    #         block = block.next()
    #         top = bottom
    #         bottom = top + self.blockBoundingRect(block).height()
    #         blockNumber += 1
