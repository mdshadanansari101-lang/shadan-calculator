__version__ = "1.0.0"

import ast
import operator

from kivy.app import App
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput


# ---------- CALCULATION ----------

OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.Mod: operator.mod,
    ast.USub: operator.neg,
    ast.UAdd: operator.pos,
}


def calculate(expression):

    expression = expression.replace("×", "*")
    expression = expression.replace("÷", "/")
    expression = expression.replace("^", "**")

    tree = ast.parse(expression, mode="eval")

    def solve(node):

        if isinstance(node, ast.Expression):
            return solve(node.body)

        if isinstance(node, ast.Constant):
            if isinstance(node.value, (int, float)):
                return node.value
            raise ValueError

        if isinstance(node, ast.BinOp):

            left = solve(node.left)
            right = solve(node.right)

            operation = OPERATORS.get(type(node.op))

            if operation is None:
                raise ValueError

            return operation(left, right)

        if isinstance(node, ast.UnaryOp):

            value = solve(node.operand)

            operation = OPERATORS.get(type(node.op))

            if operation is None:
                raise ValueError

            return operation(value)

        raise ValueError

    return solve(tree)


# ---------- CALCULATOR APP ----------

class CalculatorApp(App):

    def build(self):

        Window.fullscreen = "auto"

        self.memory = 0
        self.answer = 0

        # Main layout
        main = BoxLayout(
            orientation="vertical",
            padding=6,
            spacing=5
        )

        # ---------- DISPLAY ----------

        self.display = TextInput(
            text="",
            readonly=True,
            multiline=False,
            halign="right",
            font_size=30,
            size_hint_y=None,
            height=85
        )

        main.add_widget(self.display)

        # ---------- BUTTONS ----------

        buttons = GridLayout(
            cols=4,
            spacing=5
        )

        button_list = [

            "MC", "MR", "M+", "M-",

            "AC", "(", ")", "⌫",

            "7", "8", "9", "÷",

            "4", "5", "6", "×",

            "1", "2", "3", "-",

            "0", "00", ".", "+",

            "%", "^", "+/-", "=",

            "C", "Ans"
        ]

        for text in button_list:

            button = Button(
                text=text,
                font_size=21
            )

            button.bind(
                on_press=self.button_pressed
            )

            buttons.add_widget(button)

        main.add_widget(buttons)

        return main

    # ---------- BUTTON PRESS ----------

    def button_pressed(self, button):

        text = button.text

        # AC
        if text == "AC":

            self.display.text = ""
            self.answer = 0

            return

        # C
        if text == "C":

            self.display.text = ""

            return

        # BACKSPACE
        if text == "⌫":

            self.display.text = self.display.text[:-1]

            return

        # MEMORY CLEAR
        if text == "MC":

            self.memory = 0

            return

        # MEMORY RECALL
        if text == "MR":

            self.display.text += str(self.memory)

            return

        # MEMORY PLUS
        if text == "M+":

            try:

                value = calculate(
                    self.display.text
                )

                self.memory += value

            except:

                pass

            return

        # MEMORY MINUS
        if text == "M-":

            try:

                value = calculate(
                    self.display.text
                )

                self.memory -= value

            except:

                pass

            return

        # ANSWER
        if text == "Ans":

            self.display.text += str(
                self.answer
            )

            return

        # PLUS / MINUS
        if text == "+/-":

            try:

                value = calculate(
                    self.display.text
                )

                self.display.text = str(
                    -value
                )

            except:

                pass

            return

        # PERCENT
        if text == "%":

            try:

                value = calculate(
                    self.display.text
                )

                self.display.text = str(
                    value / 100
                )

            except:

                self.display.text += "%"

            return

        # EQUAL
        if text == "=":

            self.show_answer()

            return

        # NORMAL BUTTON
        self.display.text += text

    # ---------- CALCULATE ANSWER ----------

    def show_answer(self):

        if not self.display.text:
            return

        try:

            result = calculate(
                self.display.text
            )

            if (
                isinstance(result, float)
                and result.is_integer()
            ):
                result = int(result)

            self.answer = result

            self.display.text = str(result)

        except ZeroDivisionError:

            self.display.text = "Cannot divide by zero"

        except:

            self.display.text = "Error"


# ---------- START ----------

CalculatorApp().run()