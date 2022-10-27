import string
import json
import unicodedata
import numpy as np
from random import randint
import assets
import sys
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow


matrix55 = np.empty((5,5), dtype=str)
matrix66 = np.empty((6,6), dtype=str)


def replaceDigits(text):
    text = text.replace(" ", "XMEZERAX").replace("0", "XNULAX").replace("1", "XJEDNAX").replace("2", "XDVAX").replace("3", "XTRIX").replace("4", "XCTYRIX").replace("5", "XPETX").replace("6", "XSESTX").replace("7", "XSEDMX").replace("8", "XOSMX").replace("9", "XDEVETX")
    text = "".join(text)
    return text


def replaceDigitsBack(text):
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




def findPosition(matrix, letter):
    x = 0
    y = 0
    for i in range(len(matrix)):
        for j in range(len(matrix)):
            if matrix[i][j] == letter:
                x = i
                y = j
    return x, y


class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (np.int_, np.intc, np.intp, np.int8,
                            np.int16, np.int32, np.int64, np.uint8,
                            np.uint16, np.uint32, np.uint64)):
            return int(obj)
        elif isinstance(obj, (np.float_, np.float16, np.float32,
                              np.float64)):
            return float(obj)
        elif isinstance(obj, (np.ndarray,)):
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)
    

from PyQt5.uic import loadUi


class MyApp(QMainWindow):


    def makeMatrix55(self):
        alphabet = string.ascii_uppercase
        if self.cz.isChecked():
            alphabet = alphabet.replace("W", "V")
        elif self.sk.isChecked():
            alphabet = alphabet.replace("J", "I")
        text = checkDuplicates(alphabet)
        text = swapChars(text)
        k = 0
        for i in range(len(matrix55)):
            for j in range(len(matrix55)):
                matrix55[i][j] = text[k]
                k += 1
        return matrix55


    def makeMatrix66(self):
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


    def transposition(self, ST, klic, way=""):
        from math import ceil
        klic = checkDuplicates(klic)
        klic.upper()
        n = len(ST)
        cols = len(klic)
        rows = ceil(n / cols)
        k = 0
        matrix = np.empty((rows,cols), dtype=str)
        
        klic = list(klic)
        indexes = list(range(cols))
        keyVal = dict(zip(indexes, klic))
        output = ""
        sortedKeyVal = dict(sorted(keyVal.items(), key=lambda item: item[1]))
        if way == "encode":
            for i in range(rows):
                for j in range(cols):
                    if k == n or k > n:
                        matrix[i][j] = " "
                    else:
                        matrix[i][j] = ST[k]
                        k += 1
            arr = []
            for key, _ in sortedKeyVal.items():
                arr.append(key)

            sortedMatrix = matrix[:,arr]

            for column in zip(*sortedMatrix):
                for col in column:
                    if col != " ":
                        output += col
                    else:
                        continue
        elif way == "decode":
            for i in range(cols):
                for j in range(rows):
                    if k == n or k > n:
                        matrix[j][i] = " "
                    else:
                        matrix[j][i] = ST[k]
                        k += 1
            arr = []
            for key, _ in sortedKeyVal.items():
                arr.append(key)
            matrix = matrix[:,arr]
            np.transpose(matrix)

            print(ST)
            print(matrix)
            for i in matrix:
                for j in i:
                    if j != " ":
                        output += j
                    else:
                        continue
            print(output)
        return output


    def encode(self):
        OT = self.input.toPlainText()
        OT = normalizeText(OT)
        OTsub = ""
        if self.adfgx.isChecked():
            indexes55 = {0:"A",1:"D",2:"F",3:"G",4:"X"}
            keyMatrix = self.makeMatrix55()
            for m in OT:
                m1, n1 = findPosition(keyMatrix, m)
                OTsub += indexes55[m1] + indexes55[n1]
    
        elif self.adfgvx.isChecked():
            indexes66 = {0:"A",1:"D",2:"F",3:"G",4:"V",5:"X"}
            keyMatrix = self.makeMatrix66()
            for m in OT:
                m1, n1 = findPosition(keyMatrix, m)
                OTsub += indexes66[m1]
                OTsub += indexes66[n1]

        dumped = json.dumps(keyMatrix, cls=NumpyEncoder)
        with open('keyMatrix.json', 'w') as F:
            F.write(dumped)
        klic = self.klic.text()
        if len(klic) != 0:
            output = self.transposition(OTsub, klic, way = "encode")
            self.output.setText(output)
        else:
            self.output.setText(OTsub)
        self.displayData(keyMatrix)


    def decode(self):
        from textwrap import wrap
        ST = self.input.toPlainText()
        with open('keyMatrix.json', 'r') as F:
            keyMatrix = json.loads(F.read())
        klic = self.klic.text()
        klic = checkDuplicates(klic)
        klic.upper()
        if len(klic) != 0:
            ST = self.transposition(ST, klic, way = "decode")
        ST = wrap(ST, 2)
        output = ""
        if self.adfgx.isChecked():
            indexes55 = {0:"A",1:"D",2:"F",3:"G",4:"X"}
            for m in ST:
                for i in range(len(keyMatrix)):
                    for j in range(len(keyMatrix)):
                        if m[0] == indexes55[i] and m[1] == indexes55[j]:
                            output += keyMatrix[i][j]
        elif self.adfgvx.isChecked():
            indexes66 = {0:"A",1:"D",2:"F",3:"G",4:"V",5:"X"}
            for m in ST:
                for i in range(len(keyMatrix)):
                    for j in range(len(keyMatrix)):
                        if m[0] == indexes66[i] and m[1] == indexes66[j]:
                            output += keyMatrix[i][j]
        output = replaceDigitsBack(output)
        self.output.setText(output)


    def displayData(self, keyMatrix):
        numcols = len(keyMatrix[0])
        numrows = len(keyMatrix)
        self.matrix.setColumnCount(numcols)
        self.matrix.setRowCount(numrows)
        self.matrix.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.matrix.verticalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        for row in range(numrows):
            for column in range(numcols):
                item = QtWidgets.QTableWidgetItem(keyMatrix[row][column])
                item.setTextAlignment(QtCore.Qt.AlignCenter)
                self.matrix.setItem(row, column, item)


    def __init__(self):
        super(MyApp, self).__init__()
        window = loadUi("gui.ui", self)


        self.zasifrovat.clicked.connect(self.encode)
        self.desifrovat.clicked.connect(self.decode)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = MyApp()
    w.show()
    sys.exit(app.exec_())
