import wikipedia
import re


def lookup_state_wiki(state_name):
    page = wikipedia.page(state_name)
    if page:
        return page.content


def lookup_GSP(wiki_text):
    regex = '(?:G|g)ross state product[A-Za-z\(\) 0-9]*\$([0-9]*\.?[0-9]* (?:billion|trillion|million))'
    match = re.search(regex, wiki_text)
    if match:
        return match.groups()[0]


def convert_GSP_to_int(GSP):
    amt, unit = tuple(GSP.split())
    if unit == 'billion':
        return int(float(amt) * 1000000000)
    elif unit == 'trillion':
        return int(float(amt) * 1000000000000)
    elif unit == 'million':
        return int(float(amt) * 1000000)


cali_text = lookup_state_wiki("California")
GSP = lookup_GSP(cali_text)
GSP_int = convert_GSP_to_int(GSP)
print(GSP_int)

penn_text = lookup_state_wiki("Pensylvania")
print(penn_text)

def look_up_nicknames(wiki_text):
    regex = 'Nickname\('
    match = re.search(regex, wiki_text)
    if match:
        return match.group(0)

print(look_up_nicknames(penn_text))

#\(s\): ([A-Za-z]+);

