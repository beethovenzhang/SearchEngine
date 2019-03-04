import os
import re
import sys
import heapq
import urlparse
import requests
import lxml.html
from retriever import Retriever
import requests.packages.urllib3
requests.packages.urllib3.disable_warnings()

####################
# GLOBAL VARIABLES #
####################

terminate_terms = set(['exit','q','quit','qq','bye','goodbye', 'zaijian', 'sayounara', 'annyeong'])
pattern = re.compile('([^\s\w]|_)+')


#############
# FUNCTIONS #
#############

def should_terminate(command):
    '''Determines whether the user wants to terminate'''
    return command in terminate_terms


def get_links(query, retriever):
    '''Get links from the retriever'''
    # Strip non-alphanumeric and convert query to lowercase
    query = pattern.sub('', query).lower()
    if not query:
        return []
    return retriever.retrieve(query.split())



def print_url(url):
    # Get webpage content
    try:
        r = requests.get(url, timeout=2)
    except requests.exceptions.MissingSchema:
        return print_url("http://{}".format(url))
    except:
        return False

    # Print URL and title
    try:
        html = lxml.html.fromstring(r.text)
        try: # Some valid webpages don't have titles
            print(html.find(".//title").text.strip())
        except:
            pass
        print(url)

        print('')
        sys.stdout.flush()
        return True

    except:
        return False


########
# MAIN #
########

if __name__ == '__main__':

    r = Retriever()
    c = raw_input('Enter a search term (q to quit): ')
    ask = True

    while not should_terminate(c):
        i = 0
        ask = True
        print('\n############ RESULTS ############\n')

        link_pq = get_links(c, r)
        for tuple in link_pq:
            link = tuple[1]

            if print_url(link):
                i += 1

            if i != 0 and i % 10 == 0:
                print('#################################\n')
                print("Press Enter to list more results.")
                c = raw_input('Enter a search term (q to quit): ')
                if c != '':
                    ask = False
                    break
                print('\n#################################\n')

        if ask:
            print('#################################\n')
            c = raw_input('Enter a search term (q to quit): ')


    print ('\n############\n# Goodbye! #\n############\n')
