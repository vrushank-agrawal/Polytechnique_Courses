# ------------------------------------------------------------------------------
import math

# ------------------------------------------------------------------------------
class Rdict:
    def __init__(self):
        self.__fwd = {}
        self.__bwd = {}

    def associate(self, a, b):
        if a in self.__fwd or b in self.__bwd:
            raise RuntimeError
        self.__fwd[a] = b
        self.__bwd[b] = a

    def __len__(self):
        return len(self.__fwd)

    def __getitem__(self, key):
        # check if the argument is a tuple
        if isinstance(key, int):
            if key < 0:
                return self.__bwd.values()
            return self.__fwd.values()
        (sel, x) = key
        if sel < 0:
            return self.__bwd[x]
        return self.__fwd[x]

    def __setitem__(self, key, value):
        (sel, x) = key
        if sel < 0:
            self.associate(value, x)
        else:
            self.associate(x, value)

def make_beatles():
    beatles = Rdict()
    beatles[+1, 'Paul McCartney'] = 'bass guitar'
    beatles[-1, 'drums'] = 'Ringo Starr'
    beatles[-1, 'lead guitar'] = 'George Harrison'
    beatles[+1, 'John Lennon'] = 'rhythm guitar'
    return beatles
