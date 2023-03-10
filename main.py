import sys
import os

from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QLabel, QCheckBox, QPushButton, QDialog
from PyQt5.QtGui import QPixmap

from PyQt5 import QtCore, QtGui, QtWidgets

from PIL import Image


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1183, 771)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMinimumSize(QtCore.QSize(0, 0))
        MainWindow.setMaximumSize(QtCore.QSize(9999, 9999))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.pic_label = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pic_label.sizePolicy().hasHeightForWidth())
        self.pic_label.setSizePolicy(sizePolicy)
        self.pic_label.setMaximumSize(QtCore.QSize(1300, 850))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.pic_label.setFont(font)
        self.pic_label.setText("")
        self.pic_label.setScaledContents(True)
        self.pic_label.setObjectName("pic_label")
        self.gridLayout.addWidget(self.pic_label, 1, 1, 1, 3)
        self.previous_states = QtWidgets.QComboBox(self.centralwidget)
        self.previous_states.setObjectName("previous_states")
        self.gridLayout.addWidget(self.previous_states, 2, 3, 1, 1)
        self.effects = QtWidgets.QComboBox(self.centralwidget)
        self.effects.setObjectName("effects")
        self.gridLayout.addWidget(self.effects, 2, 2, 1, 1)
        self.advertisment = QtWidgets.QLabel(self.centralwidget)
        self.advertisment.setAlignment(QtCore.Qt.AlignCenter)
        self.advertisment.setObjectName("advertisment")
        self.gridLayout.addWidget(self.advertisment, 2, 1, 1, 1)
        self.save_button = QtWidgets.QPushButton(self.centralwidget)
        self.save_button.setObjectName("save_button")
        self.gridLayout.addWidget(self.save_button, 3, 3, 1, 1)
        self.get_pic_button = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.get_pic_button.sizePolicy().hasHeightForWidth())
        self.get_pic_button.setSizePolicy(sizePolicy)
        self.get_pic_button.setObjectName("get_pic_button")
        self.gridLayout.addWidget(self.get_pic_button, 3, 1, 1, 1)
        self.apply_button = QtWidgets.QPushButton(self.centralwidget)
        self.apply_button.setObjectName("apply_button")
        self.gridLayout.addWidget(self.apply_button, 3, 2, 1, 1)
        self.accuracy_slider = QtWidgets.QSlider(self.centralwidget)
        self.accuracy_slider.setEnabled(True)
        self.accuracy_slider.setMinimum(0)
        self.accuracy_slider.setMaximum(99)
        self.accuracy_slider.setProperty("value", 0)
        self.accuracy_slider.setOrientation(QtCore.Qt.Horizontal)
        self.accuracy_slider.setObjectName("accuracy_slider")
        self.gridLayout.addWidget(self.accuracy_slider, 0, 1, 1, 2)
        self.accuracy_label = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.accuracy_label.setFont(font)
        self.accuracy_label.setObjectName("accuracy_label")
        self.gridLayout.addWidget(self.accuracy_label, 0, 3, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "??????????"))
        self.advertisment.setText(_translate("MainWindow", "?????????? ?????????? ???????? ???????? ??????????????"))
        self.save_button.setText(_translate("MainWindow", "??????????????????"))
        self.get_pic_button.setText(_translate("MainWindow", "?????????????? ????????????????"))
        self.apply_button.setText(_translate("MainWindow", "?????????????????? ????????????"))
        self.accuracy_label.setText(_translate("MainWindow", "TextLabel"))


class Point:
    """
    ?????????????????? ???????????? ?????????? (??????????????) ???? ????????????????;
    ???????????? ?? ???????? ?????????????? ???? ??????????????, ?????????? RGB ?? ?????????????????? ?????????????????????????????? / ??????????????????????????????????
    ?????????????????????????????? / ?????????????????????????????????? ?????????? ?????? ??????????????
    """

    def __init__(self, x, y, r=0, g=0, b=0):
        self.x = x
        self.y = y
        self.r = r
        self.g = g
        self.b = b
        self.painted = False

    def set_painted(self, r, g, b, state=True):
        """
        ???????????????? ?????????? ?????????????????????? (?? ?????????????????????? ???? state) ?? ???????????? ?????????? ????????
        ?????????? ?????????? ?????? ????????????????????????????
        """

        self.r = r
        self.g = g
        self.b = b
        self.painted = state


class Pic:
    """
    ?????????????????? ???????????? ???????????????? ???????????? ????????????????????
    ???????????? ???????? ?? ?????????????????????? ????????????????, ?????? ???????????????? ?????? ?????????????????? ?? ???????????? ?????????????????? ???????? ?? ???????????? ?????????????? ????????????????
    """

    def __init__(self, name, path, accuracy=None):
        self.path = path

        self.name = name

        self.im = Image.open(path)
        self.width, self.height = self.im.size
        self.pixels = self.im.load()

        self.points = self.pixels_to_points()

        if accuracy:
            self.accuracy = accuracy

    def pixels_to_points(self):
        """
        ???????????????? ?????????????? ??????????????????????, ?????????????????? ???? ?? ?????????????? ???????????? Point
        """

        points = []
        for i in range(self.width):
            points.append([])
            for j in range(self.height):
                points[i].append(Point(i, j, *self.pixels[i, j]))
        return points

    def make_black_and_white(self):
        """
        ?????????? ?????????????????????????? ?????? ?????????? ????????????????, ?????????????????? ???? ?? ??????????-??????????
        """
        for i in range(self.width):
            for j in range(self.height):
                p = self.points[i][j]
                r, g, b = p.r, p.g, p.b
                av = (r + g + b) / 3
                self.points[i][j] = Point(p.x, p.y, av, av, av)
        self.repaint()

    def make_negative(self):
        """
        ?????????? ???????????????????????????? ?????? ?????????? ????????????????, ?????????? ???????????????? ????????????????????
        """
        for i in range(self.width):
            for j in range(self.height):
                p = self.points[i][j]
                r, g, b = p.r, p.g, p.b
                self.points[i][j] = Point(p.x, p.y, 255 - r, 225 - g, 255 - b)
        self.repaint()

    def make_vitraj(self):
        """
        ?????????? ???????????????????? ???????????????? ?? ????????????
        ?????????????? ?????????? ????????????????, ???????? ?????????????? ???? ?????????????????????????? ??????????, ????
        ???????????????? ?????????????? new_piece, ?????????????? ???? ???????????? ?????????? ?????????????? '?????????? ??????????' ??????????????
        """
        for i in range(self.width):
            for j in range(self.height):
                if not self.points[i][j].painted:
                    self.new_piece(self.points[i][j])
        self.repaint()

    def new_piece(self, first_point):
        """
        ???? ???????????????? ?????????????????? ?????????? ???????????? '?????????? ??????????' ??????????????,
        ???????????????????????? ???????????? ?????????? ?? ???????????? ??????????
        """

        visited = set()
        '?????????????????? ???????????????????? ??????????'
        stack = list()
        '???????? ???????????????????????????? ??????????'
        stack.append(first_point)
        while stack:
            '???????? ???????? ?????????? ?????? ??????????????????'
            last = stack.pop()
            visited.add(last)
            '?????????????? ?????????????????? ?????????????????????? ??????????, ???????????????? ???? ?????? ????????????????????'
            if self.needs_painting(last, first_point):
                self.points[last.x][last.y].set_painted(first_point.r, first_point.g, first_point.b)
                self.next_points(last, stack, visited, first_point)

    def next_points(self, last_point, stack_of_points, visited_points, first_point):
        """
        ?????????????????? ?? ???????? ?????????? '???????????? ??????????' ???????????????? ?????????? ?????? ????????????, ???????? ???? ?????????? ????????????????????
        """
        if self.is_in_pic(Point(last_point.x, last_point.y - 1)):  # ?????????????? ??????????;
            '???????? ???????????? ???????? ??????????'
            if self.points[last_point.x][last_point.y - 1] not in visited_points:
                '???????? ?????? ?????????? ?????? ???? ????????????????????'
                if self.needs_painting(self.points[last_point.x][last_point.y - 1], first_point):
                    '???????? ???? ?????????? ????????????????????'
                    stack_of_points.append(self.points[last_point.x][last_point.y - 1])
                    '?????? ?????????????? ????????????, ???????????? ?????????? ???????????????????? ?? ????????'

        if self.is_in_pic(Point(last_point.x + 1, last_point.y)):  # ???????????? ??????????;
            '???????? ???????????? ???????? ??????????'
            if self.points[last_point.x + 1][last_point.y] not in visited_points:
                '???????? ?????? ?????????? ?????? ???? ????????????????????'
                if self.needs_painting(self.points[last_point.x + 1][last_point.y], first_point):
                    '???????? ???? ?????????? ????????????????????'
                    stack_of_points.append(self.points[last_point.x + 1][last_point.y])
                    '?????? ?????????????? ????????????, ???????????? ?????????? ???????????????????? ?? ????????'

        if self.is_in_pic(Point(last_point.x, last_point.y + 1)):  # ???????????? ??????????;
            '???????? ?????????? ???????? ??????????'
            if self.points[last_point.x][last_point.y + 1] not in visited_points:
                '???????? ?????? ?????????? ?????? ???? ????????????????????'
                if self.needs_painting(self.points[last_point.x][last_point.y + 1], first_point):
                    '???????? ???? ?????????? ????????????????????'
                    stack_of_points.append(self.points[last_point.x][last_point.y + 1])
                    '?????? ?????????????? ????????????, ???????????? ?????????? ???????????????????? ?? ????????'

        if self.is_in_pic(Point(last_point.x - 1, last_point.y)):  # ?????????? ??????????;
            '???????? ?????????? ???????? ??????????'
            if self.points[last_point.x - 1][last_point.y] not in visited_points:
                '???????? ?????? ?????????? ?????? ???? ????????????????????'
                if self.needs_painting(self.points[last_point.x - 1][last_point.y], first_point):
                    '???????? ???? ?????????? ????????????????????'
                    stack_of_points.append(self.points[last_point.x - 1][last_point.y])
                    '?????? ?????????????? ????????????, ???????????? ?????????? ???????????????????? ?? ????????'

    def is_in_pic(self, point):
        """
        ??????????????????, ?????????????????? ???? ???????????????????? ?????????? ?? ???????????????? ????????????????
        """
        return 0 <= point.x < self.width and 0 <= point.y < self.height

    def needs_painting(self, point, first_point):
        """
        ??????????????????, ?????????? ???? ?????????????????????????? ???????????? ??????????,
        ?????????????????? ???? ?? ???????????? ???????????? '???????????? ??????????'
        """
        return (abs(point.r - first_point.r) <= self.accuracy and
                abs(point.g - first_point.g) <= self.accuracy and
                abs(point.b - first_point.b) <= self.accuracy)

    def repaint(self):
        """
        ?????????? ???????????? ???????????????? ???????????????? ?????????? ????????;
        ??.??. ???????????? Image ???? PIL ???????????? ?? ???????????????? pixels, ?? ???????????? ?????? ?????????????? ???????????????????? ?? ???????????????? points,
        ?????????? ???? points ?????????? ?????????????????????? ?? pixels, ?????????? ?????????? ?????????????????? ???????????????? ?????? ?? ???????????? ??????????????
        """
        for i in range(self.width):
            for j in range(self.height):
                point = self.points[i][j]
                self.pixels[i, j] = int(point.r), int(point.g), int(point.b)


class CloseWidget(QDialog):
    """
    ?????????????????? ???????????? ????????, ?????????????????????? ?????? ?????????????? ?????????????? ????????????????????
    ?????????? ???????????????????????? ???????????????? ???? ???????????? ????????????????????, ???? ???????????????? ??????????????????, ?????????? ???????????????? ?????????????????????????? ????????????
    ?????????? ???????? ?????????????????????? ?????????????????? ???????????????? ?????????? ?????????????? ???? ????????????????????
    """
    def __init__(self, pic=False):
        super().__init__()
        self.setWindowTitle("??????????")
        self.setFixedSize(400, 170)

        self.question = QLabel(self)
        self.question.setText("???? ??????????????, ?????? ???????????? ???????????")
        f = self.question.font()
        f.setPointSize(16)
        self.question.setFont(f)
        self.question.move(40, 0)

        self.save_tick = QCheckBox(self)
        self.save_tick.setText("??????????????????")
        self.save_tick.setGeometry(40, 50, 141, 41)
        f = self.save_tick.font()
        f.setPointSize(16)
        self.save_tick.setFont(f)
        if not pic:
            '???????? ?????????????? ???????????????? ?? ???????????????????? ?????? - ?????????????????? ????????????'
            self.save_tick.setEnabled(False)

        self.yes = QPushButton(self)
        self.yes.setText("????")
        self.yes.setGeometry(40, 100, 81, 41)
        f = self.yes.font()
        f.setPointSize(18)
        self.yes.setFont(f)
        self.yes.clicked.connect(self.accept)

        self.no = QPushButton(self)
        self.no.setText("??????")
        self.no.setGeometry(279, 100, 81, 41)
        f = self.no.font()
        f.setPointSize(18)
        self.no.setFont(f)
        self.no.clicked.connect(self.reject)


class Window(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("Vitrajator 3000")

        # uic.loadUi("vitrajator_v0.1.ui", self)

        self.accuracy_slider.setMaximum(255)
        self.accuracy_slider.setValue(10)
        self.accuracy_label.setText(str(self.accuracy_slider.value()))
        self.accuracy_slider.setEnabled(False)
        self.accuracy_slider.valueChanged.connect(self.accuracy_changed)

        self.apply_button.setEnabled(False)

        self.effects.addItem("??????????-??????????")
        self.effects.addItem("??????????????")
        self.effects.addItem("????????????")
        self.effects.setEnabled(False)
        self.chosen_effect = "??????????-??????????"

        self.main_pic_path = QFileDialog.getOpenFileName(self, "???????????????? ????????????????", "", '???????????????? (*.jpg)')[0]

        self.save_button.setEnabled(False)

        self.pictures = []

        '?????????????????? ???????????????? ???????????? ???????? ?????????????????????????? ???? ?????????????????? ????????????????'
        if self.main_pic_path:
            '???????? ???????????????? ???????? - ??????????????????'
            self.pixmap = QPixmap(self.main_pic_path)
            self.pic_label.setPixmap(self.pixmap)
            self.path_to_save = '/'.join(self.main_pic_path.split('/')[:-1])

            self.apply_button.setEnabled(True)

            self.save_button.setEnabled(True)

            self.effects.setEnabled(True)

            self.previous_states.addItem("origin")
            self.previous_states.currentIndexChanged.connect(self.current_state_changed)

            self.pictures.append(Pic("origin", path=self.main_pic_path))

        self.effects.currentIndexChanged.connect(self.effect_changed)

        self.get_pic_button.clicked.connect(self.choose_new_picture)

        self.apply_button.clicked.connect(self.set_effect)

        self.save_button.clicked.connect(self.save_button_clicked)

    def effect_changed(self):
        self.chosen_effect = self.effects.currentText()
        '?????????????????????? ???????????????????????? ?????????????? ?????????????????????? ???????????????? ???????????? ?????????? ???????????? ????????????, ?????????????? :)'
        if self.chosen_effect == "????????????":
            self.accuracy_slider.setEnabled(True)
        else:
            self.accuracy_slider.setEnabled(False)

    def save_button_clicked(self):
        """
        ?????????? ???????????? ?? ?????????????? ???????????????????? ????????????????
        ?????????????????? ?????????????????? ????????????????
        """

        for i in range(len(self.pictures)):
            if self.pictures[i].name == self.previous_states.currentText():
                path = QFileDialog.getSaveFileName()[0] + ".jpg"
                if path == ".jpg":
                    '???????? ???????????????? ???? ??????????????, ?????????????????? ???????????? ???? ????????, ?????????????? :)'
                    return
                self.pictures[i].im.save(path)
                break

    def choose_new_picture(self):
        """
         ?????????? ???????????? ?? ?????????????? ???????????? ?????????? ????????????????
         ???????????????????? ?????????? ???????????????? ?? ????????????????????, ?????? ???????? ?????????????????? ?????? ?????????????????????? ???????????? ???? ????????????????????
        """
        pic_name = QFileDialog.getOpenFileName(self, "???????????????? ????????????????", "", '???????????????? (*.jpg)')[0]
        if not pic_name:
            '???????? ???????????????? ???? ??????????????, ?????????????????? ???????????? ???? ??????????, ?????????????? :)'
            return
        remove_process_pictures(self)
        self.main_pic_path = pic_name
        self.pictures.clear()
        self.pictures.append(Pic("origin", path=self.main_pic_path))
        self.pixmap = QPixmap(self.main_pic_path)
        self.pic_label.setPixmap(self.pixmap)

        self.previous_states.clear()
        self.previous_states.addItem("origin")

        self.apply_button.setEnabled(True)

        self.save_button.setEnabled(True)

        self.effects.setEnabled(True)

    def current_state_changed(self):
        """
        ?????????? ???????????? ?? ???????????????????? ?????????????? ?????????????????? ????????????????
        ?????????????????? ???????????????????????? ???? ???????????? ????????????????
        """
        for i in range(len(self.pictures)):
            if self.pictures[i].name == self.previous_states.currentText():
                path = self.pictures[i].path
                break
        if not os.path.exists(path):
            '???????? ?????????????? ????????????????, ?????????????? ?????????????? - ?????????????????? ?????? ???????????????? ????????????????'
            self.previous_states.removeItem(self.previous_states.currentIndex())
            for i in range(len(self.pictures)):
                if self.pictures[i].path == path:
                    del self.pictures[i]
        else:
            self.pixmap = QPixmap(path)
            self.pic_label.setPixmap(self.pixmap)

    def accuracy_changed(self):
        """
        ?????????? ???????????? ?? ?????????????????? ?????????????? ??????????????????????
        ?????? ?????????????????? ???????????????????? ?????????????? ???????????????? ???? ????????????
        """
        self.accuracy_label.setText(str(self.accuracy_slider.value()))

    def set_effect(self):
        """
        ?????????? ???????????? ?? ?????????????? ???????????????????? ??????????????
        ?????????????????? ?? ???????????????? ???????? ???? ???????? ????????????????, ?????????????? ???????????????????????????? ??????????
        ?????? ???????????????????? ?? ???????????????? ?????????????? ?????????????????? ?????????? ????????????????
        """

        '?????? ???????? ???????????????????????? ?????????????? ?????????????????? ???????????? ?? ???????????????????????????? ????????????????'
        for i in range(len(self.pictures)):
            if self.pictures[i].name == self.previous_states.currentText():
                if not os.path.exists(self.pictures[i].path):
                    '''
                    ???????? ???????????????????????? ???????????????? ???????????????? ???????????????????????????? ????????????????,
                    ?????????????? ???? ????????????????, ???????????? ???????????????? ????????????????????????, ?????????????????????????? ??????, ?????????? ???????????? ?????????? ????????????????
                    '''
                    del self.pictures[i]
                    self.previous_states.removeItem(self.previous_states.currentIndex())

                    self.pixmap = QPixmap("zochem.jpg")
                    self.pic_label.setPixmap(self.pixmap)

                    self.main_pic_path = ""

                    self.save_button.setEnabled(False)
                    self.apply_button.setEnabled(False)
                    self.effects.setEnabled(False)
                    self.effects.setCurrentIndex(0)

                    return
                break
        if self.chosen_effect == "????????????":
            new_path = self.vitraj()
        elif self.chosen_effect == "??????????-??????????":
            new_path = self.bw()
        else:
            new_path = self.negative()
        self.pixmap = QPixmap(new_path)
        self.pic_label.setPixmap(self.pixmap)

    def bw(self):
        """
        ?????????? ???????????? ?????????????????? ???????????????? ??????????-??????????
        ???????????????????? ???????? ?? ?????????? ?????????????????? ????????????????
        """
        for i in range(len(self.pictures)):
            if self.pictures[i].name == self.previous_states.currentText():
                '???? ???????? ???????????????????????? ?????????????? ???????????? - ??.??. ???????? ?????????? ???????????????? ???????????? ?????? ??????????????'
                if self.pictures[-1].name == "origin":
                    name_for_new = "v0.0"
                else:
                    name_for_new = 'v' + str(float(self.pictures[-1].name[1:]) + 0.1)

                '?????????????? ?????????? ?????????????? ????????????????, ?????????? ???? ????????????????????'
                path_for_new = self.path_to_save + "/" + name_for_new + ".jpg"
                Image.open(self.pictures[i].path).save(path_for_new)
                new_pic = Pic(name_for_new, path=path_for_new)
                break
        '???????????????????????? ?????????? ????????????????, ?????????????????? ??????????????????'
        new_pic.make_black_and_white()
        new_pic.im.save(path_for_new)

        '?????????????????? ???????????? ???????????????? ?? ???????????? ????????????????'
        self.pictures.append(new_pic)
        self.previous_states.addItem(name_for_new)
        self.previous_states.setCurrentIndex(len(self.previous_states) - 1)

        return path_for_new

    def negative(self):
        """
        ?????????? ???????????? ?????????????????? ???????????????? ????????????????????
        ???????????????????? ???????? ?? ?????????? ?????????????????? ????????????????
        """
        for i in range(len(self.pictures)):
            if self.pictures[i].name == self.previous_states.currentText():
                '???? ???????? ???????????????????????? ?????????????? ???????????? - ??.??. ???????? ?????????? ???????????????? ???????????? ?????? ??????????????'
                if self.pictures[-1].name == "origin":
                    name_for_new = "v0.0"
                else:
                    name_for_new = 'v' + str(float(self.pictures[-1].name[1:]) + 0.1)

                '?????????????? ?????????? ?????????????? ????????????????, ?????????? ???? ????????????????????'
                path_for_new = self.path_to_save + "/" + name_for_new + ".jpg"
                Image.open(self.pictures[i].path).save(path_for_new)
                new_pic = Pic(name_for_new, path=path_for_new)
                break
        new_pic.make_negative()
        new_pic.im.save(path_for_new)

        '???????????????????????? ?????????? ????????????????, ?????????????????? ??????????????????'
        self.pictures.append(new_pic)
        self.previous_states.addItem(name_for_new)
        self.previous_states.setCurrentIndex(len(self.previous_states) - 1)

        return path_for_new

    def vitraj(self):
        """
        ?????????? ???????????????????? ?????????????????? ???????????????? ?? ????????????
        ???????????????????? ???????? ?? ?????????? ?????????????????? ????????????????
        """
        for i in range(len(self.pictures)):
            if self.pictures[i].name == self.previous_states.currentText():
                '???? ???????? ???????????????????????? ?????????????? ???????????? - ??.??. ???????? ?????????? ???????????????? ???????????? ?????? ??????????????'
                if self.pictures[-1].name == "origin":
                    name_for_new = "v0.0"
                else:
                    name_for_new = 'v' + str(float(self.pictures[-1].name[1:]) + 0.1)

                '?????????????? ?????????? ?????????????? ????????????????, ?????????? ???? ????????????????????'
                path_for_new = self.path_to_save + "/" + name_for_new + ".jpg"
                Image.open(self.pictures[i].path).save(path_for_new)
                new_pic = Pic(name_for_new, path_for_new, accuracy=self.accuracy_slider.value())
                break
        new_pic.make_vitraj()
        new_pic.im.save(path_for_new)

        '???????????????????????? ?????????? ????????????????, ?????????????????? ??????????????????'
        self.pictures.append(new_pic)
        self.previous_states.addItem(name_for_new)
        self.previous_states.setCurrentIndex(len(self.previous_states) - 1)

        return path_for_new

    def closeEvent(self, event):
        """
        ?????????? ?????????????????????? ???????????????? ???????????????????? ?? ???????????? ?????????????????????????? ????????????
        ?????????? ??????????, ???????????????????????????? ???????????????? ????????????????
        """
        close_widget = CloseWidget(self.main_pic_path)
        if close_widget.exec_() == QDialog.Accepted:
            if close_widget.save_tick.isChecked():
                self.save_button_clicked()
            event.accept()
        else:
            event.ignore()
        close_widget.deleteLater()


def remove_process_pictures(window):
    """
    ?????????????? ?????????????? ?????????????????? 'in_process' ?????????????????? ????????????????, ?????????? ???? ???????????????????????? ????????????
    """
    for i in range(len(window.pictures)):
        if os.path.exists(window.pictures[i].path) and window.pictures[i].name != "origin":
            os.remove(window.pictures[i].path)


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    wnd = Window()
    wnd.show()
    sys.excepthook = except_hook
    app.exec()
    remove_process_pictures(wnd)
    sys.exit()