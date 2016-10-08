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

VERSIAN = '3.0'
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
PERSIAN_DETACHED = (PERSIAN_WAW, PERSIAN_ALEF, PERSIAN_DAL, PERSIAN_ZAL, \
                    PERSIAN_RE, PERSIAN_ZE, PERSIAN_ZHE, PERSIAN_HAMZE)


def remove(filename):
    if os.path.isfile(filename):
        os.remove(filename)

 
def debug(message):
    try:
        if DEBUG:
            print(message)
    except:
        pass

def count_dandane(word):
    dandane = 0;
    
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
    
    return dandane
    
class Parser:
    def __init__(self):
        self.dictionary = {}
        
        
    def read_lexicon(self, filename):
        with open(filename, 'r', encoding='utf-8') as f:
            for line in f.readlines():
                if line.startswith('#'):
                    continue

                tags = line[:-1].split(',')  # remove line breaks, split it

                # attributes: (pos, offensive, ends_with_vowel, ends_with_aah_uh)
                word = tags[0].strip()
                attrs = (tags[1], tags[2], tags[3], tags[4])

                if not word:
                    continue

                if ' ' in word:
                    continue  # hunspell doesn't work with compound words.

                if word not in self.dictionary:
                    self.dictionary[word] = []

                if attrs not in self.dictionary[word]:
                    self.dictionary[word].append(attrs)
                else:
                    debug('{0} is duplicated.'.format(line[:-1]))



    def pars(self):
        words = set()
        for key, value in self.dictionary.items():
            for attrs in value:
                word = key
                pos = attrs[0]
                offensive = attrs[1]
                ends_with_vowel = attrs[2]
                ends_with_aah_uh = attrs[3]
                label = ''
                kam_dandane = count_dandane(word) < 5

        ###############################################################################################
        # VERB                                                                                        #
        ###############################################################################################
                if pos.startswith('verb') :
                    label += ''
                

        #################################################################################################
        # NOUN                                                                                          #
        #################################################################################################
                elif pos == 'noun_common_singular': 
                    if word.endswith(PERSIAN_HE):
                        if ends_with_aah_uh:
                            label += 'z1'   # نگاهم، نگاهت، نگاهش، نگاهمان، نگاهتان، نگاهشان
                                            # کوهم، کوهت، کوهش، کوهمان، کوهتان، کوهشان
                            label += 'b4'   # نگاهم، نگاهی، نگاهیم، نگاهید، نگاهند
                                            # کوهم، کوهی، کوهیم، کوهید، کوهند
                            label += 'z5'   # نگاه‌هایم، نگاه‌هایت، نگاه‌هایش، نگاه‌هایمان، نگاه‌هایتان، نگاه‌هایشان
                                            # کوه‌هایم، کوه‌هایت، کوه‌هایش، کوه‌هایمان، کوه‌هایتان، کوه‌هایشان
                            label += 'j2'   # نگاه‌ها، کوه‌ها
                            label += 'j4'   # نگاه‌های، کوه‌های
                            label += 'j6'   # نگاه‌هایی، کوه‌هایی
                            label += 'j8'   # نگاه‌هاست، کوه‌هاست
                            label += 'y1'   # نگاهی، کوهی
                            if kam_dandane:
                                label += 'j1'   # نگاهها، کوهها
                        elif  ends_with_vowel:
                            label += 'z3'   # خانه‌ام، خانه‌ات، خانه‌اش، خانه‌مان، خانه‌تان، خانه‌شان
                            label += 'b2'   # خانه‌ام، خانه‌ای، خانه‌ایم، خانه‌اید، خانه‌اند
                            label += 'z5'   # خانه‌هایم، خانه‌هایت، خانه‌هایش، خانه‌هایمان، خانه‌هایتان، خانه‌هایشان
                            label += 'j2'   # خانه‌ها
                            label += 'j4'   # خانه‌های
                            label += 'j6'   # خانه‌هایی
                            label += 'j8'   # خانه‌هاست
                            label += 'y2'   # خانه‌ای
                            label += 'hz'   # خانه‌ی، خانهٔ
                        else:
                            label += 'z3'   # روبه‌ام، روبه‌ات، روبه‌اش، روبه‌مان، روبه‌تان، روبه‌شان
                            label += 'b2'   # روبه‌ام، روبه‌ای، روبه‌ایم، روبه‌اید، روبه‌اند
                            label += 'z5'   # روبه‌هایم، روبه‌هایت، روبه‌هایش، روبه‌هایمان، روبه‌هایتان، روبه‌هایشان
                            label += 'j2'   # روبه‌ها
                            label += 'j4'   # روبه‌های
                            label += 'j6'   # روبه‌هایی
                            label += 'j8'   # روبه‌هاست
                            label += 'y1'   # روبهی

                    elif word.endswith(PERSIAN_WAW): 
                        if ends_with_vowel:
                            label += 'z2'   # عمویم، عمویت، عمویش، عمویمان، عمویتان، عمویشان
                            label += 'b3'   # عمویم، عمویی، عموست، عموییم، عمویید، عمویند
                            label += 'z4'   # عموهایم، عموهایت، عموهایش، عموهایمان، عموهایتان، عموهایشان
                            label += 'j1'   # عموها
                            label += 'j3'   # عموهای
                            label += 'j5'   # عموهایی
                            label += 'j7'   # عموهاست
                            label += 'y1'   # عموی
                            label += 'y3'   # عمویی
                        else:
                            label += 'z1'   # رهروم، رهروت، رهروش، رهرومان، رهروتان، رهروشان
                                            ## [???] ambiguous here: شما کارمند متروید/مترواید/مترویید
                            label += 'b4'   # رهروم، رهروی، رهرویم، رهروید، رهروند
                            label += 'z4'   # رهروهایم، رهروهایت، رهروهایش، رهروهایمان، رهروهایتان، رهروهایشان
                            label += 'j1'   # رهروها
                            label += 'j3'   # رهروهای
                            label += 'j5'   # رهروهایی
                            label += 'j7'   # رهروهاست
                            label += 'y1'   # رهروی
                            label += 'an'   # رهروان، رهروانی

                    elif word.endswith(PERSIAN_YE):
                        label += 'z3'   # کشتی‌ام، کشتی‌ات، کشتی‌اش، کشتی‌مان، کشتی‌تان، کشتی‌شان
                        label += 'b2'   # کشتی‌ام، کشتی‌ای، کشتی‌ایم، کشتی‌اید، کشتی‌اند
                        label += 'z5'   # کشتی‌هایم، کشتی‌هایت، کشتی‌هایش، کشتی‌هایمان، کشتی‌هایتان، کشتی‌هایشان
                        label += 'j2'   # کشتی‌ها
                        label += 'j4'   # کشتی‌های
                        label += 'j6'   # کشتی‌هایی
                        label += 'j8'   # کشتی‌هاست
                        label += 'y2'   # کشتی‌ای
                        label += 'an'   # شکارچیان، شکارچیانی

                    elif word.endswith(PERSIAN_ALEF):
                        label += 'z2'   # پایم، پایت، پایش، پایمان، پایتان، پایشان
                        label += 'b3'   # پایم، پایی، پاست، پاییم، پایید، پایند
                        label += 'z4'   # پاهایم، پاهایت، پاهایش، پاهایمان، پاهایتان، پاهایشان
                        label += 'j1'   # پاها
                        label += 'j3'   # پاهای
                        label += 'j5'   # پاهایی
                        label += 'j7'   # پاهاست
                        label += 'y1'   # پای
                        label += 'y3'   # پایی

                    elif word.endswith(PERSIAN_DETACHED):
                        label += 'z1'   # برادرم، برادرت، برادرش، برادرمان، برادرتان، برادرشان
                        label += 'b1'   # برادرم، برادری، برادرست، برادریم، برادرید، برادرند
                        label += 'z4'   # برادرهایم، برادرهایت، برادرهایش، برادرهایمان، برادرهایتان، برادرهایشان
                        label += 'j1'   # برادرها
                        label += 'j3'   # برادرهای
                        label += 'j5'   # برادرهایی
                        label += 'j7'   # برادرهاست
                        label += 'y1'   # برادری
                        label += 'an'   # برادران، برادرانی
                        
                    elif word.endswith(PERSIAN_TA) or \
                         word.endswith(PERSIAN_ZA):
                        label += 'z1'   # خطم، خطت، خطش، خطمان، خطتان، خطشان
                        label += 'b1'   # خطم، خطی، خطست، خطیم، خطید، خطند
                        label += 'z5'   # خط‌هایم، خط‌هایت، خط‌هایش، خط‌هایمان، خط‌هایتان، خط‌هایشان
                        label += 'j2'   # خط‌ها
                        label += 'j4'   # خط‌های
                        label += 'j6'   # خط‌هایی
                        label += 'j8'   # خط‌هاست
                        label += 'y1'   # خطی
                        label += 'an'   # خیاطان، خیاطانی
                    
                    else:
                        label += 'z1'   # کتابم، کتابت، کتابش، کتابمان، کتابتان، کتابشان
                        label += 'b1'   # کتابم، کتابی، کتابست، کتابیم، کتابید، کتابند
                        label += 'z5'   # کتاب‌هایم، کتاب‌هایت، کتاب‌هایش، کتاب‌هایمان، کتاب‌هایتان، کتاب‌هایشان                        
                        label += 'j2'   # کتاب‌ها
                        label += 'j4'   # کتاب‌های
                        label += 'j6'   # کتاب‌هایی
                        label += 'j8'   # کتاب‌هاست
                        label += 'y1'   # کتابی
                        label += 'an'   # صاحبان، صاحبانی
                        if kam_dandane:
                            label += 'z4'   # کتابهایم، کتابهایت، کتابهایش، کتابهایمان، کتابهایتان، کتابهایشان
                            label += 'j1'   # کتابها
                            label += 'j3'   # کتابهای
                            label += 'j5'   # کتابهایی
                            label += 'j7'   # کتابهاست

                elif pos == 'noun_common_plural':
                    if word.endswith(PERSIAN_HE):
                        if ends_with_aah_uh:
                            label += ''     # وجوه
                        elif  ends_with_vowel:
                            label += 'z3'   # فلاسفه‌ام، فلاسفه‌ات، فلاسفه‌اش، فلاسفه‌مان، فلاسفه‌تان، فلاسفه‌شان
                            label += 'b2'   # فلاسفه‌ام، فلاسفه‌ای، فلاسفه‌ایم، فلاسفه‌اید، فلاسفه‌اند
                            label += 'hz'   # فلاسفه‌ی، فلاسفهٔ
                            label += 'y2'   # فلاسفه‌ای
                        else:
                            label += ''     # اشربه
                            
                    elif word.endswith(PERSIAN_YE):
                        label += 'z3'   # فتاوی‌ام، فتاوی‌ات، فتاوی‌اش، فتاوی‌مان، فتاوی‌تان، فتاوی‌شان
                        label += 'b2'   # فتاوی‌ام، فتاوی‌ای، فتاوی‌ایم، فتاوی‌اید، فتاوی‌اند
                        label += 'y2'   # فتاوی‌ای
                        
                    elif word.endswith(PERSIAN_WAW):
                        debug('unpredicted case for: ' + word + ':' + pos)
                        label += ''
                        
                    elif word.endswith(PERSIAN_ALEF):
                        label += 'z2'   # هدایایم، هدایایت، هدایایش، هدایایمان، هدایایتان، هدایایشان
                        label += 'b3'   # هدایایم، هدایایی، هدایاست، هدایاییم، هدایایید، هدایایند
                        label += 'y1'   # هدایای
                        label += 'y3'   # هدایایی
                        
                    elif word.endswith(PERSIAN_TA) or \
                         word.endswith(PERSIAN_ZA):
                        label += 'z1'   # اقساطم، اقساطت، اقساطش، اقساطمان، اقساطتان، اقساطشان
                        label += 'b1'   # اقساطم، اقساطی، اقساطست، اقساطیم، اقساطید، اقساطند
                        label += 'y1'   # اقساطی
                        # label += 'an'   # [???]
                        
                    elif word.endswith(PERSIAN_DETACHED):
                        label += 'z1'   # آثارم، آثارت، آثارش، آثارمان، آثارتان، آثارشان
                        label += 'b1'   # آثارم، آثاری، آثارست، آثاریم، آثارید، آثارند
                        label += 'y1'   # آثاری
                        
                    else:
                        label += 'z1'   # احزابم، احزابت، احزابش، احزابمان، احزابتان، احزابشان
                        label += 'b1'   # احزابم، احزابی، احزابست، احزابیم، احزابید، احزابند
                        label += 'y1'   # احزابی

                elif pos == 'noun_proper_singular':
                    if word.endswith(PERSIAN_HE):
                        if ends_with_aah_uh:
                            label += 'z1'   # کرمانشاهم، کرمانشاهت، کرمانشاهش، کرمانشاهمان، کرمانشاهتان، کرمانشاهشان
                            label += 'b4'   # کرمانشاهم، کرمانشاهی، کرمانشاهیم، کرمانشاهید، کرمانشاهند
                            label += 'z5'   # کرمانشاه‌هایم، کرمانشاه‌هایت، کرمانشاه‌هایش، کرمانشاه‌هایمان، کرمانشاه‌هایتان، کرمانشاه‌هایشان
                            label += 'j2'   # کرمانشاه‌ها
                            label += 'j4'   # کرمانشاه‌های
                            label += 'j6'   # کرمانشاه‌هایی
                            label += 'j8'   # کرمانشاه‌هاست
                            label += 'y1'   # کرمانشاهی
                        elif  ends_with_vowel:
                            label += 'z3'   # آباده‌ام، آباده‌ات، آباده‌اش، آباده‌مان، آباده‌تان، آباده‌شان
                            label += 'b2'   # آباده‌ام، آباده‌ای، آباده‌ایم، آباده‌اید، آباده‌اند
                            label += 'z5'   # آباده‌هایم، آباده‌هایت، آباده‌هایش، آباده‌هایمان، آباده‌هایتان، آباده‌هایشان
                            label += 'j2'   # آباده‌ها
                            label += 'j4'   # آباده‌های
                            label += 'j6'   # آباده‌هایی
                            label += 'j8'   # آباده‌هاست
                            label += 'y2'   # آباده‌ای
                            label += 'hz'   # آباده‌ی، آبادهٔ
                        else:
                                            # [???] 
                                            # عبده -> abdoh 
                            label += 'z3'   # عبده‌ام، عبده‌ات، عبده‌اش، عبده‌مان، عبده‌تان، عبده‌شان
                            label += 'b2'   # عبده‌ام، عبده‌ای، عبده‌ایم، عبده‌اید، عبده‌اند
                            label += 'z5'   # عبده‌هایم، عبده‌هایت، عبده‌هایش، عبده‌هایمان، عبده‌هایتان، عبده‌هایشان
                            label += 'j2'   # عبده‌ها
                            label += 'j4'   # عبده‌های
                            label += 'j6'   # عبده‌هایی
                            label += 'j8'   # عبده‌هاست
                            label += 'y2'   # عبده‌ای

                    elif word.endswith(PERSIAN_WAW):
                        if ends_with_vowel:
                            label += 'z2'   # باکویم، باکویت، باکویش، باکویمان، باکویتان، باکویشان
                            label += 'b3'   # باکویم، باکویی، باکوست، باکوییم، باکویید، باکویند
                            label += 'z4'   # باکوهایم، باکوهایت، باکوهایش، باکوهایمان، باکوهایتان، باکوهایشان
                            label += 'j1'   # باکوها
                            label += 'j3'   # باکوهای
                            label += 'j5'   # باکوهایی
                            label += 'j7'   # باکوهاست
                            label += 'y1'   # باکوی
                            label += 'y3'   # باکویی
                        else:
                            label += 'z1'   # آپولوم، آپولوت، آپولوش، آپولومان، آپولوتان، آپولوشان
                            label += 'b4'   # آپولوم، آپولوی، آپولویم، آپولوید، آپولوند
                            label += 'z4'   # آپولوهایم، آپولوهایت، آپولوهایش، آپولوهایمان، آپولوهایتان، آپولوهایشان
                            label += 'j1'   # آپولوها
                            label += 'j3'   # آپولوهای
                            label += 'j5'   # آپولوهایی
                            label += 'j7'   # آپولوهاست
                            label += 'y1'   # آپولوی

                    elif word.endswith(PERSIAN_YE):
                        label += 'z3'   # آبادانی‌ام، آبادانی‌ات، آبادانی‌اش، آبادانی‌مان، آبادانی‌تان، آبادانی‌شان
                        label += 'b2'   # آبادانی‌ام، آبادانی‌ای، آبادانی‌ایم، آبادانی‌اید، آبادانی‌اند
                        label += 'z5'   # آبادانی‌هایم، آبادانی‌هایت، آبادانی‌هایش، آبادانی‌هایمان، آبادانی‌هایتان، آبادانی‌هایشان
                        label += 'j2'   # آبادانی‌ها
                        label += 'j4'   # آبادانی‌های
                        label += 'j6'   # آبادانی‌هایی
                        label += 'j8'   # آبادانی‌هاست
                        label += 'y2'   # آبادانی‌ای

                    elif word.endswith(PERSIAN_ALEF):
                        label += 'z2'   # آپادانایم، آپادانایت، آپادانایش، آپادانایمان، آپادانایتان، آپادانایشان
                        label += 'b3'   # آپادانایم، آپادانایی، آپاداناست، آپاداناییم، آپادانایید، آپادانایند
                        label += 'z4'   # آپاداناهایم، آپاداناهایت، آپاداناهایش، آپاداناهایمان، آپاداناهایتان، آپاداناهایشان
                        label += 'j1'   # آپاداناها
                        label += 'j3'   # آپاداناهای
                        label += 'j5'   # آپاداناهایی
                        label += 'j7'   # آپاداناهاست
                        label += 'y1'   # آپادانای
                        label += 'y3'   # آپادانایی

                    elif word.endswith(PERSIAN_DETACHED):
                        label += 'z1'   # البرزم، البرزت، البرزش، البرزمان، البرزتان، البرزشان
                        label += 'b1'   # البرزم، البرزی، البرزست، البرزیم، البرزید، البرزند
                        label += 'z4'   # البرزهایم، البرزهایت، البرزهایش، البرزهایمان، البرزهایتان، البرزهایشان
                        label += 'j1'   # البرزها
                        label += 'j3'   # البرزهای
                        label += 'j5'   # البرزهایی
                        label += 'j7'   # البرزهاست
                        label += 'y1'   # البرزی

                    elif word.endswith(PERSIAN_TA) or \
                         word.endswith(PERSIAN_ZA):
                        label += 'z1'   # بقراطم، بقراطت، بقراطش، بقراطمان، بقراطتان، بقراطشان
                        label += 'b1'   # بقراطم، بقراطی، بقراطست، بقراطیم، بقراطید، بقراطند
                        label += 'z5'   # بقراط‌هایم، بقراط‌هایت، بقراط‌هایش، بقراط‌هایمان، بقراط‌هایتان، بقراط‌هایشان
                        label += 'j2'   # بقراط‌ها
                        label += 'j4'   # بقراط‌های
                        label += 'j6'   # بقراط‌هایی
                        label += 'j8'   # بقراط‌هاست
                        label += 'y1'   # بقراطی
                        # label += 'an'   # [???]
                        
                    else:
                        label += 'z1'   # بنابم، بنابت، بنابش، بنابمان، بنابتان، بنابشان
                        label += 'b1'   # بنابم، بنابی، بنابست، بنابیم، بنابید، بنابند
                        label += 'z5'   # بناب‌هایم، بناب‌هایت، بناب‌هایش، بناب‌هایمان، بناب‌هایتان، بناب‌هایشان
                        label += 'j2'   # بناب‌ها
                        label += 'j4'   # بناب‌های
                        label += 'j6'   # بناب‌هایی
                        label += 'j8'   # بناب‌هاست
                        label += 'y1'   # بنابی

                elif pos == 'noun_proper_plural':
                    if word.endswith(PERSIAN_HE):
                        if ends_with_aah_uh:
                            debug('unpredicted case for: ' + word + ':' + pos)
                        elif  ends_with_vowel:
                            label += 'z3'   # ارامنه‌ام، ارامنه‌ات، ارامنه‌اش، ارامنه‌مان، ارامنه‌تان، ارامنه‌شان
                            label += 'b2'   # ارامنه‌ام، ارامنه‌ای، ارامنه‌ایم، ارامنه‌اید، ارامنه‌اند
                            label += 'hz'   # ارامنه‌ی، ارامنهٔ
                            label += 'y2'   # ارامنه‌ای
                        else:
                            debug('unpredicted case for: ' + word + ':' + pos)

                    elif word.endswith(PERSIAN_YE):
                        debug('unpredicted case for: ' + word + ':' + pos)
                        label += ''

                    elif word.endswith(PERSIAN_WAW):
                        debug('unpredicted case for: ' + word + ':' + pos)
                        label += ''

                    elif word.endswith(PERSIAN_ALEF):
                        debug('unpredicted case for: ' + word + ':' + pos)
                        label += ''

                    elif word.endswith(PERSIAN_DETACHED):
                        label += 'z1'   # عادم، عادت، عادش، عادمان، عادتان، عادشان
                        label += 'b1'   # عادم، عادی، عادست، عادیم، عادید، عادند
                        label += 'y1'   # عادی
                    
                    elif word.endswith(PERSIAN_TA) or \
                         word.endswith(PERSIAN_ZA):
                        debug('unpredicted case for: ' + word + ':' + pos)
                        label += ''
                        
                    else:
                        label += 'z1'   # اماراتم، اماراتت، اماراتش، اماراتمان، اماراتتان، اماراتشان
                        label += 'b1'   # اماراتم، اماراتی، اماراتست، اماراتیم، اماراتید، اماراتند
                        label += 'y1'   # اماراتی

        #################################################################################################
        # ADJECTIVE                                                                                     #
        #################################################################################################
                elif pos == 'adjective_positive':
                    if word.endswith(PERSIAN_HE):
                        if ends_with_aah_uh:
                            label += 'z1'   # کوتاهم، کوتاهت، کوتاهش، کوتاهمان، کوتاهتان، کوتاهشان
                                            # باشکوهم، باشکوهت، باشکوهش، باشکوهمان، باشکوهتان، باشکوهشان
                            label += 'b4'   # کوتاهم، کوتاهی، کوتاهیم، کوتاهید، کوتاهند
                                            # باشکوهم، باشکوهی، باشکوهیم، باشکوهید، باشکوهند
                            label += 'y1'   # کوتاهی، باشکوهی
                            label += 'j2'   # کوتاه‌ها، باشکوه‌ها
                            label += 'j4'   # کوتاه‌های، باشکوه‌های
                            label += 'j8'   # کوتاه‌هاست، باشکوه‌هاست
                            label += 't2'   # کوتاه‌تر، کوتاه‌ترین
                                            # باشکوه‌تر، باشکوه‌ترین
                                            # کوتاه‌تری، باشکوه‌تری
                                            # کوتاه‌ترها، کوتاه‌ترهای
                                            # باشکوه‌ترها، باشکوه‌ترهای
                                            # کوتاه‌ترین‌ها، کوتاه‌ترین‌های
                                            # باشکوه‌ترین‌ها، باشکوه‌ترین‌های
                        elif ends_with_vowel:
                            label += 'z3'   # شایسته‌ام، شایسته‌ات، شایسته‌اش، شایسته‌مان، شایسته‌تان، شایسته‌شان
                            label += 'b2'   # شایسته‌ام، شایسته‌ای، شایسته‌ایم، شایسته‌اید، شایسته‌اند
                            label += 'hz'   # شایسته‌ی، شایستهٔ
                            label += 'j2'   # شایسته‌ها
                            label += 'j4'   # شایسته‌های
                            label += 'j8'   # شایسته‌هاست
                            label += 't2'   # شایسته‌تر، شایسته‌ترین
                                            # شایسته‌تری
                                            # شایسته‌ترها، شایسته‌ترهای
                                            # شایسته‌ترین‌ها، شایسته‌ترین‌های
                        else:
                            label += 'z3'   # کوته‌ام، کوته‌ات، کوته‌اش، کوته‌مان، کوته‌تان، کوته‌شان
                            label += 'b2'   # کوته‌ام، کوته‌ای، کوته‌ایم، کوته‌اید، کوته‌اند
                            label += 'y1'   # کوتهی
                            label += 'j2'   # کوته‌ها
                            label += 'j4'   # کوته‌های
                            label += 'j8'   # کوته‌هاست
                            label += 't2'   # کوته‌تر، کوته‌ترین
                                            # کوته‌تری
                                            # کوته‌ترها، کوته‌ترهای
                                            # کوته‌ترین‌ها، کوته‌ترین‌های

                    elif word.endswith(PERSIAN_WAW):
                        if ends_with_vowel:
                            label += 'z2'   # پررویم، پررویت، پررویش، پررویمان، پررویتان، پررویشان
                            label += 'b3'   # پررویم، پررویی، پرروست، پرروییم، پررویید، پررویند
                            label += 'y1'   # پرروی
                            label += 'y3'   # پررویی
                            label += 'j1'   # پرروها
                            label += 'j3'   # پرروهای
                            label += 'j7'   # پرروهاست
                            label += 't1'   # پرروتر، پرروترین
                                            # پرروتری
                                            # پرروترها، پرروترهای
                                            # پرروترین‌ها، پرروترین‌های
                        else:
                            label += 'z1'   # کنجکاوم، کنجکاوت، کنجکاوش، کنجکاومان، کنجکاوتان، کنجکاوشان
                            label += 'b4'   # کنجکاوم، کنجکاوی، کنجکاویم، کنجکاوید، کنجکاوند
                            label += 'y1'   # کنجکاوی
                            label += 'j1'   # کنجکاوها
                            label += 'j3'   # کنجکاوهای
                            label += 'j7'   # کنجکاوهاست
                            label += 't1'   # کنجکاوتر، کنجکاوترین
                                            # کنجکاوتری
                                            # کنجکاوترها، کنجکاوترهای
                                            # کنجکاوترین‌ها، کنجکاوترین‌های
                            label += 'an'   # کنجکاوان، کنجکاوانی

                    elif word.endswith(PERSIAN_YE):
                        label += 'z3'   # عالی‌ام، عالی‌ات، عالی‌اش، عالی‌مان، عالی‌تان، عالی‌شان
                        label += 'b2'   # عالی‌ام، عالی‌ای، عالی‌ایم، عالی‌اید، عالی‌اند
                        label += 'y2'   # عالی‌ای
                        label += 'j2'   # عالی‌ها
                        label += 'j4'   # عالی‌های
                        label += 'j8'   # عالی‌هاست
                        label += 't2'   # عالی‌تر، عالی‌ترین
                                        # عالی‌تری
                                        # عالی‌ترها، عالی‌ترهای
                                        # عالی‌ترین‌ها، عالی‌ترین‌های

                    elif word.endswith(PERSIAN_ALEF):
                        label += 'z2'   # اعلایم، اعلایت، اعلایش، اعلایمان، اعلایتان، اعلایشان
                        label += 'b3'   # اعلایم، اعلایی، اعلاست، اعلاییم، اعلایید، اعلایند
                        label += 'y1'   # اعلای
                        label += 'y3'   # اعلایی
                        label += 'j1'   # اعلاها
                        label += 'j3'   # اعلاهای
                        label += 'j7'   # اعلاهاست
                        label += 't1'   # اعلاتر، اعلاترین
                                        # اعلاتری
                                        # اعلاترها، اعلاترهای
                                        # اعلاترین‌ها، اعلاترین‌های

                    elif word.endswith(PERSIAN_DETACHED):
                        label += 'z1'   # آبادم، آبادت، آبادش، آبادمان، آبادتان، آبادشان
                        label += 'b1'   # آبادم، آبادی، آبادست، آبادیم، آبادید، آبادند
                        label += 'y1'   # آبادی
                        label += 'j1'   # آبادها
                        label += 'j3'   # آبادهای
                        label += 'j7'   # آبادهاست
                        label += 't1'   # آبادتر، آبادترین
                                        # آبادتری
                                        # آبادترها، آبادترهای
                                        # آبادترین‌ها، آبادترین‌های
                        label += 'an'   # آبادان، تنومندان، آبادانی، تنومندانی
                    
                    elif word.endswith(PERSIAN_TA) or \
                         word.endswith(PERSIAN_ZA):
                        label += 'z1'   # بانشاطم، بانشاطت، بانشاطش، بانشاطمان، بانشاطتان، بانشاطشان
                        label += 'b1'   # بانشاطم، بانشاطی، بانشاطست، بانشاطیم، بانشاطید، بانشاطند
                        label += 'y1'   # بانشاطی
                        label += 'j2'   # بانشاط‌ها
                        label += 'j4'   # بانشاط‌های
                        label += 'j8'   # بانشاط‌هاست
                        label += 't1'   # بانشاطتر، بانشاطترین
                                        # بانشاطتری
                                        # بانشاطترها، بانشاطترهای
                                        # بانشاطترین‌ها، بانشاطترین‌های
                        label += 't2'   # بانشاط‌تر، بانشاط‌ترین
                                        # بانشاط‌تری
                                        # بانشاط‌ترها، بانشاط‌ترهای
                                        # بانشاط‌ترین‌ها، بانشاط‌ترین‌های
                        label += 'an'   # بانشاطان، بانشاطانی
                        
                    else:
                        label += 'z1'   # مرتبم، مرتبت، مرتبش، مرتبمان، مرتبتان، مرتبشان
                        label += 'b1'   # مرتبم، مرتبی، مرتبست، مرتبیم، مرتبید، مرتبند
                        label += 'y1'   # مرتبی
                        label += 'j2'   # مرتب‌ها
                        label += 'j4'   # مرتب‌های
                        label += 'j8'   # مرتب‌هاست
                        label += 't2'   # مرتب‌تر، مرتب‌ترین
                                        # مرتب‌تری
                                        # مرتب‌ترها، مرتب‌ترهای
                                        # مرتب‌ترین‌ها، مرتب‌ترین‌های
                        label += 'an'   # خوبان، خوبانی
                        if kam_dandane:
                            label += 'j1'   # مرتبها
                            label += 'j3'   # مرتبهای
                            label += 'j7'   # مرتبهاست
                            label += 't1'   # مرتبتر، مرتبترین
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
                        debug('unpredicted case for: ' + word + ':' + pos)
                        label += ''

                    elif word.endswith(PERSIAN_DETACHED):
                        label += 'z1'   # ارشدم، ارشدت، ارشدش، ارشدمان، ارشدتان، ارشدشان
                        label += 'b1'   # ارشدم، ارشدی، ارشدست، ارشدیم، ارشدید، ارشدند
                        label += 'y1'   # ارشدی
                        label += 'j1'   # ارشدها
                        label += 'j3'   # ارشدهای
                        label += 'j7'   # ارشدهاست

                    elif word.endswith(PERSIAN_TA) or \
                         word.endswith(PERSIAN_ZA):
                        debug('unpredicted case for: ' + word + ':' + pos)
                        
                    else:
                        label += 'z1'   # افزونم، افزونت، افزونش، افزونمان، افزونتان، افزونشان
                        label += 'b1'   # افزونم، افزونی، افزونست، افزونیم، افزونید، افزونند
                        label += 'y1'   # افزونی
                        label += 'j2'   # افزون‌ها
                        label += 'j4'   # افزون‌های
                        ## label += 'j8'   # [???] افزون‌هاست 

                        
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
                        label += 'z1'   # اولی‌ترم، اولی‌ترت، اولی‌ترش، اولی‌ترمان، اولی‌ترتان، اولی‌ترشان
                        label += 'b1'   # اولی‌ترم، اولی‌تری، اولی‌ترست، اولی‌تریم، اولی‌ترید، اولی‌ترند
                        label += 'y1'   # اولی‌تری
                        label += 'j1'   # اولی‌ترها
                        label += 'j3'   # اولی‌ترهای
                        label += 'j7'   # اولی‌ترهاست
                    
                    elif word.endswith(PERSIAN_TA) or \
                         word.endswith(PERSIAN_ZA):
                        debug('unpredicted case for: ' + word + ':' + pos)
                        
                    else:
                        label += 'z1'   # بهترینم، بهترینت، بهترینش، بهترینمان، بهترینتان، بهترینشان
                        label += 'b1'   # بهترینم، بهترینی، بهترینست، بهترینیم، بهترینید، بهترینند
                        label += 'y1'   # بهترینی
                        label += 'j2'   # بهترین‌ها
                        label += 'j4'   # بهترین‌های
                        label += 'j8'   # بهترین‌هاست

        #################################################################################################
        # ADVERB                                                                                        #
        #################################################################################################
                elif pos == 'adverb':
                    label += ''

        #################################################################################################
        # PRONOUN                                                                                       #
        #################################################################################################
                elif pos == 'pronoun':
                    if word.endswith(PERSIAN_HE):
                        if ends_with_aah_uh:
                            debug('unpredicted case for: ' + word + ':' + pos)
                            label += ''
                        elif  ends_with_vowel:
                            label += 'b2'   # آنچه‌ام، آنچه‌ای، آنچه‌ایم، آنچه‌اید، آنچه‌اند
                        else:
                            label += ''

                    elif word.endswith(PERSIAN_WAW):
                        if ends_with_vowel:
                            label += 'b3'   # همویم، همویی، هموست، هموییم، همویید، همویند 
                        else:
                            label += ''     # تو

                    elif word.endswith(PERSIAN_YE):
                        ### label += 'z1'   # [???]  بعضی‌مان، بعضی‌تان، بعضی‌شان
                        label += 'b2'   # چی‌ام، چی‌ای، چی‌ایم، چی‌اید، چی‌اند

                    elif word.endswith(PERSIAN_ALEF):
                        label += 'b3'   # آنهایم، آنهایی، آنهاست، آنهاییم، آنهایید، آنهایند

                    elif word.endswith(PERSIAN_DETACHED):
                        label += 'b1'   # دگرم، دگری، دگرست، دگریم، دگرید، دگرند

                    else:
                        label += 'b1'   # آنم، آنی، آنست، آنیم، آنید، آنند

        #################################################################################################
        # NUMBER                                                                                        #
        #################################################################################################
                elif pos == 'number':
                    label += ''

        #################################################################################################
        # NEDA                                                                                          #
        #################################################################################################
                elif pos == 'neda':
                    label += ''

        #################################################################################################
        # PREPOSITION                                                                                   #
        #################################################################################################
                elif pos == 'preposition':
                    label += ''

        #################################################################################################
        # CONJUNCTION                                                                                   #
        #################################################################################################
                elif pos == 'conjunction':
                    label += ''

        #################################################################################################
        # ARABIC                                                                                        #
        #################################################################################################
                elif pos == 'arabic':
                    if word.endswith(PERSIAN_HE):
                        label += ''

                    else:
                        label += 'y1'   # طرفة‌العینی

                else:
                    debug('{0} {1}: unknown tag'.format(word, pos))

                # offensive word
                if offensive:
                    label += '!!'

                if label:
                    words.add(word+'/'+label)
                else:
                    words.add(word)

        # import user dictionary
        with open('dic_users', 'r', encoding='utf-8') as f:
            for line in f.readlines():
                word = line[:-1].strip()

                if word.startswith('#'):
                    continue
                    
                if not word:
                    continue

                if word not in self.dictionary:
                    #debug(word)
                    words.add(word)
 
        # sort word list
        words_s = sorted(words)

        remove('../build/fa_IR.dic')
        with open('../build/fa_IR.dic', 'w', encoding='utf-8', newline='') as f:
            f.write('{0}\n'.format(len(words_s)))
            for word in words_s:
                f.write(word + '\n')

        # letter frequency
        letters = collections.defaultdict(int)
        for word in words:
            for letter in word:
                if letter == '/':
                    break;

                letters[letter] += 1

        # sorted tuples
        letters_s = sorted(letters.items(), key=operator.itemgetter(1))
        letters_s.reverse()

        affix = ''
        with open('affixes', 'r', encoding='utf-8') as f:
            affix = f.read()

        remove('../build/fa_IR.aff')
        with open('../build/fa_IR.aff', 'w', encoding='utf-8', newline='') as f:
            frequency = ''
            for letter in letters_s:
                frequency += letter[0]

            f.write(affix.format(VERSIAN, datetime.datetime.now().strftime("%Y-%m-%d"), frequency))

        # dict_delta (foreign words)
        ################ shutil.copy('dic_delta', '../build/fa_IR.dic_delta')
        dic_delta = set()
        with open('dic_delta', 'r', encoding='utf-8') as f:
            for line in f.readlines():
                word = line[:-1].strip()

                if word.startswith('#'):
                    continue
                    
                if not word:
                    continue

                if word not in self.dictionary:
                    #debug(word)
                    dic_delta.add(word)
        
        dic_delta_s = sorted(dic_delta)
        
        remove('../build/fa_IR.dic_delta')
        with open('../build/fa_IR.dic_delta', 'w', encoding='utf-8', newline='') as f:
            for word in dic_delta_s:
                f.write(word + '\n')
                

if __name__ == '__main__':
    p = Parser()
    p.read_lexicon('lexicon')
    p.pars()

