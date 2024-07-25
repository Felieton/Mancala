import human as h
import computer as c
import random as rand

HUMAN_VS_HUMAN = '1'
HUMAN_VS_MACHINE = '2'
COMPUTER_VS_COMPUTER = '3'


class Game:
    def __init__(self):
        self.south_player = None
        self.north_player = None
        self.game_mode = None
        self.move = 1
        self.pass_move = False
        self.first_random_move = False

    def start(self):
        self.game_mode_choice()
        self.game()

    def game_mode_choice(self):
        print("------MANCALA------")
        print("1. human vs human")
        print("2. human vs computer")
        choice = input("Choose the game mode: ")

        if choice == HUMAN_VS_HUMAN:
            self.south_player = h.Human(input("south player's name: "))
            self.north_player = h.Human(input("north player's name: "))
            self.game_mode = HUMAN_VS_HUMAN
        elif choice == HUMAN_VS_MACHINE:
            choice = input("Who starts the game, player or computer p/c: ")
            if choice == 'p':
                self.south_player = h.Human(input("south player's name: "))
                self.north_player = c.Computer("Computer", self.south_player, self, 2, 'min_max', "well")
                self.south_player.opponent = self.north_player
                self.south_player.game = self
            else:
                self.north_player = h.Human(input("south player's name: "))
                self.south_player = c.Computer("Computer", self.north_player, self, 0, 'alpha_beta', "well")
                self.north_player.opponent = self.south_player
                self.north_player.game = self
            self.game_mode = HUMAN_VS_MACHINE

        choice = input("set south player's first move to random y/n: ")
        if choice == 'y':
            self.first_random_move = True

    def print_game_state(self):
        print(f'\n----------MANCALA----------\n        6 5 4 3 2 1\n        '
              f'{self.north_player.holes[5]}|{self.north_player.holes[4]}|{self.north_player.holes[3]}'
              f'|{self.north_player.holes[2]}|{self.north_player.holes[1]}|{self.north_player.holes[0]}')
        print(f'N[{self.north_player.well}]')
        print(f'                       S[{self.south_player.well}]')
        print(f'        {self.south_player.holes[0]}|{self.south_player.holes[1]}|{self.south_player.holes[2]}'
              f'|{self.south_player.holes[3]}|{self.south_player.holes[4]}|{self.south_player.holes[5]}\n'
              f'        1 2 3 4 5 6')
        print("---------------------------")

    def get_current_player(self):
        if self.move % 2 == 1:
            return self.south_player
        else:
            return self.north_player

    def get_other_player(self, player):
        if player == self.south_player:
            return self.north_player
        else:
            return self.south_player

    def has_legal_move(self, player):
        for hole in player.holes:
            if hole != 0:
                return True

        return False

    def get_score_from_holes(self, player):
        holes_sum = 0
        for hole in player.holes:
            holes_sum += hole

        return holes_sum

    def endgame(self):
        print("GAME OVER")
        south_total_score = self.south_player.well + self.get_score_from_holes(self.north_player)
        north_total_score = self.north_player.well + self.get_score_from_holes(self.south_player)

        if south_total_score > north_total_score:
            print(f"The winner is south player ({self.south_player.name})!")
        elif north_total_score > south_total_score:
            print(f"The winner is north player ({self.north_player.name})!")
        else:
            print("Draw!")

        print(f"\nsouth player score: {south_total_score}\n    well: {self.south_player.well}\n"
              f"    north player's board: {south_total_score - self.south_player.well}\n"
              f"    number of moves: {self.south_player.moves_count}\n"
              f"    average time per move: {round(self.south_player.moves_time/self.south_player.moves_count, 2)}s")
        print(f"north player score: {north_total_score}\n    well: {self.north_player.well}\n"
              f"    south player's board: {north_total_score - self.north_player.well}\n"
              f"    number of moves: {self.north_player.moves_count}\n"
              f"    average time per move: {round(self.north_player.moves_time / self.north_player.moves_count, 2)}s")

    def make_move(self, making_move_player, chosen_hole_from_zero, move):
        self.move = move
        self.pass_move = False
        current_player = self.get_current_player()
        while current_player.holes[chosen_hole_from_zero] == 0:
            chosen_hole_from_zero = int(input("choose a valid hole: ")) - 1

        stones_in_hole = current_player.holes[chosen_hole_from_zero]
        current_player.holes[chosen_hole_from_zero] = 0
        current_hole = chosen_hole_from_zero + 1

        stone = 0
        while stone < stones_in_hole:
            if current_hole < 6 and stone == stones_in_hole - 1 and making_move_player == current_player\
                    and current_player.holes[current_hole] == 0 and\
                    self.get_other_player(current_player).holes[5 - current_hole] != 0:
                current_player.well += self.get_other_player(current_player).holes[5 - current_hole] + 1
                self.get_other_player(current_player).holes[5 - current_hole] = 0

            elif current_hole < 6:
                current_player.holes[current_hole] += 1

            elif current_hole == 6:
                if making_move_player == current_player:
                    current_player.well += 1

                current_player = self.get_other_player(current_player)
                current_hole = -1

                if making_move_player == current_player:
                    stone -= 1

            current_hole += 1
            stone += 1

        if current_hole == 0 and making_move_player != current_player:
            self.pass_move = True

    def game(self):
        while self.has_legal_move(self.get_current_player()):
            self.print_game_state()

            if self.move % 2 == 1:
                print(f"south player ({self.south_player.name})'s move:")
            else:
                print(f"north player ({self.north_player.name})'s move:")

            if self.first_random_move:
                move_choice = rand.randint(0, 5)
                print(f"randomly chosen hole: {move_choice + 1}")
            else:
                move_choice = self.get_current_player().choose_a_hole()

            self.first_random_move = False
            self.make_move(self.get_current_player(), move_choice, self.move)
            if not self.pass_move:
                self.move += 1

        self.endgame()
