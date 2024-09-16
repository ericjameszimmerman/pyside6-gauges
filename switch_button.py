# https://stackoverflow.com/questions/14780517/toggle-switch-in-qt
from PySide6.QtCore import QPropertyAnimation, QRectF, QSize, Qt, Property, QPoint
from PySide6.QtGui import QPainter, QColor, QLinearGradient, QPen, QRadialGradient, QBrush
from PySide6.QtWidgets import (
    QAbstractButton,
    QApplication,
    QHBoxLayout,
    QSizePolicy,
    QWidget, QLabel,
)


class SwitchButton(QWidget):
    def __init__(self, parent=None, w1="Yes", l1=12, w2="No", l2=33, width=60):
        super(SwitchButton, self).__init__(parent)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.__labeloff = QLabel(self)
        self.__labeloff.setText(w2)
        self.__labeloff.setStyleSheet("""color: rgb(120, 120, 120); font-weight: bold;""")
        self.__background = Background(self)
        self.__labelon = QLabel(self)
        self.__labelon.setText(w1)
        self.__labelon.setStyleSheet("""color: rgb(255, 255, 255); font-weight: bold;""")
        self.__circle = Circle(self)
        self.__circlemove = None
        self.__ellipsemove = None
        self.__enabled = True
        self.__duration = 100
        self.__value = False
        self.setFixedSize(width, 24)

        self.__background.resize(20, 20)
        self.__background.move(2, 2)
        self.__circle.move(2, 2)
        self.__labelon.move(l1, 5)
        self.__labeloff.move(l2, 5)

    def setDuration(self, time):
        self.__duration = time

    def mousePressEvent(self, event):
        if not self.__enabled:
            return

        self.__circlemove = QPropertyAnimation(self.__circle, b"pos")
        self.__circlemove.setDuration(self.__duration)

        self.__ellipsemove = QPropertyAnimation(self.__background, b"size")
        self.__ellipsemove.setDuration(self.__duration)

        xs = 2
        y = 2
        xf = self.width() - 22
        hback = 20
        isize = QSize(hback, hback)
        bsize = QSize(self.width() - 4, hback)
        if self.__value:
            xf = 2
            xs = self.width() - 22
            bsize = QSize(hback, hback)
            isize = QSize(self.width() - 4, hback)

        self.__circlemove.setStartValue(QPoint(xs, y))
        self.__circlemove.setEndValue(QPoint(xf, y))

        self.__ellipsemove.setStartValue(isize)
        self.__ellipsemove.setEndValue(bsize)

        self.__circlemove.start()
        self.__ellipsemove.start()
        self.__value = not self.__value

    def paintEvent(self, event):
        s = self.size()
        qp = QPainter(self)
        qp.setRenderHint(QPainter.Antialiasing, True)
        pen = QPen(Qt.NoPen)
        qp.setPen(pen)
        qp.setBrush(QColor(120, 120, 120))
        qp.drawRoundedRect(0, 0, s.width(), s.height(), 12, 12)
        lg = QLinearGradient(35, 30, 35, 0)
        lg.setColorAt(0, QColor(210, 210, 210, 255))
        lg.setColorAt(0.25, QColor(255, 255, 255, 255))
        lg.setColorAt(0.82, QColor(255, 255, 255, 255))
        lg.setColorAt(1, QColor(210, 210, 210, 255))
        qp.setBrush(lg)
        qp.drawRoundedRect(1, 1, s.width()-2, s.height()-2, 10, 10)

        qp.setBrush(QColor(210, 210, 210))
        qp.drawRoundedRect(2, 2, s.width() - 4, s.height() - 4, 10, 10)

        if self.__enabled:
            lg = QLinearGradient(50, 30, 35, 0)
            lg.setColorAt(0, QColor(230, 230, 230, 255))
            lg.setColorAt(0.25, QColor(255, 255, 255, 255))
            lg.setColorAt(0.82, QColor(255, 255, 255, 255))
            lg.setColorAt(1, QColor(230, 230, 230, 255))
            qp.setBrush(lg)
            qp.drawRoundedRect(3, 3, s.width() - 6, s.height() - 6, 7, 7)
        else:
            lg = QLinearGradient(50, 30, 35, 0)
            lg.setColorAt(0, QColor(200, 200, 200, 255))
            lg.setColorAt(0.25, QColor(230, 230, 230, 255))
            lg.setColorAt(0.82, QColor(230, 230, 230, 255))
            lg.setColorAt(1, QColor(200, 200, 200, 255))
            qp.setBrush(lg)
            qp.drawRoundedRect(3, 3, s.width() - 6, s.height() - 6, 7, 7)
        qp.end()


class Circle(QWidget):
    def __init__(self, parent=None):
        super(Circle, self).__init__(parent)
        self.__enabled = True
        self.setFixedSize(20, 20)

    def paintEvent(self, event):
        s = self.size()
        qp = QPainter(self)
        qp.setRenderHint(QPainter.Antialiasing, True)
        qp.setPen(Qt.NoPen)
        qp.setBrush(QColor(120, 120, 120))
        qp.drawEllipse(0, 0, 20, 20)
        rg = QRadialGradient(int(self.width() / 2), int(self.height() / 2), 12)
        rg.setColorAt(0, QColor(255, 255, 255))
        rg.setColorAt(0.6, QColor(255, 255, 255))
        rg.setColorAt(1, QColor(205, 205, 205))
        qp.setBrush(QBrush(rg))
        qp.drawEllipse(1, 1, 18, 18)

        qp.setBrush(QColor(210, 210, 210))
        qp.drawEllipse(2, 2, 16, 16)

        if self.__enabled:
            lg = QLinearGradient(3, 18, 20, 4)
            lg.setColorAt(0, QColor(255, 255, 255, 255))
            lg.setColorAt(0.55, QColor(230, 230, 230, 255))
            lg.setColorAt(0.72, QColor(255, 255, 255, 255))
            lg.setColorAt(1, QColor(255, 255, 255, 255))
            qp.setBrush(lg)
            qp.drawEllipse(3, 3, 14, 14)
        else:
            lg = QLinearGradient(3, 18, 20, 4)
            lg.setColorAt(0, QColor(230, 230, 230))
            lg.setColorAt(0.55, QColor(210, 210, 210))
            lg.setColorAt(0.72, QColor(230, 230, 230))
            lg.setColorAt(1, QColor(230, 230, 230))
            qp.setBrush(lg)
            qp.drawEllipse(3, 3, 14, 14)
        qp.end()


class Background(QWidget):
    def __init__(self, parent=None):
        super(Background, self).__init__(parent)
        self.__enabled = True
        self.setFixedHeight(20)

    def paintEvent(self, event):
        s = self.size()
        qp = QPainter(self)
        qp.setRenderHint(QPainter.Antialiasing, True)
        pen = QPen(Qt.NoPen)
        qp.setPen(pen)
        qp.setBrush(QColor(154, 205, 50))
        if self.__enabled:
            qp.setBrush(QColor(154, 190, 50))
            qp.drawRoundedRect(0, 0, s.width(), s.height(), 10, 10)

            lg = QLinearGradient(0, 25, 70, 0)
            lg.setColorAt(0, QColor(154, 184, 50))
            lg.setColorAt(0.35, QColor(154, 210, 50))
            lg.setColorAt(0.85, QColor(154, 184, 50))
            qp.setBrush(lg)
            qp.drawRoundedRect(1, 1, s.width() - 2, s.height() - 2, 8, 8)
        else:
            qp.setBrush(QColor(150, 150, 150))
            qp.drawRoundedRect(0, 0, s.width(), s.height(), 10, 10)

            lg = QLinearGradient(5, 25, 60, 0)
            lg.setColorAt(0, QColor(190, 190, 190))
            lg.setColorAt(0.35, QColor(230, 230, 230))
            lg.setColorAt(0.85, QColor(190, 190, 190))
            qp.setBrush(lg)
            qp.drawRoundedRect(1, 1, s.width() - 2, s.height() - 2, 8, 8)
        qp.end()


class Switch(QAbstractButton):
    def __init__(self, parent=None, track_radius=10, thumb_radius=8):
        super().__init__(parent=parent)
        self.setCheckable(True)
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        self._track_radius = track_radius
        self._thumb_radius = thumb_radius

        self._margin = max(0, self._thumb_radius - self._track_radius)
        self._base_offset = max(self._thumb_radius, self._track_radius)
        self._end_offset = {
            True: lambda: self.width() - self._base_offset,
            False: lambda: self._base_offset,
        }
        self._offset = self._base_offset

        palette = self.palette()
        if self._thumb_radius > self._track_radius:
            self._track_color = {
                True: palette.highlight(),
                False: palette.dark(),
            }
            self._thumb_color = {
                True: palette.highlight(),
                False: palette.light(),
            }
            self._text_color = {
                True: palette.highlightedText().color(),
                False: palette.dark().color(),
            }
            self._thumb_text = {
                True: '',
                False: '',
            }
            self._track_opacity = 0.5
        else:
            self._thumb_color = {
                True: palette.highlightedText(),
                False: palette.light(),
            }
            self._track_color = {
                True: palette.highlight(),
                False: palette.dark(),
            }
            self._text_color = {
                True: palette.highlight().color(),
                False: palette.dark().color(),
            }
            self._thumb_text = {
                True: '✔',
                False: '✕',
            }
            self._track_opacity = 1

    @Property(int)
    def offset(self):
        return self._offset

    @offset.setter
    def offset(self, value):
        self._offset = value
        self.update()

    def sizeHint(self):  # pylint: disable=invalid-name
        return QSize(
            4 * self._track_radius + 2 * self._margin,
            2 * self._track_radius + 2 * self._margin,
        )

    def setChecked(self, checked):
        super().setChecked(checked)
        self.offset = self._end_offset[checked]()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.offset = self._end_offset[self.isChecked()]()

    def paintEvent(self, event):  # pylint: disable=invalid-name, unused-argument
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing, True)
        p.setPen(Qt.NoPen)
        track_opacity = self._track_opacity
        thumb_opacity = 1.0
        text_opacity = 1.0
        if self.isEnabled():
            track_brush = self._track_color[self.isChecked()]
            thumb_brush = self._thumb_color[self.isChecked()]
            text_color = self._text_color[self.isChecked()]
        else:
            track_opacity *= 0.8
            track_brush = self.palette().shadow()
            thumb_brush = self.palette().mid()
            text_color = self.palette().shadow().color()

        p.setBrush(track_brush)
        p.setOpacity(track_opacity)
        p.drawRoundedRect(
            self._margin,
            self._margin,
            self.width() - 2 * self._margin,
            self.height() - 2 * self._margin,
            self._track_radius,
            self._track_radius,
        )
        p.setBrush(thumb_brush)
        p.setOpacity(thumb_opacity)
        p.drawEllipse(
            self.offset - self._thumb_radius,
            self._base_offset - self._thumb_radius,
            2 * self._thumb_radius,
            2 * self._thumb_radius,
        )
        p.setPen(text_color)
        p.setOpacity(text_opacity)
        font = p.font()
        font.setPixelSize(1.5 * self._thumb_radius)
        p.setFont(font)
        p.drawText(
            QRectF(
                self.offset - self._thumb_radius,
                self._base_offset - self._thumb_radius,
                2 * self._thumb_radius,
                2 * self._thumb_radius,
            ),
            Qt.AlignCenter,
            self._thumb_text[self.isChecked()],
        )

    def mouseReleaseEvent(self, event):  # pylint: disable=invalid-name
        super().mouseReleaseEvent(event)
        if event.button() == Qt.LeftButton:
            anim = QPropertyAnimation(self, b'offset', self)
            anim.setDuration(120)
            anim.setStartValue(self.offset)
            anim.setEndValue(self._end_offset[self.isChecked()]())
            anim.start()

    def enterEvent(self, event):  # pylint: disable=invalid-name
        self.setCursor(Qt.PointingHandCursor)
        super().enterEvent(event)


def main():
    app = QApplication([])

    # Thumb size < track size (Gitlab style)
    s1 = Switch()
    s1.toggled.connect(lambda c: print('toggled', c))
    s1.clicked.connect(lambda c: print('clicked', c))
    s1.pressed.connect(lambda: print('pressed'))
    s1.released.connect(lambda: print('released'))
    s2 = Switch()
    s2.setEnabled(False)

    # Thumb size > track size (Android style)
    s3 = Switch(thumb_radius=11, track_radius=8)
    s4 = Switch(thumb_radius=11, track_radius=8)
    s4.setEnabled(False)

    s5 = SwitchButton()

    l = QHBoxLayout()
    l.addWidget(s1)
    l.addWidget(s2)
    l.addWidget(s3)
    l.addWidget(s4)
    l.addWidget(s5)
    w = QWidget()
    w.setLayout(l)
    w.show()

    app.exec()


if __name__ == '__main__':
    main()
