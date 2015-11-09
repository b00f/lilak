# Lilak, A Persian Dictionary for Hunspell based on Persian Morphology

[Lilak](https://github.com/m-o-s-t-a-f-a/lilak) is an open source project for generating Persian dictionary for [hunspell](https://github.com/hunspell/hunspell) spell checker. 
In Persian language affixes can change the meaning of the word. Some suffixes attached to a word as short form of verbs. For detecting these suffixes we need to know the part-of-speech and in some cases the exact pronunciation of the word.
Lilak has a lexicon of Persian words with part-of-speech tags. Lilak build a dictionary for hunspell to predict the best form of compound words based on morphological rules.


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
  |-- README.md       : 
  |-- LICENCE         : License file
  \-- RULES           : 
```

##Building Dictionary

To build dictionary, run lilak.py from 'src' folder:
```
python lilak.py
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


##How to contribute

The best way that you can contribute on this project is collecting words with 
part-of-speech tags. It will help me to make dictionary more useful and accurate.

Part-of-speech is important to build lilak.
It should classified in main types like: verb, noun, adjective, ...
Also some other tags will be useful. like tense of verb, singular or plural, ...
Check Lexicon for more information

Also if you found a mistakes please report it via email to me.

If you have any questions about the project, please don't hesitate to ask.

##About the Name

lilac in English came from French lilac "shrub of genus Syringa with mauve flowers" 
from Spanish lilac, from Arabic lilak, from Persian lilak, variant of nilak "bluish"

As  T. S. Eliot says:
```
April is the cruelest month, breeding
Lilacs out of the dead land, mixing
Memory and desire, stirring
Dull roots with spring rain. 
```

##Contact Me

Please feel free to contact me by this email address:
mostafa.sedaghat@gmail.com (Mostafa Sedaghat Joo)
