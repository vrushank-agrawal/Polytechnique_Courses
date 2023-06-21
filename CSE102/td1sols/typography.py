# --------------------------------------------------------------------
import sys, os
from   PyQt5.QtCore import Qt
import PyQt5.QtCore as QtCore
import PyQt5.QtGui as QtGui, PyQt5.QtWidgets as QtWidgets

# --------------------------------------------------------------------
class Box:
    DEBUG = True

    @property
    def width(self):
        raise NotImplementedError

    @property
    def ascent(self):
        raise NotImplementedError

    @property
    def descent(self):
        raise NotImplementedError

    @property
    def stretching(self):
        raise NotImplementedError

    def paint(self, painter, x, y, w):
        if self.DEBUG:
            painter.save()
            painter.setPen(Qt.red)
            painter.setBrush(Qt.transparent)
            painter.drawRect(x, y, w, int(self.ascent + self.descent))
            painter.restore()
        self.draw(painter, x, y, w)

    def draw(self, painter, x, y, w):
        raise NotImplementedError

    def __str__(self):
        return "[w={w}, a={a}, d={d}, sc={s}]" \
            .format(self.__class__.__name__,
                    w = self.width     ,
                    a = self.ascent    ,
                    d = self.descent   ,
                    s = self.stretching)

# --------------------------------------------------------------------
class Glyph(Box):
    def __init__(self, font, char):
        super().__init__()
        self.__char = char
        self.__font = font

    @property
    def ascent(self):
        return QtGui.QFontMetrics(self.__font).ascent()

    @property
    def descent(self):
        return QtGui.QFontMetrics(self.__font).descent()

    @property
    def width(self):
        metrics = QtGui.QFontMetrics(self.__font)
        return metrics.width(self.__char)

    @property
    def stretching(self):
        return 0.

    def draw(self, painter, x, y, width):
        painter.save()
        painter.setFont(self.__font)
        painter.drawText(x, y + self.ascent, self.__char)
        painter.restore()

    def __str__(self):
        return 'Glyph({})'.format(self.__char) + super().__str__()

# --------------------------------------------------------------------
class Space(Box):
    def __init__(self, width, stretching):
        self.__width      = width
        self.__stretching = stretching

    @property
    def ascent(self):
        return 0

    @property
    def descent(self):
        return 0

    @property
    def width(self):
        return self.__width

    @property
    def stretching(self):
        return self.__stretching

    def draw(self, painter, x, y, width):
        pass
    
    def __str__(self):
        return 'Space' + str(super())

# --------------------------------------------------------------------
class FixedSpace(Space):
    def __init__(self, width):
        super().__init__(width, 0.)

# --------------------------------------------------------------------
class RelativeSpace(Space):
    def __init__(self, c, font):
        width = QtGui.QFontInfo(font).pointSizeF() * c
        super().__init__(int(width), 1.)

# --------------------------------------------------------------------
class Group(Box):
    def __init__(self, boxes):
        self._boxes      = []
        self._width      = 0
        self._ascent     = 0
        self._descent    = 0
        self._stretching = 0.

        for b in boxes:
            self.add(b)

    @property
    def ascent(self):
        return self._ascent

    @property
    def descent(self):
        return self._descent

    @property
    def width(self):
        return self._width

    @property
    def stretching(self):
        return self._stretching

    def __len__(self):
        return len(self.__boxes)

    def add(self, box):
        self._boxes.append(box)

    def __str__(self):
        core = super().__str__()
        subs = [str(x) for x in self._boxes]
        subs = [['\t' + x for x in l.splitlines()] for l in subs]
        subs = '\n'.join(sum(subs, []))
        return '%s{\n%s\n}' % (core, subs)

# --------------------------------------------------------------------
class HGroup(Group):
    def __init__(self, boxes = []):
        super().__init__(boxes)
    
    def add(self, box):
        super().add(box)
        self._width      += box.width
        self._ascent      = max(self._ascent , box.ascent)
        self._descent     = max(self._descent, box.descent)
        self._stretching += box.stretching

    def draw(self, painter, x, y, width):
        mw   = self.width
        ac   = self.ascent
        sc   = self.stretching
        thex = float(x)

        if mw > width or sc == 0.:
            for box in self._boxes:
                box.draw(painter, int(thex), int(y + ac - box.ascent), int(mw + x - thex))
                thex += box.width
        else:
            for box in self._boxes:
                box.draw(painter, int(thex), int(y + ac - box.ascent), int(width + x - thex))
                thex += box.width
                thex += box.stretching * (width - mw) / sc

    def __str__(self):
        return 'HGroup' + super().__str__()

# --------------------------------------------------------------------
class VGroup(Group):
    def __init__(self, lk, boxes = []):
        self.__lk = lk
        super().__init__(boxes)

    def add(self, box):
        super().add(box)
        self._ascent     += self._descent + self.__lk + box.ascent
        self._descent     = box.descent
        self._width       = max(self._width, box.width)
        self._stretching  = max(self._stretching, box.stretching)

    def draw(self, painter, x, y, width):
        they = float(y)
        for box in self._boxes:
            box.draw(painter, x, int(they), width);
            they += self.__lk + box.ascent + box.descent

    def __str__(self):
        return 'VGroup' + super().__str__()

# --------------------------------------------------------------------
class BoxDisplay(QtWidgets.QMainWindow):
    class BoxWidget(QtWidgets.QWidget):
        PADDING = 50

        def __init__(self, box, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.__box = box
            self.setContentsMargins(*([10] * 4))

        def sizeHint(self):
            return QtCore.QSize(
                2 * self.PADDING + self.__box.width,
                2 * self.PADDING + self.__box.ascent + self.__box.descent)
    
        def paintEvent(self, e):
            width, height = self.size().width(), self.size().height()
    
            with QtGui.QPainter(self) as painter:
                painter.setBrush(Qt.black)
                painter.setPen(Qt.black)
    
                painter.drawLine(self.PADDING, 0, self.PADDING, height)
                painter.drawLine(width - self.PADDING, 0, width - self.PADDING, height)
                painter.drawLine(0, self.PADDING, width, self.PADDING)
                painter.translate(self.PADDING, self.PADDING)
    
                self.__box.paint(painter, 0, 0, self.width() - 2 * self.PADDING)

    def __init__(self, box, parent = None):
        super().__init__(parent)
        self._widget = BoxDisplay.BoxWidget(box = box, parent = self)
        self.setCentralWidget(self._widget)
        self.setWindowTitle('Typography')
        self.move(300, 300)
        self.setSizePolicy(QtWidgets.QSizePolicy.Preferred,
                           QtWidgets.QSizePolicy.Minimum)
        self.resize(self.sizeHint())

# --------------------------------------------------------------------
def _main_q2():
    app = QtWidgets.QApplication(sys.argv)
    fnt = QtGui.QFont("Helvetica", 30)
    glh = Glyph(fnt, "g")    

    print(glh)

# --------------------------------------------------------------------
def _main_q3():
    app = QtWidgets.QApplication(sys.argv)
    fnt = QtGui.QFont("Helvetica", 30)
    # glh = Glyph(fnt, "abdefghijklmnopqrstuvwxyzABDEFGHIJKLMNOPQRSTUVWXYZ")
    glh = Glyph(fnt, "g")
    wdg = BoxDisplay(glh)

    print(glh); wdg.show(); app.exec_()

# --------------------------------------------------------------------
def box_from_line(s):
    fnt = QtGui.QFont("Helvetica", 30)
    grp = [Glyph(fnt, x) for x in s.split()]
    grp = sum([[x, RelativeSpace(0.5, fnt)] for x in grp], [])[:-1]
    box = HGroup()

    for x in grp:
        box.add(x)

    return box

# --------------------------------------------------------------------
def _main_q7():
    app = QtWidgets.QApplication(sys.argv)
    fnt = QtGui.QFont("Helvetica", 30)
    wdg = BoxDisplay(box_from_line("Typographie sans peine"))

    wdg.show(); app.exec_()

# --------------------------------------------------------------------
TEST = r'''L'homme n'est qu'un roseau, le
plus faible de la nature ; mais
c'est un roseau pensant. Il ne
faut pas que l'univers entier s'arme
pour l'écraser : une vapeur, une
goutte d'eau, suffit pour le tuer.
'''

# --------------------------------------------------------------------
def _main_q8():
    app = QtWidgets.QApplication(sys.argv)
    box = VGroup(5)

    for b in [box_from_line(l) for l in TEST.splitlines()]:
        box.add(b)

    wdg = BoxDisplay(box)

    wdg.show(); app.exec_()

# --------------------------------------------------------------------
TEST2 = r'''L'homme n'est qu'un roseau, le
plus faible de la nature ; mais
c'est un roseau pensant. Il ne
faut pas que l'univers entier s'arme
pour l'écraser : une vapeur, une
goutte d'eau, suffit pour le tuer.
'''

# --------------------------------------------------------------------
def _main_q8_2():
    app      = QtWidgets.QApplication(sys.argv)
    lines    = [x.strip() for x in TEST2.splitlines()]

    assert (len(lines) >= 3 and len(lines[0]) > 0)

    lttf     = QtGui.QFont("Helvetica", 120);
    ltt      = lines[0][0]
    lines[0] = lines[0][1:]
    lines    = [box_from_line(l) for l in lines]

    prebox  = HGroup()
    preboxh = VGroup(5)
    box     = VGroup(5)


    for b in lines[:3]:
        preboxh.add(b)

    prebox.add(Glyph(lttf, ltt))
    prebox.add(Space(3.0, 1.0))
    prebox.add(preboxh)

    box.add(prebox)
    for b in lines[3:]:
        box.add(b)


    wdg = BoxDisplay(box)

    wdg.show(); app.exec_()

# --------------------------------------------------------------------
if __name__ == '__main__':
    _main_q8()
