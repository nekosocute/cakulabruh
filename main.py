import sys
from PyQt6 import QtWidgets

from caculator import Caculator
from ui import QtUI


class MainWindow(QtWidgets.QMainWindow, QtUI):
    DEFAULT_VALUE: str = "0"
    CACULATOR: Caculator = Caculator()

    value_currnet: str = ""
    values_stats: list = []
    is_completed_caculate: bool = False

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)

        # Init event (Number)
        self.btn_num_0.clicked.connect(lambda: self.clickNum(0))
        self.btn_num_1.clicked.connect(lambda: self.clickNum(1))
        self.btn_num_2.clicked.connect(lambda: self.clickNum(2))
        self.btn_num_3.clicked.connect(lambda: self.clickNum(3))
        self.btn_num_4.clicked.connect(lambda: self.clickNum(4))
        self.btn_num_5.clicked.connect(lambda: self.clickNum(5))
        self.btn_num_6.clicked.connect(lambda: self.clickNum(6))
        self.btn_num_7.clicked.connect(lambda: self.clickNum(7))
        self.btn_num_8.clicked.connect(lambda: self.clickNum(8))
        self.btn_num_9.clicked.connect(lambda: self.clickNum(9))

        # Init event (Operator)
        self.btn_op_plus.clicked.connect(lambda: self.clickOp("+"))
        self.btn_op_Minus.clicked.connect(lambda: self.clickOp("-"))
        self.btn_op_Multiplied.clicked.connect(lambda: self.clickOp("*"))
        self.btn_op_Divide.clicked.connect(lambda: self.clickOp("/"))

        # Init event (Parenteses)
        self.btn_op_parentheses_start.clicked.connect(lambda: self.clickParenteses("("))
        self.btn_op_parentheses_stop.clicked.connect(lambda: self.clickParenteses(")"))

        # Init event (Reset & delete and sum)
        self.btn_reset.clicked.connect(self.reset)
        self.btn_del.clicked.connect(self.clickDel)
        self.btn_op_Equals.clicked.connect(self.clickSum)

        # Reset default
        self.reset()

        # Change window title
        self.setWindowTitle("Cakulabruh 0.0.1")

    def clickNum(self, value: int):
        if value >= 0 and value <= 9:
            # Convert int to string
            int_to_str = str(value)

            # Check state
            if self.value_current == "0" or self.is_completed_caculate:
                # Set current stats and preview
                self.value_current = int_to_str
                self.joinTextPreview(int_to_str, force_replace=True)
                if self.is_completed_caculate:
                    self.values_stats = []
                    self.is_completed_caculate = False
                    self.btn_del.setDisabled(False)
            else:
                self.value_current += int_to_str
                self.joinTextPreview(int_to_str)
            

    def clickOp(self, op: str):
        if not self.isOperator(op) or self.value_current == "0":
            return

        # Reset stats
        self.values_stats.append(self.value_current)
        self.values_stats.append(op)
        self.value_current = ""
        self.joinTextPreview(op)

    def clickParenteses(self, p: str):
        if not self.isParentheses(p):
            return
        
        # Check if parenthese
        self.btn_op_parentheses_start.setDisabled(p == "(")
        self.btn_op_parentheses_stop.setDisabled(p == ")")
        
        self.joinTextPreview(p, force_replace=self.value_current == "0" or self.is_completed_caculate)
        if self.is_completed_caculate:
            self.values_stats = []
            self.is_completed_caculate = False
            self.btn_del.setDisabled(False)

        if p == ")":
            self.values_stats.append(self.value_current)
            self.values_stats.append(p)
        else:
            self.values_stats.append(p)

        self.value_current = ""
        
    
    
    def clickDel(self):
        text = self.getTextBox()
        if text == self.DEFAULT_VALUE:
            return

        text_deleted = text[: len(text) - 1]
        text_current = text[len(text) - 1]
        if text_deleted == "":
            self.reset()
            return
        
        if self.isOperator(text_current) or self.isParentheses(text_current):
            # Pop operator
            self.values_stats.pop()
            # Replace from pop stats
            self.value_current = self.values_stats.pop()

        self.joinTextPreview(text_deleted, force_replace=True)

    def clickSum(self):
        if self.value_current != "":
            # Append last value
            self.values_stats.append(self.value_current)
        try:
            # Caculate 
            result = self.CACULATOR.process(raw=self.values_stats)
            if result is None:
                self.showErrorAndReset()

            # Set completed caculate
            self.is_completed_caculate = True
            self.joinTextPreview(str(result), force_replace=True)
            self.btn_del.setDisabled(True)
        except:
            self.showErrorAndReset()
        
    def showErrorAndReset(self):
        QtWidgets.QMessageBox.critical(self, "Caculate fail", "Caculate fail. Please check syntax and try again.")
        self.reset()

    def reset(self):
        self.value_current = self.DEFAULT_VALUE
        self.values_stats = []
        self.text_preview.setText(self.DEFAULT_VALUE)
        # Lock strict button
        self.btn_op_parentheses_stop.setDisabled(True)

    def joinTextPreview(self, val: str, force_replace: bool = False):
        if not force_replace:
            self.text_preview.setText(self.getTextBox() + val)
        else:
            self.text_preview.setText(val)

    def getTextBox(self):
        return self.text_preview.toPlainText()
    
    def isOperator(self, val: str):
        return val in ["+", "-", "*", "/"]

    def isParentheses(self, val: str):
        return val in ["(", ")"]



app = QtWidgets.QApplication(sys.argv)

window = MainWindow()
window.show()
app.exec()
