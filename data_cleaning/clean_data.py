def clean_data(dataframe):

    # Import required libraries
    import regex as re
    
    # Drop pratice assessments from dataset
    test_data = dataframe[dataframe['buildChannel'] == 'test']
    # print(f"No. of test assessments: {test_data.shape[0]}")
    dataframe.drop(test_data.index, inplace=True)

    # Drop incomplete assessments from dataset
    incomplete_data = dataframe[dataframe['complete'] == "false"]
    # print(f"No. of incomplete assessments: {incomplete_data.shape[0]}")
    dataframe.drop(incomplete_data.index, inplace=True)

    # Drop assessments without child's consent from dataset
    no_consent = dataframe[dataframe['consent'] == 'no']
    # print(f"No. of assessments where children did not give consent: {no_consent.shape[0]}")
    dataframe.drop(no_consent.index, inplace=True)

    # Create dataframes to store literacy and numeracy assessments data
    lit_temp = dataframe.copy()
    num_temp = dataframe.copy()
    
    # Drop data with 'Yes' for child wants to stop any subtask
    lit_end_cols = [col for col in lit_temp.columns if re.search(r'^lit\w*end$', col)]
    num_end_cols = [col for col in num_temp.columns if re.search(r'^num\w*end$', col)]
    
    total_lit_stopped = 0
    total_num_stopped = 0
    
    for lit_col, num_col in zip(lit_end_cols, num_end_cols):
        lit_stopped = lit_temp[lit_temp[lit_col] == '1']
        num_stopped = num_temp[num_temp[num_col] == '1']
        
        # print(f"No. of literacy assessments stopped after {lit_col}: {lit_stopped.shape[0]}")
        # print(f"No. of numeracy assessments stopped after {num_col}: {num_stopped.shape[0]}")

        total_lit_stopped += lit_stopped.shape[0]
        total_num_stopped += num_stopped.shape[0]

        lit_temp.drop(lit_stopped.index, inplace=True)
        num_temp.drop(num_stopped.index, inplace=True)

    # print(f"Total no. of literacy assessments stopped: {total_lit_stopped}")
    # print(f"Total no. of numeracy assessments stopped: {total_num_stopped}")

    # Drop data where any sub-task (other than valid skipable tasks) was disabled
    lit_disabled_cols = ['listening_comprehension_disabled', 'oral_vocabulary_disabled', 'initial_sounds_disabled', \
                         'letter_naming_untimed_disabled', 'letter_naming_timed_disabled', 'familiar_words_untimed_disabled', \
                         'orf_timed_disabled', 'dictation_untimed_letters_disabled', 'dictation_untimed_words_disabled']
    
    num_disabled_cols = ['counting_timed_disabled', 'number_recognition_untimed_disabled', 'number_recognition_timed_disabled', \
                         'number_comparison_untimed_disabled', 'counting_in_bundles_untimed_disabled', 'missing_number_untimed_disabled', \
                         'addition_untimed_disabled', 'subtraction_untimed_disabled', 'word_problems_untimed_disabled', \
                         'shape_recognition_a_untimed_disabled', 'shape_recognition_b_untimed_disabled']

    total_lit_disabled = 0
    total_num_disabled = 0

    for lit_col, num_col in zip(lit_disabled_cols, num_disabled_cols):
        lit_disabled = lit_temp[lit_temp[lit_col] == True]
        num_disabled = num_temp[num_temp[num_col] == True]
    
        # print(f"No. of assessments disabled after {lit_col}: {lit_disabled.shape[0]}")
        # print(f"No. of assessments disabled after {num_col}: {num_disabled.shape[0]}")
    
        lit_temp.drop(lit_disabled.index, inplace=True)
        num_temp.drop(num_disabled.index, inplace=True)

        total_lit_disabled += lit_disabled.shape[0]
        total_num_disabled += num_disabled.shape[0]

    # print(f"Total no. of literacy assessments disabled: {total_lit_disabled}")
    # print(f"Total no. of numeracy assessments disabled: {total_num_disabled}")
    
    
    # Create lists of required non sub-task data columns
    general_info =['tabletUserName', 'assessment_date', 'school_details.State_label', 'school_details.District_label', \
                   'school_details.Block_label', 'school_details.School_label', 'school_details.UDISE_cd_label']

    student_info = ['SI_std_name', 'GI_std_name', 'student_age', 'student_gender']

    # Create names for dataframes to hold literacy and numeracy data
    df_lit = dataframe.name + '_lit' # Concat name of original dataframe with _lit suffix
    df_num = dataframe.name + '_num' # Concat name of original dataframe with _num suffix
    
    # Create list of required literacy sub-task columns
    lit_cols = [col for col in lit_temp.columns if re.search(r'^literacy\d.', col)]
    
    # Create list of required numeracy sub-task columns
    num_cols = [col for col in num_temp.columns if re.search(r'^numeracy\d.', col)]
    
    # Assign literacy and numeracy data to respective dataframes
    locals()[df_lit] = lit_temp.loc[:, general_info + student_info + lit_cols]
    locals()[df_num] = num_temp.loc[:, general_info + student_info + num_cols]
    
    # Code gender variable to 'male' and 'female'
    for dataframe in [locals()[df_lit], locals()[df_num]]:
        dataframe.loc[:, 'student_gender'] = dataframe.loc[:, 'student_gender'].astype('str').apply(lambda x: 'Male' if (x=='0') else 'Female')

    locals()[df_lit].to_excel(df_lit + '.xlsx')
    locals()[df_num].to_excel(df_num + '.xlsx')  
    
    return (locals()[df_lit], locals()[df_num])
