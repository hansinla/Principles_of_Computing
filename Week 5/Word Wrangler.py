"""
Student code for Word Wrangler game
"""
import time
FILENAME = "assets_scrabble_words3.txt"

# Functions to manipulate ordered word lists

def remove_duplicates(list1):
    """
    Eliminate duplicates in a sorted list.

    Returns a new sorted list with the same elements in list1, but
    with no duplicates.

    This function can be iterative.
    """
    return_list = []
    for item in list1:
        if item not in return_list:
            return_list.append(item)
    
    return return_list

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
            index = list2.index(item)
            list2 = list2[index:]
            return_list.append(item)
    
    return return_list

# Functions to perform merge sort

def merge(list1, list2):
    """
    Merge two sorted lists.

    Returns a new sorted list containing all of the elements that
    are in both list1 and list2.

    This function can be iterative.
    """   
    new_list = []
    index_1 = 0
    index_2 = 0

    # For each pair of items list1[i1] and list2[i2], copy the smaller into newL.
    while index_1 != len(list1) and index_2 != len(list2):
        if list1[index_1] <= list2[index_2]:
            new_list.append(list1[index_1])
            index_1 += 1
        else:
            new_list.append(list2[index_2])
            index_2 += 1

    # Gather any leftover items from the two sections.
    # Note that one of them will be empty because of the loop condition.
    new_list.extend(list1[index_1:])
    new_list.extend(list2[index_2:])

    return new_list


def merge_sort(list1):
    """
    Sort the elements of list1.

    Return a new sorted list with the same elements as list1.

    This function should be recursive.
    """
    return_list = []

    if len(list1) > 2:
        mid = int(len(list1)/2)
        new_list_1 = list1[:mid]
        new_list_2 = list1[mid:]
        return_list = merge(merge_sort(new_list_1 ), merge_sort(new_list_2))
    else:
        if len(list1) == 2:
            if list1[0] > list1[1]:
                return [list1[1],list1[0]]
            else:
                return list1
        else:
            return list1

    return return_list

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
    for perm in gen_all_strings(word[1:]):
        for idx in range(len(perm)+1):
            word_list.append( perm[:idx] + word[0:1] + perm[idx:])
    return word_list

# Function to load words from a file

def load_words(filename):
    """
    Load word list from the file named filename.

    Returns a list of strings.
    """
    wordlist = []
    
    #url = codeskulptor.file2url(filename)
    #netfile = urllib2.urlopen(url)
    netfile = open(filename, 'r')
    for line in netfile.readlines():
        wordlist.append(line[:-1])

    return wordlist

word = "python"
time1 = time.clock()
dictionary = load_words(FILENAME)
list1 = gen_all_strings(word)
#print(list1)
list2 = merge_sort(list1)
#print(list2)
list3 = intersect(dictionary, list2)
#print(list3)
time2 = time.clock()
print("Done, time used: ", time2-time1)
print("Word: ", word)
print()
print("Possible permutations: ("+str( len(list3))+")")
for item in list3:
    print(item)    

