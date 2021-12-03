from aalpy.base import SUL
from aalpy.learning_algs import run_Lstar
from aalpy.oracles import RandomWMethodEqOracle
from aalpy.utils import visualize_automaton


class GearBox:
    def __init__(self, num_gears=5):
        self.gear = 1
        self.num_gears = num_gears
        self.faults = []
        self.reverse_fault_counter = 0

        self.clutch_pressed = False
        self.gear_changed = False

    def reset(self):
        self.gear = 1
        self.faults = []
        self.reverse_fault_counter = 0
        self.clutch_pressed = False
        self.gear_changed = False

    def press_clutch(self):
        if not self.clutch_pressed:
            self.clutch_pressed = True
            return 'CLUTCH_PRESSED'
        return 'NO_EFFECT'

    def release_clutch(self):
        if self.clutch_pressed:
            self.clutch_pressed = False
            self.gear_changed = False
            return 'CLUTCH_RELEASED'
        return 'NO_EFFECT'

    def put_in_reverse(self):
        if self.clutch_pressed and not self.gear_changed:
            if self.gear == 1:
                self.gear = -1
                self.gear_changed = True
                return self.gear
            else:
                self.reverse_fault_counter += 1
                if self.reverse_fault_counter >= 2:
                    return "BROKEN"
                return self.gear
        return 'NO_EFFECT'

    def increase_gear(self):
        if self.clutch_pressed and not self.gear_changed:
            self.gear = min(max(self.gear + 1, 1), self.num_gears)
            self.gear_changed = True
            return self.gear
        return 'NO_EFFECT'

    def decrease_gear(self):
        if self.clutch_pressed and not self.gear_changed:
            self.gear = max(self.gear - 1, 1)
            self.gear_changed = True
            return self.gear
        return 'NO_EFFECT'


class GearBoxSUL(SUL):
    def __init__(self):
        super().__init__()
        self.gearbox = GearBox()

    def pre(self):
        self.gearbox.reset()

    def post(self):
        pass

    def step(self, letter):
        if letter == 'press_clutch':
            out = self.gearbox.press_clutch()
        elif letter == 'release_clutch':
            out = self.gearbox.release_clutch()
        elif letter == 'put_in_reverse':
            out = self.gearbox.put_in_reverse()
        elif letter == 'increase_gear':
            out = self.gearbox.increase_gear()
        else:
            out = self.gearbox.decrease_gear()
        return out


alphabet = ['press_clutch', 'release_clutch', 'put_in_reverse', 'increase_gear', 'decrease_gear']

sul = GearBoxSUL()

eq_oracle = RandomWMethodEqOracle(alphabet, sul, walks_per_state=2000, walk_len=15)

learned_model = run_Lstar(alphabet, sul, eq_oracle, automaton_type='mealy')

visualize_automaton(learned_model, display_same_state_trans=False)
