# coding: utf-8

def replace_last_substring(s, old, new, occurrence=1):
    s = s.rsplit(old, occurrence)
    return new.join(s)
