import pandas as pd
import numpy as np

df = pd.read_csv('webscraping\outputs\janus_webscraping.csv', sep = ",")
#print(df.loc[0,"summary"])

test = {"name": ["Ibuprofen","Ibuprofen2","essai"], "Summary":["SummaryThis summary information comes from Fass.Persistence. Abacavir is potentially persistent.Bioaccumulation. Abacavir has low potential for bioaccumulation.Toxicity. Abacavir has low chronic toxicity.Risk. The use of abacavir (sales data Sweden 2019) has been considered to result in insignificant environmental risk.","SummaryHazard 5 P 3 B 0 T 2 Risk InsignificantÂ The T-value in the score for hazard refers to chronic toxicity. Underlying data for P, B and T are from assessment report. Risk is from Fass.","Vive les aranchinis et je ne sais pas comment ça s'écrit"]}
test = pd.DataFrame.from_dict(test)

#test = {"name": ["Ibuprofen"], "Summary":["SummaryPersistence. Allopurinol is potentially persistent.Bioaccumulation. Allopurinol has low potential for bioaccumulation.Toxicity. Allopurinol has very high acute toxicity.Risk. The use of allopurinol (sales data Sweden 2021) has been considered to result in moderate environmental risk.Â This summary information comes from Fass."]}
#test = pd.DataFrame.from_dict(test)


Persistence = np.zeros(len(test))
Bioaccumulation = np.zeros(len(test))
Toxicity = np.zeros(len(test))
Risk = np.zeros(len(test))
test["Persistence"] = Persistence
test["Bioaccumulation"] = Bioaccumulation
test["Toxicity"] = Toxicity
test["Risk"] = Risk

'''
def parserAcc(data,column,Acc) :
    if Acc >= len(data) : 
        return("job done")
    else :
        column = str(column)
        parserAcc(data,column,Acc+1)
        return(data.loc[Acc,column])

def parser(data, column) : 
    return(parserAcc(data,column,0))

print(parser(test,"Summary"))
'''

def parserAcc(data,column,Acc) :
    while Acc < len(data) : 
        column = str(column)
        print(data.loc[Acc,column])
        Acc = Acc +1
   

def parser(data, column) : 
    parserAcc(data,column,0)

#parser(test,"Summary")
pd.set_option('display.max_columns', None)

test2 = "SummaryThis summary information comes from Fass.Persistence. Abacavir is potentially persistent.Bioaccumulation. Abacavir has low potential for bioaccumulation.Toxicity. Abacavir has low chronic toxicity.Risk. The use of abacavir (sales data Sweden 2019) has been considered to result in insignificant environmental risk."

'''
test_split = test.loc[0,"Summary"].split("Persistence")
test.loc[0,"Persistence"] = test_split[1]
test_split2 = test_split[1].split("Bioaccumulation")
test.loc[0,"Bioaccumulation"] = test_split2[1]

print(test_split2[0])
'''

def splitter(data, num_row, num_column, word_split, store) :
    first_split = data.iloc[num_row,num_column].split(word_split)
    if len(first_split) > 1 & store == True :
        data.iloc[num_row,num_column] = first_split[0]
        data.iloc[num_row,num_column+1] = first_split[1]
    return len(first_split)

for i, row in test.iterrows() :
    x = splitter(test,i,1,"Persistence",True)
    if x > 1 :
        splitter(test,i,2,"Bioaccumulation",True)
        splitter(test,i,3,"Toxicity",True)
        splitter(test,i,4,"Risk",True)
    else :
        y = splitter(test,i,1,"SummaryHazard",False)
        if y > 1 :
            splitter(test,i,1,"P",True)
            splitter(test,i,2,"B",True)
            splitter(test,i,3,"T",True)
            splitter(test,i,4,"Risk",True)
        else :
            test.iloc[i,2] = "see summary"
            test.iloc[i,3] = "see summary"
            test.iloc[i,4] = "see summary"
            test.iloc[i,5] = "see summary"


test.to_csv('parsing\est.csv',index=False)

print(df.iloc[3,2])


s = "Bio acc."
print(s.strip("."))