def code_scores(df, cols):
    for col in cols:
	# print(f"No. of NaN values in {col} = {df.loc[:, col].isna().sum()}")
	# print(f"No. of UNDEFINED values in {col} = {df[df[col] == 'UNDEFINED'].shape[0]}")    
	# print(f"No. of SKIPPED values in {col} = {df[df[col] == 'SKIPPED'].shape[0]}")
        df.loc[:, col] = df.loc[:, col].astype('str')
        df.loc[:, col].fillna('0', inplace=True)
        df.loc[:, col].replace('UNDEFINED', '0', inplace=True)
        df.loc[:, col].replace('SKIPPED', '0', inplace=True)
        df.loc[:, col].replace('999', '0', inplace=True)
        df.loc[:, col].replace('88', '0', inplace=True)
        df.loc[:, col].replace('.', '0', inplace=True)
	# print(f"Unique values in {col} = {df[col].unique()}\n")
    return None
