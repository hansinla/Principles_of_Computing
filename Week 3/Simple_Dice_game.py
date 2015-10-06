"""
Analyzing a simple dice game
"""

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

# example for digits


def max_repeats(seq):
    """
    Compute the maxium number of times that an outcome is repeated
    in a sequence
    """
    return max(seq.count(dummy_i) for dummy_i in range(1, 7))


def compute_expected_value(outcomes, length):
    """
    Function to compute expected value of simpe dice game
    """
    winnings = 0.0
    my_set = gen_all_sequences(outcomes, length)
    for roll in my_set:
        result = max_repeats(roll)
        if result == 3:
            winnings += 200
        elif result == 2:
            winnings += 10
    return winnings/len(my_set)


def run_test():
    """
    Testing code, note that the initial cost of playing the game
    has been subtracted
    """
    outcomes = set([1, 2, 3, 4, 5, 6])
##    print ("All possible sequences of three dice are")
##    print (gen_all_sequences(outcomes, 3))
##    print ()
##    print ("Test for max repeats")
##    print ("Max repeat for (3, 1, 2) is", max_repeats((3, 1, 2)))
##    print ("Max repeat for (3, 3, 2) is", max_repeats((3, 3, 2)))
##    print ("Max repeat for (3, 3, 3) is", max_repeats((3, 3, 3)))
##    print ()
    print ("Ignoring the initial $10, the expected value was $", compute_expected_value(outcomes, 3))
    
run_test()
