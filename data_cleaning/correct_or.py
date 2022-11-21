def correct_or(dataframe, or_sheets):
    for sheet in or_sheets.sheet_names:
        other_responses = or_sheets.parse(sheet)
        correct_responses = []
        for index, row in other_responses.iterrows():
            if (row["Code"]) == 1:
                correct_responses.append(row["Child's response"])
        col = re.match(r'.+\d', sheet)[0]
        filter = dataframe[col].isin(correct)
        dataframe.loc[filter, col] = 1
