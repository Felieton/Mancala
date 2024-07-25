class Player:
    def __init__(self, name, eval_strat="well", opponent=None, game=None):
        self.name = name
        self.well = 0
        self.holes = [4, 4, 4, 4, 4, 4]
        self.opponent = opponent
        self.game = game
        self.moves_count = 0
        self.moves_time = 0
        self.eval_strat = eval_strat

    def choose_a_hole(self):
        pass

    def get_valid_holes(self):
        valid_holes = []
        for i in range(6):
            if self.holes[i] != 0:
                valid_holes.append(i)

        return valid_holes

    def evaluate_board(self, name):
        if self.eval_strat == "well":
            return self.well_difference(name)
        elif self.eval_strat == "holes":
            return self.holes_sum(name)
        else:
            return self.score_difference(name)

    def well_difference(self, name):
        if self.name == name:
            return self.well - self.opponent.well
        else:
            return self.opponent.well - self.well

    def holes_sum(self, name):
        sum = 0
        for i in range(6):
            sum += self.holes[i]

        if self.name == name:
            return -sum
        else:
            return sum

    def score_difference(self, name):
        self_points = self.well
        opponent_points = self.opponent.well

        for i in range(6):
            opponent_points += self.holes[i]
            self_points += self.opponent.holes[i]

        if self.name == name:
            return self_points - opponent_points
        else:
            return opponent_points - self_points
