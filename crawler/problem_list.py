import re
import requests
import os.path
from bs4 import BeautifulSoup

CUR_DIR = os.path.dirname(os.path.realpath(__file__))
PROBLEM_LIST_PATH = 'http://vn.spoj.com/VM14/problems/round_%d'

def crawl_round(round_id):
    cur_url = PROBLEM_LIST_PATH % (round_id)
    print 'Crawling %s' % (cur_url)

    request = requests.get(cur_url)
    if request.status_code != 200:
        print 'Unable to crawl page', page
        return

    html = BeautifulSoup(request.text)
    elements = html.select('tr[class="problemrow"]')
    problems = []

    for element in elements:
        text = element.__str__().replace('\n', ' ')
        problem_re = re.compile(r'.*href="\/VM14\/problems\/(?P<id>[A-Z][A-Z0-9_]{1,7})\/.*').match(text)

        if problem_re:
            problems += [problem_re.groupdict()['id']]
        else:
            print 'Regex error', text
    return problems


all_problems = []
for round_id in xrange(1, 6):
    all_problems += crawl_round(round_id)

full_output_path = os.path.join(CUR_DIR, '..', 'output', 'problems.txt')
with open(full_output_path, 'w') as output_file:
    for problem in all_problems:
        output_file.write(problem + '\n')
