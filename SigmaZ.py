import math
import sys
import os
import sympy
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton,
    QGridLayout, QStackedWidget, QVBoxLayout, QLineEdit)
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt, QTimer, QUrl
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput


class Calculator(QWidget):
    def __init__(calc):
        super().__init__()
        #Track current mode to handle button behavior differently
        calc.current_mode = "normal"  # Can be "normal" or "poly"
        
        #normal buttons
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

        calc.buttonmode = QPushButton("mode", calc)
        calc.buttonmode.clicked.connect(calc.mode_toggle)

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

        #StackedWidget setup for swithing modes
        calc.StackedWidget = QStackedWidget(calc)
        calc.normal_mode = QWidget()
        calc.normal_mode_layout()
        calc.poly_mode = QWidget()
        calc.poly_mode_layout()
        calc.StackedWidget.addWidget(calc.normal_mode)
        calc.StackedWidget.addWidget(calc.poly_mode)

        #Layout setup
        container = QWidget()
        container.setObjectName("calculator_screen_container")
        layout = QVBoxLayout(container)
        layout.addWidget(calc.history)
        layout.addWidget(calc.display)

        main = QVBoxLayout()
        main.setSpacing(12)
        main.addWidget(container)
        main.addWidget(calc.StackedWidget)
        calc.setLayout(main)

        calc.Style()
        calc.initSound()

    def mode_toggle(calc):
        current_mode = calc.StackedWidget.currentIndex()
        calc.StackedWidget.setCurrentIndex(1 - current_mode)
        # mode tracker
        calc.current_mode = "poly" if current_mode == 0 else "normal"
        # Clear display when switching modes
        calc.display.setText("0")

    def normal_mode_layout(calc):
        Grid = QGridLayout(calc.normal_mode)

        Grid.addWidget(calc.buttonmode, 0, 0)
        Grid.addWidget(calc.buttonsin, 0, 1)
        Grid.addWidget(calc.buttoncos, 0, 2)
        Grid.addWidget(calc.buttontan, 0, 3)

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

    #create independent buttons
    def poly_mode_layout(calc):
        layout = QGridLayout(calc.poly_mode)
        
        # Create NEW buttons specific to poly mode , completely independent from normal mode
        poly_buttonmode = QPushButton("mode", calc)
        poly_buttonx = QPushButton("x", calc)
        poly_buttonpower = QPushButton("^", calc)
        poly_buttonadd = QPushButton("+", calc)
        poly_buttonsub = QPushButton("-", calc)
        poly_buttonequal = QPushButton("=", calc)
        poly_buttonclear = QPushButton("C", calc)
        poly_buttonbackspace = QPushButton("←", calc)
        poly_buttonsolve = QPushButton("Solve", calc)
        
        poly_button0 = QPushButton("0", calc)
        poly_button1 = QPushButton("1", calc)
        poly_button2 = QPushButton("2", calc)
        poly_button3 = QPushButton("3", calc)
        poly_button4 = QPushButton("4", calc)
        poly_button5 = QPushButton("5", calc)
        poly_button6 = QPushButton("6", calc)
        poly_button7 = QPushButton("7", calc)
        poly_button8 = QPushButton("8", calc)
        poly_button9 = QPushButton("9", calc)
        
        #Connect all poly buttons to DisplayText (separate from normal mode buttons)
        poly_buttons_display = [
            poly_buttonx, poly_buttonpower, poly_buttonadd, poly_buttonsub,
            poly_buttonequal, poly_buttonclear, poly_buttonbackspace,
            poly_button0, poly_button1, poly_button2, poly_button3, poly_button4,
            poly_button5, poly_button6, poly_button7, poly_button8, poly_button9
        ]
        
        #Connect DisplayText and SoundEffects to poly buttons
        for btn in poly_buttons_display:
            btn.clicked.connect(calc.DisplayText)
            btn.clicked.connect(calc.SoundEffects)
        
        #Connect special buttons
        poly_buttonsolve.clicked.connect(calc.SolvePolynomial)
        poly_buttonsolve.clicked.connect(calc.SoundEffects)
        poly_buttonmode.clicked.connect(calc.mode_toggle)
        poly_buttonmode.clicked.connect(calc.SoundEffects)
        
        #Layout
        # Row 0: mode
        layout.addWidget(poly_buttonmode, 0, 0, 1, 4)
        
        # Row 1: x, ^, +, -
        layout.addWidget(poly_buttonx, 1, 0)
        layout.addWidget(poly_buttonpower, 1, 1)
        layout.addWidget(poly_buttonadd, 1, 2)
        layout.addWidget(poly_buttonsub, 1, 3)
        
        # Row 2: C, ←, =, Solve
        layout.addWidget(poly_buttonclear, 2, 0)
        layout.addWidget(poly_buttonbackspace, 2, 1)
        layout.addWidget(poly_buttonequal, 2, 2)
        layout.addWidget(poly_buttonsolve, 2, 3 )
        
        # Row 3-6: Number pad (7-9, 4-6, 1-3, 0)
        layout.addWidget(poly_button7, 3, 0)
        layout.addWidget(poly_button8, 3, 1)
        layout.addWidget(poly_button9, 3, 2)
        layout.addWidget(poly_button0, 3, 3) 
        
        layout.addWidget(poly_button4, 4, 0)
        layout.addWidget(poly_button5, 4, 1)
        layout.addWidget(poly_button6, 4, 2)
        
        layout.addWidget(poly_button1, 5, 0)
        layout.addWidget(poly_button2, 5, 1)
        layout.addWidget(poly_button3, 5, 2)
        
        layout.setSpacing(16)
        layout.setContentsMargins(10, 10, 10, 10)

    def SolvePolynomial(calc):
        try:
            expression = calc.display.text()
            
            # Check if expression contains '='
            if '=' not in expression:
                calc.display.setText("Error: Need =")
                QTimer.singleShot(1500, lambda: calc.display.setText("0"))
                return
             # Split by '=' and parse
            left, right = expression.split('=')

            def add_multiplication(expr):
                result = ""
                for i in range(len(expr)):
                    result += expr[i]  # Add current character
                    # Check if we need to add '*'
                    if i < len(expr) - 1:  # Make sure there's a next character
                        if expr[i].isdigit() and expr[i+1] == 'x':
                            result += '*'  # Add multiplication sign
                return result

            left = add_multiplication(left)
            right = add_multiplication(right)
            #replace ^ with **
            left = left.replace('^', '**')
            right = right.replace('^', '**')
            
            # Create equation: left - right = 0
            x = sympy.Symbol('x')
            equation = sympy.sympify(left) - sympy.sympify(right)
            
            # Solve the equation
            solutions = sympy.solve(equation, x)
            
            if not solutions:
                calc.display.setText("No solution")
                QTimer.singleShot(1500, lambda: calc.display.setText("0"))
                return
            
            # Format solutions
            if len(solutions) == 1:
                result = f"x = {solutions[0]}"
            else:
                result = "x = " + ", ".join([str(sol) for sol in solutions])
                if "I" in result: result= result.replace("I", "i")
            
            # Update display and history
            calc.display.setText(result)
            calc.history_list.append(f"{expression} → {result}")
            calc.history_list = calc.history_list[-3:]
            calc.history.setText("  ||  ".join(calc.history_list))
            
        except Exception as e:
            calc.display.setText("Error")
            QTimer.singleShot(1500, lambda: calc.display.setText("0"))

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
                    if current_text in ["0", "Error", "No solution"]:
                        return
                    if len(current_text) == 1:
                        calc.display.setText("0")
                    else:
                        calc.display.setText(current_text[:-1])
                    return

                #Auto-bracket (only in normal mode)
                elif sender.text() in ["sin", "cos", "tan", "log", "ln"]:
                    if current_text == "0":
                        calc.display.setText(sender.text() + "(")
                    else:
                        calc.display.setText(current_text + sender.text() + "(")
                    return

                #HANDLE EVALUATION (=) - Different behavior based on mode
                elif sender.text() == "=":
                    # In polynomial mode, just add = to the expression (don't evaluate)
                    if calc.current_mode == "poly":
                        if current_text == "0":
                            return  # Don't start with =
                        if "=" in current_text:
                            return  # Only one = allowed
                        calc.display.setText(current_text + "=")
                        return
                    
                    # In normal mode, evaluate the expression
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
                    if current_text in ["0", "Error", "No solution"]:
                        #In poly mode, allow starting with 'x' or numbers
                        if calc.current_mode == "poly":
                            if input_char in "+-×/)^.":
                                return
                            calc.display.setText(input_char)
                        else:
                            # In normal mode, don't allow starting with operators
                            if input_char in "+-×/)=^.":
                                return
                            calc.display.setText(input_char)
                    else:
                        #In poly mode, allow 'x' to be added
                        # Prevent double operators (e.g., ++ or *+)
                        if input_char in "+-×/^." and current_text[-1] in "+-×/^.":
                            return
                        
                        # Special rule for %: only allow operators after it (normal mode only)
                        if current_text[-1] == "%" and input_char not in "+-×/":
                            return
                        
                        #In poly mode, prevent adding operators after '='
                        if calc.current_mode == "poly" and "=" in current_text:
                            # After =, only allow numbers, x, +, -, ^
                            if input_char not in "0123456789x+-^":
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
    calc.resize(350, 300)
    icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "SigmaZ_icon.ico")
    calc.setWindowIcon(QIcon(icon_path))
    calc.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()