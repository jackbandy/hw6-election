import mmap

target_file='fte_domains.txt'
merge_file='rcp_poll_domain_state.txt'

# open merge file (from file)
with open(merge_file, 'r') as mf:
    for line in mf:
        #cur_line=line.split(',')
        #url=cur_line[0]
        url = line
        # open target file
        with open (target_file, 'r') as fr:
            s = mmap.mmap(fr.fileno(), 0, access=mmap.ACCESS_READ)
            if s.find(url) == -1:
                # append to line to file
                with open(target_file, "a") as fw:
                    #fw.write(url+','+cur_line[1]+','+cur_line[2]+','+cur_line[3]+','+cur_line[4]+','+cur_line[5]+','+cur_line[6])
                    fw.write(url)
#        print(type(str(cur_line)))
