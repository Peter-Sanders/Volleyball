import math

def get_vars():
    n_teams = input("How many teams? Enter a single number: ")
    n_divisions = input("How many divisions? Enter a single number: ")

    divisions = []
    for x in range(int(n_divisions)):
        div_tier = input(f"What tier is division {x+1}? Enter 'upper', 'mid', or 'lower' without quotes: ")
        div_size = input(f"How large is {div_tier} division {x+1}? Enter a single number: ")
        divisions.append([div_tier, div_size])

    return divisions, n_teams


def make_playoff_bracket(n_teams):
    max_court = 6
    # max_bracket = 4
    min_teams = 6

    if n_teams < min_teams:
        return False

    n_games = n_teams -1
    if n_games < 8:
        max_bracket = 4
        bracket_depth = 3
    elif n_games < 16:
        max_bracket = 8
        bracket_depth = 4
    elif n_games < 32:
        max_bracket = 16
        bracket_depth = 5
    elif n_games < 64:
        max_bracket = 32
        bracket_depth = 6
    else:
        return False
    num_courts = math.ceil(n_teams/max_court)
    num_rounds = n_teams - 3

    res = make_first_round(n_teams, max_bracket)
    for level in range(2, bracket_depth):
        res = make_n_round(res, level)
    res = make_final_round(res, bracket_depth)

    print(res)



def make_final_round(res:dict, bracket_depth:int) -> dict:
    final_div_1 = res[f'Round {bracket_depth-1}']['Division 1']['Matchups']
    final_div_2 = res[f'Round {bracket_depth-1}']['Division 2']['Matchups']
    div_1_winner = ['w_' + '_'.join([str(m) for m in match]) for match in final_div_1]
    div_2_winner = ['w_' + '_'.join([str(m) for m in match]) for match in final_div_2]
    res[f'Final Round']={'Matchups':[div_1_winner[0], div_2_winner[0]]}
    
    return res


def make_n_round(res:dict, level:int) -> dict:
    div_1_matches = res['Round 1']['Division 1']['Matchups']
    div_1_byes = res['Round 1']['Division 1']['Byes']
    div_1_winners = ['w_' + '_'.join([str(m) for m in match]) for match in div_1_matches]
    next_div_1_matchups = []
    for bye in div_1_byes:
        next_div_1_matchups.append([bye, div_1_winners[0]])
        div_1_winners.pop(0)
    if div_1_winners:
        next_div_1_matchups = list_to_matchups_from_center(div_1_winners, next_div_1_matchups)

    div_2_matches = res['Round 1']['Division 2']['Matchups']
    div_2_byes = res['Round 1']['Division 2']['Byes']
    div_2_winners = ['w_' + '_'.join([str(m) for m in match]) for match in div_2_matches]
    next_div_2_matchups = []
    for bye in div_2_byes:
        next_div_2_matchups.append([bye, div_2_winners[0]])
        div_2_winners.pop(0)
    if div_2_winners:
        next_div_2_matchups = list_to_matchups_from_center(div_2_winners, next_div_2_matchups)
    res[f'Round {level}']={'Division 1':{'Matchups':next_div_1_matchups}, 'Division 2':{'Matchups':next_div_2_matchups}}

    return res
    

def make_first_round(n_teams:int, max_bracket:int) -> dict:

    teams = list(range(1, n_teams+1, 1))

    num_byes = n_teams - math.floor(n_teams/max_bracket)*max_bracket

    if n_teams > (max_bracket * 1.4):
        num_byes = int((max_bracket/2)) - abs(int((max_bracket*1.5)-n_teams))

    in_bye = teams[:num_byes]
    not_in_bye = list(set(teams)-set(in_bye))
    matchups = []
    rounds = []
    div = assign_bracket_divisions(n_teams)
    if n_teams < (max_bracket*1.5):
        offset = (n_teams - max_bracket)*2
        low_tiers = not_in_bye[-offset:]
        not_in_bye = not_in_bye[: len(not_in_bye) - offset]
        matchups = list_to_matchups(low_tiers, matchups)
        matchups = list_to_matchups(not_in_bye, matchups)
    else:
        matchups = list_to_matchups(not_in_bye, matchups)
        matchups.reverse()

    res = {'Round 1': {'Division 1':{'Matchups':[], 'Byes':[]}, 'Division 2':{'Matchups':[], 'Byes':[]}}}
    for match in matchups:
        if match[0] in div[0]:
            res['Round 1']['Division 1']['Matchups'].append(match)
        else:
            res['Round 1']['Division 2']['Matchups'].append(match)

    for bye in in_bye:
        if bye in div[0]:
            res['Round 1']['Division 1']['Byes'].append(bye)
        else:
            res['Round 1']['Division 2']['Byes'].append(bye)
    # print(f"{n_teams} Teams first bracket depth matchups: {res}")

    return res


def assign_bracket_divisions(n_teams:int) -> list:
    div_1 = []
    div_2 = []
    cntr = 0
    target = 1

    for i in range(n_teams):
        team = i+1
        if i == 0:
            div_1.append(team)
            target = 2 
            continue
        if cntr < 2:
            div_1, div_2 = assign_target_dev(team, target, div_1, div_2) 
            cntr += 1
        else:
            cntr = 1
            if target == 1:
                target = 2 
            else:
                target = 1
            div_1, div_2 = assign_target_dev(team, target, div_1, div_2)
    return [div_1, div_2]


def assign_target_dev(team:int, target:int, div_1:list, div_2:list) -> tuple:
    if target == 1:
        div_1.append(team)
    else:
        div_2.append(team)
    return div_1, div_2


def list_to_matchups(lst:list, matchups:list) -> list:
    for i in range(int(len(lst)/2)):
        matchups.append([lst[i], lst[len(lst)-i-1]])
    return matchups


def list_to_matchups_from_center(lst:list, matchups:list) -> list:
    for i in range(int(len(lst)/2)):
        matchups.append([lst[int(len(lst)/2)-i],lst[int(len(lst)/2)-i-1]])
    return matchups


if __name__ == "__main__":
    for i in range(5,18):
        make_playoff_bracket(i)

