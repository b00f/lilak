# Lilak, Persian Spell Checking Dictionary
  [![Build Status](https://travis-ci.org/b00f/lilak.svg?branch=master)](https://travis-ci.org/b00f/lilak)
  [![Donate](https://img.shields.io/badge/support-patreon-F96854.svg?style=flat-square)](https://patreon.com/b00f)

[Lilak](https://github.com/b00f/lilak) is an open source project for generating Persian dictionary for [hunspell](https://github.com/hunspell/hunspell) spell checker based on Persian Morphology.

In Persian language affixes can change the meaning of the word. Some suffixes attached to a word as short form of verbs. Part-of-speech plays an important role in Persian language. In some cases the pronunciation of the word can change the suffixes. Check the code for more information.

Lilak has a [lexicon](http://lilak-project.com) of Persian words with part-of-speech tags. Lilak builds a dictionary for hunspell to predict the best form of compound words based on morphological rules.

## Content

```text
lilak
  |-- build           : Build folder. Compiled dictionary goes here.
  |
  |-- src
  |   |-- data
  |   |   |-- lexicon       : Lexicon of Persian words with part-of-speech tags
  |   |   |-- affixes       : Affix (prefix or suffix) rules
  |   |   |-- dic_users     : List of words without POS tag.
  |   |   \-- verbs.htm     : List of Persian verbs (unstemmed)
  |   |
  |   |-- lilak.py    : Python script for building lilak dictionary
  |   \-- test.py     : Python script to test lilak accuracy
  |
  |-- test
  |   |-- text1       : "Farsi(Persian) is Sugar", A short story by Mohammad-Ali Jamalzadeh
  |   |-- text2       : "A Hekayat" By Saadi
  |   |-- text3       : "A Ghazal" By Hafez
  |   |-- text4       : "Yazdgerd Kingdom" By Ferdowsi
  |   |-- text5       : "A Ghazal" By Muhammad Husayn Tabataba'i
  |   |-- text6       : "Have a Safe Trip" A poem by Shafii Kadkani
  |   |-- text7       : "Se Tar" A short story by Jalal Al-e-Ahmad
  |   |-- text8       : "End of Shahname" By Mehdi Akhavan-Sales
  |   |-- text9       : "The Water"s Footsteps" By Sohrab Sepehri
  |   |-- text10      : "Nei Name" By Rumi
  |   \-- verbs       : Some inflected verbs
  |
  |-- README.md       :
  \-- LICENCE         : License file
```

## Building Dictionary

Before using lilak please make sure you have install python 3.x.

To build the lilak dictionary, run lilak.py from `src` folder:

```bash
make build
make test
```

You can find the compiled dictionary at the `build` folder.

check [result.log](./test/result.log) for test result.

## How to contribute

The best way you can contribute on this project is collecting words with correct part-of-speech tags.
Part-of-speech is important to build Lilak. It should classified in main types like: verb, noun, adjective, etc. Also some other tags will be useful. like tense of verb, singular or plural, etc.
Check the `src/data/lexicon` for more information

Please open an issue if you find any mistakes while using lilak.

## Using Lilak

- You can find compiled dictionaries [here](https://github.com/b00f/lilak/releases/).
- Mozilla Firefox: Install lilak extension from here [here](https://addons.mozilla.org/en-US/firefox/addon/lilak-persian-dictionary/).
- Google Chrome: Go to Settings, find Language and input settings, add Persian language and make sure you have enabled the spell checker option.

## Supporting Lilak
If you like this project, please [donate](http://lilak-project.com/donate.php) or consider becoming a patron:

[![Become a patron](https://c5.patreon.com/external/logo/become_a_patron_button.png)](https://patreon.com/b00f)

## License
Lilak is published under Apache licence. You may freely use, reproduce, modify or distribute it. If you think lilak is useful please support it.

## About the Name

*lilac* in English came from French lilac "shrub of genus Syringa with mauve flowers"
from Spanish lilac, from Arabic *lilak*, from Persian *lilak*, variant of nilak "bluish"

## In Memory of Abolhassan Najafi

[Abolhassan Najafi](https://en.wikipedia.org/wiki/Abolhassan_Najafi) was an associate member of Iran's Academy of Persian Language and Literature. His most famous books is "Ghalat Nanevisim" (Let’s not write incorrect).


## Thanks

Special thanks to

- Dr. Hamid Farrroukh : [alefbaye2om](http://alefbaye2om.org/)
- Dr. Hamid Hassani : [wikipedia](https://en.wikipedia.org/wiki/Hamid_Hassani)
- Dr. Reza Moshksar : [github](https://github.com/reza1615)
- 5j9 : [github](https://github.com/5j9)
