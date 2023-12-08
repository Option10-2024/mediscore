import os

def makeOutputDir():
    cwd = os.getcwd()
    
    if not os.path.exists(cwd+'/outputs'):
        os.makedirs(cwd+'/outputs')
        print('outputs folder created')
    else:
        print('outputs folder already exists')
        