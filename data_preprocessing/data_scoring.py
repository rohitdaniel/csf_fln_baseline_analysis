# Import required libraries
import regex as re

def total_score(score_cols):
    total_score = 0
    for score in score_cols:
        if  (str(score) == '1'):
            total_score += 1
    return total_score
    

def fluency_score(dataframe, score_cols, duration ):
    score_pattern = task + r'((?!end|or|p|number|Stop|item|time|duration).)*$'
        score_cols = [col for col in dataframe.columns if re.search(score_pattern, col)]
        time_pattern = task + r'.*(time_remaining)$'
        duration = (60 - dataframe[[col for col in dataframe.columns if re.search(time_pattern, col)][0]].astype(int))

        score_fluency = task + '_fluency'
        dataframe.loc[:, score_fluency] = dataframe.apply(lambda x: fluency_score(x, score_cols, duration), axis=1)

fluency = 0
    total = total_score(dataframe[score_cols])

    if duration != 0:
        fluency = ((60*total)/duration)
    return fluency


def score_data(dataframe, untimed_tasks: list, timed_tasks: list):
    
    for task in untimed_tasks:
        pattern = task + r'((?!end|tt|or|p|number|Stop|item|time|duration).)*$'
        score_cols = [col for col in dataframe.columns if re.search(pattern, col)]

        score_total = task + '_total'
        score_percent_correct = task + '_%_correct'
        dataframe.loc[:, score_total] = dataframe.apply(lambda x: total_score([x[col] for col in score_cols]), axis=1)
        dataframe.loc[:, score_percent_correct] = dataframe.apply(lambda x: 100*x[score_total]/len(score_cols), axis=1)

    for task in timed_tasks:
        score_pattern = task + r'((?!end|or|p|number|Stop|item|time|duration).)*$'
        score_cols = [col for col in dataframe.columns if re.search(score_pattern, col)]
        time_pattern = task + r'.*(time_remaining)$'
        duration = (60 - int([col for col in dataframe.columns if re.search(time_pattern, col)][0]))

        score_fluency = task + '_fluency'
        dataframe.loc[:, score_fluency] = dataframe.apply(lambda x: fluency_score(x, score_cols, duration), axis=1)

#     dataframe.loc[:, 'familiar_words_timed_fluency'] = dataframe[0].apply(lambda x: calculations.fluency_score(x, lit5_tt_raw), axis=1)
#     dataframe.loc[:, 'non_words_timed_fluency'] = dataframe[0].apply(lambda x: calculations.fluency_score(x, lit6_tt_raw), axis=1)
#     dataframe.loc[:, 'oral_reading_fluency'] = dataframe[0].apply(lambda x: calculations.fluency_score(x, lit7_raw), axis=1)


    

# literacy1=[col for col in literacy_raw.columns if re.search(r'literacy1_q\d$',col)]
# literacy2=[col for col in literacy_raw.columns if re.search(r'literacy2_q\d+$',col)]
# literacy3=[col for col in literacy_raw.columns if re.search(r'literacy3_q+',col)]
# literacy4_ut=[col for col in literacy_raw.columns if re.search(r'literacy4_ut_grid_\d*$',col)]
# literacy4_tt=[col for col in literacy_raw.columns if re.search(r'literacy4_tt_grid_\d*$',col)]

#     dataframe.loc[:, 'listening_comprehension_total'] = dataframe[0].apply(lambda x: calculations.total_score([x[col] for col in lit1_raw]), axis=1)
#     dataframe.loc[:, 'listening_comprehension_%_correct'] = dataframe[1].apply(lambda x: 100*x['listening_comprehension_total']/len(lit1_raw), axis=1)
#     dataframe.loc[:, 'oral_vocabulary_total'] = dataframe[0].apply(lambda x: calculations.total_score([x[col] for col in lit2_raw]), axis=1)
#     dataframe.loc[:, 'oral_vocabulary_%_correct'] = dataframe[1].apply(lambda x: 100*x['oral_vocabulary_total']/len(lit2_raw), axis=1)
#     dataframe.loc[:, 'initial_sound_identification_total'] = dataframe[0].apply(lambda x: calculations.total_score([x[col] for col in lit3_raw]), axis=1)
#     dataframe.loc[:, 'initial_sound_identification_%_correct'] = dataframe[1].apply(lambda x: 100*x['initial_sound_identification_total']/len(lit3_raw), axis=1)
#     dataframe.loc[:, 'letter_naming_untimed_total'] = dataframe[0].apply(lambda x: calculations.total_score([x[score] for score in lit4_ut_raw]), axis=1)
#     dataframe.loc[:, 'letter_naming_untimed_%_correct'] = dataframe[1].apply(lambda x: 100*x['letter_naming_untimed_total']/len(lit4_ut_raw), axis=1)

#     dataframe.loc[:, 'familiar_words_timed_fluency'] = dataframe[0].apply(lambda x: calculations.fluency_score(x, lit5_tt_raw), axis=1)
#     dataframe.loc[:, 'non_words_timed_fluency'] = dataframe[0].apply(lambda x: calculations.fluency_score(x, lit6_tt_raw), axis=1)
#     dataframe.loc[:, 'oral_reading_fluency'] = dataframe[0].apply(lambda x: calculations.fluency_score(x, lit7_raw), axis=1)

#     dataframe.loc[:, 'reading_untimed_total'] = dataframe[0].apply(lambda x: calculations.total_score([x[score] for score in lit8_raw_reading]), axis=1)
#     dataframe.loc[:, 'reading_untimed_%_correct'] = dataframe[1].apply(lambda x: 100*x['reading_untimed_total']/len(lit8_raw_reading), axis=1)
#     dataframe.loc[:, 'reading_comprehension_untimed_total'] = dataframe[0].apply(lambda x: calculations.total_score([x[score] for score in lit8_raw_comprehension]), axis=1)
#     dataframe.loc[:, 'reading_comprehension_untimed_%_correct'] = dataframe[1].apply(lambda x: 100*x['reading_comprehension_untimed_total']/len(lit8_raw_comprehension), axis=1)
#     dataframe.loc[:, 'dictation_letters_total'] = dataframe[0].apply(lambda x: calculations.total_score([x[score] for score in lit9a_raw]), axis=1)
#     dataframe.loc[:, 'dictation_letters_%_correct'] = dataframe[1].apply(lambda x: 100*x['dictation_letters_total']/len(lit9a_raw), axis=1)
#     dataframe.loc[:, 'dictation_words_total'] = dataframe[0].apply(lambda x: calculations.total_score([x[score] for score in lit9b_raw]), axis=1)
#     dataframe.loc[:, 'dictation_words_%_correct'] = dataframe[1].apply(lambda x: 100*x['dictation_words_total']/len(lit9b_raw), axis=1)
