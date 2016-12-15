'''
state_tally.py
'''

import numpy as np
import pickle

#polls=np.genfromtxt('poll_list/state_poll_urls.txt', dtype=np.str,delimiter=',')
polls=np.genfromtxt('fte_poll_list/fte_polls.csv',
        dtype=np.str,delimiter='\n')
links = pickle.load(open('pickle_jar/depth0_link_dict.pkl', 'r'))

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
        if poll_states.get(pl): # if there's a state for pl
            if state_tally.get(poll_states[pl]):
                state_tally[poll_states[pl]] += 1
            else:
                state_tally[poll_states[pl]] = 1
        else:
            misses +=1
print("misses: {} / {}".format(misses,total))
out = open("tally_states.txt", "w")
for s in state_tally.keys():
    out.write("{}: {}\n".format(s, state_tally[s]))

out.close()

