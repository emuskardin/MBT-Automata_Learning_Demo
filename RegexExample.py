from aalpy.base import SUL
import re

from aalpy.learning_algs import run_Lstar
from aalpy.oracles import RandomWalkEqOracle
from aalpy.utils import visualize_automaton


class RegexSUL(SUL):
    """
    An example implementation of a system under learning that can be used to learn any regex expression.
    Note that the $ is added to the expression as in this SUL only exact matches are learned.
    """

    def __init__(self, regex: str):
        super().__init__()
        self.regex = regex if regex[-1] == '$' else regex + '$'
        self.string = ""

    def pre(self):
        self.string = ""
        pass

    def post(self):
        pass

    def step(self, letter):
        """
        Args:
            letter: single element of the input alphabet
        Returns:
            Whether the current string (previous string + letter) is accepted
        """
        if letter is not None:
            self.string += str(letter)
        return True if re.match(self.regex, self.string) else False


regex = 'edi(a|b)+'
input_al = [i for i in list(regex) if i not in {'(', ')', '+', '*', '|'}]

sul = RegexSUL(regex)

eq_oracle = RandomWalkEqOracle(input_al, sul, num_steps=10000, reset_after_cex=True)

model = run_Lstar(input_al, sul, eq_oracle, 'dfa', print_level=3)

visualize_automaton(model)
