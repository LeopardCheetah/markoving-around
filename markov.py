import random
# markov chains (but they're lowercase)


# for each string: encode as number
def encode(s):
    # s is a string

    chars = [' '] + [chr(ord('a') + i) for i in range(26)]
    chars += ['.', ',', '?', '!', '/', '-', '_', ':', "'", '"'] + [chr(ord('0') + i) for i in range(10)] + ['(', ')'] # len 48

    n = 0
    for i in range(len(s)):
        try: 
            k = chars.index(s[i])
            n += k*(50**(len(s) - 1 - i))
        except:
            pass
    
    return n

def decode(s, l):
    # here s is an integer

    # 50
    # go from low to high?
    # or high to low?
    # let's do low to high

    chars = [' '] + [chr(ord('a') + i) for i in range(26)]
    chars += ['.', ',', '?', '!', '/', '-', '_', ':', "'", '"'] + [chr(ord('0') + i) for i in range(10)] + ['(', ')'] # len 48

    r = ''

    while s > 0:
        r += chars[s % 50]
        s = s // 50

    if len(r) < l:
        return ' '+r[::-1]

    return r[::-1]


def search(ls, target):
    if len(ls) == 0:
        return [target]
    
    if len(ls) == 1:
        if target <= ls[0]:
            return 0
        
        return 1
    
    c = 0
    for i in range(len(ls)):
        if ls[i] == target:
            return i
        
        if ls[i] < target:
            c += 1
    
    return c

def bsearch(ls, target):
    left = 0
    right = len(ls) - 1

    while left <= right:
        mid = left + (right - left)//2
        if ls[mid] == target:
            return mid
        
        if ls[mid] < target:
            left = mid + 1
            continue
        
        right = mid - 1
    
    return left

    # bsearch if the item does not exist gives the index where it should be placed (then u move everything else)

# add item to sorted list


def upd_lists(seen, frequency, item):
    # update time :P
    # item is unencoded
    e = encode(item)
    ind = bsearch(seen, e)
    
    if len(seen) == 0:
        return [e], [1]


    freq = frequency.copy()
    
    if ind > len(seen) - 1:
        # add to end
        return seen + [e], frequency + [1]


    if seen[ind] == e:
        # it exists
        # update frequency
        freq[ind] += 1
        return seen, freq  

    strs = seen.copy()
    # item does not exist
    
    strs = strs[:ind] + [e] + strs[ind:]
    freq = freq[:ind] + [1] + freq[ind:]

    return strs, freq


def partial_sums(ls):
    lst = [ls[0]]

    for i in range(1, len(ls)):
        lst.append(lst[i - 1] + ls[i])
    
    return lst



def generate_string(strings, frequencies):
    # now we invoke random
    lst = partial_sums(frequencies)
    
    rand = random.randint(1, lst[-1]) # or use sum(frequencies) instead of lst[-1]

    # bsearch!
    ind = bsearch(lst, rand)

    # this should be good
    return strings[ind]
    



# markoving time
def markov(sample_text, length_to_gen, look_ahead):
    # varying look ahead can be a model for increasing/decresaing temperature in this (as well as controlling the randomness)
    # here i wont care -- see previous commits for more details

    # sample_text - sample text to generate from
    # length_to_gen - figure out how much text needs to be generated
    # look_ahead - how many char "bytes" we should look ahead in (int)

    if len(sample_text) < 1:
        return "text cannot be generated from this input"

    if look_ahead > len(sample_text):
        return "look_ahead parameter cannot be smaller than input text length!"
    
    if length_to_gen < 1:
        return "cannot generate such small quantities of text"

    
    sample_text = sample_text.lower()
    
    # break up into chunks and store
    # array of strings and one corresponding to their frequency

    str_array = []
    str_frequency = []

    # now just parse each line of text
    for ind in range(len(sample_text) - look_ahead + 1):
        to_parse = sample_text[ind:ind + look_ahead] # to parse

        str_array, str_frequency = upd_lists(str_array, str_frequency, to_parse)
    
    # above works

    # print(str_array, str_frequency, [decode(str_array[i], look_ahead) for i in range(len(str_array))])

    # text generation time :)
    s = ''

    s += decode(generate_string(str_array, str_frequency), look_ahead)

    if length_to_gen < len(s):
        return s[:length_to_gen]
    

    for index in range(length_to_gen - look_ahead):
        # now just generate characters and add them on!

        # take a look at last few chars
        # encode that then that + 50
        # then yeah
        
        left = encode(s[-look_ahead + 1:] + ' ') # gives me length_to_gen - 1 characters
        right = left + 50 - 1

        low = bsearch(str_array, left)
        high = bsearch(str_array, right)
        generated = decode(generate_string(str_array[low:high], str_frequency[low:high]), look_ahead)

        s += generated[-1] # last char only
    
    return s
    
    
text = input('\nInput some text: ')
length = input('\n\nHow long do you need the text to be? ')
look_ahead = input('\n\nLook ahead? ')

print(markov(text, int(length), int(look_ahead)))
    