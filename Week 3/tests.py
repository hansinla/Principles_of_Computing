def gen_all_sequences(outcomes, length):
    """
    Iterative function that enumerates the set of all sequences of
    outcomes of given length
    """
    ans = set([()])
    for dummy_idx in range(length):
        temp = set()
        for seq in ans:
            for item in outcomes:
                new_seq = list(seq)
                new_seq.append(item)
                temp.add(tuple(new_seq))
        ans = temp
    return ans

def score(hand):
    """
    Compute the maximal score for a Yahtzee hand according to the
    upper section of the Yahtzee score card.

    hand: full yahtzee hand

    Returns an integer score 
    """
    return max(hand.count(dummy_i) * dummy_i for dummy_i in range(1, 7))

def expected_value(held_dice, num_die_sides, num_free_dice):
    """
    Compute the expected value of the held_dice given that there
    are num_free_dice to be rolled, each with num_die_sides.

    held_dice: dice that you will hold
    num_die_sides: number of sides on each die
    num_free_dice: number of dice to be rolled

    Returns a floating point expected value
    """
    outcomes = set(range(1, num_die_sides + 1))
    my_set = gen_all_sequences(outcomes, num_free_dice)
    all_scores = 0.0
    for hand in my_set:
        all_scores += score(hand)                   
    return score(held_dice) + all_scores / len(my_set)

def gen_all_holds(hand):
    """
    Generate all possible choices of dice from hand to hold.

    hand: full yahtzee hand

    Returns a set of tuples, where each tuple is dice to hold
    """
    target = []
    result_list = [tuple()]
    
    combinations(target, hand, result_list)

    return set([tuple(dummy_i) for dummy_i in result_list])

def combinations(target, hand, result_list):
    for i in range(len(hand)):
        new_target = target[:]
        new_hand = hand[:]
        new_target.append(hand[i])
        new_hand = hand[i+1:]
        result_list.append(new_target)
        combinations(new_target, new_hand, result_list)


held_dice = (1, 2, 3, 4, 5, 6)
num_free_dice = 5 - len(held_dice)
num_die_sides = 6

all = gen_all_holds(held_dice)
for hold in all:
    print(hold)

print()
print(len(all))
