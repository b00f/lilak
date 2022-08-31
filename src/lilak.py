##
## Lilak, Persian Spell Checking Dictionary
##
## Copyright 2015 Mostafa Sedaghat Joo
##
## Licensed under the Apache License, Version 2.0 (the "License");
## you may not use this file except in compliance with the License.
## You may obtain a copy of the License at
##
##     http://www.apache.org/licenses/LICENSE-2.0
##
## Unless required by applicable law or agreed to in writing, software
## distributed under the License is distributed on an "AS IS" BASIS,
## WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
## See the License for the specific language governing permissions and
## limitations under the License.
##
##


#!/usr/bin/python
# -*- coding: utf-8 -*-


# read more here:
# fa.wikipedia.org/wiki/ویکی‌پدیا:دستور_خط
# http://www.persianacademy.ir/fa/das.aspx


import os
import sys
import collections
import operator
import shutil
import datetime
import argparse

VERSIAN = '3.3'
DEBUG = 1  # set to 1 to generate a debug output file

ZWNJ          = '\u200C'
PERSIAN_HA    = '\u0647\u0627'
PERSIAN_AAN   = '\u0627\u0646'
PERSIAN_HE    = '\u0647'
PERSIAN_YE    = '\u06CC'
PERSIAN_WAW   = '\u0648'
PERSIAN_ALEF  = '\u0627'
PERSIAN_DAL   = '\u062F'
PERSIAN_ZAL   = '\u0630'
PERSIAN_RE    = '\u0631'
PERSIAN_ZE    = '\u0632'
PERSIAN_ZHE   = '\u0698'
PERSIAN_SIN   = '\u0633'
PERSIAN_SHIN  = '\u0634'
PERSIAN_SAD   = '\u0635'
PERSIAN_ZAD   = '\u0636'
PERSIAN_TA    = '\u0637'
PERSIAN_ZA    = '\u0638'
PERSIAN_BE    = '\u0628'
PERSIAN_PE    = '\u067E'
PERSIAN_TE    = '\u062A'
PERSIAN_SE    = '\u062B'
PERSIAN_NON   = '\u0646'
PERSIAN_HAMZE = '\u0621'
PERSIAN_LAM   = '\u0644'
PERSIAN_KAF   = '\u06A9'
PERSIAN_GAF   = '\u06AF'
ARABIC_TE     = '\u0629'

PERSIAN_DETACHED = (PERSIAN_WAW, PERSIAN_ALEF, PERSIAN_DAL, PERSIAN_ZAL, \
                    PERSIAN_RE, PERSIAN_ZE, PERSIAN_ZHE, PERSIAN_HAMZE)


def remove_file(filename):
    if os.path.isfile(filename):
        os.remove(filename)


def debug(message):
    try:
        if DEBUG:
            print(message)
    except:
        pass




class Lilak:
    def __init__(self, mode = 0):
        self.mode = mode
        self.dictionary = {}
        self.words = set()


    def is_kam_dandane(self, word):
        if self.mode == 'tihu':
            return True

        dandane = 0
        # http://www.persianacademy.ir/fa/pishvand.aspx
        # هرگاه کلمه پردندانه (بیش­ از سه دندانه) شود و یا به «ط» و «ظ» ختم شود.
        # نویسه‌های «ورزژدذط ظ ک گ ا لءة» و فاصلهٔ مجازی که دندانه‌ها را جدا می‌کنند نباید قبل از آنها در محاسبه بیاید.
        # مثلاً «اسباب‌بازیها» نباید دندانهٔ «اسباب‌باز» محاسبه شود
        # در نتیجه کلمهٔ «اسباب‌بازیها» را هم باید قبول کند.
        for SeperatCharacter in [PERSIAN_ALEF, PERSIAN_DAL, PERSIAN_TA, PERSIAN_ZA, PERSIAN_LAM, ZWNJ,
                                 PERSIAN_WAW, PERSIAN_DAL, PERSIAN_ZAL, PERSIAN_RE, PERSIAN_ZE, PERSIAN_ZHE,
                                 PERSIAN_HAMZE, PERSIAN_KAF, PERSIAN_GAF, ARABIC_TE]:
            if  SeperatCharacter in word:
                word=word.split(SeperatCharacter)[1]

        for i, c in enumerate(word):

            if c == PERSIAN_BE  or \
               c == PERSIAN_PE  or \
               c == PERSIAN_TE  or \
               c == PERSIAN_SE  or \
               c == PERSIAN_SAD or \
               c == PERSIAN_ZAD:
                dandane = dandane + 1

            if c == PERSIAN_SIN  or \
               c == PERSIAN_SHIN:
                dandane = dandane + 3

            if c == PERSIAN_YE  or \
               c == PERSIAN_NON:
                if(i+1 < len(word)):
                    n = word[i+1]

                    if n != ZWNJ:
                        dandane = dandane + 1

        return (dandane < 5)


    def read_lexicon(self, filename):
        debug('read lexicon')

        if not os.path.isfile(filename):
            debug('file does not exist: %s' % filename)
            return

        with open(filename, 'r', encoding='utf-8') as f:
            for line in f.readlines():
                if line.startswith('##'):
                    continue

                tags = line[:-1].split(',')  # remove line breaks, split it

                # attributes: (pos, offensive, ends_with_vowel, ends_with_aah_uh)
                word = tags[0].strip()
                attrs = tags[1:]

                if not word:
                    debug('Wrong entry: {0}.'.format(line[:-1]))
                    continue

                if ' ' in word:
                    debug('Wrong entry: {0}.'.format(line[:-1]))
                    continue

                if word.startswith('u'):
                    word = chr(int(word[1:]))

                if word not in self.dictionary:
                    self.dictionary[word] = []

                if attrs not in self.dictionary[word]:
                    self.dictionary[word].append(attrs)
                else:
                    debug('{0} is duplicated.'.format(line[:-1]))


    def pars_user_dic(self, filename):
        debug('pars user dic')

        if not os.path.isfile(filename):
            debug('file does not exist: %s' % filename)
            return

        # import user dictionary
        with open(filename, 'r', encoding='utf-8') as f:
            for line in f.readlines():
                word = line[:-1].strip()

                if word.startswith('#'):
                    continue

                if not word:
                    continue

                if word not in self.dictionary:
                    #debug(word)
                    self.words.add(word)


    def dump_affixes(self, filename):
        debug('dump affixes')

        # letter frequency
        letters = collections.defaultdict(int)
        for word in self.words:
            for letter in word:
                if letter == '/':
                    break

                letters[letter] += 1

        # sorted tuples
        letters_s = sorted(letters.items(), key=operator.itemgetter(1))
        letters_s.reverse()

        affix = ''
        with open('./data/affixes', 'r', encoding='utf-8') as f:
            affix = f.read()

        remove_file(filename)
        with open(filename, 'w', encoding='utf-8', newline='') as f:
            frequency = ''
            for letter in letters_s:
                frequency += letter[0]

            f.write(affix.format(VERSIAN, datetime.datetime.now().strftime("%Y-%m-%d"), frequency))

        if not os.path.isfile(filename):
            debug('file does not exist: %s' % filename)
            return

    def dump_dictionary(self, filename):
        debug('dump dictionary')

        # sort word list
        words_s = sorted(self.words)

        remove_file(filename)
        with open(filename, 'w', encoding='utf-8', newline='') as f:
            f.write('{0}\n'.format(len(words_s)))
            for word in words_s:
                f.write(word + '\n')


    def pars_main_dic(self):
        debug('pars main dic')

        for key, value in self.dictionary.items():
            for attrs in value:
                word = key
                pos = attrs[0]
                offensive = attrs[1]
                ends_with_vowel = attrs[2]
                ends_with_aah_uh = attrs[3]
                label = ''
                kam_dandane = self.is_kam_dandane(word)

        ### Verb ########################################################################################
                if pos.startswith('verb') :
                    label += ''


        ### Noun ########################################################################################
                elif pos == 'noun_singular':

                    label += 'pa'   # بی‌انگیزه، بی‌حوصله، بی‌خانه

                    if word.endswith(PERSIAN_HE):
                        if ends_with_aah_uh:
                            label += 'sa'   # نگاهم، نگاهت، نگاهش، نگاهمان، نگاهتان، نگاهشان
                                            # کوهم، کوهت، کوهش، کوهمان، کوهتان، کوهشان
                            label += 'sr'   # نگاهم، نگاهی، نگاهیم، نگاهید، نگاهند
                                            # کوهم، کوهی، کوهیم، کوهید، کوهند
                            label += 'sg'   # نگاه‌ها، کوه‌ها
                                            # نگاه‌های، کوه‌های
                                            # نگاه‌هایی، کوه‌هایی
                            label += 'sh'   # نگاه‌هایم، نگاه‌هایت، نگاه‌هایش، نگاه‌هایمان، نگاه‌هایتان، نگاه‌هایشان
                                            # کوه‌هایم، کوه‌هایت، کوه‌هایش، کوه‌هایمان، کوه‌هایتان، کوه‌هایشان
                            label += 'si'   # نگاه‌هاست، کوه‌هاست
                            label += 'sl'   # نگاهی، کوهی
                            if kam_dandane:
                                label += 'sd'   # نگاهها، کوهها
                                                # نگاههای، کوههای
                                                # نگاههایی، کوههایی
                                label += 'se'   # نگاههایم، نگاههایت، نگاههایش، نگاههایمان، نگاههایتان، نگاههایشان
                                label += 'sf'   # کوههاست

                        elif  ends_with_vowel:
                            label += 'sc'   # خانه‌ام، خانه‌ات، خانه‌اش، خانه‌مان، خانه‌تان، خانه‌شان
                            label += 'sp'   # خانه‌ام، خانه‌ای، خانه‌ایم، خانه‌اید، خانه‌اند
                            label += 'sg'   # خانه‌ها
                                            # خانه‌های
                                            # خانه‌هایی
                            label += 'sh'   # خانه‌هایم، خانه‌هایت، خانه‌هایش، خانه‌هایمان، خانه‌هایتان، خانه‌هایشان
                            label += 'si'   # خانه‌هاست
                            label += 'sm'   # خانه‌ای
                            label += 'sk'   # خانه‌ی، خانهٔ
                        else:
                            label += 'sc'   # روبه‌ام، روبه‌ات، روبه‌اش، روبه‌مان، روبه‌تان، روبه‌شان
                            label += 'sp'   # روبه‌ام، روبه‌ای، روبه‌ایم، روبه‌اید، روبه‌اند
                            label += 'sg'   # روبه‌ها
                                            # روبه‌های
                                            # روبه‌هایی
                            label += 'sh'   # روبه‌هایم، روبه‌هایت، روبه‌هایش، روبه‌هایمان، روبه‌هایتان، روبه‌هایشان
                            label += 'si'   # روبه‌هاست
                            label += 'sl'   # روبهی

                    elif word.endswith(PERSIAN_WAW):
                        if ends_with_vowel:
                            label += 'sb'   # عمویم، عمویت، عمویش، عمویمان، عمویتان، عمویشان
                            label += 'sa'   # عموم، عموت، عموش، عمومان، عموتان، عموشان
                            label += 'sq'   # عمویم، عمویی، عموست، عموییم، عمویید، عمویند
                            label += 'sd'   # عموها
                                            # عموهای
                                            # عموهایی
                            label += 'se'   # عموهایم، عموهایت، عموهایش، عموهایمان، عموهایتان، عموهایشان
                            label += 'sf'   # عموهاست
                            label += 'sv'   # عموی
                            label += 'sn'   # عمویی
                        else:
                            label += 'sa'   # آرشیوم، آرشیوت، آرشیوش، آرشیومان، آرشیوتان، آرشیوشان
                            label += 'sr'   # آرشیوم، آرشیوی، آرشیویم، آرشیوید، آرشیوند
                            label += 'sd'   # آرشیوها
                                            # آرشیوهای
                                            # آرشیوهایی
                            label += 'se'   # آرشیوهایم، آرشیوهایت، آرشیوهایش، آرشیوهایمان، آرشیوهایتان، آرشیوهایشان
                            label += 'sf'   # آرشیوهاست
                            label += 'sl'   # آرشیوی

                    elif word.endswith(PERSIAN_YE):
                        label += 'sc'   # کشتی‌ام، کشتی‌ات، کشتی‌اش، کشتی‌مان، کشتی‌تان، کشتی‌شان
                        label += 'sp'   # کشتی‌ام، کشتی‌ای، کشتی‌ایم، کشتی‌اید، کشتی‌اند
                        label += 'sg'   # کشتی‌ها
                                        # کشتی‌های
                                        # کشتی‌هایی
                        label += 'sh'   # کشتی‌هایم، کشتی‌هایت، کشتی‌هایش، کشتی‌هایمان، کشتی‌هایتان، کشتی‌هایشان
                        label += 'si'   # کشتی‌هاست
                        label += 'sm'   # کشتی‌ای
                        label += 'sj'   # شکارچیان، شکارچیانی
                        if kam_dandane:
                            label += 'sd'   # بازیها
                                            # بازیهای
                                            # بازیهایی
                            label += 'se'   # بازیهایم، بازیهایت، بازیهایش، بازیهایمان، بازیهایتان، بازیهایشان
                            label += 'sf'   # بازیهاست

                    elif word.endswith(PERSIAN_ALEF):
                        label += 'sb'   # پایم، پایت، پایش، پایمان، پایتان، پایشان
                        label += 'sq'   # پایم، پایی، پاست، پاییم، پایید، پایند
                        label += 'sd'   # پاها
                                        # پاهای
                                        # پاهایی
                        label += 'se'   # پاهایم، پاهایت، پاهایش، پاهایمان، پاهایتان، پاهایشان
                        label += 'sf'   # پاهاست
                        label += 'sv'   # پای
                        label += 'sn'   # پایی

                    elif word.endswith(PERSIAN_DETACHED):
                        label += 'sa'   # برادرم، برادرت، برادرش، برادرمان، برادرتان، برادرشان
                        label += 'so'   # برادرم، برادری، برادرست، برادریم، برادرید، برادرند
                        label += 'sd'   # برادرها
                                        # برادرهای
                                        # برادرهایی
                        label += 'se'   # برادرهایم، برادرهایت، برادرهایش، برادرهایمان، برادرهایتان، برادرهایشان
                        label += 'sf'   # برادرهاست
                        label += 'sl'   # برادری
                        label += 'sj'   # برادران، برادرانی

                    elif word.endswith(PERSIAN_TA) or \
                         word.endswith(PERSIAN_ZA):
                        label += 'sa'   # خطم، خطت، خطش، خطمان، خطتان، خطشان
                        label += 'so'   # خطم، خطی، خطست، خطیم، خطید، خطند
                        label += 'sg'   # خط‌ها
                                        # خط‌های
                                        # خط‌هایی
                        label += 'sh'   # خط‌هایم، خط‌هایت، خط‌هایش، خط‌هایمان، خط‌هایتان، خط‌هایشان
                        label += 'si'   # خط‌هاست
                        label += 'sl'   # خطی
                        label += 'sj'   # خیاطان، خیاطانی

                    else:
                        label += 'sa'   # کتابم، کتابت، کتابش، کتابمان، کتابتان، کتابشان
                        label += 'so'   # کتابم، کتابی، کتابست، کتابیم، کتابید، کتابند
                        label += 'sg'   # کتاب‌ها
                                        # کتاب‌های
                                        # کتاب‌هایی
                        label += 'sh'   # کتاب‌هایم، کتاب‌هایت، کتاب‌هایش، کتاب‌هایمان، کتاب‌هایتان، کتاب‌هایشان
                        label += 'si'   # کتاب‌هاست
                        label += 'sl'   # کتابی
                        label += 'sj'   # صاحبان، صاحبانی
                        if kam_dandane:
                            label += 'sd'   # کتابها
                                            # کتابهای
                                            # کتابهایی
                            label += 'se'   # کتابهایم، کتابهایت، کتابهایش، کتابهایمان، کتابهایتان، کتابهایشان
                            label += 'sf'   # کتابهاست

                elif pos == 'noun_plural':
                    if word.endswith(PERSIAN_HE):
                        if ends_with_aah_uh:
                            label += ''     # وجوه
                        elif  ends_with_vowel:
                            label += 'sc'   # فلاسفه‌ام، فلاسفه‌ات، فلاسفه‌اش، فلاسفه‌مان، فلاسفه‌تان، فلاسفه‌شان
                            label += 'sp'   # فلاسفه‌ام، فلاسفه‌ای، فلاسفه‌ایم، فلاسفه‌اید، فلاسفه‌اند
                            label += 'sk'   # فلاسفه‌ی، فلاسفهٔ
                            label += 'sm'   # فلاسفه‌ای
                        else:
                            label += ''     # اشربه

                    elif word.endswith(PERSIAN_YE):
                        label += 'sc'   # فتاوی‌ام، فتاوی‌ات، فتاوی‌اش، فتاوی‌مان، فتاوی‌تان، فتاوی‌شان
                        label += 'sp'   # فتاوی‌ام، فتاوی‌ای، فتاوی‌ایم، فتاوی‌اید، فتاوی‌اند
                        label += 'sm'   # فتاوی‌ای

                    elif word.endswith(PERSIAN_WAW):
                        debug('unpredicted case for: ' + word + ':' + pos)
                        label += ''

                    elif word.endswith(PERSIAN_ALEF):
                        label += 'sb'   # هدایایم، هدایایت، هدایایش، هدایایمان، هدایایتان، هدایایشان
                        label += 'sq'   # هدایایم، هدایایی، هدایاست، هدایاییم، هدایایید، هدایایند
                        label += 'sv'   # هدایای
                        label += 'sn'   # هدایایی

                    elif word.endswith(PERSIAN_TA) or \
                         word.endswith(PERSIAN_ZA):
                        label += 'sa'   # اقساطم، اقساطت، اقساطش، اقساطمان، اقساطتان، اقساطشان
                        label += 'so'   # اقساطم، اقساطی، اقساطست، اقساطیم، اقساطید، اقساطند
                        label += 'sl'   # اقساطی

                    elif word.endswith(PERSIAN_DETACHED):
                        label += 'sa'   # آثارم، آثارت، آثارش، آثارمان، آثارتان، آثارشان
                        label += 'so'   # آثارم، آثاری، آثارست، آثاریم، آثارید، آثارند
                        label += 'sl'   # آثاری

                    else:
                        label += 'sa'   # احزابم، احزابت، احزابش، احزابمان، احزابتان، احزابشان
                        label += 'so'   # احزابم، احزابی، احزابست، احزابیم، احزابید، احزابند
                        label += 'sl'   # احزابی

        ### Adjective ########################################################################################
                elif pos == 'adjective':
                    if word.endswith(PERSIAN_HE):
                        if ends_with_aah_uh:
                            label += 'sa'   # کوتاهم، کوتاهت، کوتاهش، کوتاهمان، کوتاهتان، کوتاهشان
                                            # باشکوهم، باشکوهت، باشکوهش، باشکوهمان، باشکوهتان، باشکوهشان
                            label += 'sr'   # کوتاهم، کوتاهی، کوتاهیم، کوتاهید، کوتاهند
                                            # باشکوهم، باشکوهی، باشکوهیم، باشکوهید، باشکوهند
                            label += 'sl'   # کوتاهی، باشکوهی
                            label += 'sg'   # کوتاه‌ها، باشکوه‌ها
                                            # کوتاه‌های، باشکوه‌های
                                            # کوتاه‌هایی، باشکوه‌هایی
                            label += 'si'   # کوتاه‌هاست، باشکوه‌هاست
                            label += 'st'   # کوتاهترین
                            label += 'su'   # کوتاه‌تر، کوتاه‌ترین
                                            # باشکوه‌تر، باشکوه‌ترین
                                            # کوتاه‌تری، باشکوه‌تری
                                            # کوتاه‌ترها، کوتاه‌ترهای
                                            # باشکوه‌ترها، باشکوه‌ترهای
                                            # کوتاه‌ترین‌ها، کوتاه‌ترین‌های
                                            # باشکوه‌ترین‌ها، باشکوه‌ترین‌های
                        elif ends_with_vowel:
                            label += 'sc'   # شایسته‌ام، شایسته‌ات، شایسته‌اش، شایسته‌مان، شایسته‌تان، شایسته‌شان
                            label += 'sp'   # شایسته‌ام، شایسته‌ای، شایسته‌ایم، شایسته‌اید، شایسته‌اند
                            label += 'sk'   # شایسته‌ی، شایستهٔ
                            label += 'sg'   # شایسته‌ها
                                            # شایسته‌های
                                            # شایسته‌هایی
                            label += 'si'   # شایسته‌هاست
                            label += 'su'   # شایسته‌تر، شایسته‌ترین
                                            # شایسته‌تری
                                            # شایسته‌ترها، شایسته‌ترهای
                                            # شایسته‌ترین‌ها، شایسته‌ترین‌های
                        else:
                            label += 'sc'   # کوتاه‌ام، کوتاه‌ات، کوتاه‌اش، کوتاه‌مان، کوتاه‌تان، کوتاه‌شان
                            label += 'sp'   # کوتاه‌ام، کوتاه‌ای، کوتاه‌ایم، کوتاه‌اید، کوتاه‌اند
                            label += 'sl'   # کوتاهی
                            label += 'sg'   # کوتاه‌ها
                                            # کوتاه‌های
                                            # کوتاه‌هایی
                            label += 'si'   # کوتاه‌هاست
                            label += 'su'   # کوتاه‌تر، کوتاه‌ترین
                                            # کوتاه‌تری
                                            # کوتاه‌ترها، کوتاه‌ترهای
                                            # کوتاه‌ترین‌ها، کوتاه‌ترین‌های

                    elif word.endswith(PERSIAN_WAW):
                        if ends_with_vowel:
                            label += 'sb'   # پررویم، پررویت، پررویش، پررویمان، پررویتان، پررویشان
                            label += 'sq'   # پررویم، پررویی، پرروست، پرروییم، پررویید، پررویند
                            label += 'sv'   # پرروی
                            label += 'sn'   # پررویی
                            label += 'sd'   # پرروها
                                            # پرروهای
                                            # پرروهایی
                            label += 'sf'   # پرروهاست
                            label += 'st'   # پرروتر، پرروترین
                                            # پرروتری
                                            # پرروترها، پرروترهای
                                            # پرروترین‌ها، پرروترین‌های
                        else:
                            label += 'sa'   # کنجکاوم، کنجکاوت، کنجکاوش، کنجکاومان، کنجکاوتان، کنجکاوشان
                            label += 'sr'   # کنجکاوم، کنجکاوی، کنجکاویم، کنجکاوید، کنجکاوند
                            label += 'sl'   # کنجکاوی
                            label += 'sd'   # کنجکاوها
                                            # کنجکاوهای
                                            # کنجکاوهایی
                            label += 'sf'   # کنجکاوهاست
                            label += 'st'   # کنجکاوتر، کنجکاوترین
                                            # کنجکاوتری
                                            # کنجکاوترها، کنجکاوترهای
                                            # کنجکاوترین‌ها، کنجکاوترین‌های
                            label += 'sj'   # کنجکاوان، کنجکاوانی

                    elif word.endswith(PERSIAN_YE):
                        label += 'sc'   # عالی‌ام، عالی‌ات، عالی‌اش، عالی‌مان، عالی‌تان، عالی‌شان
                        label += 'sp'   # عالی‌ام، عالی‌ای، عالی‌ایم، عالی‌اید، عالی‌اند
                        label += 'sm'   # عالی‌ای
                        label += 'sg'   # عالی‌ها
                                        # عالی‌های
                                        # عالی‌هایی
                        label += 'si'   # عالی‌هاست
                        label += 'su'   # عالی‌تر، عالی‌ترین
                                        # عالی‌تری
                                        # عالی‌ترها، عالی‌ترهای
                                        # عالی‌ترین‌ها، عالی‌ترین‌های
                        if kam_dandane:
                            label += 'sd'   # فلسطینیها
                                            # فلسطینیهای
                                            # فلسطینیهایی
                            label += 'sf'   # فلسطینیهاست

                    elif word.endswith(PERSIAN_ALEF):
                        label += 'sb'   # اعلایم، اعلایت، اعلایش، اعلایمان، اعلایتان، اعلایشان
                        label += 'sq'   # اعلایم، اعلایی، اعلاست، اعلاییم، اعلایید، اعلایند
                        label += 'sv'   # اعلای
                        label += 'sn'   # اعلایی
                        label += 'sd'   # اعلاها
                                        # اعلاهای
                                        # اعلاهایی
                        label += 'sf'   # اعلاهاست
                        label += 'st'   # اعلاتر، اعلاترین
                                        # اعلاتری
                                        # اعلاترها، اعلاترهای
                                        # اعلاترین‌ها، اعلاترین‌های

                    elif word.endswith(PERSIAN_DETACHED):
                        label += 'sa'   # آبادم، آبادت، آبادش، آبادمان، آبادتان، آبادشان
                        label += 'so'   # آبادم، آبادی، آبادست، آبادیم، آبادید، آبادند
                        label += 'sl'   # آبادی
                        label += 'sd'   # آبادها
                                        # آبادهای
                                        # آبادهایی
                        label += 'sf'   # آبادهاست
                        label += 'st'   # آبادتر، آبادترین
                                        # آبادتری
                                        # آبادترها، آبادترهای
                                        # آبادترین‌ها، آبادترین‌های
                        label += 'sj'   # تنومندان، تنومندانی

                    elif word.endswith(PERSIAN_TA) or \
                         word.endswith(PERSIAN_ZA):
                        label += 'sa'   # بانشاطم، بانشاطت، بانشاطش، بانشاطمان، بانشاطتان، بانشاطشان
                        label += 'so'   # بانشاطم، بانشاطی، بانشاطست، بانشاطیم، بانشاطید، بانشاطند
                        label += 'sl'   # بانشاطی
                        label += 'sg'   # بانشاط‌ها
                                        # بانشاط‌های
                                        # بانشاط‌هایی
                        label += 'si'   # بانشاط‌هاست
                        label += 'st'   # بانشاطتر، بانشاطترین
                                        # بانشاطتری
                                        # بانشاطترها، بانشاطترهای
                                        # بانشاطترین‌ها، بانشاطترین‌های
                        label += 'su'   # بانشاط‌تر، بانشاط‌ترین
                                        # بانشاط‌تری
                                        # بانشاط‌ترها، بانشاط‌ترهای
                                        # بانشاط‌ترین‌ها، بانشاط‌ترین‌های
                        label += 'sj'   # بانشاطان، بانشاطانی

                    else:
                        label += 'sa'   # مرتبم، مرتبت، مرتبش، مرتبمان، مرتبتان، مرتبشان
                        label += 'so'   # مرتبم، مرتبی، مرتبست، مرتبیم، مرتبید، مرتبند
                        label += 'sl'   # مرتبی
                        label += 'sg'   # مرتب‌ها
                                        # مرتب‌های
                                        # مرتب‌هایی
                        label += 'si'   # مرتب‌هاست
                        label += 'su'   # مرتب‌تر، مرتب‌ترین
                                        # مرتب‌تری
                                        # مرتب‌ترها، مرتب‌ترهای
                                        # مرتب‌ترین‌ها، مرتب‌ترین‌های
                        label += 'sj'   # خوبان، خوبانی
                        if kam_dandane:
                            label += 'sd'   # مرتبها
                                            # مرتبهای
                                            # مرتبهایی
                            label += 'sf'   # مرتبهاست
                            label += 'st'   # مرتبتر، مرتبترین
                                            # مرتبتری
                                            # مرتبترها، مرتبترهای
                                            # مرتبترین‌ها، مرتبترین‌های

                elif pos == 'adjective_comparative':
                    if word.endswith(PERSIAN_HE):
                        debug('unpredicted case for: ' + word + ':' + pos)
                        label += ''

                    elif word.endswith(PERSIAN_WAW):
                        debug('unpredicted case for: ' + word + ':' + pos)
                        label += ''

                    elif word.endswith(PERSIAN_YE):
                        label += '' # بارزتری، جوانتری

                    elif word.endswith(PERSIAN_DETACHED):
                        label += 'sa'   # ارشدم، ارشدت، ارشدش، ارشدمان، ارشدتان، ارشدشان
                        label += 'so'   # ارشدم، ارشدی، ارشدست، ارشدیم، ارشدید، ارشدند
                        label += 'sl'   # ارشدی
                        label += 'sd'   # ارشدها
                                        # ارشدهای
                                        # ارشدهایی
                        label += 'sf'   # ارشدهاست

                    elif word.endswith(PERSIAN_TA) or \
                         word.endswith(PERSIAN_ZA):
                        debug('unpredicted case for: ' + word + ':' + pos)

                    else:
                        label += 'sa'   # افزونم، افزونت، افزونش، افزونمان، افزونتان، افزونشان
                        label += 'so'   # افزونم، افزونی، افزونست، افزونیم، افزونید، افزونند
                        label += 'sl'   # افزونی
                        label += 'sg'   # افزون‌ها
                                        # افزون‌های
                                        # افزون‌هایی
                        ## label += 'si'   # [???] افزون‌هاست


                elif pos == 'adjective_superlative':
                    if word.endswith(PERSIAN_HE):
                        debug('unpredicted case for: ' + word + ':' + pos)
                        label += ''

                    elif word.endswith(PERSIAN_WAW):
                        debug('unpredicted case for: ' + word + ':' + pos)
                        label += ''

                    elif word.endswith(PERSIAN_YE):
                        debug('unpredicted case for: ' + word + ':' + pos)
                        label += ''

                    elif word.endswith(PERSIAN_DETACHED):
                        label += 'sa'   # اولی‌ترم، اولی‌ترت، اولی‌ترش، اولی‌ترمان، اولی‌ترتان، اولی‌ترشان
                        label += 'so'   # اولی‌ترم، اولی‌تری، اولی‌ترست، اولی‌تریم، اولی‌ترید، اولی‌ترند
                        label += 'sl'   # اولی‌تری
                        label += 'sd'   # اولی‌ترها
                                        # اولی‌ترهای
                                        # اولی‌ترهایی
                        label += 'sf'   # اولی‌ترهاست

                    elif word.endswith(PERSIAN_TA) or \
                         word.endswith(PERSIAN_ZA):
                        debug('unpredicted case for: ' + word + ':' + pos)

                    else:
                        label += 'sa'   # بهترینم، بهترینت، بهترینش، بهترینمان، بهترینتان، بهترینشان
                        label += 'so'   # بهترینم، بهترینی، بهترینست، بهترینیم، بهترینید، بهترینند
                        label += 'sl'   # بهترینی
                        label += 'sg'   # بهترین‌ها
                                        # بهترین‌های
                                        # بهترین‌هایی
                        label += 'si'   # بهترین‌هاست
                        if kam_dandane:
                            label += 'sd'   # بهترینها
                                            # بهترینهای
                                            # بهترینهایی
                            label += 'se'   # بهترینهایم، بهترینهایت، بهترینهایش، بهترینهایمان، بهترینهایتان، بهترینهایشان
                            label += 'sf'   # بهترینهاست

        ### Adverb ########################################################################################
                elif pos == 'adverb':
                    label += ''

        ### Pronoun ########################################################################################
                elif pos == 'pronoun':
                    label += ''

        ### Number ########################################################################################
                elif pos == 'numeral':
                    label += ''
        ### Neda ########################################################################################
                elif pos == 'interjection':
                    label += ''

        ### Preposition ########################################################################################
                elif pos == 'adposition':
                    label += ''

        ### Conjunction ########################################################################################
                elif pos == 'conjunction':
                    label += ''

        ### classifier ########################################################################################
                elif pos == 'classifier':
                    label += ''

        ### Foreign ########################################################################################
                elif pos == 'foreign':
                    if word.endswith(PERSIAN_HE):
                        label += ''

                    else:
                        label += 'sl'   # طرفة‌العینی

                else:
                    debug('{0} {1}: unknown tag'.format(word, pos))


                # offensive word
                if offensive:
                    label += '!!'

                if label:
                    word += '/'+label

                if len(attrs) > 4:
                    word += attrs[4]

                self.words.add(word)



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-m", "--mode", help="Run mode")
    parser.add_argument("-i", "--input", help="input lexicon file")
    parser.add_argument("-o", "--output", help="input dictionary file")
    parser.add_argument('-v', '--version', action='version', version=VERSIAN)
    args = parser.parse_args()

    if args.mode == 'tihu':
        lilak = Lilak(args.mode)
        lilak.read_lexicon(args.input)
        lilak.pars_main_dic()
        lilak.dump_dictionary(args.output)
    else:
        lilak = Lilak()
        lilak.read_lexicon('./data/lexicon')
        lilak.pars_main_dic()
        lilak.pars_user_dic('./data/dic_users')
        lilak.dump_affixes('../build/fa-IR.aff')
        lilak.dump_dictionary('../build/fa-IR.dic')

    debug('done!')
