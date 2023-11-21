
#%%
import re
import pandas as pd
import os


df = pd.read_csv('janus_parsed.csv', sep = ",")

# Search a specified string in a specified row and column in a DF
def finder(data, num_row, num_column, find_word) :
    find = re.search(find_word, str(data.iloc[num_row,num_column]))
    return find


def converter2(data, num_row, num_column,words) :
    done = False

    ra = finder(data, num_row, num_column,"lack of data") #generic cases without data
    rb = finder(data, num_row,num_column,"No data") 
    rc = finder(data, num_row,num_column,"no data") 
    rd = finder(data, num_row,num_column,"not enough data") 

    if ra or rb or rc or rd :
        data.iloc[num_row,num_column] = "pas de données"  #replace the rows without data
        done = True

    for i in words :
        r = finder(data, num_row, num_column,i[0])   #use finder with the text part of words
        if r :
            data.iloc[num_row,num_column] = i[1]     #if found it, replace by the associated value
            done = True
    
    return done
        
# define the key words
words1 = [["very persistent",3],["is potentially persistent",3],["is degraded slowly",3],["slowly degraded",3],["slowly degrade",3],["is not persistent",0],["is potentially peristent", 3],["degraded in the environment", 3],["is likely non-persistent",0],["not considered to be persistent",0],["is persistent",3]]
#words1 = [["is potentially persistent",3],["is degraded slowly",3],["slowly degraded",3]]
#words2 =[["Has high potential for bioaccumulation",3],["Has low potential for bioaccumulation",0]]
words2 =[["has high potential for bioaccumulation",3],["low potential",0],["has high potential to bioaccumulate",3],["has high potential to bioaccumulate",3],["has a high potential to bioaccumulate",3],["high potential for bioconcentration",3],["has the potential to be stored",3],["has the potential to bioaccumulate",3],["a strong bioconcentration can be expected",3],["does not have the potential",0],["has no potential to bioaccumulate",0],["No significant bioaccumulation potential",0]]
words3 =[["very high toxicity",3],["very high acute toxicity",3],["very high chronic toxicity",3],["high toxicity",2],["high acute toxicity",2],["high chronic toxicity",2],["moderate toxicity",1],["moderate chronic toxicity",1],["moderate acute toxicity",1],["low toxicity",0],["low chronic toxicity",0],["low acute toxicity",0],["moderat chronic toxicity",1],["very high acute/chronic toxicity",3],["very hig acute toxicity",3]]

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


df.to_csv('janus_to_numbers.csv',index=False)# %%



# %%
