import pandas as pd
import numpy as np

df = pd.read_csv('webscraping\outputs\janus_webscraping.csv', sep = ",")

Persistence = np.zeros(len(df))
Bioaccumulation = np.zeros(len(df))
Toxicity = np.zeros(len(df))
Risk = np.zeros(len(df))
df["Persistence"] = Persistence
df["Bioaccumulation"] = Bioaccumulation
df["Toxicity"] = Toxicity
df["Risk"] = Risk
Acc = 0

def splitter(data, num_row, num_column, word_split, store) :
    first_split = str(data.iloc[num_row,num_column]).split(word_split)
    if len(first_split) > 1 & store == True :
        data.iloc[num_row,num_column] = first_split[0].strip(".Â")
        data.iloc[num_row,num_column+1] = first_split[1].strip(".Â")
    return len(first_split)

for i, row in df.iterrows() :
    x = splitter(df,i,2,"Persistence",True)
    if x > 1 :
        splitter(df,i,3,"Bioaccumulation",True)
        splitter(df,i,4,"Toxicity",True)
        splitter(df,i,5,"Risk",True)
    else :
        y = splitter(df,i,2,"SummaryHazard",False)
        if y > 1 :
            splitter(df,i,2,"P",True)
            splitter(df,i,3,"B",True)
            splitter(df,i,4,"T",True)
            splitter(df,i,5,"Risk",True)
        else :
            Acc = Acc + 1
            df.iloc[i,3] = "see summary"
            df.iloc[i,4] = "see summary"
            df.iloc[i,5] = "see summary"
            df.iloc[i,6] = "see summary"

print("Parsing done, " + str(Acc) + " not correctly parsed")

df.to_csv('parsing\df.csv',index=False)