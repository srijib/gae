import re, urllib
#link_re = re.compile(r'<a.*?href\s*=\s*[\'"\s]*(.*?)(?:[\'">]|$)')
link_re = re.compile(r'<img.*?src\s*=\s*[\'"\s]*(.*?)(?:[\'">]|$)')
#start_url = "http://bbs.sjtu.edu.cn/php/bbsindex.html"
start_url = "http://www.mnsfz.com"
fp = urllib.urlopen(start_url)
content = fp.read()
links = link_re.findall(content)
print len(links)
