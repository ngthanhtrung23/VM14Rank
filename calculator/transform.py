import os.path
import math

CHALLENGE_SCORE = [math.log(100.0 / (i+1)) * (100.0 / math.log(100.0 / 2)) for i in range(1, 300)]
CUR_DIR = os.path.dirname(os.path.realpath(__file__))
PROBLEM_LIST_PATH = os.path.join(CUR_DIR, '..', 'output', 'problems.txt')
PROBLEM_RESULT_PATH = os.path.join(CUR_DIR, '..', 'output')


with open(PROBLEM_LIST_PATH, 'r') as f:
    problem_count = 0
    for line in f.readlines():
        problem_code = line.strip()
        round_id = 1 + problem_count / 4

        if round_id == 5 and problem_code != 'VMHEARTS':
            print 'Transform %s in round %d' % (problem_code, round_id)
            users = []

            last_score = last_actual_score = -1
            order = 0
            with open(os.path.join(PROBLEM_RESULT_PATH, problem_code + '.txt'), 'r') as f:
                for line in f.readlines():
                    user, score = line.strip().split(' ')
                    order += 1
                    score = float(score)

                    if abs(score - last_score) < 1e-6:
                        actual_score = last_actual_score
                    else:
                        actual_score = CHALLENGE_SCORE[order - 1]

                    last_score = score
                    last_actual_score = actual_score

                    users.append([user, score, actual_score])

            with open(os.path.join(PROBLEM_RESULT_PATH, problem_code + '.txt'), 'w') as f:
                for user in users:
                    f.write(user[0] + ' ' + str(user[2]) + '\n')

        problem_count += 1
