
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


def init_n_gram_dict():
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
    return bigram_counts, trigram_counts


bigram_counts, trigram_counts = init_n_gram_dict()


def predict_next_char(prev_chars, n_gram_dict):
    return rank_most_likely_char(n_gram_dict[prev_chars])


def rank_most_likely_char(adict):
    letter_counts = []
    for key in adict:

        temp = [str(key), int(adict[key])]
        letter_counts.append(temp)
    ranking = sorted(letter_counts, key=lambda x: x[1],reverse=True)
    return ranking

print(predict_next_char("ab", trigram_counts))























