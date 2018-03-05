import re


def parse_by_codepoints():
    files = ['Unihan_DictionaryIndices.txt', 'Unihan_DictionaryLikeData.txt', 'Unihan_IRGSources.txt',
             'Unihan_NumericValues.txt', 'Unihan_OtherMappings.txt', 'Unihan_RadicalStrokeCounts.txt',
             'Unihan_Readings.txt', 'Unihan_Variants.txt']
    ideograms = {}
    codepoints = {}
    for f in files:
        with open(f, 'r') as g:
            content = g.read().strip().split('\n')
            for line in content:
                if line.startswith('U+'):
                    parts = line.split('\t')
                    codepoint = parts[0]
                    entry = parts[1]
                    if codepoint in codepoints:
                        codepoints[codepoint].append(entry)
                    else:
                        codepoints[codepoint] = [entry]

                    referenced_codepoints = re.findall(r'U\+[0-9A-Z]{4}', line)
                    for c in referenced_codepoints:
                        ideograms[c] = True

    return codepoints


def count_TC_SC(unihan):
    A, B, C, D = 0, 0, 0, 0
    for codepoint, entries in unihan.items():
        trad = False
        simp = False
        for e in entries:
            # if can be simplified
            if 'SimplifiedVariant' in e:
                trad = True
            # if can be traditionalized
            elif 'TraditionalVariant' in e:
                simp = True

        if not trad and not simp:
            A += 1
        elif simp and not trad:
            B += 1
        elif not simp and trad:
            C += 1
        elif trad and simp:
            D += 1

    return A, B, C, D


def count_PY(unihan):
    pinyin_count = 0
    for codepoint, entries in unihan.items():
        for e in entries:
            if 'Hanyu' in e or 'Mandarin' in e or 'YHC1983' in e:
                pinyin_count += 1

    return pinyin_count


def count_pinyin():
    lazy_dict = {"ā": "a", "á": "a", "ǎ": "a", "à": "a",
            "ē": "e", "é": "e", "ě": "e", "è": "e",
            "ǖ": "u", "ǘ": "u", "ǚ": "u", "ǜ": "u"}

    PY_types = {}
    PY_lazy_types = {}
    pinyin_files = ['kHanyuPinlu.txt', 'kHanyuPinyin.txt', 'kMandarin.txt', 'kXHC1983.txt']
    for p in pinyin_files:
        with open('{}/{}'.format('pinyin', p), 'r') as f:
            content = f.read().strip().split('\n')
            for line in content:
                pinyins = line[7:].split('  #')[0].split(',')
                for i in pinyins:
                    lazy = ''
                    for char in i:
                        if char in lazy_dict.keys():
                            lazy += lazy_dict[char]
                        else:
                            lazy += char

                    PY_types[i] = True
                    PY_lazy_types[lazy] = True
    return len(PY_types), len(PY_lazy_types)


unihan = parse_by_codepoints()
print('total unihan', len(unihan))

neutral, SC, TC, both = count_TC_SC(unihan)
print('neutral {}\nTC only {}\nSC only {}\nTC and SC{}'.format(neutral, TC, SC, both))

types, lazy_types = count_pinyin()
print('PY {}\nPY lazy {}'.format(types, lazy_types))
