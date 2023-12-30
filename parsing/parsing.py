#%%

import pandas as pd
import numpy as np
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)  
#pd as a bug with .loc fct returning a warning


# Import dataframe
#df_1 = pd.read_csv('webscraping\outputs\janus_webscraping.csv', sep = ",")
df = pd.read_csv('janus_webscraping.csv', sep = ",")

# Add empty columns to the DF that'll be filled later
Persistence = np.zeros(len(df))
Bioaccumulation = np.zeros(len(df))
Toxicity = np.zeros(len(df))
Risk = np.zeros(len(df))
df["Persistence"] = Persistence
df["Bioaccumulation"] = Bioaccumulation
df["Toxicity"] = Toxicity
df["Risk"] = Risk
Acc = 0


# Definition of the parsing function
def splitter(data, num_row, num_column, word_split, store) :
    first_split = str(data.iloc[num_row,num_column]).split(word_split) #.split() returns a list of two element, before and after "word_split" and has to be applied on a string
    if len(first_split) > 1 & store == True :                          #len()>1 otherwise it means that "word_split" is not in the string
        data.iloc[num_row,num_column] = first_split[0].strip(".Â")     #store the interesting part in first column 
        data.iloc[num_row,num_column+1] = first_split[1].strip(".Â")   #store the rest in second columns + remove "." and "Â" with .strip()
    return len(first_split)


# Iteration over the wall DF
for i, row in df.iterrows() :
    x = splitter(df,i,3,"Persistence",True)          #FIRST CASE --> text description
    if x > 1 :                                       #x and y refers to len() --> if worked or not
        splitter(df,i,4,"Bioaccumulation",True)      #each function takes for input the "rest" of
        splitter(df,i,5,"Toxicity",True)             #the previous one to isolate the wanted part
        splitter(df,i,6,"Risk",True)
    else :
        y = splitter(df,i,3,"SummaryHazard",False)   #SECOND CASE --> numbers
        if y > 1 :
            splitter(df,i,3,"P",True)
            splitter(df,i,4,"B",True)
            splitter(df,i,5,"T",True)
            splitter(df,i,6,"Risk",True)
        else :                                       #UNKNOWN CASE
            Acc = Acc + 1                            #counts the number
            df.iloc[i,4] = "voir colonne notes supplémentaires"             #P,B,T and R columns refers to the summary
            df.iloc[i,5] = "voir colonne notes supplémentaires" 
            df.iloc[i,6] = "voir colonne notes supplémentaires" 
            df.iloc[i,7] = "voir colonne notes supplémentaires" 


print("Parsing done, " + str(Acc) + " not correctly parsed")
#most of those rows don't have any PBT values due to the fact that the molec is a protein, vitamin,...

# Rewrite the column order to facilitate next step
df = df[['drug_name','atc','summary','Persistence','Bioaccumulation','Toxicity','Risk','uncertainty_atc_match']]

# Export
df.to_csv('janus_parsed.csv',index=False)
# %%
