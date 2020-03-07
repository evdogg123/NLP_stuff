
training_data = []

with open("training set.txt", "r") as file:
    for line in file:
        data = line.split('\t')
        training_data.append([" " +data[0].strip() + " ", int(data[1])])


def init_n_gram_dict(data_pairs):
    '''
    Initializes:
    char_count, a total count of all the characters
    monogram_counts, dictionary where monogram_counts[a] is the number of appearances of char 'a'
    bigram_counts, dictionary where bigram_counts[a][b] is the number of appearances of substring 'ab'
    trigram_counts, dictionary where trigram_counts['ab'][c] is the number of appearances of substring 'abc'
    '''

    char_count = 0
    monogram_counts = {}
    bigram_counts = {}
    trigram_counts = {}

    for data in data_pairs:
        for i in range(0, len(data[0]) - 1):
            char = data[0][i]
            next_char = data[0][i + 1]
            if char not in bigram_counts:
                bigram_counts[char] = {}
                bigram_counts[char][next_char] = [data[1]]
            elif next_char not in bigram_counts[char]:
                bigram_counts[char][next_char] = [data[1]]
            else:
                bigram_counts[char][next_char][0] += data[1]

        for i in range(1, len(data[0]) - 2):
            bigram_key = data[0][i - 1: i + 1]
            next_char = data[0][i + 1]
            if bigram_key not in trigram_counts:
                trigram_counts[bigram_key] = {}
                trigram_counts[bigram_key][next_char] = [data[1]]
            elif next_char not in trigram_counts[bigram_key]:
                trigram_counts[bigram_key][next_char] = [data[1]]
            else:
                trigram_counts[bigram_key][next_char][0] += data[1]

        for i in range(0,len(data[0])):
            mono_gram_key = data[0][i]
            char_count += data[1]
            if mono_gram_key not in monogram_counts:
                monogram_counts[mono_gram_key] = [data[1]]
            else:
                monogram_counts[mono_gram_key][0] += data[1]
    return char_count, monogram_counts, bigram_counts, trigram_counts





def compute_prob_dict(monogram_cts, bigram_cts, trigram_cts, char_ct):
    '''
    Updates the count dictionaries with the probability of the given event occuring
    p_char_given_bigram['ab']['c'][1] is the probability of seeing c given 'ab' was before
    p_char_given_monogram['a']['b][1] is the probablility of seeing b given a was before
    p_char['a'] is the probability of seeing 'a'
    '''

    p_char_given_bigram = trigram_cts
    p_char_given_monogram = bigram_cts
    p_char = monogram_cts
    char_count = char_ct

    for char in p_char:
        p_char[char].append(p_char[char][0] / char_count)

    for monogram_key in p_char_given_monogram:
        for char in p_char_given_monogram[monogram_key]:
            p_char_given_monogram[monogram_key][char].append(p_char_given_monogram[monogram_key][char][0] /  monogram_counts[monogram_key][0] )
    for bigram_key in p_char_given_bigram:
        for char in p_char_given_bigram[bigram_key]:
            p_char_given_bigram[bigram_key][char].append( p_char_given_bigram[bigram_key][char][0]/bigram_counts[bigram_key[0]][bigram_key[1]][0])
    return p_char, p_char_given_monogram, p_char_given_bigram


def predict_next_char(prev_chars):
    '''
    Ranks the next possible chars given that prev_chars has been seen.
    Returns a list of lists in the form [char, count, probability] where
    the most likely next char appears first
    '''
    letter_counts = []
    if len(prev_chars) == 1:
        if prev_chars in bigram_counts:
            for key in bigram_counts[prev_chars]:
                temp = [str(key), int(bigram_counts[prev_chars][key][0]), float(bigram_counts[prev_chars][key][1])]
                letter_counts.append(temp)
    elif len(prev_chars) == 2:
        if prev_chars in trigram_counts:
            for key in trigram_counts[prev_chars]:
                temp = [str(key), int(trigram_counts[prev_chars][key][0]), float(trigram_counts[prev_chars][key][1])]
                letter_counts.append(temp)
    ranking = sorted(letter_counts, key=lambda x: x[2], reverse=True)
    return ranking





def interactive_next_char_predictor():
    '''
    Creates an interactive prompt. User inputs characters, most likely next characters are printed and
    the rank of the observed character is printed
    '''
    input_string = ""
    char = input("Input a single character, or nothing to exit")
    if not char:
        return
    next_char_ranking = predict_next_char(char)
    input_string += char
    print("Most likely next characters:")
    print("1. \'" + next_char_ranking[0][0] + "\' (%" + str(round(next_char_ranking[0][2] * 100, 3)) + ")")
    print("2. \'" + next_char_ranking[1][0] + "\' (%" + str(round(next_char_ranking[1][2] * 100, 3)) + ")")
    print("3. \'" + next_char_ranking[2][0] + "\' (%" + str(round(next_char_ranking[2][2] * 100, 3)) + ")")
    chars_before = char
    char = input("Input a single character, or nothing to exit")
    if not char:
        return
    input_string += char

    while char:
        observed_prob = calc_observed_probability(char, chars_before)
        observed_rank = find_observed_rank(next_char_ranking, char, observed_prob)
        print("The observed character \'" + char + "\' was ranked " + str(observed_rank) + " most likely (%" + str(
            round(observed_prob * 100, 3)))
        chars_before = chars_before[-1] + char
        next_char_ranking = predict_next_char(chars_before)
        print("Most likely next characters:")
        if next_char_ranking:
            i = 0
            while i < 3 and i < len(next_char_ranking):
                print(str(i + 1) + ". \'" + next_char_ranking[i][0] + "\' (%" + str(round(
                    next_char_ranking[i][2] * 100, 3)) + ")")
                i += 1

        print("Your String: " + input_string)

        char = input("Input a single character, or nothing to exit")
        input_string += char



def find_observed_rank(rank_list, observed_char, p):
    '''
    Finds the rank of the observed char given previous chars.

    '''
    for i in range(0, len(rank_list)):
        if rank_list[i][0] == observed_char:
            return i + 1
    #If observed_char is not in rank list, use stupid backoff probability
    rank_list.append([observed_char, -1, p])
    updated_ranking = sorted(rank_list, key=lambda x: x[2], reverse=True)
    for i in range(0, len(updated_ranking)):
        if updated_ranking[i][0] == observed_char:
            return i + 1


def calc_observed_probability(observed, previous_chars):
    '''
    Calculates the probability of seeing observed given previous_chars
    If P(observed | previous_chars) = 0, Use stupid backoff
    '''
    if len(previous_chars) == 1:
        if previous_chars in p_char_given_monogram and observed in p_char_given_monogram[previous_chars]:
            return p_char_given_monogram[previous_chars][observed][-1]
        else:
            return .4 * p_char[observed] #Applying stupid backoff
    if len(previous_chars) == 2:
        if previous_chars in p_char_given_bigram and observed in p_char_given_bigram[previous_chars]:
            return p_char_given_bigram[previous_chars][observed][-1]
        elif observed in p_char_given_monogram[previous_chars[-1]]:
            return p_char_given_monogram[previous_chars[-1]][observed][-1] * .4 #Stupid backoff
        else:
            return .16 * p_char[observed] #Stupid backoff twice



char_count, monogram_counts, bigram_counts, trigram_counts = init_n_gram_dict(training_data)
p_char, p_char_given_monogram, p_char_given_bigram = compute_prob_dict(monogram_counts, bigram_counts, trigram_counts, char_count)
interactive_next_char_predictor()












