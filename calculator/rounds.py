import os.path
import json
from collections import OrderedDict

CUR_DIR = os.path.dirname(os.path.realpath(__file__))
PROBLEM_LIST_PATH = os.path.join(CUR_DIR, '..', 'output', 'problems.txt')
PROBLEM_RESULT_PATH = os.path.join(CUR_DIR, '..', 'output')
JSON_DATA_PATH = os.path.join(CUR_DIR, '..', 'js', 'data.js')

users = {}
rounds = {}
with open(PROBLEM_LIST_PATH, 'r') as f:
    problem_count = 0
    for line in f.readlines():
        problem_code = line.strip()
        round_id = 1 + problem_count / 4

        print 'Add problem %8s to round %d' % (problem_code, round_id)

        round_code = 'round' + str(round_id)
        if round_code not in users:
            users[round_code] = {}

        if round_code not in rounds:
            rounds[round_code] = []
        rounds[round_code].append(problem_code)

        with open(os.path.join(PROBLEM_RESULT_PATH, problem_code + '.txt')) as f:
            for line in f.readlines():
                user, score = line.strip().split(' ')
                score = float(score)
                if user not in users[round_code]:
                    users[round_code][user] = {}
                users[round_code][user][problem_code] = score
                users[round_code][user]['total'] = users[round_code][user].get('total', 0) + score
        problem_count += 1

for round_id in xrange(1, 6):
    round_code = 'round' + str(round_id)
    users[round_code] = users[round_code].items()

with open(JSON_DATA_PATH, 'w') as f:
    f.write('users = ')
    f.write(json.dumps(users))
    f.write(';\n')
    f.write('rounds = ')
    f.write(json.dumps(rounds))
    f.write(';\n')
