def gen_all_sequences(outcomes, length):
    """
    Iterative function that enumerates the set of all sequences of
    outcomes of given length.
    """
    
    answer_set = set([()])
    for dummy_idx in range(length):
        temp_set = set()
        for partial_sequence in answer_set:
            for item in outcomes:
                new_sequence = list(partial_sequence)
                new_sequence.append(item)
                temp_set.add(tuple(new_sequence))
        answer_set = temp_set
    return answer_set

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
        full_hand = hand + held_dice
        all_scores += max(full_hand.count(dummy_i) * dummy_i for dummy_i in range(1, num_die_sides + 1))
    return all_scores / len(my_set)

print(expected_value((3, 3), 8, 5))

#expected_value((2, 2), 6, 2) expected 5.83333333333
#expected_value((3, 3), 8, 5) expected 11.3590087891 but received 9.16546630859
