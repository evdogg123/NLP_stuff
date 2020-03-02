import nltk
ASCII_OFFSET = 97


def init_next_char_list():
    return [0]*26


def add_to_char_list(char_list, char, num_appearances):
    char_list[ord(char) - ASCII_OFFSET] += num_appearances
    return char_list


data_pairs = []

with open("training set.txt", "r") as file:
    for line in file:
        data = line.strip().split('\t')
        data_pairs.append([data[0], int(data[1])])

print(data_pairs)

bigram_counts = {}
trigram_counts = {}

for data in data_pairs:
    for char in data[0]:
        if char not in bigram_counts:
            bigram_counts[char] = init_next_char_list()
            bigram_counts[char] = data[1]














