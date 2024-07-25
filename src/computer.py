import player as p
import copy
import sys
import time


class Computer(p.Player):
    def __init__(self, name, opponent, game, depth, mode, eval_strat):
        super().__init__(name, eval_strat, opponent, game)
        self.depth = depth
        self.mode = mode
        self.eval_strat = eval_strat

    def choose_a_hole(self):
        self.moves_count += 1
        start = time.time()
        print("chosen hole: ")
        if self.mode == 'min_max':
            hole = self.min_max_choice(self.name)
        else:
            hole = self.min_max_alpha_beta_choice(self.name)
        print(hole + 1)
        end = time.time()
        self.moves_time += (end - start)
        print(f'{end - start}s')
        return hole

    def min_max_choice(self, name):
        hole_eval_list = {}
        for hole in self.get_valid_holes():
            self_copy = copy.deepcopy(self)
            move = self_copy.game.move
            self_copy.game.make_move(self_copy, hole, move)
            if self_copy.game.get_current_player() == self:
                hole_eval_list[hole] = self.max_value(0, self_copy, name)
            else:
                hole_eval_list[hole] = self.min_value(0, self_copy.opponent, name)

        return max(hole_eval_list, key=lambda key: hole_eval_list[key])

    def max_value(self, depth, current_player, name):
        if depth >= self.depth:
            return current_player.evaluate_board(name)

        value = - sys.maxsize
        for hole in current_player.get_valid_holes():
            self_copy = copy.deepcopy(current_player)
            move = self_copy.game.move
            self_copy.game.make_move(self_copy, hole, move + 1)
            if self_copy.game.get_current_player() == self:
                v = self.max_value(depth + 1, self_copy, name)
            else:
                v = self.min_value(depth + 1, self_copy.opponent, name)
            if v > value:
                value = v

        return value

    def min_value(self, depth, current_player, name):
        if depth >= self.depth:
            return current_player.evaluate_board(name)

        value = sys.maxsize
        for hole in current_player.get_valid_holes():
            self_copy = copy.deepcopy(current_player)
            move = self_copy.game.move
            self_copy.game.make_move(self_copy, hole, move + 1)
            if self_copy.game.get_current_player() == self:
                v = self.min_value(depth + 1, self_copy, name)
            else:
                v = self.max_value(depth + 1, self_copy.opponent, name)
            if v < value:
                value = v

        return value

    def min_max_alpha_beta_choice(self, name):
        hole_eval_list = {}
        for hole in self.get_valid_holes():
            self_copy = copy.deepcopy(self)
            move = self_copy.game.move
            self_copy.game.make_move(self_copy, hole, move)
            if self_copy.game.get_current_player() == self:
                hole_eval_list[hole] = self.max_value_alpha_beta(0, self_copy, name, -sys.maxsize, sys.maxsize)
            else:
                hole_eval_list[hole] = self.min_value_alpha_beta(0, self_copy.opponent, name, -sys.maxsize, sys.maxsize)

        print(hole_eval_list)
        return max(hole_eval_list, key=lambda key: hole_eval_list[key])

    def max_value_alpha_beta(self, depth, current_player, name, alpha, beta):
        if depth >= self.depth:
            return current_player.evaluate_board(name)

        value = - sys.maxsize
        for hole in current_player.get_valid_holes():
            self_copy = copy.deepcopy(current_player)
            move = self_copy.game.move
            self_copy.game.make_move(self_copy, hole, move + 1)
            if self_copy.game.get_current_player() == self:
                v = self.max_value_alpha_beta(depth + 1, self_copy, name, alpha, beta)
            else:
                v = self.min_value_alpha_beta(depth + 1, self_copy.opponent, name, alpha, beta)
            if v > value:
                value = v
            if v >= beta:
                return value
            if v > alpha:
                alpha = v

        return value

    def min_value_alpha_beta(self, depth, current_player, name, alpha, beta):
        if depth >= self.depth:
            return current_player.evaluate_board(name)

        value = sys.maxsize
        for hole in current_player.get_valid_holes():
            self_copy = copy.deepcopy(current_player)
            move = self_copy.game.move
            self_copy.game.make_move(self_copy, hole, move + 1)
            if self_copy.game.get_current_player() == self:
                v = self.min_value_alpha_beta(depth + 1, self_copy, name, alpha, beta)
            else:
                v = self.max_value_alpha_beta(depth + 1, self_copy.opponent, name, alpha, beta)
            if v < value:
                value = v
            if v <= alpha:
                return value
            if v < beta:
                beta = v

        return value
