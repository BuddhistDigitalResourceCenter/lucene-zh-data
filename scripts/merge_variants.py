# file generated by Makefile
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
    with open('../output/alternatives.tsv', 'w') as g:
        g.write(f.read())

# copy the content as-is
with open('variants/kSemanticVariant.txt', 'r') as f:
    with open('../output/synonyms.tsv', 'w') as g:
        g.write(f.read())
