all: build test

build:
	cd src && python3 lilak.py

test:
	sudo apt-get install libhunspell-dev
	pip3 install hunspell
	cd src && python3 test.py

extensions:
	# mozila xpi
	rm -rf ./build/mozile ./build/fa-IR-dictionary.xpi
	mkdir -p ./build/mozile ./build/mozile/dictionaries ./build/mozile/icons
	cp ./LICENSE ./build/mozile/LICENSE
	cp ./icon.png ./build/mozile/icon.png
	cp ./README_fa_IR.txt ./build/mozile/dictionaries/README_fa_IR.txt
	cp ./build/fa-IR.dic  ./build/mozile/dictionaries/fa-IR.dic
	cp ./build/fa-IR.aff  ./build/mozile/dictionaries/fa-IR.aff
	echo '{ "manifest_version": 2, "dictionaries": { "fa-IR": "dictionaries/fa-IR.dic" }, "applications": { "gecko": { "id": "fa-IR@dictionaries.addons.mozilla.org" } }, "name": "Lilak", "version": "3.2", "description": "Lilak, Persian Spell Checking Dictionary" }' > ./build/mozile/manifest.json
	cd ./build/mozile && zip -r ../fa-IR-dictionary.xpi *

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
