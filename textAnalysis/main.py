'''
Created on 2018-04-28

@author: Administrator
'''

import os
from dictionary.dict_utils import load_dict_by_type
#from dictionary.dict_utils import load_extreme_dict
from dictionary.dict_utils import load_extent_dict
from segementation_utils import get_simple_sentences_gen
from segementation_utils import get_jieba_word_list
from functools import reduce
import sys

word_dict = {}
extreme_dict = {}
deny_word_set = set()
extent_dict = {}
sense_word_kind_set = {"a", "ad", "an", "ag", "al", "d", "dg","n","l",'v','m','z','i','zg','nr'}


def __init_dict__(dict_type):
    os.chdir(sys.path[0]);
#    global word_dict
    word_dict.update(load_dict_by_type(dict_type))
#    extreme_dict = load_extreme_dict()
#    global extent_dict
    extent_dict.update(load_extent_dict())

def __init_deny_word_set__():
    os.chdir(sys.path[0]);
    deny_word_file_path = os.path.abspath('dictionary/data/dict_common/reversed.txt')
    with open(deny_word_file_path, encoding="utf-8") as f:
        for items in f:
            item = items.strip()
            deny_word_set.add(item)

def __fill_with_word_info__(word, k, s, p = None):
    word_info = {};
    word_info['n'] = word                   #word
    word_info['k'] = k                      #kind
    word_info['s'] = s                      #score
    word_info['p'] = p                      #property
    return word_info

def __getScore__(dict, word):
    return dict.get(word, 0)
            
def __get_word_detail_info__(word, word_kind):
    word_info = {};
    if word in deny_word_set:
        word_info = __fill_with_word_info__(word, 'deny', None, None)
    elif word_kind in sense_word_kind_set:
        score = __getScore__(extent_dict, word)
        if score != 0:
            word_info = __fill_with_word_info__(word, word_kind, score, None)
        else:
            score = __getScore__(word_dict, word)
            if score >0:
                word_info = __fill_with_word_info__(word, word_kind, score, 'pos')
            elif score < 0:
                word_info = __fill_with_word_info__(word, word_kind, score, 'neg')
            else:
                word_info = __fill_with_word_info__(word, word_kind, score)
    else:
        word_info = __fill_with_word_info__(word, word_kind, 0)
        
    return word_info

def __caculate_score_of_simple_sentence__(stack = [], ExtInNoAndSen = False):
    if ExtInNoAndSen:
        return reduce(lambda item1, item2: item1 * item2, stack) * -0.5
    else:
        return reduce(lambda item1, item2: item1 * item2, stack)
    
def get_simple_sentence_score(word_list=[{}]):
    if len(word_list) > 0:
        stack = []
        copystack = []
        GroupScore = 0
        NoWordFirst = False
        HaveSenWord = False
        ExtInNoAndSen = False
        if word_list[0].get("k") == 'no':
            NoWordFirst = True
            copystack.append('no')

        for item in word_list:
            if item.get('p') == 'pos' or item.get('p') == 'neg':
                HaveSenWord = True
                stack.append(item.get('s'))
            elif item.get('p') == 'ext':
                stack.append(item.get('s'))
                if NoWordFirst == True and HaveSenWord == False:
                    ExtInNoAndSen = True
            elif item.get('k') == 'c':
                pass
            elif item.get('k') == 'no':
                stack.append(-1)
        copystack.append(stack)
        if HaveSenWord:
            GroupScore = __caculate_score_of_simple_sentence__(stack, ExtInNoAndSen)
        return GroupScore, copystack
    return 0, None

if __name__ == '__main__':
    text_doc = sys.argv[1]
    dict_type = int(sys.argv[2])
    __init_dict__(dict_type)
    simple_sentences_gen = get_simple_sentences_gen(text_doc)
    _score_sum_ = 0;
    for simple_sentence in simple_sentences_gen:
        jieba_word_list = get_jieba_word_list(simple_sentence)
        word_info_list = []
        for word, kind in jieba_word_list:
            word_info = __get_word_detail_info__(word, kind)
            word_info_list.append(word_info)
            
        score, stack = get_simple_sentence_score(word_info_list)
        _score_sum_ += score
    
    coding_type = sys.getfilesystemencoding()
#    print(text_doc)
    print('sentence score is: '+str(_score_sum_))
        
    
    
    