import sys

# Fixed global definitions provided in the assignment.
FIRST_PERSON = ["i", "me", "mine", "we", "us", "our", "ours"]
SECOND_PERSON = ["you", "your", "yours", "u", "ur", "urs"]
THIRD_PERSON = ["he", "him", "his", "she", "her", "hers", "it", "its", "they",\
                "them", "their", "theirs"]
FUTURE_TENSE = ["'ll", "will", "gonna"]
COMMON_NOUNS = ["/NN", "/NNS"]
PROPER_NOUNS = ["/NNP", "/NNPS"]
ADVERBS = ["/RB", "/RBR", "/RBS"]
WH_WORDS = ["/WDT", "/WP", "/WP$", "/WRB"]
SLANG_LST = []

PUNCTUATIONS = ["#", "$", ".", "'", ":", ";", ",", "(", ")", "\"", "!", "?"]

'''
This class is used to interpret tweet file arguments on command line.
Accounting for forms similar to: 
"<name>.twt", "<cls_name>:<name>.twt", "<cls_name>:<name>.twt+<name2>.twt+.."
'''
class TweetArg:
    
    def __init__(self, argStr):
        self.cls_name = self.determine_cls_name(argStr)
        self.twt_files = self.determine_twt_files(argStr)
    
    '''
    Return the appropriate class name provided the argument string.
    '''
    def determine_cls_name(self, arg_str):
        
        cls_name = ""
        opt_cls_index = arg_str.find(":")
        
        if not opt_cls_index == -1:
            cls_name = arg_str[:opt_cls_index]
        else:
            cls_name = arg_str

        return cls_name
        
    '''
    Return a list of tweet files (string) provided the argument string.
    '''
    def determine_twt_files(self, arg_str):
        
        twt_file_lst = []
        opt_cls_index = arg_str.find(":")
        additional_cls_index = arg_str.find("+")
        
        file_section = arg_str[opt_cls_index + 1:]

        if additional_cls_index == -1:
            twt_file_lst.append(file_section)
        else:
            twt_file_lst = file_section.split("+")
            
        return twt_file_lst
    
    def get_name(self):
        return self.cls_name
    
    def get_twt_files(self):
        return self.twt_files
            
'''
The FeatureCounter class is used to determine the respective feature counts
when provided a tweet(string) and class name(string).

If you wish to add new features, you must add a new instance as well as 
adjusting the __str__ method and adding its respective function.
'''
class FeatureCounter:
    
    def __init__(self, cls_name, tweet):
        
        self.cls_name = cls_name
        
        # If we find the tweet is completely empty make all the entries 0.
        if tweet == "":
            self.fpps = self.spps = self.tpps = self.ccs = self.ptvs = \
                self.commas = self.all_colons = self.dashes = \
                self.parentheses = self.ellipses = self.cns = self.pns = \
                self.advs = self.slangs = self.all_uppers = \
                self.avg_sent_len = self.avg_token_len = self.num_of_sent = 0
        else:
            self.lst_of_tokens = tweet.split(" ")
            
            self.fpps = self.count_1st_person_pros()
            self.spps = self.count_2nd_person_pros()
            self.tpps = self.count_3rd_person_pros()
            self.ccs = self.count_coord_conjs(tweet)
            self.ptvs = self.count_past_verbs(tweet)
            self.commas = self.count_commas()
            self.all_colons = self.count_colons()
            self.dashes = self.count_dashes()
            self.parentheses = self.count_parentheses()
            self.ellipses = self.count_ellipses()
            self.cns = self.count_common_nouns()
            self.pns = self.count_proper_nouns()
            self.advs = self.count_adverbs()
            self.slangs = self.count_slangs()
            self.all_uppers = self.count_all_upper_words()
            self.avg_sent_len = self.count_avg_sent_len(tweet)
            self.avg_token_len = self.count_avg_token_len()
            self.num_of_sent = self.count_sentences(tweet)
    
    def __str__(self):
        
        return \
        "%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%f,%f,%d,%s\n" % \
        (self.fpps, self.spps, self.tpps, self.ccs, self.ptvs,
        self.commas, self.all_colons, self.dashes, self.parentheses,
        self.ellipses, self.cns, self.pns, self.advs,
        self.slangs, self.all_uppers, self.avg_sent_len, self.avg_token_len,
        self.num_of_sent, self.cls_name)
 
    '''
    Return a count of all element occurences of the provided list that are in 
    the list of tokens within this FeatureCounter.  A not_tag boolean must be 
    specified, if False then it will count the elements within the provided 
    list for whether or not they are equal to the tag in the token, if True it 
    do similarly but whether or not the word is equal in the token.
    '''
    def sum_by_list(self, lst, not_tag):
        
        count = 0
        
        for token in self.lst_of_tokens:
            
            word = token[:token.rfind("/")].lower()
            tag = token[token.rfind("/"):].lower()
            
            for element in lst:
                element = element.lower()
                
                if (not_tag and word == element) or \
                   (not not_tag and tag == element):
                    
                    count += 1

        return count
    
    '''
    Return the number of appearances of example (string) within the 
    lst_of_tokens of this FeatureCounter object, by checking whether the token
    begins with example.
    '''
    def sum_by_example(self, example):
        
        count = 0
        
        for token in self.lst_of_tokens:
            if token.lower().startswith(example):
                count += 1
                
        return count
    
    def count_1st_person_pros(self):

        return self.sum_by_list(FIRST_PERSON, True)
    
    def count_2nd_person_pros(self):
        
        return self.sum_by_list(SECOND_PERSON, True)
    
    def count_3rd_person_pros(self):
        
        return self.sum_by_list(THIRD_PERSON, True)
    
    def count_coord_conjs(self, tweet):
        
        return tweet.count("/CC")
    
    def count_past_verbs(self, tweet):
        
        return tweet.count("/VBD")
    
    def count_commas(self):
        
        return self.sum_by_example(",")
    
    def count_colons(self):
        
        return self.sum_by_example(":")
    
    def count_dashes(self):
        
        return self.sum_by_example("-")
    
    def count_parentheses(self):
        
        return self.sum_by_example("(") + self.sum_by_example(")")

    def count_ellipses(self):
        
        return self.sum_by_example("..")
    
    def count_common_nouns(self):
        
        return self.sum_by_list(COMMON_NOUNS, False)
    
    def count_proper_nouns(self):
        
        return self.sum_by_list(PROPER_NOUNS, False)
    
    def count_adverbs(self):
        
        return self.sum_by_list(ADVERBS, False)

    def count_slangs(self):

        return self.sum_by_list(SLANG_LST, True)
    
    def count_all_upper_words(self):
        
        count = 0
        
        for word in self.remove_punctuations(self.lst_of_tokens):
            word = word[:word.find("/")]
            if word.isupper() and len(word) >= 2:
                
                # Check each letter and count for at least 2.
                letters = 0
                k = 0
                while letters < 2 and k < len(word):
                    if word[k].isalpha():
                        letters += 1
                    k += 1
                if letters >= 2:
                    count += 1
                    
        return count

    def remove_punctuations(self, lst_of_tokens):
        
        new_lst = []
        
        for token in lst_of_tokens:

            add = True
            for punct in PUNCTUATIONS:
                if token.startswith(punct):
                    add = False
                    break
            if add:
                new_lst.append(token)
        
        return new_lst
    
    def count_avg_sent_len(self, tweet):
        
        if not tweet.endswith('\n'):
            tweet += '\n'
        
        # All tweets has '\n' at the very end we don't want empty [''] list.
        sentences = tweet.split("\n")[:-1]
        
        count = 0.0
        for sentence in sentences:
            count += len(self.remove_punctuations(sentence.strip().split(" ")))
        
        return (count / len(sentences))
    
    def count_avg_token_len(self):
        
        num_of_tokens = len(self.lst_of_tokens)
        count = 0.0
        for token in self.remove_punctuations(self.lst_of_tokens):
            token = token[:token.rfind("/")]
            count += len(token)
        
        return (count / num_of_tokens)
    
    def count_sentences(self, tweet):
        
        sent_count = tweet.count("\n")
        
        #To consider last tweet where it could possibly not have a new line.
        if sent_count == 0:
            if not tweet.strip() == "":
                sent_count = 1
            else:
                sent_count = 0
                
        return sent_count

 
'''
Interpret the command line arguments, interpreting the optional number of tweet
flags as well as tweet file arguments and output file.  Return the interpreted
information in a 3 element tuple respectively; 
(num_of_twts, lst_of_TweetArgs, out_file)
'''
def interpret_input():

    flag = sys.argv[1]    
    
    lst_of_TweetArgs = []
    num_of_twts = -1
    
    # twt_marker is used to find out which argument index 
    # marks the start of twt files.
    twt_marker = 1
    if flag.startswith("-"):
        num_of_twts = int(flag[1:])
        twt_marker = 2
        
    # minus 1 to not include the output file argument.
    twt_args = len(sys.argv) - 1
    for k in range(twt_marker, twt_args):
        lst_of_TweetArgs.append(TweetArg(sys.argv[k]))
    
    # last argument is the output file.
    out_file = sys.argv[twt_args]
            
    return (num_of_twts, lst_of_TweetArgs, out_file)

'''
Provided an output file (assumed to be already open) and list of classes
(TweetArg), write out the fixed schema to the output file.
'''
def write_schema(lst_of_classes, out_file):    
    
    out_file.write("@relation twit_classification\n\n")  
    out_file.write("@attribute 1st_person_pro numeric\n")
    out_file.write("@attribute 2nd_person_pro numeric\n")
    out_file.write("@attribute 3rd_person_pro numeric\n")
    out_file.write("@attribute coord_conj numeric\n") 
    out_file.write("@attribute past_verb numeric\n") 
    out_file.write("@attribute future_tense numeric\n") 
    out_file.write("@attribute comma numeric\n") 
    out_file.write("@attribute colon numeric\n") 
    out_file.write("@attribute dash numeric\n") 
    out_file.write("@attribute parenthese numeric\n") 
    out_file.write("@attribute ellipse numeric\n") 
    out_file.write("@attribute common_noun numeric\n") 
    out_file.write("@attribute proper_noun numeric\n") 
    out_file.write("@attribute adverb numeric\n") 
    out_file.write("@attribute wh_word numeric\n") 
    out_file.write("@attribute slang numeric\n") 
    out_file.write("@attribute all_upper_word numeric\n") 
    out_file.write("@attribute avg_sent_len numeric\n") 
    out_file.write("@attribute avg_token_len numeric\n") 
    out_file.write("@attribute num_of_sent numeric\n") 

    classes = []
    for cls in lst_of_classes:
        classes.append(cls.get_name())

    out_file.write("@attribute twit {%s}\n\n@data\n" % ",".join(classes))     
    
'''
Return a list containing the contents of the specified file directory. The list
consists of the lines within that file.
'''
def readFile(file_directory):
    
    temp_file = open(file_directory, 'r')
    temp_lst = []

    for line in temp_file:
        temp_lst.append(line.lower().strip())
    
    temp_file.close()
    
    return temp_lst    
    
'''
Perform the procedure of counting the features provided tweet (String) & the
class name (string), and writing it out to the provided out_file (assumed to be
already open). Once completed, read and return the next tweet within the reader 
(assumed to be already open), also returning the previously passed in tweet.
'''
def write_out_data(cls_name, twt, out_file, reader):
    
    # Need for corner case: last tweet is a blank line.
    prev_twt = twt
    
    if twt.strip() == "":
        out_file.write(str(FeatureCounter(cls_name, "")))   
    else:
        out_file.write(str(FeatureCounter(cls_name, twt)))
        
    twt = get_tweet(reader)
    
    return (twt, prev_twt)

'''
Read and return a string of appended lines within the provided reader (assumed 
to be already open) up to the first appearance of"|\n" or to the end of file.  
Return None if there is nothing left to read.
'''
def get_tweet(reader):
    
    nothing_left = False
    tweet = ""
    
    line = reader.readline()
    
    if not line:
        nothing_left = True
    else:
        while line and (not line == "|\n"):
            tweet += line
            line = reader.readline()   

    if nothing_left:
        return None
    else:
        return tweet
        

'''
Perform the core procedures in writing out the arff file data provided the user
inputs; num_of_twts (Integer), lst_of_TweetArgs, out_file (assumed to be 
already open).
'''
def buildarff_data(num_of_twts, lst_of_TweetArgs, out_file):
    
   # Loop through all individual twt file arguments
    for twtArg in lst_of_TweetArgs:
        twt_file_lst = twtArg.get_twt_files()
        cls_name = twtArg.get_name()
        
        # Loop through all joined twt files (ex: <ex1>.twt+<ex2>.twt)
        for twt_file in twt_file_lst:
            twt_path = sys.path[0] + "/" + twt_file
            reader = open(twt_path, 'r')
            prev_twt = None
            
            # Act accordingly if the number of tweets are specified.
            if not num_of_twts == -1:
                twt = get_tweet(reader)
                k = 1
                while k <= num_of_twts and (not twt == None):     
                    (twt, prev_twt) = \
                     write_out_data(cls_name, twt, out_file, reader)
                    k += 1
            else:
                twt = get_tweet(reader)
                
                # Have to explicitly say not None since if (twt == "") it'll 
                # break out of the loop.
                while (not twt == None):
                    (twt, prev_twt) = \
                     write_out_data(cls_name, twt, out_file, reader)
                        
                # Corner case of last line being blank.
                if prev_twt and prev_twt.endswith("\n"):
                    out_file.write(str(FeatureCounter(cls_name, "")))
                    
            reader.close()


if __name__ == "__main__":
    
    # Read into a global variable.
    SLANG_LST = readFile("/u/cs401/Wordlists/Slang")

    # Interpret input and prepare the output file.
    (num_of_twts, lst_of_TweetArgs, out_file) = interpret_input()
    
    out_file = open(sys.path[0] + "/" + out_file, 'w')
    
    # Write out the arff data.
    write_schema(lst_of_TweetArgs, out_file)
    buildarff_data(num_of_twts, lst_of_TweetArgs, out_file)

    out_file.close()