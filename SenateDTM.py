# Runs on Python 3.7
# Packages and programs needed
from bs4 import BeautifulSoup
from urllib.request import urlopen, Request
from nltk import word_tokenize, bigrams, trigrams
from nltk.stem import PorterStemmer
from collections import Counter
import re, os, itertools, csv

# Getting stop words from MIT's site
stop_words = urlopen('http://www.ai.mit.edu/projects/jmlr/papers/volume5/lewis04a/a11-smart-stop-list/english.stop').read().decode().split('\n')
# Making my own list of stopwords if I want to add names of candidates or other words
original_stopwords =('')
# Getting the porter stemmer ready to use
pt = PorterStemmer()

# It should not be necessary to set it up like this, but it kept glitching when I tried to add this to the for loop later
# creating lists of the stemmed stop words so they can easily be removed from the stemmed corpuses later
stop_words_stemmed = []
original_stopwords_stemmed = []

for w in stop_words:
    stop_words_stemmed.append(pt.stem(w))

for w in original_stopwords:
    original_stopwords_stemmed.append(pt.stem(w))

# Using so states all appear as "my_state". Trying to break this into multiple lines throws too many errors.
states_regex = re.compile(r'alabama|alaska|arizona|arkansas|california|colorado|connecticut|delaware|florida|georgia|hawaii|idaho|illinois|indiana|iowa|kansas|kentucky|louisiana|maine|maryland|massachusetts|michigan|minnesota|mississippi|missouri|montana|nebraska|nevada|ohio|oklahoma|oregon|pennsylvania|tennessee|texas|utah|vermont|wisconsin|wyoming|virginia')

# Candidate names (need to catch any words belonging to the candidates name (first, middle, maiden, last))
# I want to later be able to catch all names as belonging to family members
def replace_candidate_name(split_name, text):
    # Find all permutations of the words in a candidates' name
    _gen = (itertools.permutations(split_name, i + 1) for i in range(len(split_name)))
    all_permutations_gen = itertools.chain(*_gen)

    # Create a regex from them
    name_phrases = [' '. join(w) for w in all_permutations_gen]
    name_phrases_no_single_initials = []

    # Drop initials (they would match too many things)
    for name_phrase in name_phrases:
        if len(name_phrase) > 1:
            name_phrases_no_single_initials.append(name_phrase)

    # Have it do matches in decreasing order of complexity so full names get matched first
    name_phrases_no_single_initials.reverse()

    # Create regex.
    candidate_regex ='|'.join(name_phrases_no_single_initials)
    # Making sure the expression isn't catching when names are part of words
    compiled_candidate_regex =  re.compile('((^|\s)('+ candidate_regex + ')($|\s))')

    return compiled_candidate_regex.sub(' candidate.name ', text)

# Reading in a list of common first names

myfile = open("firstnames.csv", "r")  # "r" to only read the file
firstnames = csv.reader(myfile)  # Get rows in the file
firstnameslist = []
for row in firstnames:
     firstnameslist.append(row)


# Concatenating all first names into a single string separated by |
firstnames_data = ''
for item in firstnameslist:
   firstnames_data += str(item[0]) +'|'

# Remove the final pipe so ever word used doesn't get added
firstnames_data
firstnames_data = firstnames_data[:-1]


# Making sure only exact matches happen
compiled_firstnames_regex = re.compile('((\s)('+ firstnames_data + ')($|\s))')

# Formatting how bigrams and trigrams will be reported
def cleaner(tuple):
    out = tuple[0] + '_' + tuple[1]
    return(out)


def cleaner_tri(tuple):
    out = tuple[0] + '_' + tuple[1] + '_' + tuple[2]
    return(out)


# Where to look for the files
os.chdir('Senate Bios/')
stuff = ['Cleaned Senate Bios']


# Making dictionaries to store each file as a statement and store counts of words and phrases
# Making lists to fill with all unigrams, bigrams, and trigrams
statements = {}
word_store = {}
all_unigrams = []
all_bigrams = []
all_trigrams = []


# Storing the identifying information of each file along with all the text in each file
for z in stuff:
    os.chdir('[redacted]' + z)
    files = os.listdir(os.getcwd())
    for y in files:
        splits = re.split("_", y)
        state = splits[0]
        party = splits[1]
        name = splits[-1].split('.txt')[0]
        split_name = re.split("-", name.lower())
        filename = y
        # Reading in text from each file, making lowercase, removing numbers, removing whitespace
        text = open(y, 'r').readlines()
        text = ' '.join(text)
        text = text.lower()
        text = re.sub('[0-9]+', '', text)
        text = re.sub('\W', ' ', text)

        #Making all states show up as "my.state", two state names are more complicated
        text = re.sub(r'new hampshire', 'my.state', text)
        text = re.sub(r'new jersey','my.state', text)
        text = re.sub(r'new mexico', 'my.state',text)
        text = re.sub(r'new york', 'my.state', text)
        text = re.sub(r'north arolina', 'my.state', text)
        text = re.sub(r'north dakota', 'my.state', text)
        text = re.sub(r'rhode island', 'my.state', text)
        text = re.sub(r'south carolina', 'my.state', text)
        text = re.sub(r'south dakota', 'my.state', text)
        text = re.sub(r'west virgina', 'my.state', text)
        text = re.sub(states_regex, 'my.state', text)

        #This is necessary to be able to find family names later
        text = re.sub(r'nancy pelosi|pelosi', 'nancy_pelosi', text)
        text = re.sub(r'chuck schumer|schumer', 'chuck_schumer', text)
        text = re.sub(r'hillary clinton|clinton', 'hillary_clinton', text)
        text = re.sub(r'donald trump|trump', 'donald_trump', text)
        text = re.sub(r'mitch mcconnell|mcconnell', 'mitch_mcconnell', text)
        text = re.sub(r'paul ryan', 'paul_ryan', text)
        text = re.sub(r'joe biden|biden', 'joe_biden', text)
        text = re.sub(r'barack obama', 'barack_obama', text)
        text = re.sub(r'hugo chavez', 'hugo_chavez', text)
        text = re.sub(r'fidel castro', 'fidel_castro', text)
        text = re.sub(r'kim jong un', 'kim_jong_un', text)
        text = re.sub(r'benjamin netanyahu', 'benjamin_netanyahu', text)
        text = re.sub(r'mao_zedong', 'mao_zedong', text)
        text = re.sub(r'hurricane katrina', 'hurricane_katrina', text)
        text = re.sub(r'hurricane hermine|hurricanes hermine', 'hurricane_hermine', text)

        # All mentions of the candidate will now appear as candidate.name
        text = replace_candidate_name(split_name,text)

        # All other first names will appear as family.name
        text = re.sub(compiled_firstnames_regex, ' family.name ', text)

        # Storing all of the identifying information of a file with the text
        statements[y] = {"State": state, "Party": party,
                         "Name": name, "Text": text}


# Dictionaries for counts per statement for unigrams, bigrams, trigrams for words/phrases that aren't stop words
nestedDict = statements

for entry in nestedDict.values():
    unigrams_statements = {}
    bigrams_statements = {}
    trigrams_statements = {}
    tokes = word_tokenize(entry["Text"])
    tokes_stemmed = map(pt.stem, tokes)
    tokes_cleaned = [w for w in tokes_stemmed if w not in stop_words_stemmed and w not in original_stopwords_stemmed]

    # Finding and formatting bigrams and trigrams
    tokes_bi = bigrams(tokes_cleaned)
    clean_bis = map(cleaner, list(tokes_bi))
    tokes_tri = trigrams(tokes_cleaned)
    clean_tris = map(cleaner_tri, list(tokes_tri))


    # Counting unigrams, bigrams and trigrams per statement
    for word in tokes_cleaned:
        if word in unigrams_statements:
            unigrams_statements[
                word] += 1
        elif word not in unigrams_statements:
            unigrams_statements[word] = 1
        all_unigrams.append(word)

    for word in clean_bis:
        if word in bigrams_statements:
            bigrams_statements[
                word] += 1
        elif word not in bigrams_statements:
            bigrams_statements[word] = 1
        all_bigrams.append(word)

    for word in clean_tris:
        if word in trigrams_statements:
            trigrams_statements[
                word] += 1
        elif word not in trigrams_statements:
            trigrams_statements[word] = 1
        all_trigrams.append(word)

    entry['unigrams_statements'] = unigrams_statements
    entry['bigrams_statements'] = bigrams_statements
    entry['trigrams_statements'] = trigrams_statements


# Storing all unigrams and the most common bigrams and trigrams
most_used_unigrams = Counter(all_unigrams).most_common(20098)
most_used_bigrams = Counter(all_bigrams).most_common(100)
most_used_trigrams = Counter(all_trigrams).most_common(50)


# Writing the DTM
out = open('[/Redacted]SenateDTM.csv', 'w')
out.write('State,Party,Name')

for word in most_used_unigrams:
    out.write("," + word[0])

for word in most_used_bigrams:
    out.write("," + word[0])

for word in most_used_trigrams:
    out.write("," + word[0])
out.write('\n')

# Iterates through each statement of each senator
nestedDict = statements
for key in nestedDict:
    out.write(nestedDict[key]["State"] + "," + nestedDict[key]["Party"] + "," + nestedDict[key]["Name"])

    for word in most_used_unigrams:
        if word[0] in nestedDict[key]["unigrams_statements"]:
            count = nestedDict[key]["unigrams_statements"][
                word[0]]  # word is a tuple, so need to make sure it's only using the first element
        else:
            count = 0
        out.write("," + str(count))

    for word in most_used_bigrams:
        if word[0] in nestedDict[key]["bigrams_statements"]:
            count = nestedDict[key]["bigrams_statements"][
                word[0]]  # word is a tuple, so need to make sure it's only using the first element
        else:
            count = 0
        out.write("," + str(count))

    for word in most_used_trigrams:
        if word[0] in nestedDict[key]["trigrams_statements"]:
            count = nestedDict[key]["trigrams_statements"][
                word[0]]  # word is a tuple, so need to make sure it's only using the first element
        else:
            count = 0
        out.write("," + str(count))
    out.write('\n')

out.write("\n")
out.close()



