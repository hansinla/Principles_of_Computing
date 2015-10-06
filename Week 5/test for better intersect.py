FILENAME = 'dictionary.txt'

def intersect(list1, list2):
    """
    Compute the intersection of two sorted lists.

    Returns a new sorted list containing only elements that are in
    both list1 and list2.

    This function can be iterative.
    """
    return_list = []
    
    for item in list1:
        if item in list2:
            new_index = list2.index(item)
            list2 = list2[new_index:]
            return_list.append(item)
     
    return return_list

def load_words(filename):
    """
    Load word list from the file named filename.

    Returns a list of strings.
    """
    wordlist = []

    file_ptr = open(FILENAME, 'r')
    
    for line in file_ptr.readlines():
        wordlist.append(line[:-1])

    return wordlist

list2 = load_words(FILENAME)

list1 = ["AIRCRAFT", "CHILD", "COUNTRY", "SALE", "SING", "sprookjeshuis", "ZULU" ]

print(intersect(list1, list2))
