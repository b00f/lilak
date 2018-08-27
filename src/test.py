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

# -*- coding: utf-8 -*-

import hunspell
hobj = hunspell.HunSpell('../build/fa_IR.dic', '../build/fa_IR.aff')
result = open('result.log', 'w', encoding='utf-8')

detected = 0
not_detected = 0

def run_test(filename):
    global detected
    global not_detected
    
    print('processing \'{0}\' ...'.format(filename))
    result.write(filename + '\n')
    
    f = open(filename, 'r', encoding='utf-8')
    lines = f.readlines()
    for line in lines:
        
        if line.startswith('#'): # ignore comment lines
            continue
        
        tokens = line[:-1].split(' ')
        for token in tokens:
            word = token.strip((' ?.!؟»«،:؛()-"/\\\t\'…'))

            # ignore commented words
            if word.startswith('#'):
                continue
            
            if not hobj.spell(word):
                not_detected = not_detected + 1
                suggests = ''
                for s in hobj.suggest(word):
                    suggests += s
                    suggests += ', '
                result.write('{0} -> {1}\n'.format(word, suggests[:-2]))
            else:
                detected = detected + 1
            ##     stems = ''
            ##     for s in hobj.analyze(word):
            ##         stems += s.decode('utf-8')
            ##         stems += ', '
            ##     result.write('{0} -> {1}\n'.format(word, stems[:-2]))



run_test('../test/text1')
run_test('../test/text2')
run_test('../test/text3')
run_test('../test/text4')
run_test('../test/text5')
run_test('../test/text6')
run_test('../test/text7')
run_test('../test/text8')
run_test('../test/text9')
run_test('../test/text10')
run_test('../test/text11')
run_test('../test/verbs')

percentage = ((detected * 100.0) / (detected + not_detected))
result.write('detected: {0}, not_detected {1}, accuracy {2}\n'.format(detected, not_detected, percentage))
    
result.close()

