import sys

from PyQt5.QtWidgets import QApplication
from views import Main

app = QApplication(sys.argv)

main_window = Main()
main_window.showMaximized()
sys.exit(app.exec_())