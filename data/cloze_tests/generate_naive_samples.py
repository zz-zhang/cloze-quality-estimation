import nltk
import json
from nltk import pos_tag
import os
from collections import defaultdict
import re
from tqdm import tqdm
from random import sample, shuffle
import sys

dictionary_path = '/Users/zz_zhang/Desktop/cloze annotation/mturk/samples/dict.json'
cloth_path = '/Users/zz_zhang/Desktop/cloze annotation/mturk/samples/cloth'
out_path = '/Users/zz_zhang/Desktop/cloze annotation/mturk/samples'

def clean_passage(article):
    multi_space = r'(\s)+'
    start_wi_space = r'^\s+'
    end_wi_space = r'\s+$'

    article = re.sub(multi_space, ' ', article)
    article = re.sub(start_wi_space, '', article)
    article = re.sub(end_wi_space, '', article)

    return article

def cloze2passage(cloze):
    article = cloze['article'].replace('\n', '')
    answers = [opt[ord(ans) - ord('A')] for opt, ans in zip(cloze['options'], cloze['answers'])]
    tokens = article.split(' ')

    blank_count = 0
    for idx, token in enumerate(tokens):
        if token == '_':
            tokens[idx] = answers[blank_count]
            blank_count += 1
    article = ' '.join(tokens)
    article = clean_passage(article)
    return article

def fill_passage(cloze):
    blank_idx = 0
    blank_indcis = []
    answers = [opt[ord(ans) - ord('A')] for opt, ans in zip(cloze['options'], cloze['answers'])]
    tokens = clean_passage(cloze['article']).split(' ')
    for token_idx, token in enumerate(tokens):
        if token == '_':
            tokens[token_idx] = answers[blank_idx]
            blank_indcis.append(token_idx)
            blank_idx += 1
    return tokens, blank_indcis

def build_dictionary(cloth_path):
    print("Building Dictionary")
    res = defaultdict(set)
    for name in tqdm(os.listdir(cloth_path)):
        cloze = json.load(open(os.path.join(cloth_path, name)))
        article, _ = fill_passage(cloze)
        tags = pos_tag(article)
        for word, tag in tags:
            res[tag].add(word)
    for tag in res.keys():
        res[tag] = list(res[tag])
    json.dump(res, open(dictionary_path, 'w'))
    return res

def load_dictionary(path):
    if os.path.isfile(path):
        print("Dictionary Loaded.")
        return json.load(open(path))
    else:
        print("Dictionary Loaded.")
        return build_dictionary(cloth_path)

def build_new_cloze(article, answers, distractors, source, split):
    cloze = {}
    cloze['article'] = article
    cloze['source'] = f'{split}_{source}'
    cloze['options'] = []
    cloze['answers'] = []
    # print(answers, distractors)
    for ans, dis in zip(answers, distractors):
        options = [ans] + dis
        shuffle(options)
        ans_idx = chr(options.index(ans) + ord('A'))
        cloze['options'].append(options)
        cloze['answers'].append(ans_idx)
    return cloze

def build_cbt(cloth_path, out_path, dic, split='cbt'):
    print('Building CBT cloze tests.')
    succ_counter = 0
    for name in tqdm(os.listdir(cloth_path)):
        cloze = json.load(open(os.path.join(cloth_path, name)))
        if len(cloze['answers']) != 20:
            continue
        article, blank_indices = fill_passage(cloze)
        answers = [article[idx] for idx in blank_indices]
        tags = pos_tag(article)
        required_tags = [tags[idx][1] for idx in blank_indices]
        distractors = [sample(dic[tag], 3) if len(dic[tag]) >= 3 else sample(dic[tag] + dic[tag] + dic[tag], 3) for tag in required_tags]
        new_cloze = build_new_cloze(cloze['article'], answers, distractors, cloze['source'], split)

        json.dump(new_cloze, open(os.path.join(out_path, split, f'cbt_{name}'), 'w'))
        succ_counter += 1
    print(f'CBT cloze tests built, total number: {succ_counter}')

def build_random(cloth_path, out_path, dic, split='random'):
    print('Building random cloze tests.')
    flatten_dic = [word for wordlist in dic.values() for word in wordlist]
    succ_counter = 0
    for name in tqdm(os.listdir(cloth_path)):
        cloze = json.load(open(os.path.join(cloth_path, name)))
        if len(cloze['answers']) != 20:
            continue
        article, blank_indices = fill_passage(cloze)
        answers = [article[idx] for idx in blank_indices]
        distractors = [sample(flatten_dic, 3) for _ in answers]
        new_cloze = build_new_cloze(cloze['article'], answers, distractors, cloze['source'], split)

        json.dump(new_cloze, open(os.path.join(out_path, split, f'random_{name}'), 'w'))
        succ_counter += 1
    print(f'Random cloze tests built, total number: {succ_counter}')

if __name__ == '__main__':
    dic = load_dictionary(dictionary_path)

    if 'cbt' in sys.argv:
        build_cbt(cloth_path, out_path, dic, 'cbt')
    if 'random' in sys.argv:
        build_random(cloth_path, out_path, dic, 'random')
