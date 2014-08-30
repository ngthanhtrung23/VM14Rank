import re
import requests
import os.path
import operator
from bs4 import BeautifulSoup
from collections import OrderedDict

CUR_DIR = os.path.dirname(os.path.realpath(__file__))
PROBLEM_LIST_PATH = os.path.join(CUR_DIR, '..', 'output', 'problems.txt')
PROBLEM_RESULT_PATH = os.path.join(CUR_DIR, '..', 'output')
SUBMISSION_PER_PAGE = 20
PROBLEM_RANK_URL = 'http://vn.spoj.com/VM14/ranks/%s/start=%d'

def crawl_problem(code):
    last_crawl = SUBMISSION_PER_PAGE
    page = 0
    users = {}
    while last_crawl == SUBMISSION_PER_PAGE:
        url = PROBLEM_RANK_URL % (code, page * SUBMISSION_PER_PAGE)
        print 'Crawling ', url

        request = requests.get(url)
        if request.status_code != 200:
            print 'Unable to crawl problem', problem_id
            break

        html = BeautifulSoup(request.text)
        elements = html.select('td[class="status_sm"]')

        last_crawl = 0
        for element in elements:
            submission = element.next.next.next
            score = submission.next.next.next

            score = str(score.text)
            score = score.replace('\n', '')
            score = score.replace('\t', '')
            space_index = score.find(' ')
            if space_index > -1:
                score = score[:space_index]
            score = float(score)

            if score == 0:
                continue

            text = submission.__str__()
            submission_re = re.compile(r'.*href="\/VM14\/users\/(?P<id>[a-z][a-z0-9_]*)\/.*').match(text)

            if submission_re:
                user_id = submission_re.groupdict()['id']
                if user_id not in users:
                    users[user_id] = score
                last_crawl += 1
            else:
                print 'Regex error', text

        page += 1


    sorted_user = OrderedDict(sorted(users.items(), key=lambda t: -t[1]))
    with open(os.path.join(PROBLEM_RESULT_PATH, problem_code + '.txt'), 'w') as f:
        for user, score in sorted_user.items():
            f.write(user + ' ' + str(score) + '\n')



with open(PROBLEM_LIST_PATH, 'r') as f:
    for l in f.readlines():
        problem_code = l.strip()
        print 'Problem: ', problem_code
        crawl_problem(problem_code)