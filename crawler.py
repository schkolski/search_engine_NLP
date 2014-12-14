# -*- coding: utf-8 -*-

import urlparse
import urllib
from bs4 import BeautifulSoup
import time


def get_domain(url):
    try:
        parsed_uri = urlparse.urlparse(url)
        domain = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)
        return domain
    except Exception:
        print 'Error unicode', url
        return ''


def mak_sites(link):
    return '.mk' in link or 'macedonia' in link


def crawl(url, max_links=10000):
    urls = [url]
    visited = {url}

    point_to = []
    point_to_added = set([])
        
    c = 1

    while len(urls) > 0:
        try:
            htmltext = urllib.urlopen(urls[0]).read()

            soup = BeautifulSoup(htmltext)

            urls.pop(0)

            for tag in soup.findAll('a', href=True):
                tag['href'] = urlparse.urljoin(url, tag['href'])

                if url in tag['href'] and tag['href'] not in visited:
                    urls.append(tag['href'])
                    visited.add(tag['href'])
                    c += 1
                elif url not in tag['href'] and get_domain(tag['href']) not in point_to_added:
                    if 'http' in get_domain(tag['href']) and 'admin' not in get_domain(tag['href']):
                        point_to.append(get_domain(tag['href']))
                        point_to_added.add(get_domain(tag['href']))
        except Exception, e:
            #print 'ERROR! ' + urls[0]
            pass

        if c > max_links:
            break

    return point_to, visited


def read_urls(file_name):
    f = open(file_name, 'r')
    urls = f.read().split('\n')
    f.close()
    mk_urls = set([])  # mk_urls = set(filter(mkSites,mk_urls)
    for line in urls:
        if '.mk' in line or 'macedonia' in line:
            mk_urls.add(line)
    
    return list(mk_urls)

        
def write_crawled_urls(urls, start_url, file_name):
    f = open(file_name, 'a')
    f.write('FROM: ' + start_url + '\n')
    for u in urls:
        f.write(u + '\n')
    f.close()


def crawl_urls():
    urls_to_crawl = read_urls('urls.txt')
    from_to = {}
    for url in urls_to_crawl:
        from_to[url] = []
    
    for url in urls_to_crawl:
        point_links, crawled_links = crawl(url)
        write_crawled_urls(point_links, url, 'crawled.txt')
        from_to[url] += point_links
    return from_to
"""
##while True:
##    try:
##        crawlURLS()
##    except Exception ,e:
##        print 'error internet connection'
##        print e
##        print '-'*80
##
"""
# URL = 'http://www.macedonia.eu.org/'
#  p, v = crawl(URL, 1000)


def get_next_urls_for_crawling(mapa):
    urls = []
    for key in mapa.keys():
        urls += mapa[key]
    return filter(mak_sites, urls)


def write_to_file(file_name, option, urls):
    f = open(file_name, option)
    for u in urls:
        f.write(u + '\n')
    f.close()


def main():
    start = time.time()
    print "Crawler is started! Let's crawl the web!"
    for i in xrange(DEEP):
        print "Starting to crawl level:", i
        mapa = crawl_urls()
        urls = get_next_urls_for_crawling(mapa)
        write_to_file('urls.txt', 'w', urls)
        print "Succsessful crawled level:", i
    end = time.time()
    print 'Crawler has finished! Web is crawled! :) for ', (end - start), 'sec'
DEEP = 3

if __name__ == '__main__':
    print main()