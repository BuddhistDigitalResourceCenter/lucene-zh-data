with open('../output/zh-numbers.tsv', 'w') as f:
    for num in ('kPrimaryNumeric.txt', 'kAccountingNumeric.txt', 'kOtherNumeric.txt'):
        with open('numerics/{}'.format(num), 'r') as g:
            for line in g.readlines():
                f.write(line)  # Unihan contains no numeric duplicate, so no deduplicate needed
