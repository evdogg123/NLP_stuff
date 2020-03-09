from nltk import sent_tokenize

t = open("sentence_splitter_input.txt", "r")
text = t.read()
print(text)


split_text = sent_tokenize(text)
for sent in split_text:
    print(sent)
    print("")
