
#%%
import re
import pandas as pd
import os


df = pd.read_csv('parsing\janus_parsed.csv', sep = ",")

# Search a specified string in a specified row and column in a DF
def finder(data, num_row, num_column, find_word) :
    find = re.search(find_word, str(data.iloc[num_row,num_column]))
    return find


def converter2(data, num_row, num_column,words) :
    done = False
    for i in words :
        r = finder(data, num_row, num_column,i[0])   #use finder with the text part of words
        if r :
            data.iloc[num_row,num_column] = i[1]     #if found it, replace by the associated value
            done = True
    ra = finder(data, num_row, num_column,"lack of data") #generic cases without data
    rb = finder(data, num_row,num_column,"No data") 

    if ra or rb :
        data.iloc[num_row,num_column] = "pas de données"  #replace the rows without data
        done = True
    return done
        
# define the key words
words1 = [["very persistent",3],["is potentially persistent",3],["is degraded slowly",3],["slowly degraded",3],["slowly degrades",3],["is not persistent",0]]
#words1 = [["is potentially persistent",3],["is degraded slowly",3],["slowly degraded",3]]
words2 =[["Has high potential for bioaccumulation",3],["Has low potential for bioaccumulation",0]]
words3 =[["Very high toxicity",3],["High toxicity",2],["Moderate toxicity",1],["Low toxicity",0]]

#Applied on the three main columns
Unmatched = 0
for i, row in df.iterrows() :
    if converter2(df, i, 3,words1) == False : 
        Unmatched += 1
print(str(Unmatched) + " rows unmatched")

Unmatched = 0
for i, row in df.iterrows() :
    if converter2(df, i, 4,words2) == False :
        Unmatched += 1
print(str(Unmatched) + " rows unmatched")

Unmatched = 0
for i, row in df.iterrows() :
    if converter2(df, i, 5,words3) == False :
        Unmatched += 1
print(str(Unmatched) + " rows unmatched")


df.to_csv('parsing\janus_to_numbers.csv',index=False)
# %%


