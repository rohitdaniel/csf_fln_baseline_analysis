def fix_scores(scores):
    for i in range(len(scores)-3):
        if (int(scores[i]) + int(scores [i+1]) + int(scores [i+2]) + int(scores [i+3])) == 0:
            for j in range(i+4, len(scores)):
                scores[j] = '0'
            break
    return scores

