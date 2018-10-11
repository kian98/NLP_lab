#!/usr/bin/python
# -*- coding: GB18030 -*-
import re
import math


def is_chinese(chars):
    for ch in chars:
        if ch < u'\u4e00' or ch > u'\u9fa5':
            return False
    return True


def rid_non_ch(chars):
    result = ''
    for c in chars:
        if not is_chinese(c):
            continue
        else:
            result += c
    return result


def cut_sentence(s):
    cut_result = []
    piece = ''
    is_cur_chinese = is_chinese(s[0])
    for w in s:
        if not is_chinese(w):
            if piece != '' and is_cur_chinese:
                cut_result.append(piece)
                piece = ''
        else:
            if piece != '' and not is_cur_chinese:
                cut_result.append(piece)
                piece = ''
        is_cur_chinese = is_chinese(w)
        piece += w
    if piece != '':
        cut_result.append(piece)
    return cut_result


def get_words_classified(wdict):
    max_length = 0
    for w in wdict:
        if len(w) > max_length:
            max_length = len(w)
    classify_list = []
    while max_length > 0:
        classify_list.append([])
        max_length -= 1
    for w in wdict:
        classify_list[len(w) - 1].append(w)
    return classify_list


def forward_match(texts, word_list):
    match_result = []
    for text in texts:
        if not is_chinese(text):
            match_result.append(text)
            continue
        s_length = len(text)
        s_left = s_length
        span = len(word_list)
        index = 0
        while index < s_length:
            search_span = span if span < s_left else s_length - index
            has_added = False
            while search_span > 0 and not has_added:
                s_part = text[index:(index + search_span)]
                if s_part in word_list[search_span - 1]:
                    match_result.append(s_part)
                    has_added = True
                    index += search_span
                    s_left -= len(s_part)
                else:
                    search_span -= 1
            if not has_added:
                match_result.append(text[index])
                index += 1
                s_left -= 1
    return match_result


def backward_match(texts, word_list):
    match_result = []
    for text in texts:
        if not is_chinese(text):
            match_result.append(text)
            continue
        temp_list = []
        s_length = len(text)
        s_left = s_length
        span = len(word_list)
        index = s_length - 1
        while index >= 0:
            search_span = span if span < s_left else index + 1
            has_added = False
            while search_span > 0 and not has_added:
                s_part = text[(index - search_span + 1):(index + 1)]
                if s_part in word_list[search_span - 1]:
                    temp_list.append(s_part)
                    has_added = True
                    index -= search_span
                    s_left -= len(s_part)
                else:
                    search_span -= 1
            if not has_added:
                temp_list.append(text[index])
                index -= 1
                s_left -= 1
        temp_list.reverse()
        match_result.extend(temp_list)
    return match_result


def calProb(sentence, prob):
    sentence.insert(0, '<BOS>')
    sentence.append('<EOS>')
    p = 0
    mol, der, v_list = [], [], []
    flag = False
    for index in range(len(sentence) - 1):
        if not is_chinese(sentence[index]) and (sentence[index] != '<EOS>' or '<BOS>'):
            index += 1
            continue
        link_word = sentence[index] + '-' + sentence[index + 1]
        if sentence[index] not in v_list:
            v_list.append(sentence[index])
        if link_word not in prob:
            mol.append(1.0)
            if sentence[index] not in prob:
                der.append(0.0)
            else:
                der.append(float(prob[sentence[index]][1]))
            flag = True
        else:
            mol.append(float(prob[link_word][0]))
            der.append(float(prob[link_word][1]))
    v_num = len(v_list)
    for index in range(len(mol)):
        p = p + math.log((mol[index] + 1) / (der[index] + v_num)) if flag else p + math.log(mol[index] / der[index])
    return p


def get_part(sentence_list, index):
    has_started = False
    has_ended = False
    start, end = -1, -1
    while index < len(sentence_list) - 1 and not has_ended:
        if not has_started and is_chinese(sentence_list[index]):
            has_started = True
            start = index
            index += 1
        elif has_started and not is_chinese(sentence_list[index]):
            has_ended = True
            end = index
        else:
            index += 1
    if not has_ended and start > 0:
        end = len(sentence_list) - 1
    return start, end, index


def polish_result(forward, backward, prob):
    f_index, b_index = 0, 0
    final_result = []
    if not is_chinese(forward[1]):
        final_result.append(forward[0])
    while f_index < len(forward) - 1 and b_index < len(backward) - 1:
        f_start, f_end, f_index = get_part(forward, f_index)
        b_start, b_end, b_index = get_part(backward, b_index)
        if calProb(forward[f_start:f_end], prob) > calProb(backward[b_start:b_end], prob):
            final_result.extend(forward[f_start:f_end + 1])
            # print('f' + ' ')
            # print(forward[f_start:f_end + 1])
        else:
            final_result.extend(backward[b_start:b_end + 1])
    return final_result


def get_sentence_spilt(input_text):
    word_dict = {}
    with open(r'.\sources\1998-01-2003版-带音.txt') as material:
        lines = material.readlines()
        for line in lines:
            line_cut = line.strip().split('  ')
            line_cut.pop(0)
            for wnp in line_cut:
                pair = wnp.split('/')
                re.sub(r'\{.*?\}', '', pair[0])
                ch, part = pair[0], pair[1]
                ch = rid_non_ch(ch)
                if ch == '' or part[0] == 'w':
                    continue
                if ch in word_dict:
                    word_dict[ch] += 1
                else:
                    word_dict[ch] = 1
    material.close()

    query_list = get_words_classified(word_dict)

    # '''保存查询文件'''
    # with open(r'..\query_list.txt', 'w') as query_file:
    #     i = 1
    #     for l in query_list:
    #         query_file.write(str(i) + ':\n')
    #         i += 1
    #         for c in l:
    #             query_file.write(c + ' ')
    #         query_file.write('\n')
    # query_file.close()

    spilt_text = cut_sentence(input_text)

    forward_match_result = forward_match(spilt_text, query_list)
    backward_match_result = backward_match(spilt_text, query_list)

    bigram_prob = {}
    with open(r'.\sources\bigram_prob.txt') as prob_file:
        content = prob_file.readline().split(' ')
        content.remove('')
        i = 0
        while i < len(content):
            bigram_prob[content[i]] = [float(content[i + 1]), float(content[i + 2])]
            i += 3
    prob_file.close()

    return polish_result(forward_match_result, backward_match_result, bigram_prob)
