from collections import defaultdict

def parse_variants(lines):
    syns = {}
    for line in lines:
        v1, v2 = line.split('\t')
        if v1 in syns.keys():
            syns[v1].append(v2)
        elif v2 in syns.keys():
            syns[v2].append(v1)
        else:
            syns[v1] = [v2]

    output = []
    for word, synonyms in syns.items():
        for syn in sorted(set(synonyms)):
            if syn != word:
                entry = '{}\t{}'.format(syn, word)
                if entry not in output:
                    output.append(entry)

    return output


with open('variants/kSimplifiedVariant.txt', 'r') as f:
    unihansv = defaultdict(list)
    for line in f.read().strip().split('\n'):
        key, value = line.split('\t')
        unihansv[key].append(value)

with open('variants/kTraditionalVariant.txt', 'r') as f:
    unihantv = defaultdict(list)
    for line in f.read().strip().split('\n'):
        key, value = line.split('\t')
        unihantv[key].append(value)

with open('variants/TSCharacters.txt', 'r') as f:
    openccts = defaultdict(list)
    for line in f.read().strip().split('\n'):
        key, value = line.split('\t')
        values = value.split(' ')
        for v in values:
            openccts[key].append(v)

with open('variants/STCharacters.txt', 'r') as f:
    openccst = defaultdict(list)
    for line in f.read().strip().split('\n'):
        key, value = line.split('\t')
        values = value.split(' ')
        for v in values:
            openccst[key].append(v)

with open('../output/tc2sc.tsv', 'w') as f:
    for k, v in openccts.items():
        if k not in unihansv:
            for value in v:
                if value != k:
                    f.write('{}\t{}\n'.format(k, value))
        else:
            for value in v:
                if value not in unihansv[k] and value != k:
                    f.write('{}\t{}\n'.format(k, value))

    for k, v in unihansv.items():
        for value in v:
            if value != k:
                f.write('{}\t{}\n'.format(k, value))

with open('../output/sc2tc.tsv', 'w') as f:
    for k, v in openccst.items():
        if k not in unihantv:
            for value in v:
                if value != k:
                    f.write('{}\t{}\n'.format(k, value))
        else:
            for value in v:
                if value not in unihantv[k] and value != k:
                    f.write('{}\t{}\n'.format(k, value))

    for k, v in unihantv.items():
        for value in v:
            if value != k:
                f.write('{}\t{}\n'.format(k, value))

# copy the content as-is
with open('variants/kZVariant.txt', 'r') as f:
    with open('../output/zh-alternatives.tsv', 'w') as g:
        lines = f.read().strip().split('\n')
        variants = parse_variants(lines)
        g.write('\n'.join(variants))

with open('variants/kSemanticVariant.txt', 'r') as f:
    with open('../output/zh-synonyms.tsv', 'w') as g:
        lines = f.read().strip().split('\n')
        synonyms = parse_variants(lines)
        g.write('\n'.join(synonyms))
