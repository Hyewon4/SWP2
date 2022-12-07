# 남은 횟수가 1 ~ 3회일때 사람/무기/장소에 대한 힌트
import random

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *


class HintWindow2(QDialog, QWidget):
    def __init__(self, answer_dic):
        super().__init__()
        self.hintStatus_2 = True
        self.answer = answer_dic
        self.feature = {}
        self.initUI()
        self.show()

    def initUI(self):

        MainLayout = QVBoxLayout()

        self.hint = QLabel(self.getFeature())
        self.hint.setStyleSheet("color: blue")  # QLabel 텍스트의 색을 파란색으로 설정
        font = self.hint.font()
        font.setBold(True)  # 굵게
        font.setPointSize(font.pointSize() + 1)  # 폰트 사이즈 크게
        self.hint.setFont(font)
        self.backBtn = QPushButton('확인')
        self.backBtn.clicked.connect(self.backClicked)

        MainLayout.addStretch(25)
        MainLayout.addWidget(self.hint, alignment=Qt.AlignCenter)
        MainLayout.addStretch(10)
        MainLayout.addWidget(self.backBtn, alignment=Qt.AlignCenter)
        MainLayout.addStretch(25)

        self.setLayout(MainLayout)
        self.resize(1200, 850)
        self.setWindowTitle('Clue game: Hint')
        self.center()

    def center(self):  # 창 중심에 띄우기
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def getFeature(self):
        if self.hintStatus_2:
            self.feature = random.choice(list(self.answer.keys()))
            if self.feature == '남자' or self.feature == '여자':
                return "범인은 %s입니다" % self.feature
            elif self.feature == '실외' or self.feature == '실내':
                return "사건 장소는 %s입니다" % self.feature
            else:
                return "흉기는 %s입니다" % self.feature
        else:
            return "이미 힌트를 사용했습니다"

    def backClicked(self):
        self.featureText = self.hint.text()
        self.close()
