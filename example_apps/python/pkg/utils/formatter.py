from sty import *

def as_in_progress_msg(msg):
    return fg.li_blue + '==> ' + fg.rs + fg.yellow + ef.bold + msg + fg.rs + rs.bold

def as_done_msg(msg):
    return msg + fg.green + ' ' + u'\u2714' + rs.bold + fg.rs

def as_error_msg(msg):
    return msg + fg.red + ' ' + u'\u2715' + rs.bold + fg.rs

def display_in_progress_animation(msg, i):
    animation = '|/-\\'
    return msg + animation[i % len(animation)]
