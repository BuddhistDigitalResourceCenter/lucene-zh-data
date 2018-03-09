.PHONY: help
help:
	@echo "update                update with latest UniHan database"

.PHONY: update
update:
	-rm Unihan*
	wget ftp://ftp.unicode.org/Public/UNIDATA/Unihan.zip -O Unihan.zip
	unzip Unihan.zip
	mkdir -p variants/
	mkdir -p pinyin/
	mkdir -p numerics/
	mkdir -p ../output/
	python3 parse_pinyin.py
	python3 merge_pinyin.py
	python3 parse_numerics.py
	python3 merge_numerics.py
	python3 parse_variants.py
	python3 merge_variants.py
