import sys

from random import choices
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog


class App(QMainWindow):
    digits = "0123456789"
    alpha_lower = "abcdefghijklmnopqrstuvwxyz"
    alpha_upper = alpha_lower.upper()
    symbols = "~!@#$%^&*()_+/<>"

    def __init__(self):
        super().__init__()
        uic.loadUi('form.ui', self)

        self.gen.clicked.connect(self.generate)
        self.reset.clicked.connect(self.res)

    def generate(self):
        line = ""

        if self.digit.isChecked():
            line += self.digits

        if self.alpha.isChecked():
            line += self.alpha_lower + self.alpha_upper

        if self.symbol.isChecked():
            line += self.symbols

        data = []

        for elem in range(self.count_pass.value()):
            data.append(''.join(choices(line, k=self.count_symbols.value())))

        with open(QFileDialog.getSaveFileName(self, "Сохранить", "/password.txt")[0], "w") as file:
            file.write("\n".join(data))

    def res(self):
        self.count_pass.setValue(0)
        self.count_symbols.setValue(0)

        self.digit.setChecked(False)
        self.alpha.setChecked(False)
        self.symbol.setChecked(False)


def main():
    app = QApplication(sys.argv)

    form = App()
    form.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
