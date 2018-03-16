# -*- coding: utf-8 -*-
import collections


def code_to_hanzi(code):
    hanzi = chr(int(code.replace('U+', '0x'), 16))
    return hanzi


def sort_pinyin_dict(pinyin_dict):
    return collections.OrderedDict(
        sorted(pinyin_dict.items(),
               key=lambda item: int(item[0].replace('U+', '0x'), 16))
    )


def remove_dup_items(lst):
    new_lst = []
    for item in lst:
        if item not in new_lst:
            new_lst.append(item)
    return new_lst


def parse_pinyins(fp):
    pinyin_map = {}
    for line in fp:
        line = line.strip()
        if line.startswith('#') or not line:
            continue
        code, pinyin = line.split('#')[0].split(':')
        pinyin = ','.join([x.strip() for x in pinyin.split() if x.strip()])
        pinyin_map[code.strip()] = pinyin.split(',')
    return pinyin_map


def merge(raw_pinyin_map, adjust_pinyin_map, overwrite_pinyin_map):
    new_pinyin_map = {}
    for code, pinyins in raw_pinyin_map.items():
        if code in overwrite_pinyin_map:
            pinyins = overwrite_pinyin_map[code]
        elif code in adjust_pinyin_map:
            pinyins = adjust_pinyin_map[code] + pinyins
        new_pinyin_map[code] = remove_dup_items(pinyins)

    return new_pinyin_map


def save_data(pinyin_map, writer):
    """
    Only keeps the first pinyin in case there are more than one possibility
    """
    for code, pinyins in pinyin_map.items():
        hanzi = code_to_hanzi(code)
        line = '{hanzi}\t{pinyin}\n'.format(
            pinyin=pinyins[0], hanzi=hanzi
        )
        writer.write(line)


def extend_pinyins(old_map, new_map, only_no_exists=False):
    for code, pinyins in new_map.items():
        if only_no_exists:   # 只当 code 不存在时才更新
            if code not in old_map:
                old_map[code] = pinyins
        else:
            old_map.setdefault(code, []).extend(pinyins)


if __name__ == '__main__':
    raw_pinyin_map = {}
    with open('pinyin/kMandarin.txt') as fp:
        mandarin = parse_pinyins(fp)
        raw_pinyin_map.update(mandarin)
    with open('pinyin/kHanyuPinyin.txt') as fp:
        khanyupinyin = parse_pinyins(fp)
        extend_pinyins(raw_pinyin_map, khanyupinyin, only_no_exists=True)
    with open('pinyin/kXHC1983.txt') as fp:
        kxhc1983 = parse_pinyins(fp)
        extend_pinyins(raw_pinyin_map, kxhc1983, only_no_exists=True)
    with open('pinyin/kHanyuPinlu.txt') as fp:
        khanyupinyinlu = parse_pinyins(fp)
        # 之所以只增加不存在的拼音数据而不更新已有的数据
        # 是因为 kHanyuPinlu 的拼音数据中存在一部分不需要的轻声拼音
        # 以及部分音调标错了位置，比如把 ``ǒu`` 标成了 ``oǔ``

        # Google Translated:
        # The only increase does not exist pinyin data without updating the existing data
        # Is because kHanyuPinlu pinyin data there is some unwanted soft pinyin
        # And some of the tone of the wrong place, such as the ``ǒu`` labeled ``oǔ``

        extend_pinyins(raw_pinyin_map, khanyupinyinlu, only_no_exists=True)

    with open('../output/pinyin.tsv', 'w') as fp:
        save_data(raw_pinyin_map, fp)

