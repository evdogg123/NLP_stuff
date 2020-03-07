import wikipedia
import re
from bs4 import BeautifulSoup

state_names = ["California", "Nevada", "Arizona", "Florida", "Maryland", "Pennsylvania",
               "New Jersey", "North Carolina", "Vermont", "Idaho"]

def lookup_state_wiki(state_name):
    '''
    Finds wikipedia page for given state_name
    Converts html to text
    '''
    page_html = wikipedia.WikipediaPage(state_name).html()
    if page_html:
        soup = BeautifulSoup(page_html, "html.parser")
        return soup.get_text()
    else:
        print("State not found")



def lookup_GSP(wiki_text):
    '''
    Takes text from a wikipedia page
    Uses a regex to find the state's gross state product
    '''
    regex = '(?:G|g)ross state product[A-Za-z\(\)\s0-9]*\$([0-9]*\.?[0-9]*\s(?:billion|trillion|million))'
    match = re.search(regex, wiki_text)
    if match:
        return match.groups()[0]
    else:
        return "Not Found"


def convert_GSP_to_int(GSP):
    '''
    Converts GSP found with lookup_GSP into a number
    '''
    amt, unit = tuple(GSP.split())
    if unit == 'billion':
        return int(float(amt) * 1000000000)
    elif unit == 'trillion':
        return int(float(amt) * 1000000000000)
    elif unit == 'million':
        return int(float(amt) * 1000000)


def look_up_nicknames(wiki_text):
    '''
    Finds the states nicknames
    '''
    regex = r'Nickname\(s\)\:\s([A-za-z;\s0-9\[\]\(\)\",]+)Motto'
    match = re.search(regex, wiki_text)
    if match:
        return match.groups()[0]
    else:
        return "Not Found"


def clean_nickname_data(data):
    '''
    Cleans the nicknames retrieved by look_up_nicknames
    '''
    data = re.sub("\[[0-9]\]", "", data)
    data = data.replace("\"", "")
    temp = re.split(r'[;,]', data)
   #temp = data.split(";")
    nicknames = []
    for nickname in temp:
        nicknames.append(nickname.strip())
    return nicknames





def collect_state_info(state_names):
    """
    Iterates through given state_names
    Finds the states GSP and nicknames
    stores this data in a file called output.tsv
    """
    state_outputs = []
    for state in state_names:
        state_text = lookup_state_wiki(state)
        GSP = lookup_GSP(state_text)
        if GSP != "Not Found":
            GSP = convert_GSP_to_int(GSP)
        nicknames = look_up_nicknames(state_text)
        nicknames = clean_nickname_data(nicknames)
        nicknames_as_string = ";"
        nicknames_as_string = nicknames_as_string.join(nicknames)
        state_outputs.append(state + '\t' + str(GSP) + '\t' + nicknames_as_string)
    with open('output.tsv', 'w') as fp:
        for state_output in state_outputs:
            fp.write(state_output + '\n')


collect_state_info(state_names)




