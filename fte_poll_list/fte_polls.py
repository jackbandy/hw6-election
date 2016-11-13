import numpy as np

polls=np.genfromtxt('fte_polls.csv', dtype=np.str, delimiter='\n')

nat_polls_file = open('fte_polls.txt','w')
nat_polls_file.write('url,trump,clinton,johnson,stein,mcmullin\n')
state_polls_file = open('fte_polls_state.txt','w')
nat_polls_file.write('url,trump,clinton,johnson,stein,mcmullin,state\n')
domains_file = open('fte_domains.txt','w')
domains = []

# for each line
for poll in polls:
    info = poll.split(',')
    matchup = info[3]
    date = info[6]

    clinton = 0
    trump = 0
    johnson = 0
    mcmullin = 0
    stein = 0
    clinton = info[13]
    trump = info[14]
    try: johnson = info[15]
    except: pass
    try: mcmullin = info[16]
    except: pass

    url = info[22]
    dot_index = url.find('.')
    slash_index = url[dot_index:].find('/')
    domain = url[:slash_index+dot_index]
    if(domain not in domains):
        domains.append(domain)
        domains_file.write(domain.replace("\"","")+"\n")

    poll_str = '{},{},{},{},{},{}'.format(
            url,trump,clinton,johnson,stein,mcmullin)
    location = info[5]
    if('U.S.' in location):
        # write to national file
        nat_polls_file.write((poll_str + '\n').replace("\"",""))
    else:
        # write to states file
        state_polls_file.write((poll_str+location + '\n').replace("\"",""))


nat_polls_file.close()
state_polls_file.close()
domains_file.close()
