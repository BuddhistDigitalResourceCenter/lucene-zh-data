

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
    unihan = {line.split('\t')[0]: line.split('\t')[1] for line in f.read().strip().split('\n')}

with open('variants/TSCharacters.txt', 'r') as f:
    opencc = {line.split('\t')[0]: line.split('\t')[1] for line in f.read().strip().split('\n')}

with open('../output/tc2sc.tsv', 'w') as f:
    for k, v in opencc.items():
        if k not in unihan:
            unihan[k] = v

    for k, v in unihan.items():
        f.write('{}\t{}\n'.format(k, v))

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
