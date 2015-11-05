##
## Lilak - The Aruma of Persian Sugar
## Copyright (C) 2015 Mostafa Sedaghat Joo (mostafa.sedaghat@gmail.com)
##
## This file is part of Lilak.
##
## Lilak is free software: you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation, either version 3 of the License, or
## (at your option) any later version.
##
## Lilak is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.
##
## You should have received a copy of the GNU General Public License
## along with Lilak.  If not, see <http://www.gnu.org/licenses/>.
##

# -*- coding: utf-8 -*-

import hunspell
hobj = hunspell.HunSpell('../build/fa-IR.dic', '../build/fa-IR.aff')
result = open('result.log', 'w', encoding='utf-8')


def run_test(filename):
    print('processing \'{0}\' ...'.format(filename))
    result.write(filename + '\n')
    
    f = open(filename, 'r', encoding='utf-8')
    lines = f.readlines()
    for line in lines:
        
        if line.startswith('#'): # ignore comment lines
            continue
        
        tokens = line[:-1].split(' ')
            
        for token in tokens:
            word = token.strip((' ?.!؟»«،:؛()-"/\\\t\''))

            # ignore commented words
            if word.startswith('#'):
                continue
            
            if not hobj.spell(word):
                suggests = ''
                for s in hobj.suggest(word):
                    suggests += s.decode('utf-8')
                    suggests += ', '
                result.write('{0} -> {1}\n'.format(word, suggests[:-2]))
            ## else:
            ##     stems = ''
            ##     for s in hobj.analyze(word):
            ##         stems += s.decode('utf-8')
            ##         stems += ', '
            ##     result.write('{0} -> {1}\n'.format(word, stems[:-2]))
                

run_test('text1')
run_test('text2')
run_test('text3')
run_test('text4')
run_test('text5')
run_test('text6')
run_test('text7')
run_test('text8')


result.close()

