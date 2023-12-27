import random
# markov chains (but they're lowercase)


# for each string: encode as number
def encode(s):
    # s is a string

    chars = [' '] + [chr(ord('a') + i) for i in range(26)]
    chars += ['.', ',', ';', '?', '!', '/', '-', '_', ':', "'", '"'] + [chr(ord('0') + i) for i in range(10)] # len 48

    n = 0
    for i in range(len(s)):
        try: 
            k = chars.index(s[i])
            n += k*(50**(len(s) - 1 - i))
        except:
            pass
    
    return n

def decode(s):
    # here s is an integer

    # 50
    # go from low to high?
    # or high to low?
    # let's do low to high

    chars = [' '] + [chr(ord('a') + i) for i in range(26)]
    chars += ['.', ',', ';', '?', '!', '/', '-', '_', ':', "'", '"'] + [chr(ord('0') + i) for i in range(10)] # len 48

    r = ''

    while s > 0:
        r += chars[s % 50]
        s = s // 50
    
    return r[::-1]





def bsearch(ls, target):
    left = 0
    right = len(ls) - 1

    while left + 1 < right:
        mid = (left + right)//2
        if ls[mid] == target:
            return mid
        
        if ls[mid] < target:
            left = mid 
            continue
        
        right = mid
    
    return left + 1

def add_to_list(strings_seen, frequencies, item):
    # item is an encoded piece of text
    e = encode(item)

    if len(strings_seen) == 0:
        return [e], [1]

   
    ind = bsearch(strings_seen, e) - 1
    freq = frequencies.copy()

    if strings_seen[ind] == e:
        freq[ind] += 1
        return strings_seen, freq
    
    # add new item
    ss = strings_seen.copy()
    ss = ss[:ind] + [e] + ss[ind:]

    freq = freq[:ind] + [1] + freq[ind:] 
    
    # arguably here you could store all numbers up to 50^(sample_size) in an array 
    # which is a funny approach but not really feasible since that needs hella memory

    return ss, freq





def partial_sum(ls):
    if len(ls) == 0:
        return []

    lst = [ls[0]]


    for i in range(1, len(ls)):

        lst.append(lst[i - 1] + ls[i])
    
    return lst


def random_s(ls, weights):
    # len(ls) == len(weights)

    s = sum(weights)

    rand = random.randint(1, s)
    # now bsearch on a list :P

    partial_sums = partial_sum(weights)
    ind = bsearch(partial_sums, rand)

    
    if partial_sums[ind - 1] <= rand:
        return decode(ls[ind - 1])
    
    return decode(ls[ind - 2])






# time to do the markoving

def markov(string, length, preview_size):
    # generate markov string of 'length' based on sample text 'string' with a preview_size or look ahead of 'preview_size'


    # 1. generate the possibilities or whatever

    weights = [] # weights
    str_list = [] # has the strings (but they're encoded)

    
    if preview_size < 1:
        print('preview_size is non-existent')
        return -1

    if len(string) < preview_size:
        print('string is shorter than preview size :(')
        return -1

    # if length < preview_size, then roll the dice and trim is the best option (tho this may not be the most accurate way of doing it)
    # oooh this could be a way to sense temperature?

    # idea: since a markov text of sample size 5 can be modeled by one with length 6 but removing the last character, 
    # we could use that variable as one of "temperature"

    # highest temperature (1) == sample size = string
    # lowest temperature (randomness) -> sample_size = 1
    # this is an interesting concept to be expanded upon (later)


    for ind in range(len(string) - preview_size + 1):
        to_add = string[ind:ind + preview_size]
        str_list, weights = add_to_list(str_list, weights, to_add)
    
    # now time to generate text!
    
    # generate starting string
    s = ''
    r = random_s(str_list, weights)
    s += r
    
    if len(s) >= length:
        return s[:length]
    
    # now do char by char
    for counter in range(length - len(s)):
        # generate string
        # chop off end
        # profit

        # first encode the last n - 1
        # then take a look at that section in the list
        # then get string from that 

        lower_bound = encode(s[-preview_size+1:] + ' ') # use python's negative string syntax mwahahahahahha
        upper_bound = lower_bound + 49 # lower, lower + 1, ... lower + 49
        
        # now find all strings that fit this property
        low = bsearch(str_list, lower_bound)
        high = bsearch(str_list, upper_bound)

        random_string = random_s(str_list[low:high + 1], weights[low: high + 1])
        s += random_string[-1]

        # yay we win
    
    return s

print(markov('abcdefghi', 3, 2))


  