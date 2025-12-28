import sys
from PyQt5 import QtCore, QtGui, QtWidgets
import os
from chat_html import chat_html
import json
import pickle
import numpy as np
import qdarkstyle
from tensorflow.keras.models import load_model
import random
import nltk
from nltk.stem import WordNetLemmatizer

log_contents = ""
mode = 0

class settings:
    Training_folname = "C:\Assistant\Jarvis_Final\Training"
    logfilename = "C:\Assistant\Jarvis_Final\log.txt"

class response_predictor:
    resp_settings = settings()
    model = load_model(os.path.join(resp_settings.Training_folname, 'chatbot_model.h5'))
    lemmatizer = WordNetLemmatizer()
    intents = json.loads(open(os.path.join(resp_settings.Training_folname, 'intents.json')).read())
    words = pickle.load(open(os.path.join(resp_settings.Training_folname, 'words.pkl'), 'rb'))
    classes = pickle.load(open(os.path.join(resp_settings.Training_folname, 'classes.pkl'), 'rb'))

    user_input = ""
    input_words = ""

    username = "Raam"

    bag = []
    ints_list = []
    result = ""

# Other variables

    def clean_up_sentence(self):
        self.input_words = nltk.word_tokenize(self.user_input)
        self.input_words = [self.lemmatizer.lemmatize(word.lower()) for word in self.input_words]
        

    def bag_of_words(self, show_details=False):          # return bag of words array: 0 or 1 for each word in the bag that exists in the sentence
        self.clean_up_sentence()
        self.bag = [0]*len(self.words)                  # bag of words - matrix of N words, vocabulary matrix
        for s in self.input_words:
            for i,w in enumerate(self.words):
                if w == s:
                    self.bag[i] = 1            # assign 1 if current word is in the vocabulary position
                    if show_details:
                        print ("found in bag: %s" % w)
        self.bag = np.array(self.bag)

    def predict_class(self):
        self.bag_of_words(show_details=False)    # filter out predictions below a threshold
        res = self.model.predict(np.array([self.bag]))[0]
        ERROR_THRESHOLD = 0.25
        results = [[i,r] for i,r in enumerate(res) if r>ERROR_THRESHOLD]
        results.sort(key=lambda x: x[1], reverse=True)                # sort by strength of probability
        self.ints_list = []
        for r in results:
            self.ints_list.append({"intent": self.classes[r[0]], "probability": str(r[1])})

    def getResponse(self):
        tag = self.ints_list[0]['intent']
        list_of_intents = self.intents['intents']
        for i in list_of_intents:
            if(i['tag']== tag):
                self.result = random.choice(i['responses'])
                break

    def chatbot_response(self, umsg):
        self.user_input = umsg
        self.predict_class()
        self.getResponse()
        self.result = self.result.replace("user_name", self.username)
        
        return self.ints_list, self.result

class Ui_MainWindow(object):

    html_object = chat_html()
    
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(264, 429)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.textBrowser_messageView = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser_messageView.setObjectName("textBrowser_messageView")
        self.gridLayout.addWidget(self.textBrowser_messageView, 0, 0, 1, 2)
        self.lineEdit_userInput = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_userInput.setObjectName("lineEdit_userInput")
        self.gridLayout.addWidget(self.lineEdit_userInput, 1, 0, 1, 1)
        self.pushButton_Send = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_Send.setObjectName("pushButton_Send")
        self.gridLayout.addWidget(self.pushButton_Send, 1, 1, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 264, 21))
        self.menubar.setObjectName("menubar")
        self.menuAssistant = QtWidgets.QMenu(self.menubar)
        self.menuAssistant.setObjectName("menuAssistant")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionQuit = QtWidgets.QAction(MainWindow)
        self.actionQuit.setObjectName("actionQuit")
        self.actionHelp = QtWidgets.QAction(MainWindow)
        self.actionHelp.setObjectName("actionHelp")
        self.menuAssistant.addSeparator()
        self.menuAssistant.addAction(self.actionHelp)
        self.menuAssistant.addAction(self.actionQuit)
        self.menubar.addAction(self.menuAssistant.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        
        #  Changes after pyuic5

        self.pushButton_Send.clicked.connect(self.SendClicked)
        self.lineEdit_userInput.returnPressed.connect(self.SendClicked)
        self.lineEdit_userInput.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.textBrowser_messageView.textChanged.connect(self.bring_scrollbar_below)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton_Send.setText(_translate("MainWindow", "Send"))
        self.menuAssistant.setTitle(_translate("MainWindow", "Assistant"))
        self.actionQuit.setText(_translate("MainWindow", "Quit"))
        self.actionHelp.setText(_translate("MainWindow", "Help"))
        
    def bring_scrollbar_below(self):
        self.textBrowser_messageView.verticalScrollBar().setValue(self.textBrowser_messageView.verticalScrollBar().maximum())
        
    def SendClicked(self):
        global mode
        global log_contents
        predictor = response_predictor()
        Usermsg = self.lineEdit_userInput.text()
        log_contents+= '\nUser' + ': ' + Usermsg
        self.lineEdit_userInput.setText("")
        
        self.html_object.add_text('You: ' + Usermsg, 'user')
        self.textBrowser_messageView.setHtml(self.html_object.html_text)
		

        if Usermsg == "Exit" or Usermsg == "exit":
            sys.exit()
            
        if mode == 0:
            intent, res = predictor.chatbot_response(Usermsg)
            self.html_object.add_text("Jarvis: " + res, "bot")
            self.textBrowser_messageView.setHtml(self.html_object.html_text)
            log_contents+= str(intent)
            log_contents+= '\nJarvis: ' + res
            intent_tag = intent[0]['intent']
            self.bring_scrollbar_below()
            self.point_to_function(intent_tag)
        
    def point_to_function(self, intent_tag):
        pass
        
class MyWindow(QtWidgets.QMainWindow):        # inheriting from original QMainWindow class and overriding already present closeEvent() function to ensure saving of chat log and confirming exit
    def closeEvent(self,event):
        global log_contents
        sett = settings()
        print("closeEvent triggered")
        event.ignore()

        result = QtWidgets.QMessageBox.question(self, "Confirm Exit...", "Are you sure you want to exit ?", QtWidgets.QMessageBox.Yes| QtWidgets.QMessageBox.No)
        event.ignore()

        if result == QtWidgets.QMessageBox.Yes:
            logfile=open(sett.logfilename, 'a')
            logfile.write(log_contents)
            logfile.close()

            event.accept()
            
def run_assistant():
    #store log_contents
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = MyWindow()             # Creating an instance object of explicitly inherited class rather than the default QtWidgets.QMainWindow() class
    app.setStyleSheet(qdarkstyle.load_stylesheet())
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    ret = sys.exit(app.exec_())

if __name__ == "__main__":
    run_assistant()

