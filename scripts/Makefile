.PHONY: help
help:
	@echo "update                run the migration script"
	@echo "dl                    update data with latest UniHan database"

.PHONY: update

Unihan.zip:
	rm -f Unihan*
	wget -q ftp://ftp.unicode.org/Public/UNIDATA/Unihan.zip -O Unihan.zip

dl:
	rm -f Unihan*
	wget -q ftp://ftp.unicode.org/Public/UNIDATA/Unihan.zip -O Unihan.zip

update: Unihan.zip 
	unzip -f Unihan.zip
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
