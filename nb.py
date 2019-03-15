import sys, os, csv, math
from collections import Counter

## 10-601 Section A HW9 nb.py ##

## Jae Kang ##
## jkang2 ##


## P(conservative) = 64 / 120
## P(liberal) = 56 / 120

def retrieve_words(train_files):
    conserv_words, liberal_words = ([], [])
    for i in train_files:
        if i.startswith('con'):
            for word in open(i, "r").readlines():
                n_word = (word.strip("\n")).lower()
                conserv_words.append(n_word)
        elif i.startswith('lib'):
            for word in open(i, "r").readlines():
                n_word = (word.strip("\n")).lower()
                liberal_words.append(n_word)
    return conserv_words, liberal_words

def retrieve_words_test(test_file):
    words = []
    for word in open(test_file, "r").readlines():
        n_word = (word.strip("\r\n")).lower()
        words.append(n_word)
    return words

def get_post_prob_L_total(test_words, vocab_dict):
    total_prob = 0
    for word in test_words:
        try:
            #print ("vocab_dict[word][0] :", vocab_dict[word][0])
            #print ("math.log(vocab_dict[word][0] :", math.log(vocab_dict[word][0]))
            total_prob += math.log(vocab_dict[word][0])
        except:
            continue
    return total_prob

def get_post_prob_C_total(test_words, vocab_dict):
    total_prob = 0
    for word in test_words:
        try:
            #print ("vocab_dict[word][1] :", vocab_dict[word][1])
            #print ("math.log(vocab_dict[word][1] :", math.log(vocab_dict[word][1]))
            total_prob += math.log(vocab_dict[word][1])
        except:
            continue
    #print "post_prob C total_prob :", total_prob
    return total_prob

def get_test_con_lib_file_count(test_files):
    lib_file_count, con_file_count = 0, 0
    for file in test_files:
        if file.startswith("lib"):
            lib_file_count += 1
        elif file.startswith("con"):
            con_file_count += 1
    return lib_file_count, con_file_count


def get_lib_dict(liberal_words):
    return Counter(liberal_words)

def get_cons_dict(conserv_words):
    return Counter(conserv_words)


def main():
    vocab_dict = dict()
    train_files = []
    test_files = []
    train_txt = sys.argv[-2]
    test_txt = sys.argv[-1]
    for tr_file in open(train_txt, 'r').readlines():
        train_files.append(tr_file.strip("\n"))
    for te_file in open(test_txt, 'r').readlines():
        test_files.append(te_file.strip("\n"))
    conserv_words, liberal_words = retrieve_words(train_files)
    vocabulary = set(conserv_words + liberal_words)
    lib_dict = get_lib_dict(liberal_words)
    cons_dict = get_cons_dict(conserv_words)
    values = ["L", "C"]
    ## training phase
    for val in values:
        if val == "L":
            for word in vocabulary:
                #print ("word :", word)
                num = float(lib_dict[word] + 1)
                denom = float(len(liberal_words) + len(vocabulary))
                #print "num :", num
                #print "denom :", denom
                posterior_prob_L = num / denom
                #print ("posterior_prob_L :", posterior_prob_L)
                vocab_dict[word] = [posterior_prob_L]
                #print ("vocab_dict[word] :", vocab_dict[word])
        if val == "C":
            for word in vocabulary:
                #print ("word :", word)
                num = float(cons_dict[word] + 1)
                denom = float(len(conserv_words) + len(vocabulary))
                #print "num :", num
                #print "denom :", denom
                posterior_prob_C = num / denom
                #print ("posterior_prob_C :", posterior_prob_C)
                temp = vocab_dict[word]
                temp.append(posterior_prob_C)
                vocab_dict[word] = temp
                #print ("vocab_dict[word] :", vocab_dict[word])
    ## predict / generalize to new instances
    ## testing phase
    correct_guesses = 0
    total_n = float(len(test_files))
    te_lib_count, te_con_count = get_test_con_lib_file_count(test_files)
    # prior probability
    prior_prob_L =  float(te_lib_count) / total_n
    prior_prob_C = float(te_con_count) / total_n
    for test_file in test_files:
        label = "L" if test_file.startswith("lib") else "C"
        test_words = retrieve_words_test(test_file)
        # calculating liberal probability
        post_prob_L_total = get_post_prob_L_total(test_words, vocab_dict)
        lib_prob = math.log(prior_prob_L) + post_prob_L_total
        # calculating conservative probability
        post_prob_C_total = get_post_prob_C_total(test_words, vocab_dict)
        cons_prob = math.log(prior_prob_C) + post_prob_C_total
        if lib_prob >= cons_prob:
            print "L"
            if label == "L": correct_guesses += 1
        else:
            print "C"
            if label == "C": correct_guesses += 1
    print "Accuracy: %.04f " % (correct_guesses / total_n)
    return None

if __name__ == "__main__":
    main()
