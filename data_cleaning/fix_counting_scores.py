def fix_counting_scores(scores):
    for i in range(len(scores)):
        if scores[i] == '0':
            for j in range(i, len(scores)):
                scores[j] = '0'
            break
    return scores
