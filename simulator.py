#!/usr/bin/env python3

"""
Name: Jumbo Cactpot Simulator
Date: 2021-09-26 Sunday 

Simulates Jumbo Cactpot "Work Smarter, Not Harder Achievement"
a bunch of times to guess how long it would take on average to grind with 
the current environment as of 2021-09-26

"""
import random
from functools import cache
from math import floor
from collections import defaultdict
import pickle

# Estimated Rewards is a list with indices indicating how many numbers matched.
estimated_rewards = [50, 1_000, 10_000, 100_000, 1_000_000]
better_estimated_rewards = [300, 2_000, 12_000, 130_000, 1_000_000]

@cache
def ticket_to_string(ticket):
    t_string = str(ticket).zfill(4)
    return(t_string)


def score_tickets(winning_number, ticket_list, early_bird_bonus = False):
    total_score = 0
    winning_string_r = reversed(ticket_to_string(winning_number))
    for ticket in ticket_list:
        t_string_r = reversed(ticket_to_string(ticket))
        index = 0
        for cw, ct in zip(winning_string_r, t_string_r):
            if cw == ct:
                index += 1
            else:
                break
        total_score += better_estimated_rewards[index]
    if early_bird_bonus:
        total_score = floor(total_score * 1.05)
    return(total_score)
        
def simulation(iterations = 100_000):
    ticket_pool = [num for num in range(10_000)]
    w_list = []
    for i in range(iterations):
        weeks = 0
        cumulative_score = 0
        while cumulative_score < 1_000_000:
            # Generate three random tickets
            tickets = []
            for j in range(3):
                tickets.append(random.choice(ticket_pool))
            # Generate winning number
            winning_number = random.choice(ticket_pool)
            # Score tickets
            cumulative_score += score_tickets(winning_number, tickets, early_bird_bonus=True)
            weeks += 1
        w_list.append(weeks)
    w_list = sorted(w_list)
    with open('week_list_with_bonus', 'wb') as w_file:
        pickle.dump(w_list, w_file)
    #w_list = []
    #for i in range(iterations):
    #    weeks = 0
    #    cumulative_score = 0
    #    while cumulative_score < 1_000_000:
    #        # Generate three random tickets
    #        tickets = []
    #        for j in range(3):
    #            tickets.append(random.choice(ticket_pool))
    #        # Generate winning number
    #        winning_number = random.choice(ticket_pool)
    #        # Score tickets
    #        cumulative_score += score_tickets(winning_number, tickets)
    #        weeks += 1
    #    w_list.append(weeks)
    #w_list = sorted(w_list)
    #with open('week_list', 'wb') as w_file:
    #    pickle.dump(w_list, w_file)

def survivor_data(w_list):
    s_list = []
    still_in = len(w_list)
    s_list.append(still_in)
    back_index = 0
    mem_value = 1
    while back_index < len(w_list):
        for value in w_list[back_index:]:
            back_index += 1
            if value != mem_value:
                for i in range(value - mem_value - 1):
                    s_list.append(still_in)
                mem_value = value
                s_list.append(still_in)
            still_in -= 1
    s_list.append(0)
    return(s_list)


def main():
    #simulation()
    with open('week_list', 'rb') as w_file:
        w_list = pickle.load(w_file)
    #print(survivor_data(w_list))


    print("For the data set without early bird bonus:")
    ave = sum(w_list) / len(w_list)
    print(f'The average weeks lengh in this data set is {round(ave,2)}, which is about {round(ave/52, 1)} years.')
    print(f'The max time to get the achievement in this data set is {max(w_list)} which is {round(max(w_list)/52,1)} years.')


    print()
    with open('week_list_with_bonus', 'rb') as w_file:
        w_list = pickle.load(w_file)
    #print(survivor_data(w_list))
    print("For the data set with early bird bonus:")
    ave = sum(w_list) / len(w_list)
    print(f'The average weeks lengh in this data set is {round(ave,2)}, which is about {round(ave/52, 1)} years.')
    print(f'The max time to get the achievement in this data set is {max(w_list)} which is {round(max(w_list)/52,1)} years.')


if __name__ == "__main__":
    main()
