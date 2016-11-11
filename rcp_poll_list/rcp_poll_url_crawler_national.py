from urlparse import urlparse
import urllib2
from bs4 import BeautifulSoup
import mmap


#html =
'''
            <td class="lp-race"><a href="/epolls/2016/president/us/general_election_trump_vs_clinton_vs_johnson_vs_stein-5952.html">General Election: Trump vs. Clinton vs. Johnson vs. Stein</a></td>
				<td class="lp-poll"><a href="http://www.investors.com/politics/ibd-tipp-presidential-election-poll/">IBD/TIPP Tracking</a></td>
				<td class="lp-results"><a href="/epolls/2016/president/us/general_election_trump_vs_clinton_vs_johnson_vs_stein-5952.html">Clinton 43, Trump 45, Johnson 8, Stein 2</a></td>
				<td class="lp-spread"><font color="black"><span class="rep">Trump +2</span></font></td>
			</tr>
			<tr class="alt">
				<td class="lp-race"><a href="/epolls/2016/president/us/general_election_trump_vs_clinton-5491.html">General Election: Trump vs. Clinton</a></td>
				<td class="lp-poll"><a href="http://www.investors.com/politics/ibd-tipp-presidential-election-poll/">IBD/TIPP Tracking</a></td>
				<td class="lp-results"><a href="/epolls/2016/president/us/general_election_trump_vs_clinton-5491.html">Clinton 43, Trump 42</a></td>
				<td class="lp-spread"><font color="black"><span class="dem">Clinton +1</span></font></td>
			</tr>
			<tr class="">
				<td class="lp-race"><a href="/epolls/2016/president/us/general_election_trump_vs_clinton-5491.html">General Election: Trump vs. Clinton</a></td>
				<td class="lp-poll"><a href="http://cesrusc.org/election/">LA Times/USC Tracking</a></td>
				<td class="lp-results"><a href="/epolls/2016/president/us/general_election_trump_vs_clinton-5491.html">Clinton 44, Trump 47</a></td>
				<td class="lp-spread"><font color="black"><span class="rep">Trump +3</span></font></td>
'''
#soup = BeautifulSoup(html)

url = 'http://www.realclearpolitics.com/epolls/latest_polls/president/#'
url_file = 'rcp_poll_url_national.txt'
domain_file = 'rcp_poll_domain_national.txt'

req = urllib2.Request(url)
response = urllib2.urlopen(req, timeout=4)
html = response.read()
soup = BeautifulSoup(html, "lxml")

for tag in soup.find_all('td'):
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
                        +str(jn_result)+','+str(st_result)+','+str(mc_result)+'\n')

        # url domain
        url_domain = urlparse(poll_url).scheme+'://'+urlparse(poll_url).netloc
        # if url domain is not exist, append it
        with open(domain_file, 'r') as fr:
            s = mmap.mmap(fr.fileno(), 0, access=mmap.ACCESS_READ)
            if s.find(url_domain) == -1:
                # append to text file
                with open(domain_file, "a") as fw:
                    fw.write(url_domain+'\n')
