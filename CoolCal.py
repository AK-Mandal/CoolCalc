import math
import sys
import os
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton,
    QGridLayout, QStackedWidget, QVBoxLayout, QLineEdit)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QTimer,QUrl
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer

class Calculator(QWidget):
    def __init__(calc):
        super().__init__()
        calc.button0 = QPushButton("0" , calc)
        calc.button1 = QPushButton("1" , calc)
        calc.button2 = QPushButton("2" , calc)
        calc.button3 = QPushButton("3" , calc)
        calc.button4 = QPushButton("4" , calc)
        calc.button5 = QPushButton("5" , calc)
        calc.button6 = QPushButton("6" , calc)
        calc.button7 = QPushButton("7" , calc)
        calc.button8 = QPushButton("8" , calc)
        calc.button9 = QPushButton("9" , calc)
        calc.buttondot = QPushButton("." , calc)
        calc.buttonadd = QPushButton("+", calc)
        calc.buttonsub = QPushButton("-", calc)
        calc.buttonmul = QPushButton("×", calc)
        calc.buttondiv = QPushButton("/", calc)
        calc.buttonclear = QPushButton("C", calc)
        calc.buttonequal = QPushButton("=" , calc)
        calc.buttonpercent = QPushButton("%", calc)
        calc.buttonpower = QPushButton("^", calc)
        calc.buttonbracket1 = QPushButton("(", calc)
        calc.buttonbracket2 = QPushButton(")", calc)
        calc.buttonbackspace = QPushButton("←", calc)
        calc.buttonlog = QPushButton("log", calc)
        calc.buttonln = QPushButton("ln", calc)
        
        calc.all_button = [calc.button0 ,calc.button1 ,calc.button2 ,calc.button3 ,calc.button4 ,calc.button5 ,
                      calc.button6 ,calc.button7 ,calc.button8 ,calc.button9 ,calc.buttondot ,calc.buttonadd ,
                      calc.buttonsub ,calc.buttonmul ,calc.buttondiv ,calc.buttonclear ,calc.buttonpower ,
                      calc.buttonlog ,calc.buttonln ,calc.buttonbracket1 ,calc.buttonbracket2 ,calc.buttonequal ,
                      calc.buttonbackspace ,calc.buttonpercent]
        for button in calc.all_button:
            button.clicked.connect(calc.ButtonClicked)
            button.clicked.connect(calc.SoundEffects)

        calc.display = QLineEdit(calc)
        calc.display.setReadOnly(True)
        calc.display.setAlignment(Qt.AlignRight)
        calc.display.setFixedHeight(80)
        calc.display.setText("0")

        calc.history = QLineEdit(calc)
        calc.history.setReadOnly(True)
        calc.history.setAlignment(Qt.AlignRight)
        calc.history.setFixedHeight(60)
        calc.history.setText("")
        calc.history_list = []
        calc.history.setObjectName("history")

        calc.ButtonLayout()
        calc.Style()
        calc.initSound()

    def ButtonLayout(calc):
        Grid = QGridLayout()
        Grid.addWidget(calc.button0, 6, 0)
        Grid.addWidget(calc.button1, 5, 0)
        Grid.addWidget(calc.button2, 5, 1)
        Grid.addWidget(calc.button3, 5, 2)
        Grid.addWidget(calc.button4, 4, 0)
        Grid.addWidget(calc.button5, 4, 1)
        Grid.addWidget(calc.button6, 4, 2)
        Grid.addWidget(calc.button7, 3, 0)
        Grid.addWidget(calc.button8, 3, 1)
        Grid.addWidget(calc.button9, 3, 2)
        Grid.addWidget(calc.buttondot, 6, 1)
        Grid.addWidget(calc.buttonadd, 6, 3)
        Grid.addWidget(calc.buttonsub, 5, 3)
        Grid.addWidget(calc.buttonmul, 4, 3)
        Grid.addWidget(calc.buttondiv, 3, 3)
        Grid.addWidget(calc.buttonclear, 2, 2)
        Grid.addWidget(calc.buttonequal, 6, 2)
        Grid.addWidget(calc.buttonpercent, 2, 1)
        Grid.addWidget(calc.buttonpower, 2, 0)
        Grid.addWidget(calc.buttonbracket1, 1, 0)
        Grid.addWidget(calc.buttonbracket2, 1, 1)
        Grid.addWidget(calc.buttonbackspace, 2, 3)
        Grid.addWidget(calc.buttonlog, 1, 2)
        Grid.addWidget(calc.buttonln, 1, 3)
        Grid.setSpacing(12)
        Grid.setContentsMargins(10, 10, 10, 10)

        calculator_screen_container = QWidget()
        calculator_screen_container.setObjectName("calculator_screen_container")

        calculator_screen_layout = QVBoxLayout(calculator_screen_container)
        calculator_screen_layout.addWidget(calc.history)
        calculator_screen_layout.addWidget(calc.display)
        calculator_screen_layout.setSpacing(0)

        MainLayout = QVBoxLayout()
        MainLayout.addWidget(calculator_screen_container)
        MainLayout.addLayout(Grid)
        calc.setLayout(MainLayout)
    

    def Style(calc):
        try:
            base_dir = os.path.dirname(os.path.abspath(__file__)) 
            target_path = "style.qss"
            found_path = None

            for root, dirs, files in os.walk(base_dir):
                if target_path in files:
                    found_path = os.path.join(root, target_path)
                    break  
            if found_path:
                with open(found_path, "r", encoding="utf-8") as file:
                    style = file.read()
                    calc.setStyleSheet(style)
                 
        except FileNotFoundError:
            print("Style file not found! Using default appearance.")
        except Exception as e:
            print(f"Error loading stylesheet: {e}")

    def ButtonClicked(calc):
        sender = calc.sender()
        try:
            if sender.text() == "=":
                user_expression = calc.display.text()
                expression = user_expression.replace("^", "**")
                expression = expression.replace("×", "*")
                expression = expression.replace("%", "/100")
                expression = expression.replace("log", "math.log10")
                expression = expression.replace("ln", "math.log")
                result = str(eval(expression))
                calc.display.setText(result)

                if any(op in user_expression for op in "+-×/="):
                        calc.history_list.append(f"{user_expression} = {result}")
                        calc.history_list = calc.history_list[-3:]
                        calc.history.setText("   ||   ".join(calc.history_list))
            elif sender.text() == "C":
                calc.display.setText("0")
            elif sender.text() == "←":
                if calc.display.text() == "0":
                    return
                else:
                    if len(calc.display.text()) == 1:
                        calc.display.setText("0")
                    else:
                        calc.display.setText(calc.display.text()[:-1]) 
            else:
                OPERATORS = "+-×/="
                if calc.display.text() == "0":
                    if sender.text() in OPERATORS:
                        return
                    calc.display.setText(sender.text())
                elif sender.text() in OPERATORS and calc.display.text()[-1] in OPERATORS:
                    return    
           
                else:                   
                    calc.display.setText(calc.display.text() + sender.text())
        except  Exception as exception:
            calc.display.setText(f"Error {exception}")
            QTimer.singleShot(2000, lambda: calc.display.setText("0"))
    
    def initSound(calc):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        targets = ["Button_Sound1.wav", "Button_Sound2.wav", "Button_Sound3.wav"]
        found_paths = []

        for root, dirs, files in os.walk(base_dir):
            for target in targets:
                if target in files:
                    full_path = os.path.join(root, target)
                    found_paths.append(full_path)
            if len(found_paths) == len(targets):
                break

        target_path1 = found_paths[0]
        target_path2 = found_paths[1]
        target_path3 = found_paths[2]

        calc.sound1 = QMediaPlayer()
        calc.sound1.setMedia(QMediaContent(QUrl.fromLocalFile(target_path1)))
        calc.sound1.setVolume(50)
        calc.sound2 = QMediaPlayer()
        calc.sound2.setMedia(QMediaContent(QUrl.fromLocalFile(target_path2)))
        calc.sound2.setVolume(50)
        calc.sound3 = QMediaPlayer()
        calc.sound3.setMedia(QMediaContent(QUrl.fromLocalFile(target_path3)))
        calc.sound3.setVolume(50)

    def SoundEffects(calc):
        sender = calc.sender()
        if sender.text() in "0123456789.":
            calc.sound1.stop()
            calc.sound1.play()
        if sender.text() in "C←":
            calc.sound3.stop()
            calc.sound3.play()
        if sender.text() in "+-×/=%^()" or sender.text() == "ln" or sender.text() == "log":
            calc.sound2.stop()
            calc.sound2.play()


def main():
    app = QApplication(sys.argv)
    calc = Calculator()
    calc.setWindowTitle("CoolCalc")
    calc.setGeometry(625, 400, 500, 600)
    calc.setWindowIcon(QIcon("CoolCalIcon.ico"))
    calc.show()
    sys.exit(app.exec_())
if __name__ == '__main__':
    main()