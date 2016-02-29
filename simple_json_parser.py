#!/usr/bin/python2.7

import ijson
import nltk.data
import HTMLParser
import re


class HnParser():
    def __init__(self):
        self.json_filename = '/opt/projects/domain_nlp/hackernews.json'
        self.parser = HTMLParser.HTMLParser()
        self.tokenizer = nltk.data.load('tokenizers/punkt/english.pickle') 

    def collect_data(self):
        outfile = open('/opt/projects/domain_nlp/sentences','w+', buffering=False)
        story_title=None
        parsed = ijson.parse(open(self.json_filename),buf_size=1024)
        comments = []
        line = 0
        while True:
            key,val = parsed.next()
            if not key and not val:
                break
        
            line+=1
        
            if key == 'map_key': 
                next_key,next_val = parsed.next()
                line+=1
        
                if val == 'points':
                    points = next_val
                    if points < 1:
                        continue
                elif val == 'story_title':
                    story_title = next_val
        
                elif val == 'comment_text' and next_val: 
                    comment_text = self.sanitize_text(next_val, story_title)
                    outfile.writelines(comment_text)
                    
        #            comments.append({'comment':comment_text,'points':points,
        #                             'story_title':story_title})
        
            if line % 100000 == 0:
                print len(comments)
    
        return comments
    
    def sanitize_text(self, comment_text, story_title):
        #comment_text = str(comment_text)
        if story_title:
            comment_text = story_title + comment_text + ". "
        comment_text = comment_text.replace('<p>','\n')
        comment_text = self.parser.unescape(comment_text)
        comment_text = self.tokenizer.sentences_from_text(comment_text)
        comment_text = [ re.sub("[^a-zA-Z'\ ]",'', sentence) for sentence in comment_text ]
        comment_text = [ sentence + '\n' for sentence in comment_text ]
        #comment_text = [ sentence.split(' ') for sentence in comment_text ]

        return comment_text

hp = HnParser()        
data = hp.collect_data()
tokenizer = nltk.data.load('tokenizers/punkt/english.pickle') 

for comment in data:
    comment_text = comment['comment'] 
    for i in comment_text:
        print i
