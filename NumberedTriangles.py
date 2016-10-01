"""
Our robots like games that require the ability to calculate equations. Mission control recently sent them the new game
to occupy their time while flying from one Island to the next. This game is called "Numbered Triangles".
Players take 6 chips from the pile, each chip is made of an equilateral triangle with three numbers one on each edge.
You can move, rotate and flip the chips so they form a hexagon. The hexagon is only legal if the adjacent edges for each
triangle have matching numbers.
The score for a legal hexagon is the sum of the numbers on the outside six edges. The player's goal is to find the
highest score that can be achieved with the given six chips.
Each chip is represented as a list with three positive numbers. You should help the robots find the highest score for
the given chips and return the score as a number. If you cannot form legal hexagon from the chips, then return a score
of 0.
Input: The chip info as a list of lists. Each list contain three integers.
Output: The highest possible score as an integer.
Precondition:
len(chips) == 6
all(all(0 < x < 100 for x in ch) for ch in chips)
"""



def rotate(piece):
        return [piece[2],piece[0],piece[1]]


def create_positions(fr):
    r=[]
    if len(fr) > 1:
        next_perm = create_positions(fr[1:])
        for i in range(3):
            u=[[fr[0]]+el for el in next_perm]
            r.extend(u)
            fr[0] = rotate(fr[0])
        return r
    else:
        for i in range(3):
            r.append([fr[0]])
            fr[0] = rotate(fr[0])
        return r


def get_sum(pcs):
    return sum(a for a,b,c in pcs)


class Node:
    # pattern - numbered set of pieces
    pieces = []
    def __init__(self, placed):
        # list - what is placed already
        self.placed = placed
        # matching number for joining another pices
        self.first_last = {}
        self.children = set()
        self.free = [x for x in range(6) if not(x in placed)]

    def get_match_numbers(self, piece):
        return Node.pieces[piece][1][1:]

    def create_child(self, piece):
        pmatch = self.get_match_numbers(piece)
        if self.first_last['f'] in pmatch:
            child = Node([piece]+self.placed)
            child.first_last['f'] = pmatch[0] if pmatch[1] == self.first_last['f'] else pmatch[1]
            child.first_last['l'] = self.first_last['l']
            self.children.add(child)
        if self.first_last['l'] in pmatch:
            child = Node(self.placed+[piece])
            child.first_last['l'] = pmatch[0] if pmatch[1] == self.first_last['l'] else pmatch[1]
            child.first_last['f'] = self.first_last['f']
            self.children.add(child)

    def is_ok(self):
        """is this node solution?"""
        if len(self.free) == 1: # is last piece fitting?
            numfree = self.get_match_numbers(self.free[0])
            if (self.first_last['f'] == numfree[0] and self.first_last['l'] == numfree[1])\
                    or (self.first_last['f'] == numfree[1] and self.first_last['l'] == numfree[0]):
                return True
            else:
                return False
        else: # maybe my children?
            for i in self.free:
                self.create_child(i)
        for ch in self.children:
            if ch.is_ok():
                return True
        return False

def checkio(chips):
    # create recursive all positions
    ns = create_positions(chips)
    # every position has its value
    pr = [(get_sum(x), x) for x in ns]
    # sort by value, most valuable positions are first
    sort_pos = sorted(pr, key=lambda a:a[0], reverse=True)
    # start to check positions from most valuable
    for i in sort_pos:
        Node.pieces = [*enumerate(i[1])]
        root = Node([0])
        root.first_last = {'f':Node.pieces[0][1][1], 'l':Node.pieces[0][1][2]}
        if root.is_ok(): # numbers of pices are matching
            return i[0]  # get its value
    # can't be constructed
    return 0


# These "asserts" using only for self-checking and not necessary for auto-testing
if __name__ == '__main__':
    assert checkio(
        [[1, 4, 20], [3, 1, 5], [50, 2, 3],
         [5, 2, 7], [7, 5, 20], [4, 7, 50]]) == 152, "First"
    assert checkio(
        [[1, 10, 2], [2, 20, 3], [3, 30, 4],
         [4, 40, 5], [5, 50, 6], [6, 60, 1]]) == 210, "Second"
    assert checkio(
        [[1, 2, 3], [2, 1, 3], [4, 5, 6],
         [6, 5, 4], [5, 1, 2], [6, 4, 3]]) == 21, "Third"
    assert checkio(
        [[5, 9, 5], [9, 6, 9], [6, 7, 6],
         [7, 8, 7], [8, 1, 8], [1, 2, 1]]) == 0, "Fourth"


