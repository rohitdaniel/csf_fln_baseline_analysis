def fluency_score(dataframe, cols):
    fluency = 0
    score_cols = [col for col in cols if re.search(r'.+\d$', col)]
    total = total_score(dataframe[score_cols])
    duration_col = [col for col in cols if re.search(r'.+time_remaining', col)]
    duration = (60 - int(dataframe[duration_col]))
    if duration != 0:
        fluency = ((60*total)/duration)
    return fluency
