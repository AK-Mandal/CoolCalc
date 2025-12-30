import math
import sys
import os
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton,
    QGridLayout, QStackedWidget, QVBoxLayout, QLineEdit)
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt, QTimer, QUrl
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput


class Calculator(QWidget):
    def __init__(calc):
        super().__init__()
        calc.button0 = QPushButton("0", calc)
        calc.button1 = QPushButton("1", calc)
        calc.button2 = QPushButton("2", calc)
        calc.button3 = QPushButton("3", calc)
        calc.button4 = QPushButton("4", calc)
        calc.button5 = QPushButton("5", calc)
        calc.button6 = QPushButton("6", calc)
        calc.button7 = QPushButton("7", calc)
        calc.button8 = QPushButton("8", calc)
        calc.button9 = QPushButton("9", calc)
        calc.buttondot = QPushButton(".", calc)
        calc.buttonadd = QPushButton("+", calc)
        calc.buttonsub = QPushButton("-", calc)
        calc.buttonmul = QPushButton("×", calc)
        calc.buttondiv = QPushButton("/", calc)
        calc.buttonclear = QPushButton("C", calc)
        calc.buttonequal = QPushButton("=", calc)
        calc.buttonpercent = QPushButton("%", calc)
        calc.buttonpower = QPushButton("^", calc)
        calc.buttonbracket1 = QPushButton("(", calc)
        calc.buttonbracket2 = QPushButton(")", calc)
        calc.buttonbackspace = QPushButton("←", calc)
        calc.buttonlog = QPushButton("log", calc)
        calc.buttonln = QPushButton("ln", calc)
        calc.buttonsin = QPushButton("sin", calc)
        calc.buttoncos = QPushButton("cos", calc)
        calc.buttontan = QPushButton("tan", calc)

        calc.all_button = [
            calc.button0, calc.button1, calc.button2, calc.button3, calc.button4,
            calc.button5, calc.button6, calc.button7, calc.button8, calc.button9,
            calc.buttondot, calc.buttonadd, calc.buttonsub, calc.buttonmul,
            calc.buttondiv, calc.buttonclear, calc.buttonpower, calc.buttonlog,
            calc.buttonln, calc.buttonbracket1, calc.buttonbracket2,
            calc.buttonequal, calc.buttonbackspace, calc.buttonpercent,
            calc.buttontan, calc.buttonsin, calc.buttoncos
        ]

        for button in calc.all_button:
            button.clicked.connect(calc.DisplayText)
            button.clicked.connect(calc.SoundEffects)

        calc.display = QLineEdit(calc)
        calc.display.setReadOnly(True)
        calc.display.setAlignment(Qt.AlignmentFlag.AlignRight)
        calc.display.setText("0")

        calc.history = QLineEdit(calc)
        calc.history.setReadOnly(True)
        calc.history.setAlignment(Qt.AlignmentFlag.AlignRight)
        calc.history.setText("")
        calc.history_list = []
        calc.history.setObjectName("history")

        calc.ButtonLayout()
        calc.Style()
        calc.initSound()

    def ButtonLayout(calc):
        Grid = QGridLayout()

        Grid.addWidget(calc.buttonsin, 0, 0)
        Grid.addWidget(calc.buttoncos, 0, 1)
        Grid.addWidget(calc.buttontan, 0, 2, 1, 2)

        Grid.addWidget(calc.buttonlog, 1, 0)
        Grid.addWidget(calc.buttonln, 1, 1)
        Grid.addWidget(calc.buttonpercent, 1, 2)
        Grid.addWidget(calc.buttonbackspace, 1, 3)

        Grid.addWidget(calc.buttonbracket1, 2, 0)
        Grid.addWidget(calc.buttonbracket2, 2, 1)
        Grid.addWidget(calc.buttonpower, 2, 2)
        Grid.addWidget(calc.buttonclear, 2, 3)

        Grid.addWidget(calc.button7, 3, 0)
        Grid.addWidget(calc.button8, 3, 1)
        Grid.addWidget(calc.button9, 3, 2)
        Grid.addWidget(calc.buttondiv, 3, 3)

        Grid.addWidget(calc.button4, 4, 0)
        Grid.addWidget(calc.button5, 4, 1)
        Grid.addWidget(calc.button6, 4, 2)
        Grid.addWidget(calc.buttonmul, 4, 3)

        Grid.addWidget(calc.button1, 5, 0)
        Grid.addWidget(calc.button2, 5, 1)
        Grid.addWidget(calc.button3, 5, 2)
        Grid.addWidget(calc.buttonsub, 5, 3)

        Grid.addWidget(calc.button0, 6, 0)
        Grid.addWidget(calc.buttondot, 6, 1)
        Grid.addWidget(calc.buttonequal, 6, 2)
        Grid.addWidget(calc.buttonadd, 6, 3)

        Grid.setSpacing(16)
        Grid.setContentsMargins(10, 10, 10, 10)

        container = QWidget()
        container.setObjectName("calculator_screen_container")
        layout = QVBoxLayout(container)
        layout.addWidget(calc.history)
        layout.addWidget(calc.display)

        main = QVBoxLayout()
        main.setSpacing(12)
        main.addWidget(container)
        main.addLayout(Grid)
        calc.setLayout(main)

    def Style(calc):
        try:
            base_dir = os.path.dirname(os.path.abspath(__file__))
            for root, dirs, files in os.walk(base_dir):
                if "style.qss" in files:
                    with open(os.path.join(root, "style.qss"), "r", encoding="utf-8") as f:
                        calc.setStyleSheet(f.read())
                    break
        except Exception:
            pass

    def DisplayText(calc):
            sender = calc.sender()
            current_text = calc.display.text()

            try:
                # HANDLE CLEAR
                if sender.text() == "C":
                    calc.display.setText("0")
                    return

                #HANDLE BACKSPACE
                elif sender.text() == "←":
                    if current_text in ["0", "Error"]:
                        return
                    if len(current_text) == 1:
                        calc.display.setText("0")
                    else:
                        calc.display.setText(current_text[:-1])
                    return

                #Auto-bracket
                elif sender.text() in ["sin", "cos", "tan", "log", "ln"]:
                    if current_text == "0":
                        calc.display.setText(sender.text() + "(")
                    else:
                        calc.display.setText(current_text + sender.text() + "(")
                    return

                #HANDLE EVALUATION (=)
                elif sender.text() == "=":
                    user_expression = current_text

                    replacements = {
                        "^": "**",
                        "×": "*",
                        "%": "/100",
                        "log(": "math.log10(",
                        "ln(": "math.log(",
                        "sin(": "math.sin(math.radians(",
                        "cos(": "math.cos(math.radians(",
                        "tan(": "math.tan(math.radians("
                    }

                    eval_expr = user_expression
                    for old, new in replacements.items():
                        eval_expr = eval_expr.replace(old, new)

                    #Count unclosed parentheses specifically for radians  and close them so eval() doesn't fail
                    open_rad = eval_expr.count("math.radians(")
                    close_needed = eval_expr.count("(") - eval_expr.count(")")
                    if close_needed > 0:
                        eval_expr += ")" * close_needed

                    # Calculate result
                    raw_result = eval(eval_expr)
                    
                    # Format: limit decimals but remove trailing zeros
                    result_str = f"{raw_result:.6f}".rstrip('0').rstrip('.')

                    # If the result was 0.000000, result_str becomes empty, so we fix it:
                    if result_str == "":
                        result_str = "0"
                    
                    #display text
                    calc.display.setText(result_str)

                    # Update History (only if it was an actual calculation)
                    if any(op in user_expression for op in "+-×/^%"):
                        calc.history_list.append(f"{user_expression} = {result_str}")
                        calc.history_list = calc.history_list[-3:]  # Keep last 3
                        calc.history.setText("  ||  ".join(calc.history_list))
                    return

                # HANDLE GENERAL INPUT (Numbers and Operators)
                else:
                    input_char = sender.text()

                    # If current display is 0 or Error, replace it with the new digit
                    if current_text in ["0", "Error"]:
                        if input_char in "+-×/)=^.": # Don't start with these
                            return
                        calc.display.setText(input_char)
                    else:
                        # Prevent double operators (e.g., ++ or *+)
                        if input_char in "+-×/^." and current_text[-1] in "+-×/^.":
                            return
                        
                        # Special rule for %: only allow operators after it
                        if current_text[-1] == "%" and input_char not in "+-×/":
                            return
                            
                        calc.display.setText(current_text + input_char)

            except ZeroDivisionError:
                calc.display.setText("Error: Div by 0")
                QTimer.singleShot(1500, lambda: calc.display.setText("0"))
            except Exception:
                calc.display.setText("Error")
                QTimer.singleShot(1500, lambda: calc.display.setText("0"))

    def initSound(calc):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        files = ["Button_Sound1.wav", "Button_Sound2.wav", "Button_Sound3.wav"]
        paths = []

        for root, dirs, fs in os.walk(base_dir):
            for f in files:
                if f in fs:
                    paths.append(os.path.join(root, f))
            if len(paths) == 3:
                break

        calc.sound1 = QMediaPlayer()
        calc.audio1 = QAudioOutput()
        calc.audio1.setVolume(0.5)
        calc.sound1.setAudioOutput(calc.audio1)
        calc.sound1.setSource(QUrl.fromLocalFile(paths[0]))

        calc.sound2 = QMediaPlayer()
        calc.audio2 = QAudioOutput()
        calc.audio2.setVolume(0.5)
        calc.sound2.setAudioOutput(calc.audio2)
        calc.sound2.setSource(QUrl.fromLocalFile(paths[1]))

        calc.sound3 = QMediaPlayer()
        calc.audio3 = QAudioOutput()
        calc.audio3.setVolume(0.5)
        calc.sound3.setAudioOutput(calc.audio3)
        calc.sound3.setSource(QUrl.fromLocalFile(paths[2]))

    def SoundEffects(calc):
        sender = calc.sender()
        if sender.text() in "0123456789.":
            calc.sound1.stop()
            calc.sound1.play()
        elif sender.text() in "C←":
            calc.sound3.stop()
            calc.sound3.play()
        else:
            calc.sound2.stop()
            calc.sound2.play()


def main():
    app = QApplication(sys.argv)
    calc = Calculator()
    calc.setWindowTitle("SigmaZ")
    calc.setFixedSize(350, 500)
    icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "SigmaZ_icon.ico")
    calc.setWindowIcon(QIcon(icon_path))
    calc.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()