
ASCII_OFFSET = 97


'''
def add_to_char_list(char_list, char, num_appearances):
    char_list[ord(char) - ASCII_OFFSET] += num_appearances
    return char_list
'''

'''
def init_bigram_dict():
    bigrams = {}
    for i in range(0, 26):
        bigrams[chr(i + ASCII_OFFSET)] = init_next_char_list()
    return bigrams


def init_trigram_dict():
    trigrams = {}
    for i in range(0, 26):
        for j in range(0, 26):
            key = chr(i + ASCII_OFFSET) + chr(j + ASCII_OFFSET)
            trigrams[key] = init_next_char_list()
    return trigrams


print(init_bigram_dict())
print("")
print(init_trigram_dict())
'''

data_pairs = []

with open("training set.txt", "r") as file:
    for line in file:
        data = line.strip().split('\t')
        data_pairs.append([data[0].strip(), int(data[1])])

print(data_pairs)

bigram_counts = {}
trigram_counts = {}

for data in data_pairs:
    for i in range(0, len(data[0]) - 1):
        char = data[0][i]
        next_char = data[0][i + 1]
        if char not in bigram_counts:
            bigram_counts[char] = {}
            bigram_counts[char][next_char] = data[1]
        elif next_char not in bigram_counts[char]:
            bigram_counts[char][next_char] = data[1]
        else:
            bigram_counts[char][next_char] += data[1]

    for i in range(1, len(data[0]) - 2):    #This range might be incorrect
        bigram_key = data[0][i - 1: i + 1]
        next_char = data[0][i + 1]
        if bigram_key not in trigram_counts:
            trigram_counts[bigram_key] = {}
            trigram_counts[bigram_key][next_char] = data[1]
        elif next_char not in trigram_counts[bigram_key]:
            trigram_counts[bigram_key][next_char] = data[1]
        else:
            trigram_counts[bigram_key][next_char] += data[1]

print(trigram_counts)
print(bigram_counts)




















