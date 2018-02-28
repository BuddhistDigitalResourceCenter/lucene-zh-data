# Data for the Chinese Lucene Analyzers and Filters
 
## Generated Resources

Format for all resources: `<char to be mapped>\t<mapped char(s)>`

In case multiple equivalences exist, only the first one is retained. This follows the behaviour of OpenCC. 

#### `tc2sc.tsv`

Maps Traditional Chinese (TC) to Simplified Chinese (SC).

When OpenCC differs from Unihan, the latter is prefered.
Additional entries from OpenCC are mostly scientific and technologic entries from Taiwan.  

#### `pinyin.tsv`

From `pinyin-data`.

See [here](https://github.com/mozillazg/pinyin-data/tree/master/tools) for the generation of files in `unihan/pinyin/`.

#### `synonyms.tsv`

Strict semantic variants from Unihan.

#### `numbers.tsv`

Ideograms to arabic numbers from UniHan.

#### Update with latest Unihan release

```
cd scripts
make update
```

## Acknowledgments

 - [Unihan Database](http://www.unicode.org/charts/unihan.html)
 - The scripts to parse UniHan come from [pinyin-data](https://github.com/mozillazg/pinyin-data).
 - `unihan/variants/TSCharacters.txt` comes from the excellent [OpenCC](https://github.com/BYVoid/OpenCC) project.

## License

The Unihan database is Copyright Unicode Consortium, [Unicode License](http://unicode.org/copyright.html).
The TC-to-SC table from OpenCC(`scripts/variants/TSCharacters.txt`) is under Apache2
The Python scripts in `scripts` are Copyright Huang Huang([mozillag](https://github.com/mozillazg)), Licence MIT
All the output remains under the same Unicode License.

