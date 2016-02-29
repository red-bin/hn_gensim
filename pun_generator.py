#!/usr/bin/python2.7

import re
from collections import defaultdict
import dictionary

#Setting to UTF8 because of syl_rep_file
import sys
reload(sys)  # Reload does the trick!
sys.setdefaultencoding('UTF8')

print 'starting'
def create_syllables_dict():
    syl_sep_file = '/opt/projects/domain_nlp/mhyph.txt'

    syl_sep_delim= '\xa5' 
    pronounce_delim = ''
    
    syllable_dict = {}
    
    for line in open(syl_sep_file, 'r'):
     
        syllables  = [ syl.replace('\r\n','').lower() for syl in re.split(syl_sep_delim,line) ]
        word = ''.join(syllables)
        
        syllable_dict[word] = syllables

    return syllable_dict

def create_pronounce_dict():
    pronounce_file = '/opt/projects/domain_nlp/cmudict.rep'
    pronounce_dict = {}
    
    for line in open(pronounce_file, 'r'):
        line = line.strip().lower()
        if not line:
            continue

        word,pronounce = line.split('  ')

        if word not in pronounce_dict:
            pronounce_dict[word] = []
        else:
            continue

        sylables = pronounce.split('-')
        phonetics = [ phon.split(' ') for phon in [ syl.strip() for syl in sylables ]]
        #print word,phonetics

        pronounce_dict[word] = phonetics
        #print word,pronounce_dict[word]
 
    return pronounce_dict           

def words_by_syl_count(count, syllable_dict):
    ret_dict = defaultdict(list,[ (word, syllables) 
        for word,syllables in syllable_dict.items()
        if len(syllables) >= count ])
        
#    print ret_dict
    return ret_dict

def get_syl_at_pos(words, pronounces,pos):
    ret = []
    for word,values in words.items():
    #    print "word %s" % (word)
        if word in pronounces:
            if len(pronounces[word]) < 3:
                continue
            phonetic = pronounces[word][pos]
            syllable = words[word][pos]
            yield (word,syllable,phonetic)
        #except:
        #    continue

print "Creating syllable dict.."
syllable_dict = create_syllables_dict()
print "Creating pronounce dict.."
pronounces = create_pronounce_dict()
print "Creating word_twosyls"
words = words_by_syl_count(2, syllable_dict)

first_syls = get_syl_at_pos(words, pronounces, 0)
last_syls = get_syl_at_pos(words, pronounces, -1)
for word,syl,pron in first_syls:
    if re.search('^cha',syl[0]) :
        print syl,pron

#for word,syl,pron in last_syls:
#    if re.search('^[ai]y',pron[-1]) :
#        print syl,pron
#FOR TOMORROW: Make dictionaries of syllables/pronunciations by word. less memory and a lot quicker.

print "Creating first syllable list"
#first_prons = [ (syl[2],syl[1]) for syl in first_syls ]
print "Creating second syllable list"
#last_prons =  [ (syl[2],syl[1]) for syl in last_syls ]

#print first_syls_list
#print last_syls_list

print "Finding uniques"
unique_words = set([])
for top_syl,top_pronounce in first_syls_list:
    for bot_syl,bot_pronounce in last_syls_list:
        combined = "%s%s" % (top_syl,bot_syl)

        if d.isInDictionary(combined):
            if combined not in unique_words:
                print top_syl,bot_syl,combined
            unique_words.add(combined)
    

combined=''
if d.isInDictionary(combined):
    print combined
