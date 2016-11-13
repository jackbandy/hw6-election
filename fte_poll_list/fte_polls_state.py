from urlparse import urlparse
import urllib2
from bs4 import BeautifulSoup
import mmap


#html =
'''
            <tr class="">
				<td class="lp-race"><a href="/epolls/2016/president/fl/florida_trump_vs_clinton_vs_johnson_vs_stein-5963.html">Florida: Trump vs. Clinton vs. Johnson vs. Stein</a></td>
				<td class="lp-poll"><a href="https://poll.qu.edu/images/polling/ps/ps11072016.pdf/">Quinnipiac</a></td>
				<td class="lp-results"><a href="/epolls/2016/president/fl/florida_trump_vs_clinton_vs_johnson_vs_stein-5963.html">Trump 45, Clinton 46, Johnson 2, Stein 1</a></td>
				<td class="lp-spread"><font color="black"><span class="dem">Clinton +1</span></font></td>
			</tr>
			<tr class="alt">
				<td class="lp-race"><a href="/epolls/2016/president/fl/florida_trump_vs_clinton_vs_johnson_vs_stein-5963.html">Florida: Trump vs. Clinton vs. Johnson vs. Stein</a></td>
				<td class="lp-poll"><a href="https://www.scribd.com/document/330329594/Florida-November-3-2016-v1-1#from_embed">Gravis</a></td>
				<td class="lp-results"><a href="/epolls/2016/president/fl/florida_trump_vs_clinton_vs_johnson_vs_stein-5963.html">Trump 45, Clinton 46, Johnson 4, Stein 0</a></td>
				<td class="lp-spread"><font color="black"><span class="dem">Clinton +1</span></font></td>
			</tr>

'''
#soup = BeautifulSoup(html)

url = 'http://www.realclearpolitics.com/epolls/latest_polls/state/#'
url_file = 'rcp_poll_url_state.txt'
domain_file = 'rcp_poll_domain_state.txt'

req = urllib2.Request(url)
response = urllib2.urlopen(req, timeout=4)
html = response.read()
soup = BeautifulSoup(html, "lxml")

for tag in soup.find_all('td'):
    # poll state
    if tag.attrs['class'] == ['lp-race']:
        line = tag.text
        last_index = line.find('Trump vs. Clinton')-2
        state = ''
        for i in range(last_index):
            state = state+line[i]

    # poll url
    if tag.attrs['class'] == ['lp-poll']:
        poll_name = tag.text
        link = tag.find('a')
        poll_url = link.get('href',None)

    # poll result
    if tag.attrs['class'] == ['lp-results']:
        result=tag.text

        # result for Clinton
        cl = result.find('Clinton')
        if cl !=-1:     cl_result = result[cl+8]+result[cl+9]
        else:   cl_result=0
        # result for Trump
        tr = result.find('Trump')
        if tr !=-1:     tr_result = result[tr+6]+result[tr+7]
        else:   tr_result=0
        # result for Johnson
        jn = result.find('Johnson')
        if jn !=-1:     jn_result = result[jn+8]
        else:   jn_result=0
        # result for Stein
        st = result.find('Stein')
        if st !=-1:
            if st+6>len(result):
                st_reslt = 0
            else:
                st_result = result[st+6]
        else:   st_result=0
        # result for McMullin
        mc = result.find('McMullin')
        if mc !=-1:     mc_result = result[mc+9]+result[mc+10]
        else:   mc_result=0


        # if url is not exist in text file, append it
        with open(url_file, 'r') as fr:
            s = mmap.mmap(fr.fileno(), 0, access=mmap.ACCESS_READ)
            if s.find(poll_url) == -1:
                # append to text file
                with open(url_file, "a") as fw:
                    fw.write(poll_url+' ,'+str(tr_result)+','+str(cl_result)+',' \
                        +str(jn_result)+','+str(st_result)+','+str(mc_result)+',' \
                        +state+'\n')

        # url domain
        url_domain = urlparse(poll_url).scheme+'://'+urlparse(poll_url).netloc
        # if url domain is not exist, append it
        with open(domain_file, 'r') as fr:
            s = mmap.mmap(fr.fileno(), 0, access=mmap.ACCESS_READ)
            if s.find(url_domain) == -1:
                # append to text file
                with open(domain_file, "a") as fw:
                    fw.write(url_domain+'\n')
