import pandas as pd

df = pd.read_excel('treated_missing_drugs.xlsx')
df.drop('Unnamed: 3', inplace=True, axis=1)
mask = (df.where(df['Nom "retravaillé"'] == '/'))
missing = df[df['Nom médicament'] == mask['Nom médicament']]['Nom médicament']
missing.to_csv('./outputs/treated_only_missing_drugs.csv', index=None)