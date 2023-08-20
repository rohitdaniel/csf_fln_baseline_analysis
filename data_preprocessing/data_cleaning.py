# Import required libraries
import regex as re
import pandas as pd
from datetime import datetime

def to_datetime(dataframe):
    # Create a list of columns with Unix time format for conversion
    unixTime_cols = [col for col in dataframe.columns if re.search(r'.*(?i)time$', col)]

    # Loop through columns with Unix time and convert valid times to datetime format
    for col in unixTime_cols:
        dataframe.loc[:, col] = dataframe.apply(lambda row: datetime.fromtimestamp(float(row[col])/1000) if not ((pd.isna(row[col])) | (row[col] == 'UNDEFINED') | (row[col] == 'SKIPPED')) else row[col], axis=1)
    
    print("Converted Unix time to datetime format\n\n**************************************************\n")
    
    return None

def clean_scores(df, cols: list):
    for col in cols:
        print(f"Cleaning scores in column: {col} ...")

        # Replace NaN values with 999
        print(f"No. of NaN values in {col} cleaned: {df.loc[:, col].isna().sum()}")
        df.loc[:, col].fillna('999', inplace=True)

        # Replace UNDEFINED values with 999
        # print(f"No. of UNDEFINED values in {col} cleaned: {df[df[col] == 'UNDEFINED'].shape[0]}")
        df.loc[:, col].replace('UNDEFINED', '999', inplace=True)

        # Replace SKIPPED values with 999
        print(f"No. of SKIPPED values in {col} cleaned: {df[df[col] == 'SKIPPED'].shape[0]}")
        df.loc[:, col].replace('SKIPPED', '999', inplace=True)

        # Replace '.' values with 999
        print(f"No. of '.' values in {col} cleaned: {df[df[col] == '.'].shape[0]}")
        df.loc[:, col].replace('.', '999', inplace=True)
        
        # Convert scores to integer format        
        df.loc[:, col] = df.loc[:, col].astype('int')
        print(f"Scores in {col} converted to integer format")
        
        # Print the unique values in each column to other non numerical values
        print(f"Unique values in {col} = {df[col].unique()}")

        print(f"\n**************************************************\n")
    
    return None

def clean_data(dataframe, cols: list):
    
    # Drop pratice assessments from dataset
    test_data = dataframe[dataframe['buildChannel'] == 'test']
    print(f"No. of test assessments dropped: {test_data.shape[0]}")
    dataframe.drop(test_data.index, inplace=True)

    # Drop incomplete assessments from dataset
    incomplete_data = dataframe[dataframe['complete'] == "false"]
    print(f"No. of incomplete assessments dropped: {incomplete_data.shape[0]}")
    dataframe.drop(incomplete_data.index, inplace=True)

    # Drop assessments without child's consent from dataset
    no_consent = dataframe[dataframe['consent'] == 'no']
    print(f"No. of assessments where children did not give consent dropped: {no_consent.shape[0]}")
    dataframe.drop(no_consent.index, inplace=True)
    
    # Change datetime form unix to datetime format
    to_datetime(dataframe)

    # Change non numerical scores to 999
    clean_scores(dataframe, cols)

    return dataframe


def fix_lit_grid_score(scores):
    for i in range(len(scores) - 3):
        if (int(scores[i]) + int(scores [i+1]) + int(scores [i+2]) + int(scores [i+3])) == 0:
            for j in range(i+4, len(scores)):
                scores[j] = '0'
            break

    return scores
   
def fix_num_grid_score(scores):
    for i in range(len(scores)):
        if scores[i] == '0':
            for j in range(i, len(scores)):
                scores[j] = '0'
            break
            
    return scores

def fix_autostop_error(dataframe, task: str, errors: int):
    pattern = task + r'.*grid_\d*$'
    grid_cols = [col for col in dataframe.columns if re.search(pattern, col)]

    if errors == 4:
        dataframe.loc[:, grid_cols] = pd.DataFrame((dataframe.apply(lambda x: fix_lit_grid_score([x[col] for col in grid_cols]), axis=1)).to_list(), index=dataframe.index, columns=grid_cols)
    elif errors == 1:
        dataframe.loc[:, grid_cols] = pd.DataFrame((dataframe.apply(lambda x: fix_num_grid_score([x[col] for col in grid_cols]), axis=1)).to_list(), index=dataframe.index, columns=grid_cols)

    return dataframe
