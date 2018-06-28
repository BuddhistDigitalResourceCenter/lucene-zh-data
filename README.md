# Data for the Chinese Lucene Analyzers and Filters
 
## Generated Resources

Format for all resources: `<char to be mapped>\t<mapped char(s)>`

Multiple equivalences are kept expanded in 1:1 equivalences, including the cases where a character simplifies to itself. 

#### `output/tc2sc.tsv`

Traditional Chinese (TC) to Simplified Chinese (SC).

When OpenCC differs from Unihan, the latter is prefered.
Additional entries from OpenCC are mostly scientific and technologic entries from Taiwan.  

#### `output/pinyin.tsv`

Ideogram (both TC and SC) to Pinyin.
The PY prefered is from `kMandarin`, as stated [in Unihan](http://www.unicode.org/reports/tr38/index.html#kMandarin).
For ideograms not contained in this field, Pinyins are searched in `kHanyuPinyin`, then `kXHC1983` and finally in `kHanyuPinlu`.
The later fields are only searched if the previous ones didn't yield any Pinyin.
As stated [here](scripts/merge_pinyin.py#L87), this last field contains inaccuracies.

#### `output/synonyms.tsv`

Strict semantic variants.

#### `output/numbers.tsv`

Ideograms to arabic numbers.

#### `output/alternatives.tsv`

Stylistic variants("z-variants"; they share the same "abstract form"). 

#### `output/pinyin-vowel-combinations.tsv`

All the vowel combinations found in Unihan that can be turned into lazy PY.

#### `output/pinyin_alphabet_expanded.txt`

The content of `pinyin/pinyin_alphabet.dict` that has been expanded with all vowel combinations in `output/pinyin-vowel-combinations.tsv`.

#### Update with latest Unihan release

```
cd scripts
make update
```

## Acknowledgments

 - All the data comes from [Unihan Database](http://www.unicode.org/charts/unihan.html), except for `unihan/variants/TSCharacters.txt`, coming from [OpenCC](https://github.com/BYVoid/OpenCC). 
 - The scripts to parse UniHan come from [pinyin-data](https://github.com/mozillazg/pinyin-data). 

## License

The Unihan database is Copyright Unicode Consortium, [Unicode License](http://unicode.org/copyright.html).

The TC-to-SC table from OpenCC(`scripts/variants/TSCharacters.txt`) is under [Apache2](https://opensource.org/licenses/Apache-2.0)

The Python scripts in `scripts` are Copyright Huang Huang([mozillag](https://github.com/mozillazg)), [Licence MIT](https://opensource.org/licenses/MIT)

All the output remains under the same [Unicode License](http://unicode.org/copyright.html).
