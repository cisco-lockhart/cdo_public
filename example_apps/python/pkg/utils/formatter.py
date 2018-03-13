from sty import *

def as_in_progress_msg(msg):
    return fg.li_blue + '==> ' + fg.rs + fg.yellow + msg + fg.rs

def as_done_msg(msg):
    return fg.yellow + msg + fg.rs + fg.green + ' ' + u'\u2714' + fg.rs

def as_error_msg(msg):
    return msg + fg.red + ' ' + u'\u2715' + fg.rs

def display_in_progress_animation(msg, i):
    animation = '|/-\\'
    return msg + animation[i % len(animation)]
