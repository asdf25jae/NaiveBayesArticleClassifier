import sys, os, math
from collections import Counter



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


def get_lib_counter(liberal_words):
    return Counter(liberal_words)

def get_cons_counter(conserv_words):
    return Counter(conserv_words)



def main():
    train_files = []
    train_txt = sys.argv[-1]
    for tr_file in open(train_txt, 'r').readlines():
        train_files.append(tr_file.strip("\n"))
    conserv_words, liberal_words = retrieve_words(train_files)
    vocabulary = set(conserv_words + liberal_words)
    liberal_dict = dict()
    conserv_dict = dict()
    lib_counter = get_lib_counter(liberal_words)
    cons_counter = get_cons_counter(conserv_words)
    values = ["L", "C"]
    for val in values:
        if val == "L":
            for word in vocabulary:
                #print ("word :", word)
                num = float(lib_counter[word] + 1)
                denom = float(len(liberal_words) + len(vocabulary))
                #print "num :", num
                #print "denom :", denom
                posterior_prob_L = num / denom
                #print ("posterior_prob_L :", posterior_prob_L)
                liberal_dict[word] = posterior_prob_L
        if val == "C":
            for word in vocabulary:
                #print ("word :", word)
                num = float(cons_counter[word] + 1)
                denom = float(len(conserv_words) + len(vocabulary))
                #print "num :", num
                #print "denom :", denom
                posterior_prob_C = num / denom
                #print ("posterior_prob_C :", posterior_prob_C)
                conserv_dict[word] = posterior_prob_C
    # print top 20 liberal words
    count = 0
    for key, value in sorted(liberal_dict.iteritems(), key=lambda (k,v): (v,k),
                             reverse=True):
        if count >= 20: break
        print "%s %.04f" % (key, value)
        count += 1
    count = 0
    print " "
    # print top 20 conservative words
    for key, value in sorted(conserv_dict.iteritems(), key=lambda (k,v): (v,k),
                             reverse=True):
        if count >= 20: break
        print "%s %.04f" % (key, value)
        count += 1

    return None



if __name__ == "__main__":
    main()
