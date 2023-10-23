import random
# i have no clue how temperature works




values = {} # this is the lookup table for what char is what value

for c in range(26):
    values[chr(ord('a') + c)] = c + 1

for c in range(10):
    values[chr(ord('0') + c)] = 27 + c

values[','] = 37
values['.'] = 38
values[' '] = 39
values['!'] = 40
values[':'] = 41
values[';'] = 42
values['"'] = 43
values["'"] = 44
values["?"] = 45
values["-"] = 46

# mirror dictionary
values_mirrored = {}

for key in values:
    values_mirrored[values[key]] = key

lookup_table = values | values_mirrored # omg pipe operator





def encode(str):
    s = str[::-1]
    c = 0

    k = 0
    for i in s:
        k += (50**c) + lookup_table[i]
        c += 1

    return k

def decode(int):
    iint = int
    s = ''

    max_power = 0
    while 50**max_power < int:
        max_power += 1
        
    max_power -= 1



    for i in range(max_power, -1, -1):
        # backwards loop
        c = iint // 50**max_power
        s += lookup_table[c]
        iint %= 50**max_power
    
    return s

def binary_search(list, item):
    # find where item is or where it would be
    # goal: use log n time

    # list - list of numbers
    # item - number

    low = 0
    high = len(list)
    
    while low != high:
        mid = (low + high)/2

        if list[mid] > item:
            # go lower
            high = mid - 1
            continue
            
        if list[mid] < item:
            # go up
            low = high + 1
            continue
    
        if list[mid] == item:
            return True, mid
    
    return False, low





class Markov_Chain_Text:

    max_look_ahead = 6 # how many chars should this model base its predictions off of?
    frequencies = [] # tally up all the letter combinations, should be a sorted list! 
    # a list of numbers in base 50
    frequencies_occurences = []

    next_char = [] # put down a probability for the next char
    temperature = 0 # 0 = absolute, 1 = random (sort of)
    chars = set(['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', ',', '.', ' ', '!', ':', ';', '"', "'", '?', '-'])

    def __init__(self):
        self.frequencies = [{} for _ in range(self.max_look_ahead + 1)]
        self.frequencies_occurences = [{} for _ in range(self.max_look_ahead + 1)]
        self.next_char = [[] for _ in range(self.max_look_ahead + 1)]


    def add_input(self, text):

        new_text = text.lower()
        new_new_text = ''
        for i in new_text:
            if i in self.chars:
                new_new_text += 'i'

        # when getting a new text, add everything to self.frequencies and stuff
        # frequencies - put more lists in lists :/
        # maybe a dict or something
        pass


    def generate_text(self, length):
        pass

    def generate_char(self, string, temperature):
        pass