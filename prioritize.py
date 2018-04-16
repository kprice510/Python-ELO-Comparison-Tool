#-------------------------------------------------------------------------------
# Name:        ELO-Based Prioritization Tool
# Purpose:
#
# Author:      Keith Price
#
# Created:     15/04/2018
# Copyright:   (c) Keith 2018
# Licence:     GNU General Public License v3.0
#-------------------------------------------------------------------------------

import random,os

def get_players(file_name):
    player_file = open(file_name, 'r')
    print('Name of the file: ', player_file.name)

    p = player_file.readlines()
    player_file.close

    p_list = [elem.strip().split(',') for elem in p]
    p_list2 = []

    for sublist in p_list:
        for element in sublist:
            p_list2.append(element)

    player_tuple = tuple(p_list2)

    player_dict = {}
    for player in player_tuple:
        player_dict[player] = 1600

    return player_dict



def main():
    os.system('cls')
    print('Welcome to the ELO simple ranking tool!')
    print('')
    while True:
        file_name = input('Please input the name of your file: ')
        try:
            player_dict = get_players(file_name)
        except FileNotFoundError:
            os.system('cls')
            print('')
            print("Oops! The file '" + file_name + "' was not found.  Please try again...")
            print('')
        else:
            break
    player_dict = get_players(file_name)
    rounds = ((len(player_dict)*(len(player_dict)-1))/2-3)
    count = 0
    matches = []
    print(player_dict)

    while count <= rounds:
        player1,player2,matches = sample(player_dict,matches)
        os.system('cls')
        print('Please make a selection.  You may choose between a(left) s(tie) or d(right)')
        print('')
        print(player1+' (a)'+'                          About the same (s)                          '+player2+' (d)')
        print('')
        print('')
        selection = ''

        while selection != "a" and selection != "d" and selection != "s":
            selection = input("Please enter the corresponding value (a, s, or d) :  ")
            if selection != "a" and selection != "d" and selection != "s":
                print('You must select a, s, or d')


        if selection == "a":
            p1_score,p2_score = 1,0
        elif selection == "d":
            p1_score,p2_score = 0,1
        elif selection == "s":
            p1_score,p2_score = 0.5,0.5

        p1_rating = player_dict[player1]
        p2_rating = player_dict[player2]

        p1_prob = winprob(p1_rating,p2_rating)
        p2_prob = winprob(p2_rating,p1_rating)

        p1_new = round(newrating(p1_rating,p1_prob,p1_score),2)
        p2_new = round(newrating(p2_rating,p2_prob,p2_score),2)

        player_dict[player1] = p1_new
        player_dict[player2] = p2_new

        count += 1

    sorted_list = [(k, player_dict[k]) for k in sorted(player_dict, key=player_dict.get, reverse = True)]
    for k, v in sorted_list:
        print(k, v)




def sample(player_dict,matches):
    rand1 = (random.choice(list(player_dict.keys())))
    player_dict2 = dict(player_dict)
    del player_dict2[rand1]
    rand2 = (random.choice(list(player_dict2.keys())))

    match = min(rand1,rand2) + max(rand1,rand2)
    #print(match)

    counter = 0

    while counter <= 0:

        if match not in matches:
            matches.append(match)
            counter = 1
        else:
            rand1 = (random.choice(list(player_dict.keys())))
            player_dict2 = dict(player_dict)
            del player_dict2[rand1]
            rand2 = (random.choice(list(player_dict2.keys())))
            match = min(rand1,rand2) + max(rand1,rand2)

    return rand1,rand2,matches


def winprob(player_rating, opponent_rating):
    exp = ((opponent_rating - player_rating)/400) + 1
    winprob = 1 / 10**exp
    return winprob

def newrating(player_rating, winprob, score):
    rating = player_rating + (10 *(score - winprob))
    return rating


main()


