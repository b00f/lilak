VERSION=$(shell python3 src/lilak.py -v)

all: hunspell build test

hunspell:
	sudo apt-get install libhunspell-dev
	pip3 install hunspell

build:
	cd src && python3 lilak.py

test:
	cd src && python3 test.py

extensions:
	# mozila xpi
	rm -rf ./build/mozila ./build/fa-IR-dictionary.xpi
	mkdir -p ./build/mozila
	cp ./build/fa-IR.dic  ./build/mozila/fa-IR.dic
	cp ./build/fa-IR.aff  ./build/mozila/fa-IR.aff
	cp ./LICENSE ./build/mozila/LICENSE
	cp ./icon.png ./build/mozila/icon.png
	cp ./src/data/README_fa_IR.txt ./build/mozila/README_fa_IR.txt
	cp ./src/data/manifest.json ./build/mozila/manifest.json
	sed -i 's/%VER%/$(VERSION)/g' ./build/mozila/manifest.json
	cd ./build/mozila && zip -r ../fa-IR-dictionary.xpi *

	# LibreOffice oxt
	rm -rf ./build/libre ./build/fa-IR-dictionary.oxt
	mkdir -p ./build/libre ./build/libre/META-INF
	cp ./build/fa-IR.dic  ./build/libre/fa-IR.dic
	cp ./build/fa-IR.aff  ./build/libre/fa-IR.aff
	cp ./LICENSE ./build/libre/LICENSE
	cp ./icon.png ./build/libre/icon.png
	cp ./src/data/META-INF/manifest.xml ./build/libre/META-INF/manifest.xml
	cp ./src/data/README_fa_IR.txt ./build/libre/README_fa_IR.txt
	cp ./src/data/dictionaries.xcu ./build/libre/dictionaries.xcu
	cp ./src/data/description.xml ./build/libre/description.xml
	sed -i 's/%VER%/$(VERSION)/g' ./build/libre/description.xml
	cd ./build/libre && zip -r ../fa-IR-dictionary.oxt *

	# chromium bdic
	rm -rf ~/chromium ~/depot_tools;
	git clone https://chromium.googlesource.com/chromium/tools/depot_tools.git ~/depot_tools; \
	export PATH=${PATH}:${HOME}/depot_tools; \
	mkdir ~/chromium && cd ~/chromium; \
	fetch --nohooks --no-history chromium; \
	cd src; \
	gclient runhooks; \
	gn gen out/Debug; \
	ninja -C out/Debug convert_dict
	# building bdic file
	cd build && ~/chromium/src/out/Debug/convert_dict fa-IR

.PHONY: all build extensions test
