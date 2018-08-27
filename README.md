# Lilak, Persian Spell Checking Dictionary

Lilak is an open source project for generating Persian dictionary for [hunspell](https://github.com/hunspell/hunspell) spell checker based on Persian Morphology.

In Persian language affixes can change the meaning of the word. Some suffixes attached to a word as short form of verbs. Part-of-speech plays an important role in attaching affixed in Perian language. In some cases the pronunciation of the word can change the suffixes. Check the code for moew information.

Lilak has a lexicon of Persian words with part-of-speech tags. Lilak builds a dictionary for hunspell to predict the best form of compound words based on morphological rules.

## Content

```
lilak
  |-- build           : Build folder. Compiled dictionary goes here.
  |
  |-- src
  |   |-- data
  |   |   |-- lexicon       : Lexicon of Persian words with part-of-speech tags
  |   |   |-- affixes       : Affix (prefix or suffix) rules
  |   |   |-- dic_users     : List of words without POS tag.
  |   |   |-- dic_delta     : List of foreign words in Persian.
  |   |   \-- verbs.htm     : List of Persian verbs (unstemmed)
  |   |
  |   |-- lilak.py    : Python script for building lilak dictionary
  |   \-- test.py     : Python script to test lilak accuracy
  |
  |-- test
  |   |-- text1       : 'Farsi(Persian) is Sugar', A short story by Mohammad-Ali Jamalzadeh
  |   |-- text2       : 'A Hekayat' By Saadi
  |   |-- text3       : 'A Ghazal' By Hafez
  |   |-- text4       : 'Yazdgerd Kingdom' By Ferdowsi
  |   |-- text5       : 'A Ghazal' By Muhammad Husayn Tabataba'i
  |   |-- text6       : 'Have a Safe Trip' A poem by Shafii Kadkani
  |   |-- text7       : 'Se Tar' A short story by Jalal Al-e-Ahmad
  |   |-- text8       : 'End of Shahname' By Mehdi Akhavan-Sales
  |   |-- text9       : 'The Water's Footsteps' By Sohrab Sepehri
  |   |-- text10      : 'Nei Name' By Rumi
  |   \-- verbs       : Some inflected verbs
  |
  |-- README.md       :
  \-- LICENCE         : License file
```

## Building Dictionary
Before using lilak please make sure you have install python 3.x.

To build the lilak dictionary, run lilak.py from `src` folder:
```
cd src
python lilak.py
```
You can find the compiled dictionary at the `build` folder.

## Testing

Before running test make sure you have installed [hunspell](https://github.com/hunspell/hunspell):
```
pip install hunspell
cd src
python test.py
```
You can find the result at 'result.log' file

## How to contribute

The best way you can contribute on this project is collecting words with correct part-of-speech tags.
Part-of-speech is important to build lilak. It should classified in main types like: verb, noun, adjective, etc. Also some other tags will be useful. like tense of verb, singular or plural, etc.
Check the `src/data/Lexicon` for more information

Please open an issue if you find any mistakes while using lilak.

## Installing Lilak

- You can download compiled dictionaries at [sourceforge](http://sourceforge.net/projects/lilak/).
- For installing Lilak on OpenOffice check [here](http://extensions.openoffice.org/en/project/persian-dictionary-apache-openoffice/).
- For installing Lilak on Mozilla Firefox check [here](https://addons.mozilla.org/en-US/firefox/addon/lilak-persian-dictionary/).
- For installing Lilak on Google Chrome: Go to Settings. Find Language and input settings. Add Persian language and make sure you have enabled the specll checker option.


## About the Name

*lilac* in English came from French lilac "shrub of genus Syringa with mauve flowers"
from Spanish lilac, from Arabic *lilak*, from Persian *lilak*, variant of nilak "bluish"

## In Memory of Abolhassan Najafi

[Abolhassan Najafi](https://en.wikipedia.org/wiki/Abolhassan_Najafi) was an associate member of Iran's Academy of Persian Language and Literature. His most famous books is "Ghalat Nanevisim" (Let’s not write incorrect).


## Thanks

Special thanks to
* Dr. Hamid Farrroukh : [alefbaye2om](http://alefbaye2om.org/)
* Dr. Hamid Hassani : [wikipedia](https://en.wikipedia.org/wiki/Hamid_Hassani)
* 5j9 : [github](https://github.com/5j9)
* Reza Moshksar : [github](https://github.com/reza1615)

