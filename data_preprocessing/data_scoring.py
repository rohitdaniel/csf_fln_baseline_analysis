# Import required libraries
import regex as re

def total_score(score_cols):
    total_score = 0
    for score in score_cols:
        if  (str(score) == '1'):
            total_score += 1
    return total_score
    

def fluency_score(series, score_cols, duration_col):
    
    fluency = 0
    total = total_score(series[score_cols])

    duration = (60 - int(series[duration_col]))

    if duration != 0:
        fluency = ((60*total)/duration)
        
    return fluency


def score_data(dataframe, untimed_tasks: list, timed_tasks: list):
    """This is a docstring!"""
    
    for task in untimed_tasks:
        pattern = task + r'((?!end|tt|or|p|number|Stop|item|time|duration|strategy|b|c).)*$'
        score_cols = [col for col in dataframe.columns if re.search(pattern, col)]

        score_total = task + '_total'
        score_percent_correct = task + '_%_correct'
        dataframe.loc[:, score_total] = dataframe.apply(lambda x: total_score([x[col] for col in score_cols]), axis=1)
        dataframe.loc[:, score_percent_correct] = dataframe.apply(lambda x: 100*x[score_total]/len(score_cols), axis=1)

    for task in timed_tasks:
        score_pattern = task + r'((?!end|or|p|number|Stop|item|time|duration|strategy).)*$'
        score_cols = [col for col in dataframe.columns if re.search(score_pattern, col)]
        time_pattern = task + r'.*(time_remaining)$'
        duration_col = [col for col in dataframe.columns if re.search(time_pattern, col)]
        score_fluency = task + '_fluency'
        dataframe.loc[:, score_fluency] = dataframe.apply(lambda x: fluency_score(x, score_cols, duration_col), axis=1)
    
    return dataframe