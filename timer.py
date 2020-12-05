'''
It's a timer.
* Accepted values >= 1 second
* Fractional seconds rounds to integer part by math rules

Created by Ivan Arzhanov (kkecher)
Dec 2020.
'''

import time
import math
import re

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

def transform_word_form_to_seconds(user_time):
    '''
    Transform word form of time to seconds, e.g. 1sec = 1, 1.5 h = 5400, etc.
    '''
    seconds = 0

    hours_word_form = re.search(r'(\d+(?:.\d+)?)(?:\s+)?[чh]', user_time, flags=re.I)
    minutes_word_form = re.search(r'(\d+(?:.\d+)?)(?:\s+)?[мm]', user_time, flags=re.I)
    seconds_word_form = re.search(r'(\d+(?:.\d+)?)(?:\s+)?[sс]', user_time, flags=re.I)

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

def countdown(seconds):
    '''
    Timer - decrease time to 0.
    '''
    if seconds < 0:
        raise ValueError('Negative seconds to countdown: ', seconds)

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

#TBD: check if time is > 1 sec
#TBD: if contain :, max len <= 8
#user_time = input('Enter user_time to count down: ')
#user_time = '5 мин'
##
#if re.search(r'[a-zа-я]', user_time, flags=re.I):
#    seconds = transform_word_form_to_seconds(user_time)
#else:
#    seconds = transform_digit_form_to_seconds(user_time)
#
#
#countdown(seconds)
