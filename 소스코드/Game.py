import sys, random
from PyQt5.QtWidgets import (QFrame, QCheckBox, QWidget, QDesktopWidget, QPushButton,
    QGridLayout, QHBoxLayout, QVBoxLayout,QSplitter, QApplication, QLabel, QTextBrowser,
    QComboBox, QLineEdit)
from PyQt5.QtCore import Qt
from suspect import suspect_list
from card import Card
from hint1 import HintWindow1
from hint2 import HintWindow2

class Label(QLabel):

    def __init__(self, text, layout, alignment):
        super().__init__()
        self.setText(text)
        layout.addWidget(self, alignment=alignment)

class CheckBox(QCheckBox): # 체크박스 생성하는 클래스

    def __init__(self, text):
        super().__init__()
        self.setText(text)

class Frame(QFrame):  # QFrame 생성과 FrameShape를 설정할 때 사용하는 클래스

    def __init__(self):
        super().__init__()
        self.setFrameShape(QFrame.Panel | QFrame.Sunken)

class ComboBox():

    def __init__(self, r, Layout):
        for i in range(len(suspect_list[r])):  # 반복문 사용
            Layout.addItem(suspect_list[r][i])

class GameMain(QWidget):

    def __init__(self):
        super().__init__()
        self.Remainingcount = 10
        self.hint1 = True
        self.hint2 = True
        self.numList1 = [1, 2, 3, 4, 5]
        self.numList2 = [1, 2, 3]
        self.rand_1 = 0
        self.rand_2 = 0

        Layout = QVBoxLayout()

        frame_1 = Frame()
        frame_2 = Frame()
        frame_3 = Frame()
        frame_4 = Frame()
        frame_5 = Frame()
        frame_6 = Frame()
        frame_7 = Frame()

        # frame_1 : 체크박스
        CheckBoxLayout = QGridLayout()
        for i in range(len(suspect_list)):
            for j in range(len(suspect_list[i])):
                checkbox = CheckBox(suspect_list[i][j])
                CheckBoxLayout.addWidget(checkbox, j, i)

        frame_1.setLayout(CheckBoxLayout)

        # frame_2 : 소유 카드
        PoccessLayout = QVBoxLayout()
        Label('소유 카드', PoccessLayout, Qt.AlignLeft)
        self.PoccessCardLine = QTextBrowser()
        self.PoccessCardLine.setStyleSheet("color: blue")  # QTextBrowser의 글자색을 파란색으로 설정
        font = self.PoccessCardLine.font()
        font.setBold(True)  # 굵게
        font.setPointSize(font.pointSize() + 1)  # 폰트 사이즈 크게
        self.PoccessCardLine.setFont(font)
        PoccessLayout.addWidget(self.PoccessCardLine)

        frame_2.setLayout(PoccessLayout)

        # frame_3 : 추리
        GuessLayout = QVBoxLayout()
        hbox = QHBoxLayout()
        hbox2 = QHBoxLayout()
        self.HumanComboBox = QComboBox()
        self.ToolComboBox = QComboBox()
        self.PlaceComboBox = QComboBox()
        self.guessError = QLabel('')  # 소유한 카드를 추리에 활용했을 때 나타나는 경고 메세지
        self.guessError.setStyleSheet("color: red")  # 경고 메세지 색깔을 빨간색으로 설정
        self.GuessButton = QPushButton('Guess')
        self.GuessButton.clicked.connect(self.guessClicked)
        GuessList = {'누가? ': self.HumanComboBox, '무엇으로?': self.ToolComboBox, '어디서? ': self.PlaceComboBox}
        Label('추리', hbox, Qt.AlignLeft)
        self.remaincnt = QLabel(f'남은 횟수: {self.Remainingcount}')
        hbox.addWidget(self.remaincnt, alignment=Qt.AlignRight)
        for i in GuessList.keys():
            Label(i, hbox2, Qt.AlignJustify)
            ComboBox(list(GuessList.keys()).index(i), GuessList[i])
            hbox2.addWidget(GuessList[i])
            hbox2.addStretch(1)
        hbox2.addWidget(self.GuessButton)
        GuessLayout.addLayout(hbox)
        GuessLayout.addLayout(hbox2)
        GuessLayout.addWidget(self.guessError, alignment=Qt.AlignCenter)

        frame_3.setLayout(GuessLayout)

        # frame_4 : Clue
        ClueLayout = QVBoxLayout()
        hbox3 = QHBoxLayout()
        hbox4 = QHBoxLayout()
        self.ClueHumanComboBox = QComboBox()
        self.ClueToolComboBox = QComboBox()
        self.CluePlaceComboBox = QComboBox()
        self.ClueButton = QPushButton('Clue')
        self.ClueButton.clicked.connect(self.clueClicked)
        ClueList = {'누가?' : self.ClueHumanComboBox, '무엇으로?': self.ClueToolComboBox, '어디서?': self.CluePlaceComboBox}
        Label('최종 추리', hbox3, Qt.AlignLeft)
        for i in ClueList.keys():
            Label(i, hbox4, Qt.AlignJustify)
            ComboBox(list(ClueList.keys()).index(i), ClueList[i])
            hbox4.addWidget(ClueList[i])
            hbox4.addStretch(1)
        hbox4.addWidget(self.ClueButton)
        ClueLayout.addLayout(hbox3)
        ClueLayout.addLayout(hbox4)

        frame_4.setLayout(ClueLayout)

        # frame_5 : Hint
        HintLayout = QVBoxLayout()
        Label('힌트', HintLayout, Qt.AlignLeft)
        self.HintText = QTextBrowser()
        self.HintText.setFixedHeight(80)
        HintLayout.addWidget(self.HintText)

        frame_5.setLayout(HintLayout)
        frame_5.setMaximumHeight(150)


        # frame_6 : 다른 플레이어가 보여준 카드
        ShowCardLayout = QVBoxLayout()
        Label('다른 플레이어가 공개한 카드', ShowCardLayout, Qt.AlignLeft)
        self.ShowCardText = QTextBrowser()
        ShowCardLayout.addWidget(self.ShowCardText)

        frame_6.setLayout(ShowCardLayout)

        # frame_7 : 최종 결과, new game
        ResultLayout = QVBoxLayout()
        Label('게임 결과', ResultLayout, Qt.AlignLeft)
        self.ResultText = QLineEdit()
        self.setMinimumHeight(30)
        font = self.ResultText.font()
        font.setBold(True)
        font.setPointSize(font.pointSize() + 1)  # 폰트 사이즈 크게
        self.ResultText.setFont(font)
        self.ResultText.setReadOnly(True)
        self.newGameButton = QPushButton('New game')
        self.newGameButton.clicked.connect(self.startGame)
        ResultLayout.addWidget(self.ResultText)
        ResultLayout.addWidget(self.newGameButton, alignment=Qt.AlignCenter)

        frame_7.setLayout(ResultLayout)

        # mainLayout 적용
        self.mainLayout = QSplitter(Qt.Vertical, self)
        self.mainLayout.addWidget(frame_1)
        self.mainLayout.addWidget(frame_2)
        self.mainLayout.addWidget(frame_3)
        self.mainLayout.addWidget(frame_4)

        self.mainLayout2 = QSplitter(Qt.Vertical, self)
        self.mainLayout2.addWidget(frame_5)
        self.mainLayout2.addWidget(frame_6)
        self.mainLayout2.addWidget(frame_7)
        self.mainLayout2.setFixedWidth(450)

        self.mainLayout3 = QSplitter(Qt.Horizontal, self)
        self.mainLayout3.addWidget(self.mainLayout)
        self.mainLayout3.addWidget(self.mainLayout2)
        self.mainLayout3.resize(1380, 800)

        Layout.addWidget(self.mainLayout3)

        self.setLayout(Layout)
        self.resize(1380, 800)
        self.setWindowTitle('Clue game')
        self.center()

        self.startGame()

    def center(self): #창 중심에 띄우기
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def startGame(self):
        self.card = Card()
        self.answer = self.card.setCrime()
        self.playerCard = self.card.takePlayerCard()
        self.comCard = self.card.takeComCard()
        self.numList1 = [1, 2, 3, 4, 5]
        self.numList2 = [1, 2, 3]
        self.clue = True
        self.hint1 = True
        self.hint2 = True
        self.rand_1 = 0
        self.rand_2 = 0
        self.Remainingcount = 10
        self.playerStr = ""
        for attr in self.playerCard:
            self.playerStr += attr + "    "
        print(self.answer, self.playerCard, self.comCard)
        print(self.card.getCrimeFeature())
        self.PoccessCardLine.setPlainText(self.playerStr)
        self.remaincnt.setText(f'남은 횟수: {self.Remainingcount}')
        self.ShowCardText.clear()
        self.HintText.clear()
        self.ResultText.clear()
        self.guessError.clear()

    def guessClicked(self):
        self.cnt = 0
        self.guessError.clear()  # 경고 메세지 초기화(안 보이게)
        if self.Remainingcount > 0:
            self.guesses = [self.HumanComboBox.currentText(), self.ToolComboBox.currentText(), self.PlaceComboBox.currentText()]
            self.com_list = []
            for guess in self.guesses:
                if guess in self.playerCard:
                    self.cnt += 1
                    break
                if guess in self.comCard:
                    self.com_list.append(guess)
            if self.cnt != 0:  # 소유한 카드를 추리에 활용한 경우: 경고 메세지 나타내기
                self.guessError.setText('소유한 카드를 추리에 사용했습니다. 소유한 카드를 제외한 카드를 사용하여 다시 추리하세요')
                return '소유한 카드를 추리에 사용했습니다'
            if len(self.com_list) == 0:
                self.ShowCardText.append('공개할 카드가 없습니다')
            else:
                self.showCard = random.choice(self.com_list)
                self.comCard.remove(self.showCard)
                self.ShowCardText.append(self.showCard)
                print(self.comCard)
            self.Remainingcount -= 1
            self.remaincnt.setText(f'남은 횟수: {self.Remainingcount}')
            self.hint()
        elif self.clue:
            self.guessError.setText('남은 추리 횟수가 없습니다. 최종 추리를 해주세요')

    def clueClicked(self):
        if self.clue:
            self.clueList = [self.ClueHumanComboBox.currentText(), self.ClueToolComboBox.currentText(), self.CluePlaceComboBox.currentText()]
            if self.answer == self.clueList:
                self.ResultText.setText('Success!')
            else:
                self.ResultText.setText('Fail!')
            self.Remainingcount = 0
            self.remaincnt.setText(f'남은 횟수: {self.Remainingcount}')
            self.clue = False

    def hint(self): # 힌트
        if 0 < self.Remainingcount <= 5 and self.hint1:  # 정답의 개수를 알려주는 힌트 랜덤 등장
            self.rand_1 = random.choice(self.numList1)
            if self.rand_1 != 4:
                self.numList1.remove(self.rand_1)

        if 0 < self.Remainingcount <= 3 and self.hint2:
            self.rand_2 = random.choice(self.numList2)
            if self.rand_2 != 1:
                self.numList2.remove(self.rand_2)

        if self.rand_1 == 4 and self.hint1:  # 정답의 개수를 알려주는 힌트(hint1.py)
            self.hide()
            self.hintWindow1 = HintWindow1(self.answer)
            self.hintWindow1.exec()  # 새 창 열기
            try:
                self.HintText.append(self.hintWindow1.resultText)
            except AttributeError:
                pass
            self.show()
            self.hint1 = False

        if self.rand_2 == 1 and self.hint2:  # 특징(성별/흉기 유형/장소 유형)을 알려주는 힌트(hint2.py)
            self.hide()
            self.hintWindow2 = HintWindow2(self.card.getCrimeFeature())
            self.hintWindow2.exec()  # 새 창 열기
            try:
                self.HintText.append(self.hintWindow2.featureText)
            except AttributeError:
                pass
            self.show()
            self.hint2 = False



if __name__ == '__main__':
   app = QApplication(sys.argv)
   ex = GameMain()
   ex.show()
   sys.exit(app.exec_())