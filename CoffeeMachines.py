import random

from aalpy.base import SUL
from aalpy.learning_algs import run_stochastic_Lstar, run_Lstar
from aalpy.oracles import RandomWordEqOracle, RandomWMethodEqOracle
from aalpy.utils import visualize_automaton


class DeterministicCoffeeMachine:
    def __init__(self, inject_fault=True):
        self.counter = 0
        self.inject_fault = inject_fault

    def add_coin(self):
        if self.counter == 3:
            return 'CoinsFull'
        self.counter = min(self.counter + 1, 3)
        return 'CoinAdded'

    def button(self):
        if self.counter >= 2:
            if self.inject_fault:
                self.counter -= 1 if self.counter == 3 else 2
            else:
                self.counter -= 2
            return 'Coffee'
        else:
            return 'NoAction'


class DeterministicCoffeeMachineDFA:
    def __init__(self):
        self.counter = 0
        self.max_coins_reached = False

    def add_coin(self):
        if self.counter == 3:
            return False
        self.counter = min(self.counter + 1, 3)
        return False

    def button(self):
        if self.counter == 3:
            self.counter -= 1
            return True
        if self.counter == 2:
            self.counter -= 2
        return False


class StochasticCoffeeMachine:
    def __init__(self):
        self.counter = 0

    def add_coin(self):
        if self.counter == 3:
            if random.random() >= 0.2:
                return 'CoinsFull'
            else:
                self.counter = 0
                return 'ReturnCoins'
        self.counter = min(self.counter + 1, 3)
        return 'CoinAdded'

    def button(self):
        if self.counter >= 2:
            self.counter -= 2
            return 'Coffee'
        else:
            if random.random() <= 0.02:
                self.counter = 0
                return 'Coffee'
            return 'NoAction'


class FaultyCoffeeMachineSUL(SUL):
    def __init__(self):
        super().__init__()
        self.coffee_machine = DeterministicCoffeeMachine(True)

    def pre(self):
        self.coffee_machine.counter = 0

    def post(self):
        pass

    def step(self, letter):
        if letter == 'coin':
            return self.coffee_machine.add_coin()
        else:
            return self.coffee_machine.button()


class FaultyCoffeeMachineSULDFA(SUL):
    def __init__(self):
        super().__init__()
        self.coffee_machine = DeterministicCoffeeMachineDFA()

    def pre(self):
        self.coffee_machine.counter = 0
        self.coffee_machine.max_coins_reached = False

    def post(self):
        pass

    def step(self, letter):
        if letter == 'coin':
            return self.coffee_machine.add_coin()
        else:
            return self.coffee_machine.button()


class StochasticCoffeeMachineSUL(SUL):
    def __init__(self):
        super().__init__()
        self.coffee_machine = StochasticCoffeeMachine()

    def pre(self):
        self.coffee_machine.counter = 0

    def post(self):
        pass

    def step(self, letter):
        if letter == 'coin':
            return self.coffee_machine.add_coin()
        else:
            return self.coffee_machine.button()


def learn_coffee_machine(visualize=False):
    sul = FaultyCoffeeMachineSUL()
    alphabet = ['coin', 'button']

    eq_oracle = RandomWMethodEqOracle(alphabet, sul, walks_per_state=5000, walk_len=20)

    learned_model = run_Lstar(alphabet, sul, eq_oracle, automaton_type='mealy', cache_and_non_det_check=True)

    if visualize:
        visualize_automaton(learned_model, display_same_state_trans=True)

    return learned_model


def learn_language_of_coffee_machine_error(visualize=False):
    sul = FaultyCoffeeMachineSULDFA()
    alphabet = ['coin', 'button']

    eq_oracle = RandomWMethodEqOracle(alphabet, sul, walks_per_state=5000, walk_len=20)

    learned_model = run_Lstar(alphabet, sul, eq_oracle, automaton_type='dfa', cache_and_non_det_check=True)

    if visualize:
        visualize_automaton(learned_model, display_same_state_trans=True)

    return learned_model


def learn_stochastic_coffee_machine(visualize=False):
    sul = StochasticCoffeeMachineSUL()
    alphabet = ['coin', 'button']

    eq_oracle = RandomWordEqOracle(alphabet, sul, num_walks=2000, min_walk_len=5, max_walk_len=10)

    learned_model = run_stochastic_Lstar(alphabet, sul, eq_oracle, automaton_type='smm', cex_processing=None)

    if visualize:
        visualize_automaton(learned_model, display_same_state_trans=True)

    return learned_model


learn_coffee_machine(visualize=True)
#learn_language_of_coffee_machine_error(True)
#learn_stochastic_coffee_machine(visualize=True)
