class BrainfuckException(Exception):
    pass


class BLexer:
    """ Static class encapsulating functionality for lexing Brainfuck programs. """

    symbols = [
        '>', '<', '+', '-',
        '.', ',', '[', ']'
    ]

    @staticmethod
    def lex(code):
        """ Return a generator for tokens in some Brainfuck code. """
        # The syntax of Brainfuck is so simple that nothing is really gained from converting
        # symbols to some sort of Token object. Just ignore everything that isn't in Brainfuck's
        # syntax.
        return (char for char in code if char in BLexer.symbols)


class BrainfuckMachine:

    """ Class encapsulating the core operations of a brainfuck machine. Namely,
            - Move pointer left,
            - Move pointer right,
            - Increment cell under pointer,
            - Decrement cell under pointer,
            - Output value of cell under pointer,
            - Input value to cell under pointer.
    """
    
    def __init__(self, cells=256, in_func=input, out_func=chr):
        self.cells = [0] * cells
        self.ptr = 0
        self.in_func = in_func
        self.out_func = out_func

        self.looppos = []
        self.out_buffer = []

    def right(self):
        if self.ptr < len(self.cells)-1:
            self.ptr += 1

    def left(self):
        if self.ptr > 0:
            self.ptr -= 1

    def incr(self):
        self.cells[self.ptr] += 1

    def decr(self):
        self.cells[self.ptr] -= 1

    def value(self):
        """ Return the value of the cell under the pointer. """
        return self.cells[self.ptr]

    def outf(self):
        return self.out_func(self.cells[self.ptr])

    def inf(self):
        self.cells[self.ptr] = self.in_func()


class BInterpreter:
    """ Class encapsulating interpretation functionality for brainfuck code. """

    def __init__(self, machine=None):
        if machine:
            self.machine = machine
        else:
            self.machine = BrainfuckMachine()

    def interpret_code(self, code):
        """ Interpret each character in a list or string of brainfuck tokens. """

        # Iterate through every character in the code. Use indexing so that we can
        # jump as necessary for square bracket loops. To identify matching brackets for forward
        # jumps, move forward a position at a time, keeping track of the nesting level (starts at 1). When a 
        # open bracket ([) is encountered, increment the nesting level, and when a close bracket
        # (]) is found, decrement it. When nesting level reaches 0, the matching bracket has been found.
        # For finding the correct bracket for a backwards jump, do the same thing but with
        # backwards iteration and swap when you increment and decrement.
        pos = 0        
        while pos < len(code):
            
            if code[pos] == '[':
                if self.machine.value() == 0:
                    nest = 1
                    while nest != 0:
                        pos += 1
                        if code[pos] == '[':
                            nest += 1
                        elif code[pos] == ']':
                            nest -= 1
                    pos += 1
                        
                else:
                    pos += 1

            elif code[pos] == ']':
                if self.machine.value() != 0:
                    nest = 1
                    while nest != 0:
                        pos -= 1
                        if code[pos] == ']':
                            nest += 1
                        elif code[pos] == '[':
                            nest -= 1
                    pos += 1
        
                else:
                    pos += 1
            
            else:
                self.interpret_one(code[pos])
                pos += 1

    def interpret_one(self, char):
        """ Perform the appropriate operation for a single brainfuck character. """
        if char == '>':
            self.machine.right()
        elif char == '<':
            self.machine.left()
        elif char == '+':
            self.machine.incr()
        elif char == '-':
            self.machine.decr()
        elif char == '.':
            # TODO output checks
            print(self.machine.outf(), end='')
        elif char == ',':
            # TODO input checks
            self.machine.inf()         


if __name__ == '__main__':
    bfm = BrainfuckMachine(cells=8, out_func=chr)
    bi = BInterpreter(bfm)

    f = open('helloworld', 'r').read()
    code = list(BLexer.lex(f))

    bi.interpret_code(code)