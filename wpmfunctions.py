import time
import curses
import random

def get_wpm(chr_count, epoch):
    if get_test_time_s(epoch) == 0: return 0
    wpm = ((chr_count // 5) / ((get_test_time_s(epoch)))) * 60  
    return round(wpm) 

def get_test_time_s(epoch):
    return time.perf_counter() - epoch 

def is_test_complete(cursor_pos, sentence):
    sentence_length = 0
    for word in sentence:
            sentence_length += len(word) # don't have to count spaces because len returns 1 indexed
    if cursor_pos == sentence_length:
        return True, sentence_length
    return False, sentence_length
              
def set_cursor_visual(pane, cursor_pos):
    pane.chgat(1, cursor_pos, 1, pane.inch(1, cursor_pos) | 0b100000000000000000)

def get_messages():
    messages = []
    messages.append("well done")
    messages.append("amazing")
    messages.append("astounding")
    messages.append("bravo")
    messages.append("(^=__=^)")
    messages.append("time to stop")
    return messages

def generate_new_sentence(max_sentence_length, wordlist):
    char_total = 0
    sentence = ""
    while char_total < max_sentence_length:
        candidate_word = wordlist[random.randint(0, len(wordlist) - 1)]
        if char_total + len(candidate_word) < max_sentence_length:
            sentence += candidate_word + " "
            char_total += len(candidate_word) + 1
        else: break
    return sentence

def is_type_error(pane, cursor_position, key):
    correct_key = pane.inch(1, cursor_position)
    correct_key &= curses.A_CHARTEXT 
    if chr(correct_key) == key:
        return False
    return True

def is_next_chr(key_pane, display_pane, y, x, cursor_index):
        next_char = key_pane.inch(1, cursor_index) & curses.A_CHARTEXT
        display_char = display_pane.inch(y, x) & curses.A_CHARTEXT
        if next_char == display_char:
            return True
        return False

def clear_lines(pane, ylist):
    for y in ylist:
        pane.move(y, 0)
        pane.clrtoeol()
