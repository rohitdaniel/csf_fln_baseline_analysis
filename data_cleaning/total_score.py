def total_score(scores):
    total_score = 0
    for score in scores:
        if  (str(score) == '1'):
            total_score += 1
    return total_score
