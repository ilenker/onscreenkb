import time

def get_wpm(test_time_s, chr_count):
    if test_time_s == 0: return 0
    return (chr_count / 5) / (test_time_s) * 60 

def get_test_time_s(epoch):
    return time.perf_counter() - epoch 
