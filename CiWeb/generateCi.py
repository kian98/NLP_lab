#!/usr/bin/python
# -*- coding: GB18030 -*-
import random


def read_in(file_path, read_type):
    with open(file_path, encoding='GB18030') as f:
        lines = f.readlines()
        if read_type == 'word_freq':
            word_dict = {}
            for line in lines:
                word, freq = line.strip().split(' ')
                word_dict[word] = int(freq)
            return word_dict
        elif read_type == 'tune_name':
            tune_name_list = []
            for line in lines:
                tune_name_list.append(line.strip())
            return tune_name_list
        elif read_type == 'format':
            format_dict = {}
            is_key = True
            value_count = 0
            for line in lines:
                if is_key:
                    key = line.strip()
                    format_dict[key] = []
                    is_key = False
                else:
                    if value_count == 0:
                        value_count = int(line.strip())
                        format_dict[key] = []
                        continue
                    fmt = line.strip().split(' ')
                    format_dict[key].append(fmt)
                    value_count -= 1
                    if value_count == 0:
                        is_key = True
            return format_dict


def generate_ci(ci_name):
    target_freq = 100
    one_word_source = read_in(r'.\sources\Ci_one_word.txt', 'word_freq')
    keys = list(one_word_source.keys())
    for w in keys:
        if one_word_source[w] < target_freq:
            del one_word_source[w]
    two_word_source = read_in(r'.\sources\Ci_two_word.txt', 'word_freq')
    keys = list(two_word_source.keys())
    for w in keys:
        if two_word_source[w] < target_freq:
            del two_word_source[w]
    choose_dict = [one_word_source, two_word_source]

    # tune_name_source = read_in('..\\Tune_name.txt', 'tune_name')
    ci_format_source = read_in(r'.\sources\Ci_format.txt', 'format')
    if ci_name == "" or ci_name == "默认随机生成":
        ci_name = random.choice(list(ci_format_source))
    elif ci_name not in ci_format_source:
        return "(******换一个词牌名试试*******)"
    title_format = random.choice(ci_format_source[ci_name])
    ci_output = ""
    for prompt in title_format:
        if prompt.isdigit():
            prompt = int(prompt)
            length = 0
            while prompt > length:
                num = random.randint(0, 1)
                x = random.choice(list(choose_dict[num]))
                if len(x) + length > prompt or x == "□" or x == "□□":
                    continue
                ci_output += x
                length += len(x)
        else:
            new_line = "\n" if prompt == "。" else ""
            ci_output += prompt + new_line
    return "《" + ci_name + "》 \n" + ci_output


def random_name():
    ci_format_source = read_in('.\sources\Ci_format.txt', 'format')
    return random.choice(list(ci_format_source))