
# importing libraries
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys
from scipy.io import arff
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
import pickle
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
import seaborn as sns
import info
from PyQt5.QtWidgets import QFileDialog


def heatmap():
    global hwindow1
    hwindow1 = QMainWindow()
    hwindow1.setGeometry(0, 30, w, h - 30)
    hwindow1.setWindowTitle("Parkinson Prediction Software")
    hwindow1.setStyleSheet("background : rgb(200,255,255)")
    hwindow1.show()

    content = QWidget(mlabel)
    hwindow1.setCentralWidget(content)
    content.setLayout(QVBoxLayout())
    content.layout().setContentsMargins(320, 0, 320, 0)
    content.layout().setSpacing(0)

    fig = Figure(figsize=(13, 13), dpi=100)
    plot1 = fig.add_subplot(111)
    ht = sns.heatmap(df.iloc[:, 1:23].corr(), linewidths=.5, annot=True, fmt='.0%', ax=plot1)
    for tick in ht.get_xticklabels():
        tick.set_rotation(90)
    for tick in ht.get_yticklabels():
        tick.set_rotation(0)

    canvas = FigureCanvas(fig)
    canvas.draw()
    scroll = QScrollArea(content)
    scroll.setWidget(canvas)
    toolbar = NavigationToolbar(canvas, content)
    toolbar.update()
    content.layout().addWidget(toolbar)
    content.layout().addWidget(scroll)


def attribute():
    global awindow1
    awindow1 = QWidget()
    awindow1.setGeometry(0, 30, w, h)
    awindow1.setWindowTitle("Parkinson Prediction Software")
    awindow1.setStyleSheet("background : rgb(200,255,255)")
    awindow1.show()
    alabel1 = QLabel(awindow1)
    alabel1.setPixmap(QPixmap("black.jpg"))
    alabel1.setScaledContents(True)
    alabel1.setGeometry(0, 0, w, h)
    alabel1.show()

    label = QLabel(awindow1)
    label.setText("Attribute Viewer")
    label.setGeometry(830, 70, 350, 50)
    label.setFont(QFont("Times", 23))
    label.setAlignment(QtCore.Qt.AlignCenter)
    label.setStyleSheet("background : rgb(230,255,255);"
                        "border : 1px solid black;"
                        "border-radius : 10px")
    label.show()

    def draw():
        value2 = adrop1.currentText()
        patt = df.loc[:, '{}'.format(value2)].values
        Latt = patt.tolist()  # contains all staus
        Latt3 = [(List1[i], Latt[i]) for i in range(0, len(List1))]  # commbined list of names and status
        Latt4 = Latt3[count1:count2:1]

        ent1 = QLineEdit(awindow1)
        ent1.setText("Name")
        ent1.setGeometry(700, 280, 300, 70)
        ent1.setFont(QFont("Times", 16))
        ent1.setAlignment(QtCore.Qt.AlignCenter)
        ent1.setStyleSheet("background : rgb(230,255,255);")
        ent1.show()

        ent2 = QLineEdit(awindow1)
        ent2.setText("{}".format(value2))
        ent2.setGeometry(1000, 280, 300, 70)
        ent2.setFont(QFont("Times", 16))
        ent2.setAlignment(QtCore.Qt.AlignCenter)
        ent2.setStyleSheet("background : rgb(230,255,255);")
        ent2.show()

        b = 350
        for i in range(total_rows):
            a = 700
            for j in range(total_columns):
                e = QLineEdit(awindow1)
                e.setFont(QFont("Times", 16))
                e.setAlignment(QtCore.Qt.AlignCenter)
                e.setGeometry(a, b, 300, 70)
                e.setText("{}".format(Latt4[i][j]))
                e.setStyleSheet("color : blue;"
                                "background : rgb(230,255,255);")
                e.show()
                a = a + 300
            b = b + 70

    list5 = list(df2.columns)
    global adrop1
    adrop1 = QComboBox(awindow1)
    adrop1.setGeometry(100, 200, 300, 55)
    adrop1.addItems(list5)
    adrop1.setFont(QFont("Times", 10))
    adrop1.setStyleSheet("background : lightgrey;")
    adrop1.show()

    button1 = QPushButton(awindow1)
    button1.setText("Draw")
    button1.setGeometry(100, 290, 300, 55)
    button1.setFont(QFont("Times", 15))
    button1.setStyleSheet("QPushButton::hover"
                          "{"
                          "background-color : skyblue;"
                          "}")
    button1.show()
    button1.clicked.connect(draw)


def piechart():
    global pwindow1
    pwindow1 = QWidget()
    pwindow1.setGeometry(0, 30, w, h)
    pwindow1.setWindowTitle("Parkinson Prediction Software")
    pwindow1.setStyleSheet("background : rgb(200,255,255)")
    pwindow1.show()

    alabel1 = QLabel(pwindow1)
    alabel1.setPixmap(QPixmap("black.jpg"))
    alabel1.setScaledContents(True)
    alabel1.setGeometry(0, 0, w, h)
    alabel1.show()

    label = QLabel(pwindow1)
    label.setText("Pie Chart")
    label.setGeometry(900, 20, 300, 50)
    label.setFont(QFont("Times", 23))
    label.setAlignment(QtCore.Qt.AlignCenter)
    label.setStyleSheet("background : rgb(230,255,255);"
                        "border : 1px solid black;"
                        "border-radius : 10px")
    label.show()

    def draw():
        value2 = pdrop1.currentText()
        mycolors = []
        myexplode = []
        found1 = 0
        found2 = 0
        for i in range(len(List4)):
            score = List4[i][1]
            if (score == 1):
                color = "red"
                found1 = found1 + 1
                mycolors.append(color)
            else:
                color = "blue"
                found2 = found2 + 1
                mycolors.append(color)

        if (found1 > found2):
            for i in range(len(List4)):
                score = List4[i][1]
                if (score == 1):
                    myexplode.append(0.01)
                elif (score == 0):
                    myexplode.append(0.2)

        elif (found2 > found1):
            for i in range(len(List4)):
                score = List4[i][1]
                if (score == 1):
                    myexplode.append(0.2)
                elif (score == 0):
                    myexplode.append(0.01)

        fig = Figure(figsize=(5, 5), dpi=100)
        plot1 = fig.add_subplot(111)
        plot1.pie(df2[('{}'.format(value2))], radius=1, labels=sList5, explode=myexplode, colors=mycolors,
                  normalize=True, autopct='%1.2f%%');
        canvas = FigureCanvas(fig)
        canvas.setParent(pwindow1)
        canvas.show()
        canvas.move(560, 100)
        canvas.resize(1000, 800)
        plot1.legend(['{}'.format(value2)])
        plot1.set_xlabel('name')
        plot1.set_title('Name Vs. {}'.format(value2))

    list5 = list(df2.columns)
    global pdrop1
    pdrop1 = QComboBox(pwindow1)
    pdrop1.setGeometry(100, 200, 300, 55)
    pdrop1.addItems(list5)
    pdrop1.setFont(QFont("Times", 10))
    pdrop1.setStyleSheet("background : lightgrey;")
    pdrop1.show()

    button1 = QPushButton(pwindow1)
    button1.setText("Draw")
    button1.setGeometry(100, 290, 300, 55)
    button1.setFont(QFont("Times", 15))
    button1.setStyleSheet("QPushButton::hover"
                          "{"
                          "background-color : skyblue;"
                          "}")
    button1.show()
    button1.clicked.connect(draw)


def scatter():
    global swindow1
    swindow1 = QWidget()
    swindow1.setGeometry(0, 30, w, h)
    swindow1.setWindowTitle("Parkinson Prediction Software")
    swindow1.setStyleSheet("background : rgb(200,255,255)")
    swindow1.show()
    alabel1 = QLabel(swindow1)
    alabel1.setPixmap(QPixmap("black.jpg"))
    alabel1.setScaledContents(True)
    alabel1.setGeometry(0, 0, w, h)
    alabel1.show()

    label = QLabel(swindow1)
    label.setText("Scatter Plot")
    label.setGeometry(900, 20, 300, 50)
    label.setFont(QFont("Times", 23))
    label.setAlignment(QtCore.Qt.AlignCenter)
    label.setStyleSheet("background : rgb(230,255,255);"
                        "border : 1px solid black;"
                        "border-radius : 10px")
    label.show()

    def draw():
        value2 = sdrop1.currentText()
        fig = Figure(figsize=(5, 5), dpi=100)
        plot1 = fig.add_subplot(111)
        plot1.scatter(df2['name'], df2['{}'.format(value2)], color='g');
        canvas = FigureCanvas(fig)
        canvas.setParent(swindow1)
        canvas.show()
        canvas.move(560, 100)
        canvas.resize(1000, 800)
        plot1.legend(['{}'.format(value2)])
        plot1.set_xlabel('name')
        plot1.set_title('Name Vs. {}'.format(value2))

    list5 = list(df2.columns)
    global sdrop1
    sdrop1 = QComboBox(swindow1)
    sdrop1.setGeometry(100, 200, 300, 55)
    sdrop1.addItems(list5)
    sdrop1.setFont(QFont("Times", 10))
    sdrop1.setStyleSheet("background : lightgrey;")
    sdrop1.show()

    button1 = QPushButton(swindow1)
    button1.setText("Draw")
    button1.setGeometry(100, 290, 300, 55)
    button1.setFont(QFont("Times", 15))
    button1.setStyleSheet("QPushButton::hover"
                          "{"
                          "background-color : skyblue;"
                          "}")
    button1.show()
    button1.clicked.connect(draw)


def linechart():
    global lwindow1
    lwindow1 = QWidget()
    lwindow1.setGeometry(0, 30, w, h)
    lwindow1.setWindowTitle("Parkinson Prediction Software")
    lwindow1.setStyleSheet("background : rgb(200,255,255)")
    lwindow1.show()
    alabel1 = QLabel(lwindow1)
    alabel1.setPixmap(QPixmap("black.jpg"))
    alabel1.setScaledContents(True)
    alabel1.setGeometry(0, 0, w, h)
    alabel1.show()

    label = QLabel(lwindow1)
    label.setText("Line Chart")
    label.setGeometry(900, 20, 300, 50)
    label.setFont(QFont("Times", 23))
    label.setAlignment(QtCore.Qt.AlignCenter)
    label.setStyleSheet("background : rgb(230,255,255);"
                        "border : 1px solid black;"
                        "border-radius : 10px")
    label.show()

    def draw():
        value2 = ldrop1.currentText()
        fig = Figure(figsize=(5, 5), dpi=100)
        plot1 = fig.add_subplot(111)
        df3 = df2[['name', '{}'.format(value2)]].groupby('name').sum()
        df3.plot(kind='line', legend=True, ax=plot1, color='r', marker='o', fontsize=10)
        canvas = FigureCanvas(fig)
        canvas.setParent(lwindow1)
        canvas.show()
        canvas.move(560, 100)
        canvas.resize(1000, 800)
        plot1.legend(['{}'.format(value2)])
        plot1.set_xlabel('name')
        plot1.set_title('Name Vs. {}'.format(value2))

    list5 = list(df2.columns)
    global ldrop1
    ldrop1 = QComboBox(lwindow1)
    ldrop1.setGeometry(100, 200, 300, 55)
    ldrop1.addItems(list5)
    ldrop1.setFont(QFont("Times", 10))
    ldrop1.setStyleSheet("background : lightgrey;")
    ldrop1.show()

    button1 = QPushButton(lwindow1)
    button1.setText("Draw")
    button1.setGeometry(100, 290, 300, 55)
    button1.setFont(QFont("Times", 15))
    button1.setStyleSheet("QPushButton::hover"
                          "{"
                          "background-color : skyblue;"
                          "}")
    button1.show()
    button1.clicked.connect(draw)


def ibackpage2():
    frame6.hide()
    frame5.show()


def visualize():
    frame5.hide()
    global frame6
    frame6 = QFrame(frame4)
    frame6.setGeometry(400, 230, 1000, 650)
    frame6.setStyleSheet("background-color: rgba(141, 242, 242,0);")
    frame6.show()

    label = QLabel(frame6)
    label.setGeometry(0, 0, 1000, 650)
    label.setFont(QFont("Times", 18))
    label.setStyleSheet("background : rgb(230,255,255);"
                        "border : 1px solid black")
    label.show()

    label1 = QLabel(frame6)
    label1.setText(value)
    label1.setGeometry(300, 30, 300, 50)
    label1.setFont(QFont("Times", 20))
    label1.setAlignment(QtCore.Qt.AlignCenter)
    label1.setStyleSheet("background : rgb(230,255,255);"
                         "border : 1px solid black;"
                         "border-radius : 5px")
    label1.show()

    text1 = '''{} has a {} percent chance of having Parkinsons disease as our model predicts that {} out of {} recordings have status as 1 '''.format(
        value, result, one, recording)

    text = QPlainTextEdit(frame6)
    text.setGeometry(80, 110, 820, 150)
    text.setFont(QFont("Times", 17))
    text.insertPlainText("{}".format(text1))
    text.setStyleSheet("background : rgb(230,255,255);"
                       "border : 1px solid black")
    text.show()

    label2 = QLabel(frame6)
    label2.setText("Visualizer")
    label2.setGeometry(375, 290, 210, 50)
    label2.setFont(QFont("Times", 18))
    label2.setAlignment(QtCore.Qt.AlignCenter)
    label2.setStyleSheet("background : rgb(230,255,255);"
                         "border : 1px solid black;"
                         "border-radius : 10px")
    label2.show()

    button1 = QPushButton(frame6)
    button1.setText("Heat Map")
    button1.setGeometry(200, 370, 240, 50)
    button1.setFont(QFont("Times", 15))
    button1.setStyleSheet("QPushButton::hover"
                          "{"
                          "background-color : skyblue;"
                          "}")
    button1.show()
    button1.clicked.connect(heatmap)

    button2 = QPushButton(frame6)
    button2.setText("Attribute Viewer")
    button2.setGeometry(510, 370, 240, 50)
    button2.setFont(QFont("Times", 15))
    button2.setStyleSheet("QPushButton::hover"
                          "{"
                          "background-color : skyblue;"
                          "}")
    button2.show()
    button2.clicked.connect(attribute)

    button3 = QPushButton(frame6)
    button3.setText("Pie Chart")
    button3.setGeometry(200, 450, 240, 50)
    button3.setFont(QFont("Times", 15))
    button3.setStyleSheet("QPushButton::hover"
                          "{"
                          "background-color : skyblue;"
                          "}")
    button3.show()
    button3.clicked.connect(piechart)

    button4 = QPushButton(frame6)
    button4.setText("Scatter Plot")
    button4.setGeometry(510, 450, 240, 50)
    button4.setFont(QFont("Times", 15))
    button4.setStyleSheet("QPushButton::hover"
                          "{"
                          "background-color : skyblue;"
                          "}")
    button4.show()
    button4.clicked.connect(scatter)

    button5 = QPushButton(frame6)
    button5.setText("Line Chart")
    button5.setGeometry(350, 530, 240, 50)
    button5.setFont(QFont("Times", 15))
    button5.setStyleSheet("QPushButton::hover"
                          "{"
                          "background-color : skyblue;"
                          "}")
    button5.show()
    button5.clicked.connect(linechart)

    button6 = QPushButton(frame6)
    button6.setText("Back")
    button6.setGeometry(820, 580, 150, 50)
    button6.setFont(QFont("Times", 18))
    button6.setStyleSheet("QPushButton::hover"
                          "{"
                          "background-color : skyblue;"
                          "}")
    button6.show()
    button6.clicked.connect(ibackpage2)


def getvalue():
    global value, df2, recording, one, List4, List5, count1, count2
    List5 = []
    value = drop.currentText()
    for data in stringlist:
        if (value == data):
            index = stringlist.index(data)
            recording = ListCount[index]

            if (index == 0):
                count1 = 0
                count2 = ListCount1[index]
                List4 = List3[count1:count2:1]
                df2 = df.iloc[count1:count2]
                i = 0
                while (i < recording):
                    temp = pnames[i][9:13]
                    List5.append(temp)
                    i = i + 1
            else:
                count1 = ListCount1[index - 1]
                count2 = ListCount1[index]
                List4 = List3[count1:count2:1]
                df2 = df.iloc[count1:count2]
                i = count1
                while (i < (recording + count1)):
                    temp = pnames[i][9:13]
                    List5.append(temp)
                    i = i + 1

            global sList5, total_rows, total_columns
            sList5 = [x.decode("utf-8") for x in List5]
            total_rows = len(List4)
            total_columns = len(List4[0])

            score = 0
            one = 0
            for i in range(total_rows):
                score1 = List4[i][1]
                score = score + score1
                if (score1 == 1):
                    one = one + 1

            global result
            result = round((score * 100) / ListCount[index], 2)

            global frame5
            frame5 = QFrame(frame4)
            frame5.setGeometry(400, 230, 1000, 650)
            frame5.setStyleSheet("background-color: rgba(141, 242, 242,0);")
            frame5.show()

            label = QLabel(frame5)
            label.setGeometry(0, 0, 1000, 660)
            label.setFont(QFont("Times", 18))
            label.setStyleSheet("background : rgb(230,255,255);"
                                "border : 1px solid black")
            label.show()

            label1 = QLabel(frame5)
            label1.setText("Total Number of Recordings: {}".format(recording))
            label1.setGeometry(260, 40, 440, 40)
            label1.setFont(QFont("Times", 18))
            label1.setStyleSheet("background : rgb(230,255,255);")
            label1.show()

            ent1 = QLineEdit(frame5)
            ent1.setText("Name")
            ent1.setGeometry(230, 110, 250, 50)
            ent1.setFont(QFont("Times", 16))
            ent1.setAlignment(QtCore.Qt.AlignCenter)
            ent1.setStyleSheet("background : rgb(230,255,255);")
            ent1.show()

            ent2 = QLineEdit(frame5)
            ent2.setText("Status")
            ent2.setGeometry(480, 110, 250, 50)
            ent2.setFont(QFont("Times", 16))
            ent2.setAlignment(QtCore.Qt.AlignCenter)
            ent2.setStyleSheet("background : rgb(230,255,255);")
            ent2.show()

            b = 160
            for i in range(total_rows):
                a = 230
                for j in range(total_columns):
                    e = QLineEdit(frame5)
                    e.setFont(QFont("Times", 16))
                    e.setAlignment(QtCore.Qt.AlignCenter)
                    e.setGeometry(a, b, 250, 50)
                    e.setText("{}".format(List4[i][j]))
                    e.setStyleSheet("color : blue;"
                                    "background : rgb(230,255,255);")
                    e.show()
                    a = a + 250
                b = b + 50

            label2 = QLabel(frame5)
            label2.setText("Chance of having Parkinson Disease: {}%".format(result))
            label2.setGeometry(200, 500, 660, 40)
            label2.setFont(QFont("Times", 18))
            label2.setStyleSheet("background : rgb(230,255,255);")
            label2.show()

            button1 = QPushButton(frame5)
            button1.setText("Visualize {} Data".format(value))
            button1.setFont(QFont("Times", 15))
            button1.setGeometry(340, 590, 300, 50)
            button1.setStyleSheet("QPushButton::hover"
                                  "{"
                                  "background-color : skyblue;"
                                  "}")
            button1.show()
            button1.clicked.connect(visualize)

        elif (drop.currentText == ""):
            mbox = QMessageBox()
            mbox.setText("Nothing to Show !!")
            mbox.setDetailedText("You have to Choose Something. Try Again!!")
            mbox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
            mbox.exec()


def inputpage2():
    frame.hide()
    frame2.hide()
    frame3.hide()
    frame4.show()

    imlabel1.hide()
    imlabel2.hide()
    imlabel3.show()
    # Create the Heading Label
    hlabel = QLabel(frame4)
    hlabel.setText("PARKINSON DISEASE PREDICTION SOFTWARE")
    hlabel.setGeometry(150, 20, 1250, 60)
    hlabel.setFont(QFont("Times", 25))
    hlabel.setAlignment(QtCore.Qt.AlignCenter)
    hlabel.setStyleSheet("background : rgb(230,255,255);"
                         "border : 3px solid black")
    hlabel.show()

    # Create the Mid Label
    mlabel = QLabel(frame4)
    mlabel.setGeometry(150, 110, 1250, 770)
    mlabel.setFont(QFont("Times", 25))
    mlabel.setStyleSheet("background : rgb(230,255,255);"
                         "border : 1px solid black;")
    mlabel.show()

    label1 = QLabel(frame4)
    label1.setText("Result")
    label1.setGeometry(690, 135, 200, 50)
    label1.setFont(QFont("Times", 23))
    label1.setAlignment(QtCore.Qt.AlignCenter)
    label1.setStyleSheet("background : rgb(230,255,255);"
                         "border : 3px solid black;"
                         "border-radius : 10px;")
    label1.show()

    label2 = QLabel(frame4)
    label2.setGeometry(150, 230, 250, 650)
    label2.setFont(QFont("Times", 25))
    label2.setStyleSheet("background : rgb(230,255,255);"
                         "border : 1px solid black")
    label2.show()

    label3 = QLabel(frame4)
    label3.setGeometry(400, 230, 1000, 650)
    label3.setFont(QFont("Times", 25))
    label3.setStyleSheet("background : rgb(230,255,255);"
                         "border : 1px solid black")
    label3.show()

    global pnames
    pnames = df.loc[:, "name"].values
    pstatus = df.loc[:, "status"].values

    global List1, List2, List3
    sList1 = pnames.tolist()
    List1 = [x.decode("utf-8") for x in sList1]
    List2 = pstatus.tolist()
    List3 = [(List1[i], List2[i]) for i in range(0, len(List1))]

    global List, ListCount, ListCount1
    List = []
    ListCount = []
    ListCount1 = []

    i = 0
    count1 = 0
    while (i < len(pnames)):
        temp = pnames[i][0:8]
        j = i
        count = 0
        while (j < len(pnames)):
            temp1 = pnames[j][0:8]
            if (temp == temp1):
                if temp1 not in List:
                    List.append(temp1)
                i = i + 1
                j = j + 1
                count = count + 1
                count1 = count1 + 1
            else:
                i = i - 1
                j = j + 1
                break;
        ListCount.append(count)
        ListCount1.append(count1)
        i = i + 1

    global stringlist
    stringlist = [x.decode("utf-8") for x in List]

    global drop
    drop = QComboBox(frame4)
    drop.setGeometry(150, 270, 250, 40)
    drop.addItems(stringlist)
    drop.setFont(QFont("Times", 15))
    drop.setStyleSheet("background : lightgrey;")
    drop.show()

    button1 = QPushButton(frame4)
    button1.setText("Get Value")
    button1.setGeometry(150, 400, 250, 40)
    button1.setFont(QFont("Times", 15))
    button1.setStyleSheet("QPushButton::hover"
                          "{"
                          "background-color : skyblue;"
                          "}")
    button1.show()
    button1.clicked.connect(getvalue)


def inputpage():
    imlabel1.hide()
    imlabel2.show()
    imlabel3.hide()

    ilabel1.hide()
    ilabel2.hide()
    ilabel3.hide()
    ilabel4.hide()
    ilabel5.hide()

    frame.hide()
    frame2.hide()
    frame4.hide()
    frame3.show()

    # Create the Heading Label
    hlabel = QLabel(frame3)
    hlabel.setText("PARKINSON DISEASE PREDICTION SOFTWARE")
    hlabel.setGeometry(150, 20, 1220, 60)
    hlabel.setFont(QFont("Times", 25))
    hlabel.setAlignment(QtCore.Qt.AlignCenter)
    hlabel.setStyleSheet("background : rgb(230,255,255);"
                         "border : 3px solid black")
    hlabel.show()

    # Create the Mid Label
    mlabel = QLabel(frame3)
    mlabel.setGeometry(150, 130, 1220, 700)
    mlabel.setStyleSheet("background : rgb(230,255,255);"
                         "border : 3px solid black")
    mlabel.show()

    label1 = QLabel(frame3)
    label1.setText("DataSet")
    label1.setGeometry(670, 165, 200, 50)
    label1.setFont(QFont("Times", 23))
    label1.setAlignment(QtCore.Qt.AlignCenter)
    label1.setStyleSheet("background : rgb(230,255,255);"
                         "border : 3px solid black;"
                         "border-radius : 10px;")
    label1.show()

    label2 = QLabel(frame3)
    label2.setText("Enter the dataset which you want to make prediction:")
    label2.setGeometry(400, 270, 790, 50)
    label2.setFont(QFont("Times", 18))
    label2.setStyleSheet("background : rgb(230,255,255);")
    label2.show()

    label3 = QLabel(frame3)
    label3.setText("Select the file:")
    label3.setGeometry(300, 465, 210, 50)
    label3.setFont(QFont("Times", 18))
    label3.setStyleSheet("background : rgb(230,255,255);")
    label3.show()

    label4 = QLabel(frame3)
    label4.setText("")
    label4.setGeometry(530,475,510, 35)
    label4.setFont(QFont("Times", 12))
    label4.setAlignment(QtCore.Qt.AlignCenter)
    label4.setStyleSheet("color : blue;"
                         "background : rgb(230,255,255);"
                         "border : 1px solid black")
    label4.show()

    label5 = QLabel(frame3)
    label5.setText("")
    label5.setGeometry(620, 570, 300, 40)
    label5.setFont(QFont("Times", 12))
    label5.setAlignment(QtCore.Qt.AlignCenter)
    label5.setStyleSheet("color : blue;"
                         "background : rgb(230,255,255);"
                         "border : 1px solid black")
    label5.show()

    def browsefile():
        path = QFileDialog.getOpenFileName(window, 'Open a file', '',
                                           'All Files (*.*)')
        filename = path[0]
        data = arff.loadarff(filename)
        global df
        df = pd.DataFrame(data[0])

        # Divide the data into Independent(X) and Dependent(Y) data sets
        x = df.loc[:, df.columns != 'status'].values[:, 1:]  # Feature
        y = df.loc[:, 'status'].values  # Label

        # Scale the data values
        scaler = MinMaxScaler((-1, 1))
        x = scaler.fit_transform(x)
        y = y

        Modelname = "model1.pkl"

        # Load the Model back from file
        with open(Modelname, 'rb') as file:
            newmodel = pickle.load(file)

        # Predict the Label using the reloaded Model
        Ypredict = newmodel.predict(x)
        df["status"] = Ypredict
        print(Ypredict)

        label4.setText(filename)

    def uploadfile():
        resbutton.setEnabled(True)
        label5.setText("File Uploaded")

    button1 = QPushButton(frame3)
    button1.setText("Browse File")
    button1.setGeometry(1060, 475, 150, 35)
    button1.setFont(QFont("Times", 15))
    button1.setStyleSheet("QPushButton::hover"
                          "{"
                          "background-color : skyblue;"
                          "}")
    button1.show()
    button1.clicked.connect(browsefile)

    button2 = QPushButton(frame3)
    button2.setText("Upload File")
    button2.setGeometry(940, 570, 150, 35)
    button2.setFont(QFont("Times", 15))
    button2.setStyleSheet("QPushButton::hover"
                          "{"
                          "background-color : skyblue;"
                          "}")
    button2.show()
    button2.clicked.connect(uploadfile)


def ibackpage():
    frame1.hide()
    frame2.hide()
    frame3.hide()
    frame4.hide()
    frame.show()


def history():
    ilabel1.show()
    ilabel2.hide()
    ilabel3.hide()
    ilabel4.hide()
    ilabel5.hide()
    label.clear()
    text1 = info.history1()
    label.setText("{}".format(text1))


def symptoms():
    ilabel1.hide()
    ilabel2.show()
    ilabel3.hide()
    ilabel4.hide()
    ilabel5.hide()
    label.clear()
    text1 = info.symptom1()
    label.setText("{}".format(text1))


def diagnosis():
    ilabel1.hide()
    ilabel2.hide()
    ilabel3.show()
    ilabel4.hide()
    ilabel5.hide()
    label.clear()
    text1 = info.diagnosis1()
    label.setText("{}".format(text1))


def treatment():
    ilabel1.hide()
    ilabel2.hide()
    ilabel3.hide()
    ilabel4.show()
    ilabel5.hide()
    label.clear()
    text1 = info.treatment1()
    label.setText("{}".format(text1))


def statistics():
    ilabel1.hide()
    ilabel2.hide()
    ilabel3.hide()
    ilabel4.hide()
    ilabel5.show()
    label.clear()
    text1 = info.statistics1()
    label.setText("{}".format(text1))


def signin():
    imlabel1.show();
    imlabel2.hide();
    imlabel3.hide();
    if (nentry.text() == "Admin" and pentry.text() == "123"):
        frame.hide()
        frame3.hide()
        frame4.hide()
        frame1.show()
        frame2.show()

        # Create the Heading Label
        hlabel = QLabel(frame2)
        hlabel.setText("PARKINSON DISEASE PREDICTION SOFTWARE")
        hlabel.setGeometry(150, 20, 1220, 60)
        hlabel.setFont(QFont("Times", 25))
        hlabel.setAlignment(QtCore.Qt.AlignCenter)
        hlabel.setStyleSheet("background : rgb(230,255,255);"
                             "border : 3px solid black")
        hlabel.show()

        # Menu
        menu = QLabel(frame1)
        menu.setText("MENU")
        menu.setGeometry(50, 70, 300, 70)
        menu.setFont(QFont("Times", 20))
        menu.setAlignment(QtCore.Qt.AlignCenter)
        menu.setStyleSheet("background : rgb(230,255,255);"
                           "border-radius : 25px;")
        menu.show()

        # Menu Buttons
        infobutton = QPushButton(frame1)
        infobutton.setText("Information")
        infobutton.setGeometry(50, 170, 300, 70)
        infobutton.setFont(QFont("Times", 17))
        infobutton.setStyleSheet("QPushButton::hover"
                                 "{"
                                 "background-color : skyblue;"
                                 "}")
        infobutton.show()
        infobutton.clicked.connect(signin)

        databutton = QPushButton(frame1)
        databutton.setText("DataSet")
        databutton.setGeometry(50, 270, 300, 70)
        databutton.setFont(QFont("Times", 17))
        databutton.setStyleSheet("QPushButton::hover"
                                 "{"
                                 "background-color : skyblue;"
                                 "}")
        databutton.show()
        databutton.clicked.connect(inputpage)

        global resbutton
        resbutton = QPushButton(frame1)
        resbutton.setText("Result")
        resbutton.setGeometry(50, 370, 300, 70)
        resbutton.setFont(QFont("Times", 17))
        resbutton.setEnabled(False)
        resbutton.setStyleSheet("QPushButton::hover"
                                "{"
                                "background-color : skyblue;"
                                "}")
        resbutton.show()
        resbutton.clicked.connect(inputpage2)

        soutbutton = QPushButton(frame1)
        soutbutton.setText("SIGN OUT")
        soutbutton.setGeometry(50, 600, 300, 60)
        soutbutton.setFont(QFont("Times", 17))
        soutbutton.setStyleSheet("QPushButton::hover"
                                 "{"
                                 "background-color : skyblue;"
                                 "}")
        soutbutton.show()
        soutbutton.clicked.connect(ibackpage)

        # Frame2 Buttons
        button = QPushButton(frame2)
        button.setText("History")
        button.setGeometry(150, 130, 210, 70)
        button.setFont(QFont("Times", 15))
        button.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        button.setStyleSheet("QPushButton::hover"
                             "{"
                             "background-color : skyblue;"
                             "}")
        button.show()
        button.clicked.connect(history)

        button = QPushButton(frame2)
        button.setText("Symptoms")
        button.setGeometry(400, 130, 210, 70)
        button.setFont(QFont("Times", 15))
        button.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        button.setStyleSheet("QPushButton::hover"
                             "{"
                             "background-color : skyblue;"
                             "}")
        button.show()
        button.clicked.connect(symptoms)

        button = QPushButton(frame2)
        button.setText("Diagnosis")
        button.setGeometry(650, 130, 210, 70)
        button.setFont(QFont("Times", 15))
        button.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        button.setStyleSheet("QPushButton::hover"
                             "{"
                             "background-color : skyblue;"
                             "}")
        button.show()
        button.clicked.connect(diagnosis)

        button = QPushButton(frame2)
        button.setText("Treatment")
        button.setGeometry(900, 130, 210, 70)
        button.setFont(QFont("Times", 15))
        button.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        button.setStyleSheet("QPushButton::hover"
                             "{"
                             "background-color : skyblue;"
                             "}")
        button.show()
        button.clicked.connect(treatment)

        button = QPushButton(frame2)
        button.setText("Statistics")
        button.setGeometry(1150, 130, 210, 70)
        button.setFont(QFont("Times", 15))
        button.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        button.setStyleSheet("QPushButton::hover"
                             "{"
                             "background-color : skyblue;"
                             "}")
        button.show()
        button.clicked.connect(statistics)

        # Frame2 Labels
        global ilabel1, ilabel2, ilabel3, ilabel4, ilabel5
        ilabel1 = QLabel(frame2)
        ilabel1.setGeometry(150, 200, 210, 4)
        ilabel1.setStyleSheet("background-color : red;"
                              "border : 0px solid black;"
                              "border-radius : 3px;")

        ilabel2 = QLabel(frame2)
        ilabel2.setGeometry(400, 200, 210, 4)
        ilabel2.setStyleSheet("background-color : red;"
                              "border : 0px solid black;"
                              "border-radius : 3px;")

        ilabel3 = QLabel(frame2)
        ilabel3.setGeometry(650, 200, 210, 4)
        ilabel3.setStyleSheet("background-color : red;"
                              "border : 0px solid black;"
                              "border-radius : 3px;")

        ilabel4 = QLabel(frame2)
        ilabel4.setGeometry(900, 200, 210, 4)
        ilabel4.setStyleSheet("background-color : red;"
                              "border : 0px solid black;"
                              "border-radius : 3px;")

        ilabel5 = QLabel(frame2)
        ilabel5.setGeometry(1150, 200, 210, 4)
        ilabel5.setStyleSheet("background-color : red;"
                              "border : 0px solid black;"
                              "border-radius : 3px;")

        global label
        # Create the Mid Label
        mlabel = QScrollArea(frame2)
        mlabel.setWidgetResizable(True)
        content = QWidget(mlabel)
        content.setStyleSheet("background : rgb(230,255,255);"
                              "border : 0px solid black")
        mlabel.setWidget(content)
        lay = QVBoxLayout(content)
        label = QLabel(content)
        label.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        label.setFont(QFont("Times", 18))
        label.setWordWrap(True)
        lay.addWidget(label)
        mlabel.setGeometry(150, 240, 1210, 650)
        mlabel.setStyleSheet("background : rgb(230,255,255);"
                             "border : 3px solid black;")
        mlabel.show()

        ilabel1.show()
        ilabel2.hide()
        ilabel3.hide()
        ilabel4.hide()
        ilabel5.hide()
        label.clear()
        text1 = info.history1()
        label.setText("{}".format(text1))

    else:
        mbox = QMessageBox()
        mbox.setText("Wrong Username or Password")
        mbox.setDetailedText("You have entered Wrong Username or Password. Try Again!!")
        mbox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        mbox.exec()


def show_hide():
    if (check.isChecked() == True):
        pentry.setEchoMode(QLineEdit.Normal)
    else:
        pentry.setEchoMode(QLineEdit.Password)


# Create the Application Main Window
app = QApplication(sys.argv)
w, h = app.primaryScreen().availableGeometry().width(), app.primaryScreen().availableGeometry().height()
window = QWidget()
window.setGeometry(0, 30, w, h)
window.setWindowTitle("Parkinson Prediction Software")
print(w, h)

# Create the Frame
frame = QFrame(window)
frame.setGeometry(0, 0, w, h)
frame.setStyleSheet("background-color: rgb(200,255,255);")
frame.show()

label = QLabel(frame)
label.setPixmap(QPixmap("1.jpg"))
label.setScaledContents(True)
label.setGeometry(0, 0, w, h)
label.show()

frame1 = QFrame(window)
frame1.setGeometry(0, 0, w, h)
frame1.setStyleSheet("background-color: rgb(200,255,255)")
frame1.hide()

label1 = QLabel(frame1)
label1.setPixmap(QPixmap("br.jpg"))
label1.setScaledContents(True)
label1.setGeometry(0, 0, w, h)
label1.show()

frame2 = QFrame(window)
frame2.setGeometry(450, 0, w, h)
frame2.setStyleSheet("background-color: rgba(200,255,255,0)")
frame2.hide()

frame3 = QFrame(window)
frame3.setGeometry(450, 0, w - 450, h)
frame3.setStyleSheet("background-color: rgba(141, 242, 242,0)")
frame3.hide()

frame4 = QFrame(window)
frame4.setGeometry(450, 0, w - 450, h)
frame4.setStyleSheet("background-color: rgba(141, 242, 242,0)")
frame4.hide()

# Create the Heading Label
hlabel = QLabel(frame)
hlabel.setText("PARKINSON DISEASE PREDICTION SOFTWARE")
hlabel.setGeometry(370, 20, 1300, 70)
hlabel.setFont(QFont("Times", 35))
# hlabel.setAttribute(Qt.WA_TranslucentBackground);
hlabel.setAlignment(QtCore.Qt.AlignCenter)
hlabel.setStyleSheet("background : rgba(0,191,255,100);"
                     "border : 3px solid black;"
                     "border-radius : 15px;")
hlabel.show()

# Create the Mid Label
mlabel = QLabel(frame)
mlabel.setGeometry(680, 320, 530, 270)
mlabel.setStyleSheet("background-color : rgba(0,191,255,0);"
                     "border : 2px solid black;"
                     "border-radius : 15px;")
mlabel.show()

imlabel1 = QLabel(frame1)
imlabel1.setGeometry(50, 240, 300, 5)
imlabel1.setStyleSheet("background-color : red;"
                       "border : 0px solid black;"
                       "border-radius : 3px;")
imlabel2 = QLabel(frame1)
imlabel2.setGeometry(50, 340, 300, 5)
imlabel2.setStyleSheet("background-color : red;"
                       "border : 0px solid black;"
                       "border-radius : 3px;")

imlabel3 = QLabel(frame1)
imlabel3.setGeometry(50, 440, 300, 5)
imlabel3.setStyleSheet("background-color : red;"
                       "border : 0px solid black;"
                       "border-radius : 3px;")

imlabel1.hide();
imlabel2.hide();
imlabel3.hide();

# Create the Login Menu
name = QLabel(frame)
name.setText("NAME")
name.setGeometry(760, 360, 150, 40)
name.setFont(QFont("Times", 15))
name.setAlignment(QtCore.Qt.AlignCenter)
name.setStyleSheet("background-color : rgba(0,191,255,100);"
                   "color:white;"
                   "border : 1px solid black;"
                   "border-radius : 7px;")
name.show()

password = QLabel(frame)
password.setText("PASSWORD")
password.setGeometry(760, 440, 150, 40)
password.setFont(QFont("Times", 15))
password.setAlignment(QtCore.Qt.AlignCenter)
password.setStyleSheet("background-color : rgba(0,191,255,100);"
                       "color:white;"
                       "border : 1px solid black;"
                       "border-radius : 7px;")
password.show()

nentry = QLineEdit(frame)
nentry.setText("")
nentry.setGeometry(950, 360, 180, 40)
nentry.setFont(QFont("Times", 15))
nentry.setStyleSheet("background : white;")

pentry = QLineEdit(frame)
pentry.setText("")
pentry.setGeometry(950, 440, 180, 40)
pentry.setFont(QFont("Times", 15))
pentry.setEchoMode(QLineEdit.Password)
pentry.setStyleSheet("background : white;")

# Password Combobox
check = QCheckBox("show password", frame)
check.setGeometry(960, 510, 170, 25)
check.setFont(QFont("Times", 12))
check.stateChanged.connect(show_hide)
check.setStyleSheet("background-color : rgba(0,191,255,100);"
                    "color: white;"
                    "border-radius: 3px;"
                    )

# Create the Sign IN Button
button = QPushButton(frame)
button.setText("SIGN IN")
button.setGeometry(820, 640, 250, 40)
button.setFont(QFont("Times", 15))
button.setStyleSheet("QPushButton::hover"
                     "{"
                     "background-color : skyblue;"
                     "}")
button.show()
button.clicked.connect(signin)

app.setStyle("Fusion")

window.show()
sys.exit(app.exec())