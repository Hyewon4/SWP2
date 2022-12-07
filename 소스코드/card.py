# 카드 분배
# 카드 특성 추출(남자,여자 / 날카로운 것, 날카롭지 않은 것 / 실외, 실내)
import random
from suspect import suspect_list, suspectFeature, suspectAll

class Card:

    def __init__(self):
        self.card = []
        self.playerCard = []
        self.comCard = []
        self.feature = {}
        self.murderer = random.choice(suspect_list[0])
        self.muder_weapon = random.choice(suspect_list[1])
        self.crime_scene = random.choice(suspect_list[2])
        self.answer = [self.murderer, self.muder_weapon, self.crime_scene]

    def setCrime(self):  # 범인, 흉기, 장소 결정
        return self.answer

    def takePlayerCard(self):  # 플레이어 카드 분배
        for suspect in suspectAll:
            if suspect not in self.answer:
                self.card.append(suspect)
        self.playerCard = random.sample(self.card, 3)
        return self.playerCard

    def takeComCard(self):  # 컴퓨터 카드 분배
        for card in self.card:
            if card not in self.playerCard:
                self.comCard.append(card)
        return self.comCard

    def getCrimeFeature(self):  # 카드 특성 추출
        i = 0
        while i < 3:
            for feature in suspectFeature.keys():
                for attr in suspectFeature[feature]:
                    if attr in self.answer:
                        self.feature[feature] = attr
                        i += 1
                        break
        return self.feature

















