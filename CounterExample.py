from aalpy.base import SUL
from aalpy.learning_algs import run_Lstar
from aalpy.oracles import RandomWalkEqOracle
from aalpy.utils import visualize_automaton


class CounterSUL(SUL):
    def __init__(self, max_count=5):
        super().__init__()
        self.max_count = max_count
        self.counter = 0

    def pre(self):
        self.counter = 0

    def post(self):
        pass

    def step(self, letter):
        if letter is None:
            return self.counter
        self.counter += letter
        if self.counter > self.max_count:
            return 'MAX_PASSED'
        return self.counter


sul = CounterSUL(5)
input_al = [1, 2, 3]

eq_oracle = RandomWalkEqOracle(input_al, sul, num_steps=5000, reset_prob=0.9, reset_after_cex=True)

model = run_Lstar(input_al, sul, eq_oracle, 'mealy') # moore is better than mealy for visualization

visualize_automaton(model)
