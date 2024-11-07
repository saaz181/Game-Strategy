from itertools import chain

matrix_size = int(input())

player_1_payoffs = []
player_2_payoffs = []

# taking inputs
for i in range(matrix_size):
    x = input().split()
    player_1_payoffs.append(list(map(float, x)))


for i in range(matrix_size):
    x = input().split()
    player_2_payoffs.append(list(map(float, x)))


# flattening the payoff matrix for players
chained = chain.from_iterable(player_1_payoffs)
player_1_payoffs = list(chained)

chained = chain.from_iterable(player_2_payoffs)
player_2_payoffs = list(chained)

matrix = [[] for _ in range(matrix_size)]

i = 0
for j in range(len(player_1_payoffs)):
    matrix[i].append([player_1_payoffs[j], player_2_payoffs[j]])
    if (j + 1) % matrix_size == 0:
        i += 1

    if i >= matrix_size:
        break


NUMBER_OF_STRATEGIES = matrix_size


def strategy_pay_off(player_1_strategy, player_2_strategy, pay_off_matrix, indexed_player=None) -> [int, int]:
    if indexed_player and indexed_player == 2:
        return pay_off_matrix[player_2_strategy - 1][player_1_strategy - 1]

    return pay_off_matrix[player_1_strategy - 1][player_2_strategy - 1]


def best_response(player, other_player_move, pay_off_matrix):
    """
    :param pay_off_matrix:
    :param player: player can have indexes from 1, 2, ....
    :param other_player_move: the move that other player moves
    :return: the maximum value the player can get
    """

    response_values = []  # store all the values that player will respond to other player move
    strategy = []  # the strategy number -> 1, 2, 3, ....

    for i in range(1, NUMBER_OF_STRATEGIES + 1):
        # get the response value
        strategy_val_for_player = \
            strategy_pay_off(i, other_player_move, pay_off_matrix, indexed_player=player)[player - 1]

        response_values.append(strategy_val_for_player)
        strategy.append(i)

    maximum = max(response_values)  # maximum value of the responses

    # the strategy(ies) number(index) which have the maximum value
    best_strategy = list(filter(lambda x: response_values[strategy.index(x)] == maximum, strategy))

    return best_strategy


def nash_equilibrium(pay_off_matrix):
    nash_eq = []  # store nash equilibrium

    for move in range(1, NUMBER_OF_STRATEGIES + 1):
        best_res_1 = best_response(1, move, pay_off_matrix)  # get the best response of player 1 when player 2 plays
        # "move"

        for _move in range(1, NUMBER_OF_STRATEGIES + 1):
            best_res_2 = best_response(2, _move,
                                       pay_off_matrix)  # get the best response of player 2 when player 1 plays
            # "_move"

            if move in best_res_2 and _move in best_res_1:  # check if it is nash equilibrium
                nash_eq.append([move, _move])

    if len(nash_eq) == 0:
        return None

    nashes = ""
    for nash in nash_eq:
        nash_str = f"({nash[0]}, {nash[1]}) "
        nashes += nash_str

    return nashes


def strongly_dominant_strategy(player, pay_off_matrix):
    best_strategies = []  # store best responses of player to all the other player strategies
    for i in range(1, NUMBER_OF_STRATEGIES + 1):
        best_strategy = best_response(player, i, pay_off_matrix)
        #  because it is strongly dominated, there must be one best strategy
        if len(best_strategy) == 1:
            best_strategies.append(best_strategy[0])
        else:
            return None

    flag = True  # to check if all best strategies of player are the same
    for i in range(len(best_strategies) - 1):
        if best_strategies[i] != best_strategies[i + 1]:
            flag = False

    if flag:
        return best_strategies[0]
    return None


def weakly_dominant_strategy(player, pay_off_matrix):

    # NOTE: there exist no second weakly dominant strategy base on article:
    # https://econweb.ucsd.edu/~jsobel/200Cs09/09-ps1-ans.pdf (question 2)

    best_strategies = []  # store best responses of player to all the other player strategies
    counter = 0           # At least one of the best responses must be unique

    for i in range(1, NUMBER_OF_STRATEGIES + 1):
        best_strategy = best_response(player, i, pay_off_matrix)

        best_strategies.append(best_strategy[0])

        # to check if there is an only greater strategy
        if len(best_strategy) == 1:
            counter += 1

    if counter < 1:  # there is no one only greater strategy
        return None

    flag = True  # to check if all best strategies of player are the same
    for j in range(len(best_strategies) - 1):
        if best_strategies[j] != best_strategies[j + 1]:
            flag = False

    if flag:
        return best_strategies[0]
    return None


def strongly_dominant_strategy_equilibrium(pay_off_matrix):
    """
        the strongly dominated strategy is unique value,
        so we determine both player strongly_dominant_strategy
        and if both of them are not None then there exist a
        strongly dominant strategy equilibrium for game
    """

    profile_1 = strongly_dominant_strategy(1, pay_off_matrix)
    profile_2 = strongly_dominant_strategy(2, pay_off_matrix)

    if profile_1 is not None and profile_2 is not None:
        return f"({profile_1}, {profile_2})"
    return None


def weakly_dominant_strategy_equilibrium(pay_off_matrix):
    """
        the weakly dominated strategy is unique value,
        so we determine both player weakly_dominant_strategy
        and if both of them are not None then there exist a
        weakly dominant strategy equilibrium for game
    """

    profile_1 = weakly_dominant_strategy(1, pay_off_matrix)
    profile_2 = weakly_dominant_strategy(2, pay_off_matrix)

    if profile_1 is not None and profile_2 is not None:
        return f"({profile_1}, {profile_2})"
    return None


def max_min_value_strategy(player, pay_off_matrix):
    values = []  # contains all the specific player payoffs (organized based on other player strategy)
    min_values = []  # minimum of each row or column base on player number
    strategies = []

    for i in range(NUMBER_OF_STRATEGIES):
        if player == 1:
            for j in range(NUMBER_OF_STRATEGIES):
                values.append(pay_off_matrix[i][j][0])  # [0] = [player_1_payoff, player_2_payoff] -> [player_1_payoff]
                                                        # [i][j] --> we want to choose a column

            minimum = min(values)  # get the minimum value of row
            strategies.append([i, values.index(minimum)])  # add strategy i within its value<min value of a row/col>
            min_values.append(minimum)                     # get the minimum value for player 1

            values.clear()

        else:
            for j in range(NUMBER_OF_STRATEGIES):
                values.append(pay_off_matrix[j][i][1])  # [1] = [player_1_payoff, player_2_payoff] -> [player_2_payoff]
                                                        # [j][i] --> we want to choose a column
            minimum = min(values)
            strategies.append([values.index(minimum), i])
            min_values.append(minimum)                  # get the minimum value for other player

            values.clear()

        max_min = max(min_values)  # determine the maximum of the minimums
        max_min_strategies = []   # store strategies with the max_min value

        for h in strategies:
            if strategy_pay_off(h[0] + 1, h[1] + 1, pay_off_matrix, indexed_player=1)[0] == max_min:
                max_min_strategies.append(h[0] + 1)
            elif strategy_pay_off(h[0] + 1, h[1] + 1, pay_off_matrix, indexed_player=2)[1] == max_min:
                max_min_strategies.append(h[1] + 1)

    if int(max_min) == max_min:
        max_min = int(max_min)

    return f"{max_min}-{','.join(map(str, max_min_strategies))}"


def min_max_value_strategy(player, pay_off_matrix):
    values = []  # contains all the specific player payoffs (organized based on other player strategy)
    max_values = []  # maximum of each row or column base on player number
    strategies = []

    for i in range(NUMBER_OF_STRATEGIES):
        if player == 1:
            for j in range(NUMBER_OF_STRATEGIES):
                values.append(pay_off_matrix[j][i][0])  # [0] = [player_1_payoff, player_2_payoff] -> [player_1_payoff]
                                                        # [j][i] --> we want to choose a column

            maximum = max(values)  # get the maximum value
            strategies.append([values.index(maximum), i])  # add strategy i within its value<max value of a row/col>
            max_values.append(maximum)                   # get the maximum value for player 1

            values.clear()
        else:
            for j in range(NUMBER_OF_STRATEGIES):
                values.append(pay_off_matrix[i][j][1])  # [1] = [player_1_payoff, player_2_payoff] -> [player_2_payoff]
                                                        # [j][i] --> we want to choose a column
            maximum = max(values)
            strategies.append([i, values.index(maximum)])
            max_values.append(maximum)
            values.clear()

        minmax = min(max_values)  # determine the minimum of the maximums
        minmax_strategies = []  # store strategies with the minmax value

        for h in strategies:
            if strategy_pay_off(h[0] + 1, h[1] + 1, pay_off_matrix, indexed_player=1)[0] == minmax:
                    minmax_strategies.append(h[0] + 1)
            elif strategy_pay_off(h[0] + 1, h[1] + 1, pay_off_matrix, indexed_player=2)[1] == minmax:
                    minmax_strategies.append(h[1] + 1)


    if int(minmax) == minmax:
        minmax = int(minmax)

    return f"{minmax}-{','.join(map(str, minmax_strategies))}"


pure_nash_equilibrium = nash_equilibrium(matrix)
strongly_dominant_strategy_player_1 = strongly_dominant_strategy(1, matrix)
strongly_dominant_strategy_player_2 = strongly_dominant_strategy(2, matrix)

weakly_dominant_strategy_player_1 = weakly_dominant_strategy(1, matrix)
weakly_dominant_strategy_player_2 = weakly_dominant_strategy(2, matrix)

strongly_dominant_strategy_equilibrium = strongly_dominant_strategy_equilibrium(matrix)
weakly_dominant_strategy_equilibrium = weakly_dominant_strategy_equilibrium(matrix)

max_min_values_strategy_player_1 = max_min_value_strategy(1, matrix)
max_min_values_strategy_player_2 = max_min_value_strategy(2, matrix)


min_max_value_strategy_player_1 = min_max_value_strategy(1, matrix)
min_max_value_strategy_player_2 = min_max_value_strategy(2, matrix)

print(f"Pure nash equilibrium\n{pure_nash_equilibrium}")
print(f"Strongly dominant strategy player 1\n{strongly_dominant_strategy_player_1}")
print(f"Strongly dominant strategy player 2\n{strongly_dominant_strategy_player_2}")

print(f"Weakly dominant strategy player 1\n{weakly_dominant_strategy_player_1}")
print(f"Weakly dominant strategy player 2\n{weakly_dominant_strategy_player_2}")

print(f"Strongly dominant strategy equilibrium\n{strongly_dominant_strategy_equilibrium}")
print(f"Weakly dominant strategy equilibrium\n{weakly_dominant_strategy_equilibrium}")

print(f"Maxmin values and strategy player 1\n{max_min_values_strategy_player_1}")
print(f"Maxmin values and strategy player 2\n{max_min_values_strategy_player_2}")


print(f"Minmax values and strategy player 1\n{min_max_value_strategy_player_2}")
print(f"Minmax values and strategy player 2\n{min_max_value_strategy_player_1}")

'''
Test Case:
3
6 8 0
10 4 2
11 20 4
6 20 8
0 5 8
0 0 4
'''
