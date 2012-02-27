# -*- coding: utf-8 -*-

from random import randint

phrases = [phrase.strip() for phrase in open("frazy.txt")]
phrase = phrases[randint(0, len(phrases) - 1)]
masked = " ".join(["_" * len(i) for i in phrase.split(" ")])
hits = set()
misses = set()

def won(entry):
    return phrase == entry or "_" not in masked

def draw_gallows(round, entry):
    gallows = ""
    if round >= 1:
        gallows += "____\n"
    gallows += "|{0} {1}   p: {2}\n".format(
        round >= 2 and '/' or ' ',
        round >= 3 and '|' or ' ',
        masked
    )
    gallows += "|  {0}   h: {1}\n".format(
        round >= 4 and '0' or ' ',
        ", ".join(hits)
    )
    gallows += "| {1}{0}{2}  m: {3}\n".format(
        round >= 5 and '|' or ' ',
        round >= 6 and '/' or ' ',
        round >= 7 and '\\' or ' ',
        ", ".join(misses)
    )
    gallows += "| {0} {1}  {2}\n".format(
        round >= 8 and '/' or ' ',
        round >= 9 and '\\' or ' ',
        won(entry) and "YOU WON" or (round == 9 and "YOU LOST" or "IN GAME")
    )
    gallows += "|_ _"
    print(gallows)

round = 0
while True:
    entry = raw_input("Enter a letter or password: ")
    if len(entry) == 1:
        if entry in phrase:
            hits.add(entry)
            indexes = [i for i, c in enumerate(phrase) if c == entry]
            masked = "".join([
                i in indexes and phrase[i] or c for i, c in enumerate(masked)
            ])
        else:
            misses.add(entry)
            round += 1
    elif won(entry):
        masked = entry
    elif not won(entry):
        round += 1
    draw_gallows(round, entry)
    if won(entry) or round == 9:
        break
