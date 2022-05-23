from aalpy.base import SUL
from aalpy.learning_algs import run_Lstar
from aalpy.oracles import RandomWalkEqOracle
from aalpy.utils import visualize_automaton

# SUL wrapper of the vending machine
# individual step on the vending machine is either insertion of the coin or push of the button with a selected item
from VendingMachinesImpl import VendingMachine, VendingMachineMutant1


class VendingMachineSUL(SUL):
    def __init__(self, vending_machine):
        super().__init__()
        self.vm = vending_machine

    def pre(self):
        self.vm.reset()

    def post(self):
        pass

    def step(self, letter):
        if letter[0] == 'coin':
            return self.vm.add_coin(letter[1])
        if letter[0] == 'order':
            return self.vm.push_button(letter[1])
        raise RuntimeError('Invalid input')


def learn_vending_machine():
    # initialize vending machine that we want to learn
    vending_machine = VendingMachine()
    # define the input alphabet
    input_alphabet = [('coin', 0.5), ('coin', 1), ('coin', 2), ('order', 'coke'), ('order', 'water'),
                      ('order', 'peanuts')]
    # input_alphabet = [('coin', 1), ('order', 'coke')]

    # wrap the vending machine in SUL interface
    sul = VendingMachineSUL(vending_machine)
    # define the equivalence oracle used for conformance testing during learning
    eq_oracle = RandomWalkEqOracle(input_alphabet, sul, num_steps=4000, reset_prob=0.1)

    # learn the mealy machine capturing the input-output behaviour of the vending machine
    learned_model = run_Lstar(input_alphabet, sul, eq_oracle, 'mealy')

    # visualize the model
    visualize_automaton(learned_model)


def learn_vending_machine_dfa():
    class VendingMachineDFA_SUL(SUL):
        def __init__(self, vending_machine, target_item):
            super().__init__()
            self.vm = vending_machine
            self.target_item = target_item

        def pre(self):
            self.vm.reset()

        def post(self):
            pass

        def step(self, letter):
            if letter is None:
                return False
            if letter[0] == 'coin':
                self.vm.add_coin(letter[1])
            if letter[0] == 'order':
                out = self.vm.push_button(letter[1])
                if out == self.target_item:
                    return True
            return False

    vending_machine = VendingMachine()
    input_alphabet = [('coin', 0.5), ('coin', 1), ('coin', 2), ('order', 'coke'), ('order', 'water'),
                      ('order', 'peanuts')]

    sul = VendingMachineDFA_SUL(vending_machine, 'Peanuts')
    eq_oracle = RandomWalkEqOracle(input_alphabet, sul, num_steps=2000, reset_prob=0.1)

    learned_model = run_Lstar(input_alphabet, sul, eq_oracle, 'dfa')

    visualize_automaton(learned_model)


def learning_based_testing(vm1, vm2):
    # define the input alphabet
    input_alphabet = [('coin', 0.5), ('coin', 1), ('coin', 2), ('order', 'coke'), ('order', 'water'),
                      ('order', 'peanuts')]

    # we learn the complete model of one vending machine
    sul_base = VendingMachineSUL(vm1)
    eq_oracle_1 = RandomWalkEqOracle(input_alphabet, sul_base, num_steps=2000, reset_prob=0.1)
    learned_model = run_Lstar(input_alphabet, sul_base, eq_oracle_1, 'mealy')

    # we initialize second vending machine SUL
    sul_test = VendingMachineSUL(vm2)
    eq_oracle_2 = RandomWalkEqOracle(input_alphabet, sul_test, num_steps=2000, reset_after_cex=0.1)
    print('Starting the search for counterexamples:')
    for _ in range(10):
        # given a second "test" SUL, we perform conformance testing against the previously learned model
        # if they are same, no counterexamples will be found
        cex = eq_oracle_2.find_cex(learned_model)
        if cex:
            print(cex)
            out1 = sul_base.query(cex)
            out2 = sul_test.query(cex)
            print(out1)
            print(out2)
            print('---------------------------------------------')


# learn_vending_machine()

learning_based_testing(VendingMachine(), VendingMachineMutant1())
