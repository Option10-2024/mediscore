
#%%
import re
import pandas as pd
import os


df = pd.read_csv('janus_parsed.csv', sep = ",")

# Search a specified string in a specified row and column in a DF
def finder(data, num_row, num_column, find_word) :
    find = re.search(find_word, str(data.iloc[num_row,num_column]))
    return find

# Fonction pour colonnes P,B,T,Risk
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


# Fonction pour colonnes summary
def converter_s(data, num_row, num_column) :
    done = False

    r = finder(data, num_row, num_column+1, "voir colonne notes supplémentaires")   #use finder with the text part of words
    if r :
        done = True
    else :
        data.iloc[num_row,num_column] = "-"
    return done
        
# Fonction pour colonnes risk
def converter_r(data, num_row, num_column) :
    done = False
    if data.iloc[num_row,num_column] == " " :
        data.iloc[num_row,num_column] = "pas de données"
        return done
    
# Fonction pour colonnes -
def converter_tir(data, num_row, num_column) :
    done = False
    if data.iloc[num_row,num_column] == " - " :
        data.iloc[num_row,num_column] = "pas de données"
        return done
    
# define the key words
words1 = [["very persistent",3],["is potentially persistent",3],["is degraded slowly",3],["slowly degraded",3],["slowly degrade",3],["is not persistent",0],["is potentially peristent", 3],["degraded in the environment", 3],["is likely non-persistent",0],["not considered to be persistent",0],["is persistent",3]]
#words1 = [["is potentially persistent",3],["is degraded slowly",3],["slowly degraded",3]]
#words2 =[["Has high potential for bioaccumulation",3],["Has low potential for bioaccumulation",0]]
words2 =[["has high potential for bioaccumulation",3],["low potential",0],["has high potential to bioaccumulate",3],["has high potential to bioaccumulate",3],["has a high potential to bioaccumulate",3],["high potential for bioconcentration",3],["has the potential to be stored",3],["has the potential to bioaccumulate",3],["a strong bioconcentration can be expected",3],["does not have the potential",0],["has no potential to bioaccumulate",0],["No significant bioaccumulation potential",0]]
words3 =[["very high toxicity",3],["very high acute toxicity",3],["very high chronic toxicity",3],["high toxicity",2],["high acute toxicity",2],["high chronic toxicity",2],["moderate toxicity",1],["moderate chronic toxicity",1],["moderate acute toxicity",1],["low toxicity",0],["low chronic toxicity",0],["low acute toxicity",0],["moderat chronic toxicity",1],["very high acute/chronic toxicity",3],["very hig acute toxicity",3]]
words4 =[["result in insignificant environmental risk",0],["gives the risk insignificant",0],["to entail a insignificant risk of environmental impact",0],["not considered to pose an environmental risk",0],["Insignificant",0],["result in low environmental risk",1],["result in moderate environmental risk",2],["entail a risk high of environmental",3],["result in high environmental risk",3],["Exempt","pas de données"],["High",3],["Moderate",2],["Low",1],["Cannot be excluded","pas de données"],["Environmental information is missing","pas de données"],["No final conclusion is possible on the potential risk","pas de données"],["risk seems entirely insignificant",0],["considered to result in nsignificant environmental",0],["environmental risk is very low",1],["considered to have a low environmental risk",1],["environmental risk is considered to be very low",1],["existing data indicate low environmental risk",1],["judged to entail a high risk of environmental",3],["result in moderate/high environmental risk",3],["See below","pas de données"],["See the report","la donnée n'a pas pu être extraite"],["See the environmental assessment","la donnée n'a pas pu être extraite"],['"',"pas de données"],["is unlikely to result in significant risk to the environment",0],["Se below","pas de données"],["See the Goopoint report","la donnée n'a pas pu être extraite"]]

#Applied on Persistence
Unmatched = 0
for i, row in df.iterrows() :
    if converter2(df, i, 3,words1) == False : 
        Unmatched += 1
    converter_tir(df, i, 3)
print(str(Unmatched) + " P rows unmatched")

#Applied on Bioaccumulation
Unmatched = 0
for i, row in df.iterrows() :
    if converter2(df, i, 4,words2) == False :
        Unmatched += 1
    converter_tir(df, i, 4)
print(str(Unmatched) + " B rows unmatched")

#Applied on Toxicity
Unmatched = 0
for i, row in df.iterrows() :
    if converter2(df, i, 5,words3) == False :
        Unmatched += 1
    converter_tir(df, i, 5)
print(str(Unmatched) + " T rows unmatched")

#Applied on Risk
Unmatched = 0
for i, row in df.iterrows() :
    if converter2(df, i, 6,words4) == False :
        Unmatched += 1
    converter_r(df, i, 6)
    converter_tir(df, i, 6)
print(str(Unmatched) + " R rows unmatched")

#Applied on Summary
Unmatched = 0
for i, row in df.iterrows() :
    if converter_s(df, i, 2) == False :
        Unmatched += 1
print(str(709 - Unmatched) + " S rows matched")


df.to_csv('janus_to_numbers.csv',index=False)



# %%
