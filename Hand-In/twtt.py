import sys
import re
import NLPlib

'''
Return a string with tweeter tags, link tags, html tags and urls removed, 
provided a line (string).
'''
def remove_variable_patterns(line):
    
    tweeter = r'@<a+?\s.+?</a>|'
    link_tag = '<a+?\s.+?</a>|'
    general_html = '<.+?>|'

    hash_tag = '#([\w]+)|'    
    
    urls = '(((http|https|ftp)://[\w\-]+\.[\w\-]+)|([\w\-\.]+))' + \
         '\.(ly|be|com|org|net|mil|edu|ly|BE|COM|ORG|NET|MIL|EDU)(/[\S]+)*'
    
    pattern = tweeter + link_tag + general_html + hash_tag + urls
    
    return re.sub(pattern, "", line)

'''
Return a string with HTML names interpreted into characters, provided a string.
'''
def remove_fixed_patterns(line):
    
    return line.replace("&quot;", "\"").replace("&amp;", "&")\
          .replace("&lt;", "<").replace("&gt;", ">").replace("&nbsp;", " ")\

'''
Return a list of tagged tokens (string) provided the list of untagged word 
tokens, an output file to write out the result and the NLPLib tagger.

The start parameter is a boolean that indicates whether or not the sentence_lst
is of the 1st tweet read; (True) otherwise (False).
'''
def tag_and_write_out(sentence_lst, out_file, tagger, start):
    
    joined_lst = []
    curr_sentence = []
    result = ""
    
    for sentence in sentence_lst:
        
        resp_tag_lst = tagger.tag(sentence)
        for k in range(0, len(resp_tag_lst)):
            word = "/".join([sentence[k], resp_tag_lst[k]])
            curr_sentence.append(word)
            
        for word in curr_sentence:
            result += "%s " % word

        joined_lst.append(result.strip())

        result = ""
        curr_sentence = []
    
    # Do not accumulate results. Write out immediately.
    if not joined_lst == []:
        if not start:
            out_file.write("\n")
        out_file.write("\n".join(joined_lst))  
        
    return joined_lst

'''
Return a tuple with a index marker and sentenized tweet where a new line 
is injected in the proper position provided the length of the tweet(in indices),
a index marker (indicating character position within the tweet) and the tweet.

The heuristic is if the next two characters follows with a space and an 
upper case letter then a newline character should be injected right after the
space character.
'''
def look_ahead(twt_len, marker, sentenized_tweet):
    
    if twt_len - marker >= 2:
        if sentenized_tweet[marker + 1] == " " and \
           sentenized_tweet[marker + 2].isupper():

            marker += 2
            if not twt_len - marker == 2:
                sentenized_tweet = "%s\n%s" % \
                        (sentenized_tweet[:marker], sentenized_tweet[marker:])
            else:
                sentenized_tweet = sentenized_tweet[:marker] + \
                                 sentenized_tweet[marker:]
                
    return (marker, sentenized_tweet)
    
'''
Return a string injected with new line characters indicating new sentences, 
provided a raw tweet (string), a list of abbreviations (string) that shouldn't 
create a new sentence. (Heuristic came from the textbook).
'''
def sentenize(raw_tweet, abbrev_lst):
    
    # Initializations and preping tweet (subst. multiple spaces to a single)
    all_sent = []
    sentenized_tweet = re.sub(r'[\s]+', ' ', raw_tweet).strip()
    curr_sent = sentenized_tweet
    twt_len = len(sentenized_tweet) - 1
    
    marker = 0
    prev_word = ""
    
    while marker < twt_len:

        # Keep track of the last word we saw.
        prev_word += sentenized_tweet[marker]
        
        # If we see any of those listed we must apply the heuristic.
        if sentenized_tweet[marker] in [".", "?", "!"]:

            if (marker + 1) < twt_len and \
               sentenized_tweet[marker + 1] == "\"":
                marker += 1
            else:

                # Adjustment of heuristic: using the abbrev_lst to avoid
                # creating new sentences when unnecessary.
                if prev_word.lower() in abbrev_lst:
                    marker += 1
                else:
                    (marker, sentenized_tweet) = \
                     look_ahead(twt_len, marker, sentenized_tweet)

        elif sentenized_tweet[marker] == " ":
            prev_word = ""
                
        marker += 1

    return sentenized_tweet
    
'''
Returns a list containing list(s) of word tokens, each list of tokens being 
of a sentence provided a sentenized string. The sentenized string must be 
delimited by new line characters.
'''
def tokenize(sentenizedStr):

    # Filter and prepare the sentenized string for token form.
    sepSentMarker = re.sub(r'([\?\.!]+)', r' \1 ', sentenizedStr.strip())
    sepHash = re.sub(r'([#]+)', r' \1 ', sepSentMarker)
    sepDollar = re.sub(r'([\$]+)', r' \1 ', sepHash)
    sepComma = re.sub(r'([,]+)', r' \1 ', sepDollar)
    sepColon = re.sub(r'([:]+)', r' \1 ', sepComma)
    sepSColon = re.sub(r'([;]+)', r' \1 ', sepColon)
    sepDQuote = re.sub(r'(["]+)', r' \1 ', sepSColon)
    sepSQuote = re.sub(r'(((n|)\'(t|ve|ll|re|s|m|d))|([\']+))', r' \1 ', \
                       sepDQuote)
    sepOBrack = re.sub(r'([\(]+)', r' \1 ', sepSQuote)
    sepCBrack = re.sub(r'([\)]+)', r' \1 ', sepOBrack)
    sentenizedStr = re.sub(r'([\-]+)', r' \1 ', sepCBrack)
    
    lstOfStrSent = sentenizedStr.split('\n')
    sentenceLst = []

    for sentence in lstOfStrSent:
        sentence = sentence.strip()
        
        # This is to account for cases like "U.S."
        reformAbbrev = re.sub(r'(([A-Z]) \. ([A-Z]) \.)', r'\2.\3.',\
                              sentence)     
        removeDupSpace = re.sub(r'[\s]+', ' ', reformAbbrev)   
                
        sentenceLst.append(removeDupSpace.split(" "))

    # Check for empty string case: Ex - [['']]
    if len(sentenceLst) == 1 and len(sentenceLst[0]) == 1 and \
       sentenceLst[0][0] == '':
        sentenceLst = []
        
    return sentenceLst
        
'''
Return a list containing the contents of the specified file directory. The list
consists of the lines within that file.
'''
def readFile(directory):
    
    temp_file = open(directory, 'r')
    temp_lst = []

    for line in temp_file:
        temp_lst.append(line.lower().strip())
    
    temp_file.close()
    
    return temp_lst
     
'''
Process the given tweet line (string) using the abbreviation list and
tagger (NLPlib).  Write that output to out_file (assumed to be already opened).
A start (boolean) value must be specified to indicate whether the line 
specified is the 1st tweet to ensure newlines are written out correctly.
'''
def buildtwtt_data(line, abbrev_lst, tagger, out_file, start):
    
    step1 = remove_variable_patterns(line)
    step2 = remove_fixed_patterns(step1)

    sentenized_step = sentenize(step2, abbrev_lst)
    sentence_lst = tokenize(sentenized_step)
    
    tag_and_write_out(sentence_lst, out_file, tagger, start)

      
if __name__ == "__main__":

    # Open the file arguments.
    tweet_file = open(sys.argv[1], 'r')
    out_file = open(sys.argv[2], 'w')
    
    # Load required files for assignment.
    abbrev_lst = readFile("/u/cs401/Wordlists/pn_abbrev.english") +\
               readFile("/u/cs401/Wordlists/abbrev.english")
    tagger = NLPlib.NLPlib()
    
    # Previous read line is kept track for the corner case of the last line 
    # being a blank tweet.
    prev_line = None
    
    # Read the 1st line first.
    line = tweet_file.readline()
    buildtwtt_data(line, abbrev_lst, tagger, out_file, True)
    prev_line = line.strip()
    
    # From this point on continue with the rest of the tweet file.
    line = tweet_file.readline()
    while line:
        
        # If we reached this point the the line must be a tweet, thus "\n|" 
        # is needed.
        out_file.write("\n|")

        buildtwtt_data(line, abbrev_lst, tagger, out_file, False)
        prev_line = line
        line = tweet_file.readline()

    # Accounts for last line possibly being a blank tweet.
    if prev_line.endswith("\n"):
        out_file.write("\n|\n")
        
    out_file.close()
    tweet_file.close()