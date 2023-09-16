import random

"""This program plays a game of Rock, Paper, Scissors between two Players,
and reports both Player's scores each round."""


class Player:
    """The Player class is the parent class for all  the Players
    in this game"""

    player_moves = ['rock', 'paper', 'scissors']
    opponent_move = ''
    my_move = ''

    def move(self):
        """
        Returns a player's move
        To be implemented by subclasses
        """
        pass

    def learn(self, my_move, their_move):
        """
        Sets the opponents move
        :param my_move: player's move
        :param their_move: opponent's move
        """
        self.my_move = my_move
        self.opponent_move = their_move


class RockPlayer(Player):
    """
    Rock Player always plays rock
    :arg: Player representing the Parent class
    """

    def move(self):
        """
        Returns a player's move
        :return: next move (e.g., 'rock' as string)
        """
        return 'rock'

    def __str__(self):
        return 'Rock Player'


class RandomPlayer(Player):
    """
    Random player plays any random moves
    :arg: Player: Parent class
    """

    def move(self):
        """
        Returns a player's move
        :return: next move (e.g., 'rock' as string)
        """
        return random.choice(self.player_moves)

    def __str__(self):
        return 'Random Player'


class ReflectPlayer(Player):
    """
    ReflectPlayer class remembers what move the opponent played last round, and plays that move this round.
    (So, if you play 'paper' on the first round, a ReflectPlayer will play 'paper' on the second round.)
    """

    def __init__(self):
        self._call_count = 0

    def move(self):
        """
        Returns a player's move
        :return: next move (e.g., 'rock' as string)
        """

        if (self.opponent_move in self.player_moves) and (self._call_count > 0):
            index_of_move = self.player_moves.index(self.opponent_move)
            return self.player_moves[index_of_move]
        self._call_count = 1
        return random.choice(self.player_moves)

    def __str__(self):
        return 'Reflect Player'


class CyclePlayer(Player):
    """
    CyclePlayer class remembers what move it played last round, and cycles through the different moves.
    (If it played 'rock' this round, it should play 'paper' in the next round.)

    """

    def __init__(self):
        self._call_count = 0
        self._next_move = ''

    def move(self):
        """
        Returns the move of the Cycle Player
        :return: next move of player as string (e.g 'scissors')
        """
        if self._call_count == 0:
            self._call_count = 1
            self._next_move = random.choice(self.player_moves)
            return self._next_move

        index_of_current_move = self.player_moves.index(self._next_move)
        index_of_next_move = (index_of_current_move + 1) % len(self.player_moves)
        self._next_move = self.player_moves[index_of_next_move]
        return self._next_move

    def __str__(self):
        return 'Cycle Player'


class HumanPlayer(Player):
    """
    Plays game based on user's moves
    """

    def get_player_move(self):
        """
        Prompts the user for a move and returns the move
        :return: user moves as string
        """
        user_move = input('Rock, paper, scissors? > ')
        if user_move.lower() == 'quit':
            return user_move
        else:
            while user_move.lower() not in self.player_moves:
                user_move = input('Rock, paper, scissors? > ')
                if user_move.lower() == 'quit':
                    break
            return user_move.lower()

    def move(self):
        return self.get_player_move()


class Game:
    """"
    Game class executes the game play according to the moves played
    """

    def __init__(self, player_1, player_2):
        """
        constructor of the Game class.
        :param player_1: player 1 representing a player Object
        :param player_2: player 2 representing a player Object
        """
        self._p1 = player_1
        self._p2 = player_2
        self._p1_score = 0
        self._p2_score = 0
        self._game_round = 0

    @staticmethod
    def beats(one, two):
        """
        Executes the game rules.
        :param one: string representing move of player1(e.g. rock, paper or scissors)
        :param two: string representing move of player2(e.g. rock, paper or scissors)
        :return: Returns true or false if the conditions are met
        """
        return (one == 'rock' and two == 'scissors') or \
            (one == 'scissors' and two == 'paper') or \
            (one == 'paper' and two == 'rock')

    def round_winner(self, move1, move2):
        """
        Checks and returns the winner of each round during the game play. Updates each player score.
        :param move1:  move of player1(e.g. rock, paper or scissors) as string
        :param move2: move of player2 as string
        :return: winner of each round as string
        """

        player_one_wins = self.beats(move1, move2)
        if move1 == move2:
            return ' ** TIE ** '
        elif player_one_wins:
            self._p1_score += 1
            return ' ** PLAYER ONE WINS ** '
        else:
            self._p2_score += 1
            return ' ** PLAYER TWO WINS ** '

    def play_round(self):
        """
        Executes each game round.
        """

        print(f"\nRound {self._game_round} --")
        move1 = self._p1.move()
        move2 = self._p2.move()

        while (move1 != 'quit') and (self._game_round < 10):
            print(f"You played {move1}\nOpponent played {move2}")
            print(self.round_winner(move1, move2))
            print(f'Score: Player One {self._p1_score}, Player Two {self._p2_score}')
            self._game_round += 1

            self._p1.learn(move1, move2)
            self._p2.learn(move2, move1)

            print(f"\nRound {self._game_round} --")
            move1 = self._p1.move()
            move2 = self._p2.move()

        # Exits game if user enters 'quit' or game finishes at round 10
        print("Game over!")
        self.announce_winner()

    def announce_winner(self):
        if self._p1_score > self._p2_score:
            print("** Congratulations. You Won! **")
            print(f" You scored: {self._p1_score} *** Opponent scored: {self._p2_score}")
        elif self._p1_score < self._p2_score:
            print("** You Lost! **")
            print(f"Opponent scored: {self._p2_score} *** You scored: {self._p1_score}")
        if self._p1_score == self._p2_score:
            print("** TIE **")
            print(f" You scored: {self._p1_score} *** Opponent scored: {self._p2_score}")


def play_game():
    """
    Prompts user to select a player to play against.
    Calls the player based on user's input
    """
    game_players = ("""
Players:
    1. Cycle player
    2. Reflect player
    3. Rock player
    4. Random player
    
Select the player strategy you want to play against: """)

    game_strategies = {
        "1": CyclePlayer(),
        "2": ReflectPlayer(),
        "3": RockPlayer(),
        "4": RandomPlayer(),
    }

    # Validates user's input
    user_input = input(game_players)
    while user_input not in game_strategies:
        print(f'\nError: {user_input} is not a valid option! Please select an option below.')
        user_input = input(game_players)

    print(f"""
Game start!
You are playing against {game_strategies[user_input]}
Enter 'quit' to exit the game! """)

    game = Game(HumanPlayer(), game_strategies[user_input])
    game.play_round()


if __name__ == '__main__':
    play_game()