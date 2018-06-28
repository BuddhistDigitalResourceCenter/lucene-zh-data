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
    unihan = defaultdict(list)
    for line in f.read().strip().split('\n'):
        key, value = line.split('\t')
        unihan[key].append(value)

with open('variants/TSCharacters.txt', 'r') as f:
    opencc = defaultdict(list)
    for line in f.read().strip().split('\n'):
        key, value = line.split('\t')
        values = value.split(' ')
        for v in values:
            opencc[key].append(v)

with open('../output/tc2sc.tsv', 'w') as f:
    for k, v in opencc.items():
        if k not in unihan:
            for value in v:
                f.write('{}\t{}\n'.format(k, value))
        else:
            for value in v:
                if v not in unihan[k]:
                    f.write('{}\t{}\n'.format(k, value))

    for k, v in unihan.items():
        for value in v:
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
