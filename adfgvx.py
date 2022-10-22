import string
import unicodedata
import numpy as np
from random import randint

matrix55 = np.empty((5,5), dtype=str)
matrix66 = np.empty((6,6), dtype=str)


def replaceDigits(text):
    text = text.replace(" ", "XMEZERAX").replace("0", "XNULAX").replace("1", "XJEDNAX").replace("2", "XDVAX").replace("3", "XTRIX").replace("4", "XCTYRIX").replace("5", "XPETX").replace("6", "XSESTX").replace("7", "XSEDMX").replace("8", "XOSMX").replace("9", "XDEVETX")
    text = "".join(text)
    return text


def convertStringRepresentationsBack(text):
    text = text.replace("XMEZERAX", " ").replace("XNULAX", "0").replace("XJEDNAX", "1").replace("XDVAX", "2").replace("XTRIX", "3").replace("XCTYRIX", "4").replace("XPETX", "5").replace("XSESTX", "6").replace("XSEDMX", "7").replace("XOSMX", "8").replace("XDEVETX", "9")
    return text


def encoding(text):
    text = unicodedata.normalize('NFD', text)
    text = u"".join(c for c in text if not unicodedata.combining(c))
    return text


def upperAndPunctuation(text):
    punc = '''!()-[]{};:'"\,<>./?@#ˇ$§%^&*_~'''
    for ele in text:
        if ele in punc: 
            text = text.replace(ele, "")
    text = text.upper()
    return text


def normalizeText(text:str):
    text = encoding(text)
    text = upperAndPunctuation(text)
    text = replaceDigits(text)
    text = text.replace("Q", "KVE")
    return text


def checkDuplicates(text):
    p=""
    for i in text:
        if i not in p:
            p += i
    return p


def swapChars(text):
    text = list(text)
    n = randint(80, 100)
    for _ in range(n):
        for i in range(len(text)):
            for j in range(len(text)):
                if i == len(text):
                    i = 0
                    j = 0
                text[i], text[j] = text[j], text[i]
                i += 1
                j += 1
    "".join(text)
    return text


def makeMatrix55():
    alphabet = string.ascii_uppercase
    alphabet = alphabet.replace("W", "V")
    text = checkDuplicates(alphabet)
    text = swapChars(text)
    k = 0
    for i in range(len(matrix55)):
        for j in range(len(matrix55)):
            matrix55[i][j] = text[k]
            k += 1
    return matrix55


def makeMatrix66():
    alphabet = string.ascii_uppercase
    nums = "0", "1", "2", "3", "4", "5", "6", "7", "8", "9"
    nums = "".join(nums)
    text = alphabet + nums
    text = swapChars(text)
    k = 0
    for i in range(len(matrix66)):
        for j in range(len(matrix66)):
            matrix66[i][j] = text[k]
            k += 1
    return matrix66


def findPosition(matrix, letter):
    x = 0
    y = 0
    for i in range(len(matrix)):
        for j in range(len(matrix)):
            if matrix[i][j] == letter:
                x = i
                y = j
    return x, y


def encode():
    OT = "Dal bych si pivo"
    OT = normalizeText(OT)
    indexes55 = {0:"A",1:"D",2:"F",3:"G",4:"X"}
    indexes66 = {0:"A",1:"D",2:"F",3:"G",4:"V",5:"X"}
    keyMatrix55 = makeMatrix55()
    keyMatrix66 = makeMatrix66()
    OTsub = ""
    OTsusb = ""
    #print(keyMatrix55) TADY BUDE EXPORT!!!! TAK NA TO NEZAPOMEŇ, DĚKUJI
    for m in OT:
        m1, n1 = findPosition(keyMatrix55, m)
        OTsusb += indexes55[m1] + indexes55[n1]
    print(OTsusb)
    # for m in OT:
    #     m1, n1 = findPosition(keyMatrix66, m)
    #     OTsub += indexes66[m1]
    #     OTsub += indexes66[n1]
    # print(OTsub)
    # return OTsub


def transposition():
    from math import ceil
    klic = "kolotoc"
    klic = checkDuplicates(klic)
    klic.upper()
    ST = "DDAAFDXGAGFXAGGA"
    n = len(ST)
    cols = len(klic)
    rows = ceil(n / cols)
    k = 0
    print(rows, cols)
    matrix = np.empty((rows,cols), dtype=str)
    for i in range(rows):
        for j in range(cols):
            if k == n:
                break
            matrix[i][j] = ST[k]
            k += 1
    print(matrix)
    




# encode()
transposition()