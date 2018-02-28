# -*- coding: utf-8 -*-
import functools
import operator
import re
import os


def re_match_numeric_line(kind):
    return re.compile(
        r'^U\+(?P<orig>[0-9A-Z]+)\t{}\t(?P<number>.+)$'.format(kind)
    )


re_accountingnumeric = re.compile(r'''
    ()
    (?P<number>[0-9]+)
''', re.X)
re_semanticvariant = re.compile(r'''
    ()
    (?:U\+(?P<number>[0-9A-Z]+)<?(?:[^ ]*,?)*)
''', re.X)
re_kinds_map = {
    'kAccountingNumeric': re_accountingnumeric,
    'kPrimaryNumeric': re_accountingnumeric,
    'kOtherNumeric': re_accountingnumeric
}


def remove_dup_items(lst):
    new_list = []
    for item in lst:
        if item not in new_list:
            new_list.append(item)
    return new_list


def parse(lines, kind, ignore_prefix='#') -> str:
    re_line = re_match_numeric_line(kind)
    re_number = re_kinds_map[kind]
    for line in lines:
        line = line.strip()
        if line.startswith(ignore_prefix):
            continue
        match = re_line.match(line)
        if match is None:
            continue
        orig = match.group('orig')
        raw_numbers = match.group('number')
        raw_numbers = re_number.findall(raw_numbers)
        # 处理有三个或三个以上拼音的情况，此时 raw_pinyins 类似
        # [(' xī,', 'lǔ '), (' lǔ,', 'xī')] or [('shú,dú,', 'tù')]
        for n, values in enumerate(raw_numbers):
            value = []
            for v in values:
                value.extend(v.split(','))
            raw_numbers[n] = value

        numbers = functools.reduce(
            operator.add, raw_numbers
        )
        numbers = [x.strip() for x in numbers if x.strip()]
        numbers = remove_dup_items(numbers)
        yield orig, numbers


def save_data(parsed, writer):
    """
    does not include the same character if it can be simplified to itself,
    to reproduce the same behaviour as OpenCC.
    in case multiple mappings, take the first one (still as OpenCC)
    """
    for orig, numbers in parsed:
        gl = {}
        exec('hanzi=chr(0x{})'.format(orig), gl)
        hanzi_orig = gl['hanzi']

        line = '{hanzi}\t{number}\n'.format(
            hanzi=hanzi_orig, number=numbers[0]
        )
        writer.write(line)


if __name__ == '__main__':
    out_path = 'numerics'
    if not os.path.exists(out_path):
        os.makedirs(out_path)
    with open('Unihan_NumericValues.txt') as fp:
        for kind in ('kAccountingNumeric', 'kPrimaryNumeric',
                     'kOtherNumeric'):
            fp.seek(0)
            with open('{}/{}.txt'.format(out_path, kind), 'w') as writer:
                pinyins = parse(fp.readlines(), kind=kind)
                save_data(pinyins, writer)
