# --------------------------------------------------------------------
import math

def sign(x):
    return (x > 0) - (x < 0)

# --------------------------------------------------------------------
class Fraction:
    def __init__(self, numerator = 1, denominator = 1):
        self.__numerator   = numerator
        self.__denominator = denominator
        self.__reduced     = False

    @property
    def numerator(self):
        return self.__numerator

    @property
    def denominator(self):
        return self.__denominator

    def reduce(self):
        if self.__reduced:
            return
        gcd = math.gcd(abs(self.numerator), abs(self.denominator))
        dsgn = sign(self.denominator)
        self.__numerator  = dsgn * self.__numerator // gcd
        self.__denominator = dsgn * self.__denominator // gcd
        self.__reduced    = True

    def __str__(self):
        self.reduce()
        if self.denominator == 1:
            return str(self.numerator)
        return '%d/%s' % (self.numerator, self.denominator)

    def __repr__(self):
        return 'Fraction(%d, %d)' % (self.numerator, self.denominator)

    def __eq__(self, other):
        lhs = self.numerator   * other.denominator
        rhs = self.denominator * other.numerator
        return lhs == rhs

    def __ne__(self, other):
        return not self.__eq__(other)

    def __add__(self, other):
        n = self.numerator * other.denominator \
                + other.numerator * self.denominator
        d = self.denominator * other.denominator
        return Fraction(n, d)

    def __sub__(self, other):
        return self + (-other)

    def __neg__(self):
        return Fraction(-self.numerator, self.denominator)

    def __mul__(self, other):
        n = self.numerator   * other.numerator
        d = self.denominator * other.denominator
        return Fraction(n, d)

    def __truediv(self, other):
        n = self.numerator   * other.denominator
        d = self.denominator * other.numerator
        return Fraction(n, d)
