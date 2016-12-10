'''
state_tally.py
'''

import numpy as np
import pickle

#polls=np.genfromtxt('poll_list/state_poll_urls.txt', dtype=np.str,delimiter=',')
polls=np.genfromtxt('fte_poll_list/fte_polls.csv',
        dtype=np.str,delimiter='\n')
links = pickle.load(open('link_dict.pkl', 'r'))

poll_grades = {}
poll_states = {}
poll_dates = {}
for poll in polls:
    info = poll.split(',')
    url = info[22].strip("\"")
    grade = info[9]
    state = info[5]
    date = info[7]
    poll_grades[url] = grade
    poll_states[url] = state
    poll_dates[url] = date
    print("{} = {}".format(url, grade))



grade_tally = {}
state_tally = {}
date_tally = {}
misses = 0
total = 0

for a in links.keys():
    pls = links[a]
    for pl in pls:
        total +=1
        if poll_dates.get(pl): # if there's a date for pl
            if date_tally.get(poll_dates[pl]):
                date_tally[poll_dates[pl]] += 1
            else:
                date_tally[poll_dates[pl]] = 1
        else:
            misses +=1
print("misses: {} / {}".format(misses,total))
out = open("tally_dates.txt", "w")
for s in date_tally.keys():
    out.write("{}: {}\n".format(s, date_tally[s]))

out.close()

