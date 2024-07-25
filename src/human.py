import player as p
import time


class Human(p.Player):
    def __init__(self, name):
        super().__init__(name)

    def choose_a_hole(self):
        self.moves_count += 1
        start = time.time()
        chosen_hole = int(input("choose hole: ")) - 1
        end = time.time()
        self.moves_time += (end - start)
        print(f'{end - start}s')
        return chosen_hole
