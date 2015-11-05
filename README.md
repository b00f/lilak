# lilak, A Persian Dictionary for Hunspell based on Persian Morphology

lilak is an open source project for generating Persian dictionary for [hunspell](https://github.com/hunspell/hunspell) spell checker. This dictionary is based on Persian morphology. In Persian language affixes can change the roll of a word in sentence. This project helps hunspell to predict the best form of compound words based on morphological rules.


##Content 
```
  lilak
    |-- build           : Build folder. 
    |
    |-- src
    |   |-- lilak.py    : Python script for building lilak dictionary
    |   |-- lexicon     : Lexicon of Persian words with part-of-speech tags
    |   |-- affixes     : Affix (prefix or suffix) rules
    |   |-- dic_users   : List of words without POS tag.
    |   |-- dic_delta   : List of foreign words in Persian.
    |   \-- verbs.htm   : List of Persian verbs (unstemmed)
    |
    |-- test
    |   |-- dotest.py   : Python script to run all test case files 
    |   |-- text1       : 'Farsi(Persian) is Sugar', A short story by Mohammad-Ali Jamalzadeh
    |   |-- text2       : 'A Hekayat' By Saadi 
    |   |-- text3       : 'A Ghazal' By Hafez 
    |   |-- text4       : 'Yazdgerd Kingdom' By Ferdowsi
    |   |-- text5       : 'A Ghazal' By Muhammad Husayn Tabataba'i 
    |   |-- text6       : 'Have a Safe Trip' A poem by Shafii Kadkani
    |   |-- text7       : 'Se Tar' A short story by Jalal Al-e-Ahmad
    |   \-- text8       : 'End of Shahname' By Mehdi Akhavan-Sales
    |
    |-- READ.me         : 
    |-- LICENCE         : License file
    \-- RULES           : 
```

##Building Dictionary

To build dictionary, run lilak.py from 'src' folder:
```
python Lilak.py
```
You can find the compiled dictionary at the 'build' folder.

##Testing

Before running test make sure you have installed hunspell:
```
pip install hunspell
```
To test Lilak, run dotest.py from 'test' folder:
```
python dotest.py
```
You can find the result at 'result.log' file


How to contribute
-----------------
The best way that you can contribute on this project is collecting words with 
part-of-speech tags. It will help me to make dictionary more useful and accurate.

Part-of-speech is important to build lilak.
It should classified in main types like: verb, noun, adjective, ...
Also some other tags will be useful. like tense of verb, singular or plural, ...
Check Lexicon for more information


About the Name
--------------
lilac in English came from French lilac "shrub of genus Syringa with mauve flowers" 
from Spanish lilac, from Arabic lilak, from Persian lilak, variant of nilak "bluish"

As  T. S. Eliot says:
```
April is the cruelest month, breeding
Lilacs out of the dead land, mixing
Memory and desire, stirring
Dull roots with spring rain. 
```

