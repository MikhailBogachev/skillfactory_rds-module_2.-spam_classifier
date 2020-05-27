import re
import pandas as pd

SPAM = 1
NOT_SPAM = 0

train_data = [
    ['Купите новое чистящее средство', SPAM],
    ['Купи мою новую книгу', SPAM],
    ['Подари себе новый телефон', SPAM],
    ['Добро пожаловать и купите новый телевизор', SPAM],
    ['Привет давно не виделись', NOT_SPAM],
    ['Довезем до аэропорта из пригорода всего за 399 рублей', SPAM],
    ['Добро пожаловать в Мой Круг', NOT_SPAM],
    ['Я все еще жду документы', NOT_SPAM],
    ['Приглашаем на конференцию Data Science', NOT_SPAM],
    ['Потерял твой телефон напомни', NOT_SPAM],
    ['Порадуй своего питомца новым костюмом', SPAM]
]
pA = 0
pNotA = 0
Spam = {}
NotSpam = {}


def calculate_word_frequencies(body, label):
    """Принимает на вход письмо и его метку - spam_l / notspam_l,
    подсчитывает частоту слов в текстах для справочников spam, notspam"""

    # text = body.lower()
    # words = re.findall(r'\b[a-z]{4,15}\b', text) # отфильтруем слова 4-15 сим

    if label == 1:  # создадим словари "спамовых" слов
        for word in body.split(' '):
            count = Spam.get(word, 0)
            Spam[word] = count + 1

    else:
        for word in body.split(' '):
            count = NotSpam.get(word, 0)
            NotSpam[word] = count + 1

spam_message = []
not_spam_message = []

for row in train_data:
    if row[1] == 1:
        spam_message.append(row)
    else:
        not_spam_message.append(row)

for row in spam_message:
    row[0] = row[0].lower()
for row in not_spam_message:
    row[0] = row[0].lower()


def train():
    """Принимает на вход тексты, заполняет словари spam, notspam,
    считает вероятности pA, pNotA"""

    pA = len(spam_message) / len(train_data)
    pNotA = 1 - pA

    for row in spam_message:
        calculate_word_frequencies(row[0], row[1])
    for row in not_spam_message:
        calculate_word_frequencies(row[0], row[1])

    return pA, pNotA


# Реализуем функцию подсчета вероятности спама и неспама для слова
def calculate_P_Bi(word):
    try:
        P_Bi_A = Spam[word] / sum(Spam.values())
    except KeyError:
        P_Bi_A = 0

    try:
        P_Bi_notA = NotSpam[word] / sum(NotSpam.values())
    except KeyError:
        P_Bi_notA = 0

    return P_Bi_A, P_Bi_notA

def classify(email):
    """Принимает на вход текст,
    и считает вероятность спама / не спама для текста"""
    text = email.lower().split(' ')
    words = text
    #words = re.findall(r'\b[a-z]{4,15}\b', text) # отфильтруем слова 4-15 сим
    P_B_A = 1
    for word in words:
        P_B_A = P_B_A * (1 + calculate_P_Bi(word)[0])
    print('P_B_A:', P_B_A)
    P_B_notA = 1
    for word in words:
        P_B_notA = P_B_notA * (1 + calculate_P_Bi(word)[1])
    #print('P_B_notA:', P_B_notA)
    #print('pA:',train()[0],'pNotA:',train()[1])
    pA = train()[0]
    pNotA = train()[1]
    if P_B_A * pA > P_B_notA * pNotA:
        return 'spam_l'
    else:
        return 'notspam_l'

    
