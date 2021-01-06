#!/usr/bin/env python3

'''
It's a GUI version of the timer.

Created by Ivan Arzhanov (kkecher), 2020-2021.
'''

from tkinter import *
from tkinter import ttk
import time
import math
import re
from playsound import playsound
from contracts import contract, new_contract


match_digit_form = re.compile(r'\d', flags=re.I)
match_word_form = re.compile(r'\d(\s+)?[чhмmsс]', flags=re.I)
match_hours = re.compile(r'(\d+(?:.\d+)?)(?:\s+)?[чh]', flags=re.I)
match_minutes = re.compile(r'(\d+(?:.\d+)?)(?:\s+)?[мm]', flags=re.I)
match_seconds = re.compile(r'(\d+(?:.\d+)?)(?:\s+)?[sс]', flags=re.I)

digit_form_contract = new_contract('digit_form_contract', lambda t: isinstance(t, str) and match_digit_form.search(t)!=None)
def digit_form_contract_test_cases():
    digit_form_contract.check('0:5:3')
    digit_form_contract.check('00:5:3')
    digit_form_contract.check('0:15:3')
    digit_form_contract.check('00:15:3')
    digit_form_contract.check('0:5:03')
    digit_form_contract.check('0:5:32')
    digit_form_contract.check('0:3')
    digit_form_contract.check('  0    : 3           ')
    digit_form_contract.check('0:03')
    digit_form_contract.check('0:12')
    digit_form_contract.check('00:12')
    digit_form_contract.check('5:0')
    digit_form_contract.check('05:00')
    digit_form_contract.check('180:05')
    digit_form_contract.check('00:73:300')
    digit_form_contract.check('0:0:0')
    digit_form_contract.check('2')
    digit_form_contract.check('2:')
    digit_form_contract.check(':20')
    digit_form_contract.check('-20')
    digit_form_contract.check(':15:4')
    digit_form_contract.check('4:2')
    digit_form_contract.check(':2')
    digit_form_contract.check('05:4:')
    digit_form_contract.check('100:04:')
    digit_form_contract.check(':444:')
    digit_form_contract.check('0')
    digit_form_contract.check('4:44:443:333')
    digit_form_contract.fail('foo')
    digit_form_contract.fail('bar:foo:baz')
    digit_form_contract.fail(0)
    digit_form_contract.fail(100)
    digit_form_contract.fail(-20)
digit_form_contract_test_cases()

@contract(user_time=digit_form_contract, returns='int,>=0')
def transform_digit_form_to_seconds(user_time):
    '''
    Transform time in format hh?:mm?:ss? to seconds
    '''

    user_time = ''.join(user_time.split())

    user_time = user_time.split(':')

    if len(user_time) == 1:
        user_time = ['00'] + [re.sub('\D', '', user_time[0])] + ['00']
    else:
        user_time = ['00' if t == '' else re.sub('\D', '', t) for t in user_time]

    if len(user_time) >= 3:
        user_time = user_time[:3]
    else:
        user_time.append('00')
    
    hours, minutes, seconds = abs(float(user_time[0])), abs(float(user_time[1])), abs(float(user_time[2]))

    seconds += minutes * 60
    seconds += hours * 60 * 60
    seconds = round(seconds, 0)
    return(int(seconds))

word_form_contract = new_contract('word_form_contract', lambda t: isinstance(t, str) and match_word_form.search(t)!=None)
def word_form_contract_test_cases():
    word_form_contract.check('5h')
    word_form_contract.check('50h')
    word_form_contract.check('-1245h')
    word_form_contract.check('50,5h')
    word_form_contract.check('50,455h')
    word_form_contract.check('0h')
    word_form_contract.check('0.5h')
    word_form_contract.check('0545hm')
    word_form_contract.check('   000034      часть')
    word_form_contract.check('Саша шла по шоссе 5часов       7       minetovand5с')

    word_form_contract.check('5 h')
    word_form_contract.check('50 h')
    word_form_contract.check('-1245 h')
    word_form_contract.check('50,5 h')
    word_form_contract.check('50,455 h')
    word_form_contract.check('0 h')
    word_form_contract.check('0.5 h')

    word_form_contract.check('5  h')
    word_form_contract.check('50  h')
    word_form_contract.check('-1245  h')
    word_form_contract.check('50,5  h')
    word_form_contract.check('50,455  h')
    word_form_contract.check('0  h')
    word_form_contract.check('0.5  h')

    word_form_contract.check('5hours')
    word_form_contract.check('50hours')
    word_form_contract.check('-1245hours')
    word_form_contract.check('50,5hours')
    word_form_contract.check('50,455hours')
    word_form_contract.check('0hours')
    word_form_contract.check('0.5hours')

    word_form_contract.check('5 час')
    word_form_contract.check('50 час')
    word_form_contract.check('-1245 час')
    word_form_contract.check('50,5 час')
    word_form_contract.check('50,455 час')
    word_form_contract.check('0 час')
    word_form_contract.check('0.5 час')

    word_form_contract.check('5ч')
    word_form_contract.check('50ч')
    word_form_contract.check('-1245ч')
    word_form_contract.check('50,5ч')
    word_form_contract.check('50,455ч')
    word_form_contract.check('0ч')
    word_form_contract.check('0.5ч')

    word_form_contract.check('5m')
    word_form_contract.check('50m')
    word_form_contract.check('-1245m')
    word_form_contract.check('50,5m')
    word_form_contract.check('50,455m')
    word_form_contract.check('0m')
    word_form_contract.check('0.5m')
    word_form_contract.check(' 5минут5секунд эту песню я пропела')

    word_form_contract.check('5 m')
    word_form_contract.check('50 m')
    word_form_contract.check('-1245 m')
    word_form_contract.check('50,5 m')
    word_form_contract.check('50,455 m')
    word_form_contract.check('0 m')
    word_form_contract.check('0.5 m')

    word_form_contract.check('5     minutes')
    word_form_contract.check('50     minutes')
    word_form_contract.check('-1245     minutes')
    word_form_contract.check('50,5     minutes')
    word_form_contract.check('50,455     minutes')
    word_form_contract.check('0     minutes')
    word_form_contract.check('0.5     minutes')

    word_form_contract.check('5минут')
    word_form_contract.check('50минут')
    word_form_contract.check('-1245минут')
    word_form_contract.check('50,5минут')
    word_form_contract.check('50,455минут')
    word_form_contract.check('0минут')
    word_form_contract.check('0.5минут')

    word_form_contract.check('5 м')
    word_form_contract.check('50 м')
    word_form_contract.check('-1245 м')
    word_form_contract.check('50,5 м')
    word_form_contract.check('50,455 м')
    word_form_contract.check('0 м')
    word_form_contract.check('0.5 м')

    word_form_contract.check('5s')
    word_form_contract.check('50s')
    word_form_contract.check('-1245s')
    word_form_contract.check('50,5s')
    word_form_contract.check('50,455s')
    word_form_contract.check('0s')
    word_form_contract.check('sadfsdafsdf54s')
    word_form_contract.check('5  s;slafjls;adfkj')

    word_form_contract.check('5   sec')
    word_form_contract.check('50   sec')
    word_form_contract.check('-1245   sec')
    word_form_contract.check('50,5   sec')
    word_form_contract.check('50,455   sec')
    word_form_contract.check('0   sec')

    word_form_contract.check('5  секу')
    word_form_contract.check('50  секу')
    word_form_contract.check('-1245  секу')
    word_form_contract.check('50,5  секу')
    word_form_contract.check('50,455  секу')
    word_form_contract.check('0  секу')

    word_form_contract.check('5с')
    word_form_contract.check('50с')
    word_form_contract.check('-1245с')
    word_form_contract.check('50,5с')
    word_form_contract.check('50,455с')
    word_form_contract.check('0с')
    word_form_contract.fail('5')

    word_form_contract.fail(-20)
    word_form_contract.fail('5afd')
    word_form_contract.fail('час')
    word_form_contract.fail('min')
    word_form_contract.fail('0:5:0')
    word_form_contract.fail('')
    word_form_contract.fail('')
word_form_contract_test_cases()

@contract(user_time=word_form_contract, returns='int,>=0')
def transform_word_form_to_seconds(user_time):
    '''
    Transform word form of time to seconds, e.g. 1sec = 1, 1.5 h = 5400, etc.
    '''
    seconds = 0

    hours_word_form = match_hours.search(user_time)
    minutes_word_form = match_minutes.search(user_time)
    seconds_word_form = match_seconds.search(user_time)

    if hours_word_form:
        hours_word_form = hours_word_form.group(1)
        hours_word_form = hours_word_form.replace(',', '.')
        hours_digit_form = float(hours_word_form)
        seconds += hours_digit_form * 60 * 60

    if minutes_word_form:
        minutes_word_form = minutes_word_form.group(1)
        minutes_word_form = minutes_word_form.replace(',', '.')
        minutes_digit_form = float(minutes_word_form)
        seconds += minutes_digit_form * 60

    if seconds_word_form:
        seconds_word_form = seconds_word_form.group(1)
        seconds_word_form = seconds_word_form.replace(',', '.')
        seconds_digit_form = float(seconds_word_form)
        seconds += seconds_digit_form

    seconds = round(seconds, 0)
    return(int(seconds))

def countdown(*args):
    '''
    Decrease user_time to 0.
    '''
    while True:
        user_time = time_.get()
        if match_word_form.search(user_time):
            seconds = transform_word_form_to_seconds(user_time)
        elif match_digit_form.search(user_time):
            seconds = transform_digit_form_to_seconds(user_time)
        else:
            print('Couldn\'t recognise input! Try again.')
            continue
        break

    start_time = round(time.perf_counter(), 0)
    end_time = start_time + seconds
    while start_time != end_time:
        if round(time.perf_counter(), 0) - start_time == 1.0:
            start_time += 1
            seconds -= 1
            print_pretty_time(seconds)

@contract(seconds='int,>=0', returns='str')
def print_pretty_time(seconds):
    '''
    Print seconds in format HH:MM:SS
    '''
    hours = seconds // 60 // 60
    if hours < 10:
        hours = '0' + str(hours)
    else:
        hours = str(hours)
    minutes = '0' + str(seconds // 60 % 60)
    seconds = '0' + str(seconds % 60)

    pretty_time = hours + ':' + minutes[-2:] + ':' + seconds[-2:]
    print(pretty_time)

    return(pretty_time)

#user_time = input('Enter user_time to count down: ')
#countdown(seconds)
#print()
#print('It\'s time to have a rest! You should consider changing type of your activity to mental or phisical.')
#while True:
#    playsound('Christmas.mp3')

if __name__ == '__main__': #doesn't start tkinter if the module was imported by unittest
    root = Tk()
    root.title("Timer by kkecher")
    
    mainframe = ttk.Frame(root, padding=10)
    mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)
    
    time_ = StringVar()
    time_entry = ttk.Entry(mainframe, textvariable=time_)
    time_entry.grid(column=0, row=0, padx=5, pady=5)
    
    #TBD: start_button is inactive while seconds == ''
    #TBD: bind start_button to `ENTER`
    #TBD: check if all elements correct expand with window expanding
    start_button = ttk.Button(mainframe, text='GO', command=countdown)
    start_button.grid(column=1, row=0, padx=5, pady=5)
    
    root.bind('<Return>', lambda e: start_button.invoke())
    time_entry.focus()
    root.mainloop()
