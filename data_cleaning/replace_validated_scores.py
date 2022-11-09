def replace_validated_scores(dataframe, validated_scores):
    count = 0
    for idx1, row1 in validated_scores.iterrows():
        for idx2, row2 in dataframe.iterrows():
            if set([int(row1['school_details.UDISE_cd_label']),\
                   str(row1['SI_std_name']),\
                   int(row1['GI_std_name'])]) == \
               set([int(row2['school_details.UDISE_cd_label']),\
                   str(row2['SI_std_name']),\
                   int(row2['GI_std_name'])]):
                count += 1
                row2['literacy9a_total'] = row1['9a']
                row2['literacy9b_total'] = row1['9b']
    return None
