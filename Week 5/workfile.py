# Function to generate all strings for the word wrangler game

def gen_all_strings(word):
    """
    Generate all strings that can be composed from the letters in word
    in any order.

    Returns a list of all strings that can be formed from the letters
    in word.

    This function should be recursive.
    """
    
    if len(word) < 1:
         return ['']
    word_list = gen_all_strings(word[1:])
    # permutations
    for perm in gen_all_strings(word[1:]):
        for idx in range(len(perm)+1):
            word_list.append( perm[:idx] + word[0:1] + perm[idx:])
    return word_list

result = gen_all_strings("ab")

print(result)


