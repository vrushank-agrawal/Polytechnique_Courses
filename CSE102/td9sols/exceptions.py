# --------------------------------------------------------------------
class InvalidInput(Exception):
    pass

# --------------------------------------------------------------------
def sum_of_input():
    s = 0
    while True:
        try:
            s += int(input())
        except ValueError:
            raise InvalidInput
        except EOFError:
            return s

# --------------------------------------------------------------------
class Found(Exception):
    def __init__(self, solution):
        self.solution = solution

# --------------------------------------------------------------------
def subset_sum(nm, S, M):
    nS = sum(S)
    
    if nS > M:
        return None
    
    if nS == M:
        raise Found(S)

    for i in nm:
        subset_sum(nm.difference([i]), S.union([i]), M)
