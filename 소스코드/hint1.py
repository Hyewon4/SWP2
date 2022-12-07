# 남은 횟수가 5회일 때 몇 개 맞췄는지
import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *
from suspect import suspect_list

class Label(QLabel):
    def __init__(self, text, layout, alignment):
        super().__init__()
        self.setText(text)
        layout.addWidget(self, alignment=alignment)

class ComboBox():
    def __init__(self, r, Layout):
        for i in range(len(suspect_list[r])):  # 반복문 사용
            Layout.addItem(suspect_list[r][i])

class HintWindow1(QDialog, QWidget):
    def __init__(self, answer_list):
        super().__init__()
        self.hintStatus_1 = True
        self.answer = answer_list
        self.cnt = 0
        self.initUI()
        self.show()

    def initUI(self):
        MainLayout = QVBoxLayout()

        hbox = QHBoxLayout()
        self.notice = QLabel('<당신의 추리에서 정답의 개수를 알려줍니다>')
        font = self.notice.font()
        font.setBold(True)  # 굵게
        font.setPointSize(font.pointSize() + 1)  # 폰트 사이즈 크게
        self.notice.setFont(font)
        self.WhoComboBox = QComboBox()
        self.WhatComboBox = QComboBox()
        self.WhereComboBox = QComboBox()
        self.guessBtn = QPushButton('Guess')
        self.guessBtn.clicked.connect(self.guessClicked)
        guessNum = {'누가? ': self.WhoComboBox, '무엇으로?': self.WhatComboBox, '어디서? ': self.WhereComboBox}
        hbox.addStretch(20)
        for i in guessNum.keys():
            Label(i, hbox, Qt.AlignCenter)
            ComboBox(list(guessNum.keys()).index(i), guessNum[i])
            hbox.addWidget(guessNum[i])
            hbox.addStretch(5)
        hbox.addWidget(self.guessBtn)
        hbox.addStretch(20)
        self.result = QLabel('')
        self.result.setStyleSheet("color: blue")  # QLabel 텍스트의 색을 파란색으로 설정
        font = self.result.font()
        font.setBold(True)  # 굵게
        font.setPointSize(font.pointSize() + 1)  # 폰트 사이즈 크게
        self.result.setFont(font)
        self.backBtn = QPushButton('확인')
        self.backBtn.clicked.connect(self.backClicked)

        MainLayout.addStretch(20)
        MainLayout.addWidget(self.notice, alignment=Qt.AlignCenter)
        MainLayout.addStretch(25)
        MainLayout.addLayout(hbox)
        MainLayout.addStretch(7)
        MainLayout.addWidget(self.result, alignment=Qt.AlignCenter)
        MainLayout.addStretch(3)
        MainLayout.addWidget(self.backBtn, alignment=Qt.AlignCenter)
        MainLayout.addStretch(20)

        self.setLayout(MainLayout)
        self.resize(1200, 850)
        self.setWindowTitle('Clue game: Hint')
        self.center()

    def center(self):  # 창 중심에 띄우기
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def guessClicked(self):
        if self.hintStatus_1:
            self.guess = [self.WhoComboBox.currentText(), self.WhatComboBox.currentText(), self.WhereComboBox.currentText()]
            print(self.answer)
            for i in range(len(self.guess)):
                if self.guess[i] == self.answer[i]:
                    self.cnt += 1
            self.resultText = ", ".join(self.guess) + " 중 정답은 %d개" % self.cnt
            self.result.setText('3개의 추리 중에서 %d개 맞았습니다' % self.cnt)
            self.hintStatus_1 = False
        else:
            self.result.setText('이미 힌트를 사용했습니다')

    def backClicked(self):
        self.close()

