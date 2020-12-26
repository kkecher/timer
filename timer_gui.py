#!/usr/bin/env python3

'''
It's a GUI version of the timer.
* Accepted values: >= 1 second
* Fractional seconds rounds to integer part by math rules

Created by Ivan Arzhanov (kkecher)
Dec 2020.
'''

from tkinter import *
from tkinter import ttk
import time
import math
import re
from playsound import playsound
from contracts import contract, new_contract


match_word_form = re.compile(r'\d(\s+)?[чhмmsс]', flags=re.I)
match_digit_form = re.compile(r'\d', flags=re.I)
match_hours = re.compile(r'(\d+(?:.\d+)?)(?:\s+)?[чh]', flags=re.I)
match_minutes = re.compile(r'(\d+(?:.\d+)?)(?:\s+)?[мm]', flags=re.I)
match_seconds = re.compile(r'(\d+(?:.\d+)?)(?:\s+)?[sс]', flags=re.I)

digit_form = new_contract('digit_form', lambda t: isinstance(t, str) and match_digit_form.search(t)!=None)
digit_form.check('4:2')
digit_form.check(':2')
digit_form.check('05:4:')
digit_form.check(':444:')
digit_form.check('2')
digit_form.check('-20')
digit_form.check('0')
digit_form.check('4:44:443:333')
digit_form.fail('foo')
digit_form.fail('bar:foo:baz')

@contract(user_time=digit_form, returns='int,>=0')
def transform_digit_form_to_seconds(user_time):
    '''
    Transform time in format hh:mm:ss to seconds
    '''

    if user_time[0] == ':':
        user_time = '00' + user_time
    user_time_list = user_time.split(':')
    
    while len(user_time_list) <= 3:
        user_time_list.append('0')

    hours, minutes, seconds = float(user_time_list[0]), float(user_time_list[1]), float(user_time_list[2])

    seconds += minutes * 60
    seconds += hours * 60 * 60
    return(int(seconds))

def transform_word_form_to_seconds(user_input):
    '''
    Transform word form of time to seconds, e.g. 1sec = 1, 1.5 h = 5400, etc.
    '''
    seconds = 0

    hours_word_form = match_hours.search(user_input)
    minutes_word_form = match_minutes.search(user_input)
    seconds_word_form = match_seconds.search(user_input)

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
    Timer - decrease time to 0.
    '''
    while True:
        user_input = time_.get()
        if match_word_form.search(user_input):
            seconds = transform_word_form_to_seconds(user_input)
        else:
            seconds = transform_digit_form_to_seconds(user_input)
        break

    start_time = round(time.perf_counter(), 0)
    end_time = start_time + seconds
    while start_time != end_time:
        if round(time.perf_counter(), 0) - start_time == 1.0:
            start_time += 1
            seconds -= 1
            print_pretty_time(seconds)

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
