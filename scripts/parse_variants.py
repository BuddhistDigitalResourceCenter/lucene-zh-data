# -*- coding: utf-8 -*-
import functools
import operator
import re
import os


def re_match_variant_line(kind):
    return re.compile(
        r'^U\+(?P<orig>[0-9A-Z]+)\t{}\t(?P<variant>.+)$'.format(kind)
    )


re_simplifiedvariant = re.compile(r'''
    ()
    U\+([0-9A-Z]+)
''', re.X)
re_semanticvariant = re.compile(r'''
    ()
    (?:U\+(?P<variant>[0-9A-Z]+)<?(?:[^ ]*,?)*)
''', re.X)
re_kinds_map = {
    'kSimplifiedVariant': re_simplifiedvariant,
    'kSemanticVariant': re_semanticvariant,
    'kZVariant': re_semanticvariant
}


def remove_dup_items(lst):
    new_list = []
    for item in lst:
        if item not in new_list:
            new_list.append(item)
    return new_list


def parse(lines, kind, ignore_prefix='#') -> str:
    re_line = re_match_variant_line(kind)
    re_variant = re_kinds_map[kind]
    for line in lines:
        line = line.strip()
        if line.startswith(ignore_prefix):
            continue
        match = re_line.match(line)
        if match is None:
            continue
        orig = match.group('orig')
        raw_variants = match.group('variant')
        raw_variants = re_variant.findall(raw_variants)
        # 处理有三个或三个以上拼音的情况，此时 raw_pinyins 类似
        # [(' xī,', 'lǔ '), (' lǔ,', 'xī')] or [('shú,dú,', 'tù')]
        for n, values in enumerate(raw_variants):
            value = []
            for v in values:
                value.extend(v.split(','))
            raw_variants[n] = value

        variants = functools.reduce(
            operator.add, raw_variants
        )
        variants = [x.strip() for x in variants if x.strip()]
        variants = remove_dup_items(variants)
        yield orig, variants


def save_data(parsed, writer):
    """
    does not include the same character if it can be simplified to itself,
    to reproduce the same behaviour as OpenCC.
    in case multiple mappings, take the first one (still as OpenCC)
    """
    for orig, variants in parsed:
        gl = {}
        exec('hanzi=chr(0x{})'.format(orig), gl)
        hanzi_orig = gl['hanzi']

        hanzi_variants = []
        for v in variants:
            lg = {}
            exec('hanzi=chr(0x{})'.format(v), lg)
            hanzi_variant = lg['hanzi']
            if hanzi_variant != hanzi_orig:
                hanzi_variants.append('{variant}'.format(variant=hanzi_variant))

        if hanzi_variants:
            line = '{hanzi}\t{variant}\n'.format(
                hanzi=hanzi_orig, variant=hanzi_variants[0]
            )
            writer.write(line)


if __name__ == '__main__':
    out_path = 'variants'
    if not os.path.exists(out_path):
        os.makedirs(out_path)
    with open('Unihan_Variants.txt') as fp:
        for kind in ('kSimplifiedVariant', 'kSemanticVariant',
                     'kZVariant'):
            fp.seek(0)
            with open('{}/{}.txt'.format(out_path, kind), 'w') as writer:
                pinyins = parse(fp.readlines(), kind=kind)
                save_data(pinyins, writer)
