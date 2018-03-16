# -*- coding: utf-8 -*-
import functools
import operator
import re
import os


def re_match_pinyin_line(kind):
    return re.compile(
        r'^U\+(?P<code>[0-9A-Z]+)\t{}\t(?P<pinyin>.+)$'.format(kind)
    )

PINYIN = r'[^\d\., ]+'
re_khanyupinyin = re.compile(r'''
    (?:\d{5}\.\d{2}0,)*\d{5}\.\d{2}0:
    ((?:%(pinyin)s,)*)
    (%(pinyin)s)
''' % ({'pinyin': PINYIN}), re.X)
re_kmandarin = re.compile(r'''
    ()()
    ({pinyin})
'''.format(pinyin=PINYIN), re.X)
re_kxhc1983 = re.compile(r'''
    ()()[0-9]{4}\.[0-9]{3}\*?
    (?:,[0-9]{4}\.[0-9]{3}\*?)*:
    (%(pinyin)s)
''' % ({'pinyin': PINYIN}), re.X)
re_khanyupinlu = re.compile(r'''
    ()()({pinyin})\([0-9]+\)
'''.format(pinyin=PINYIN), re.X)
re_kinds_map = {
    'kHanyuPinyin': re_khanyupinyin,
    'kMandarin': re_kmandarin,
    'kXHC1983': re_kxhc1983,
    'kHanyuPinlu': re_khanyupinlu,
}


def remove_dup_items(lst):
    new_list = []
    for item in lst:
        if item not in new_list:
            new_list.append(item)
    return new_list


def parse(lines, kind='kHanyuPinyin', ignore_prefix='#') -> str:
    re_line = re_match_pinyin_line(kind)
    re_pinyin = re_kinds_map[kind]
    for line in lines:
        line = line.strip()
        if line.startswith(ignore_prefix):
            continue
        match = re_line.match(line)
        if match is None:
            continue

        code = match.group('code')
        raw_pinyin = match.group('pinyin')
        raw_pinyins = re_pinyin.findall(raw_pinyin)
        # 处理有三个或三个以上拼音的情况，此时 raw_pinyins 类似
        # [(' xī,', 'lǔ '), (' lǔ,', 'xī')] or [('shú,dú,', 'tù')]
        for n, values in enumerate(raw_pinyins):
            value = []
            for v in values:
                value.extend(v.split(','))
            raw_pinyins[n] = value

        pinyins = functools.reduce(
            operator.add, raw_pinyins
        )
        pinyins = [x.strip() for x in pinyins if x.strip()]
        pinyins = remove_dup_items(pinyins)
        pinyin = ','.join(pinyins)
        yield code, pinyin


def save_data(pinyins, writer, pinyin_alphabet):

    for code, pinyin in pinyins:
        gl = {}
        exec('hanzi=chr(0x{})'.format(code), gl)
        hanzi = gl['hanzi']
        line = 'U+{code}: {pinyin}  # {hanzi}\n'.format(
            code=code, pinyin=pinyin, hanzi=hanzi
        )
        writer.write(line)

        equiv = {"ā": "a", "á": "a", "ǎ": "a", "à": "a",
         "ē": "e", "é": "e", "ě": "e", "è": "e",
         "ī": "i", "í": "i", "ǐ": "i", "ì": "i",
         "ō": "o", "ó": "o", "ǒ": "o", "ò": "o",
         "ū": "u", "ú": "u", "ǔ": "u", "ù": "u",
         "ǖ": "u", "ǘ": "u", "ǚ": "u", "ǜ": "u", "ü": "u"}

        for p in pinyin.split(','):
            vowels = re.sub(r'[bcdfghjklmnpqrstvwxyz]+', '', p).strip()
            if vowels and vowels not in 'ǹ̀ḿńň':
                simple = ''
                for v in vowels:
                    if v in equiv:
                        simple += equiv[v]
                    else:
                        simple += v
                if simple != vowels:
                    if simple not in pinyin_alphabet.keys():
                        pinyin_alphabet[simple] = {vowels: True}
                    else:
                        pinyin_alphabet[simple][vowels] = True


if __name__ == '__main__':
    pinyin_alphabet = {}

    out_path = 'pinyin'
    if not os.path.exists(out_path):
        os.makedirs(out_path)
    with open('Unihan_Readings.txt') as fp:
        for kind in ('kHanyuPinyin', 'kMandarin',
                     'kHanyuPinlu', 'kXHC1983'):
            fp.seek(0)
            with open('{}/{}.txt'.format(out_path, kind), 'w') as writer:
                pinyins = parse(fp.readlines(), kind=kind)
                save_data(pinyins, writer, pinyin_alphabet)

    with open('../output/pinyin_alphabet_expanded.txt', 'w') as f:
        with open('pinyin/pinyin_alphabet.dict', 'r') as g:
            for line in g.read().strip().split('\n'):
                f.write(line + '\n')
                for key in sorted(pinyin_alphabet.keys(), reverse=True):
                    if key in line:
                        for combination in pinyin_alphabet[key]:
                            f.write(line.replace(key, combination) + '\n')
                    continue

    with open('../output/pinyin-vowel-combinations.tsv', 'w') as f:
        for k, v in pinyin_alphabet.items():
            f.write('{}\t{}\n'.format(k, '\t'.join(sorted(list(set(v))))))
