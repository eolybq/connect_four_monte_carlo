from typing import List, Dict
from random import randint


def is_won(state):
    """
    Funkce zkontroluje vsechny radky, sloupce a diagonaly pro urceni vyhry
    """
    # Radky 
    for i in range(len(state)):
        # Sloupce
        for j in range(0, len(state[i])):
            # Kontrola vsech moznych 4ric v kazdem radku
            if j <= len(state[0]) - 4:
                test_row_l = state[i][j:(j + 4)]

                if len(set(test_row_l)) == 1 and test_row_l[0] != " ":
                    return True

    
            # Kontrola vsech moznych 4ric v kazdem sloupci
            if i <= len(state) - 4:
                test_col_l = [state[i + k][j] for k in range(4)]

                if len(set(test_col_l)) == 1 and test_col_l[0] != " ":
                    return True


            # Kontrola vsech moznych 4ric v kazde diagonale do prava
            if i <= len(state) - 4 and j <= len(state[0]) - 4:
                test_diag_right_l = [state[i + k][j + k] for k in range(4)]

                if len(set(test_diag_right_l)) == 1 and test_diag_right_l[0] != " ":
                    return True


            # Kontrola vsech moznych 4ric v kazde diagonale do leva
            if i >= 3 and j <= len(state[0]) - 4:
                test_diag_left_l = [state[i - k][j + k] for k in range(4)]

                if len(set(test_diag_left_l)) == 1 and test_diag_left_l[0] != " ":
                    return True

    return False



def is_tie(state):
    """
    Kontroluje remizu - zda neni je hraci plan plny
    """
    return all(cell != " " for row in state for cell in row)

    


def valid_move(move, state):
    """
    Kontroluje platnost tahu -> meze hraciho planu + mezera v prvni row daneho col "move"
    """
    return move < len(state[0]) and move >= 0 and state[0][move] == " "



def make_move(move, state, symbol):
    """
    Provede tah ve stavu "state" ve sloupci "move" symbolem hrace "symbol"
    """
    move_col = [row[move] for row in state]

    for i in range(len(move_col) - 1, -1, -1):
        if move_col[i] == " ":
            state[i][move] = symbol
            return state
    



def human_move(state):
    """
    Tah hrace - vola input dokud tah neni platny
    """
    move = int(input(f"Do jakeho sloupce chces hrat? (od 0 do {len(state[0]) - 1})?"))

    while not valid_move(move, state):
        move = int(input(f"Do jakeho sloupce chces hrat? (od 0 do {len(state[0]) - 1})?"))

    return move





def random_strategy(state: List[List[str]]) -> int:
    """
    Vrati nahodny platny tah pro dany stav hry
    """
    move = randint(0, len(state[0]) - 1)

    while not valid_move(move, state):
        move = randint(0, len(state[0]) - 1)

    return move
    


def one_sim(state, move, symbols):
    """
    Provede jednu simulaci hry od daneho stavu, kde PC zahraje kandidatni tah "move",
    kde se hraci i pocitac stridaji s nahodnymi tahy
    Vraci 1 pokud vyhraje pocitac, -1 pokud vyhraje hrac, 0 pokud je remiza
    """
    sim_state = [row.copy() for row in state]
    sim_state = make_move(move, sim_state, symbols["pc"])

    # kontrola okamzite vyhry stroje
    if is_won(sim_state):
        return 1

    current_player = "human"

    while not is_tie(sim_state):
        if current_player == "human":
            h_move = random_strategy(sim_state)
            sim_state = make_move(h_move, sim_state, symbols["human"])

            if is_won(sim_state):
                # vyhra cloveka
                return -1 

        else:
            pc_move = random_strategy(sim_state)
            sim_state = make_move(pc_move, sim_state, symbols["pc"])

            if is_won(sim_state):
                # vyhra stroje
                return 1

        current_player = [k for k in symbols.keys() if k != current_player][0]

    # remiza
    return 0 





def monte_carlo_sim(state, move, symbols, sim_count=300):
    """
    Pro kandidatni tah "move" spusti jednu iteraci monte carlo simulace "sim_count" krat
    spocita ocekavany vysledek pro tento kandidatni tah
    """
    wins = []

    for _ in range(sim_count):
        result = one_sim(state, move, symbols)
        wins.append(result)

    return sum(wins) / len(wins)

    


# Funkce vypise dany plan na standardni vystup. Plan je reprezentovan seznamem
#  seznamu stejne delky, ktere obsahuji znaky X (krizek), O (kolecko) nebo
#  mezera pro neobsazene pole.

# :param state:  Seznam seznamu obsahujici znaky X, 0, a mezera
def show_state(state: List[List[str]]) -> None:
    separator_list = ["-" for _col in state[0]]
    col_list = [i for i in range(len(state[0]))]

    for row in state:
        print(*row)

    print(*separator_list)
    print(*col_list)





# Funkce pro dany plan state a symbol chr vrati pozici (sloupec) tahu
# pocitace.
# Pozn. Funkce neresi zadnou logiku hry ani vypisy, jen vraci sloupec, kam
# umistuje pocitac svuj symbol.

#    :param state:  Seznam seznamu obsahujici znaky X, 0, a mezera
#    :param chr:    Znak, ktery se ma vlozit
#    :return:       Sloupec, do ktereho se ma vlozit znak chr
def strategy(state: List[List[str]], symbols: Dict[str, str]) -> int:
    """
    funkce pomoci valid_move najde vsechny platne tahy
    pro kazdy z nich spusti monte_carlo_sim a vypocita pravdepodobnost vyhry
    vrati tah s nejvyssim ocekavanym vysledkem
    """
    candidate_moves = [move for move in range(0, len(state[0])) if valid_move(move, state)] 
    exp_results = []

    for move in candidate_moves:
        exp_result = monte_carlo_sim(state, move, symbols)
        exp_results.append(exp_result)

    best_exp_result_move =  max(range(len(exp_results)), key=lambda i: exp_results[i])

    return candidate_moves[best_exp_result_move]



# Funkce umoznuje hrat hru padajicich piskvorek na planu o danem poctu radku
# a sloupcu.

#   :param rows:    Pocet radku (4..25)
#   :param cols:    Pocet sloupcu (4..25)
#   :param human_starts: True, pokud zacina hrac, False jinak


def tictactoe(rows: int, cols: int, human_starts: bool = True) -> None:
    # vytvoreni prazdneho pole
    state = [[" " for _col in range(cols)] for _row in range(rows)]
    symbols = {}

    if human_starts:
        symbols["human"] = "X"
        symbols["pc"] = "O"
    else:
        symbols["human"] = "O"
        symbols["pc"] = "X"


    current_player = [k for k, v in symbols.items() if v == "X"][0]

    while not is_tie(state):
        if current_player == "human":
            print("Na tahu je hrac")
            h_move = human_move(state)
            state = make_move(h_move, state, symbols["human"])

            show_state(state)
            if is_won(state):
                print("Vyhral jsi!")
                return

        else:
            print("Na tahu je pocitac")
            pc_move = strategy(state, symbols)
            state = make_move(pc_move, state, symbols["pc"])
            print(f"Pocitac hraje do sloupce cislo {pc_move}")

            show_state(state)
            if is_won(state):
                print("Vyhral pocitac!")
                return

        current_player = [k for k in symbols.keys() if k != current_player][0]

    print("Remiza")



tictactoe(20, 20, human_starts=False)