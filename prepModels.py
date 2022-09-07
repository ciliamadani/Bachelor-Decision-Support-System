import json
import pickle
import pandas as pd
import numpy as np 
import logging

## loading models
model_ens =pickle.load(open('orientationSystem/model/model_approche2/ENS_CATBOOST.pkl','rb+'))
model_med=pickle.load(open('orientationSystem/model/model_approche2/MED_XGBoost.pkl','rb+'))
model_prepaAll=pickle.load(open('orientationSystem/model/model_approche2/PrepaAllClasses_CATBOOST.pkl','rb+'))
model_formUniv=pickle.load(open('orientationSystem/model/model_approche2/UNIV_CATBOOST.pkl','rb+'))
model_formSup=pickle.load(open('orientationSystem/model/model_approche2/FormSup_CATBOOST.pkl','rb+'))

## loading encoders
encoder_ens = pickle.load(open('orientationSystem/model/model_approche2/encoders/encoder_ENS.pkl','rb+'))
encoder_med = pickle.load(open('orientationSystem/model/model_approche2/encoders/encoder_med.pkl','rb+'))
encoder_prepaAll = pickle.load(open('orientationSystem/model/model_approche2/encoders/encoder_prepaAll.pkl','rb+'))
encoder_formUniv = pickle.load(open('orientationSystem/model/model_approche2/encoders/encoder_univ.pkl','rb+'))
encoder_formSup = pickle.load(open('orientationSystem/model/model_approche2/encoders/encoder_formSup.pkl','rb+'))

## loading normalisers
normaliser_ens = pickle.load(open('orientationSystem/model/model_approche2/normalisers/normlaliser_ens.pkl','rb+'))
normaliser_med = pickle.load(open('orientationSystem/model/model_approche2/normalisers/normlaliser_med.pkl','rb+'))
normaliser_prepaAll = pickle.load(open('orientationSystem/model/model_approche2/normalisers/normlaliser_prepaAll.pkl','rb+'))
normaliser_formUniv = pickle.load(open('orientationSystem/model/model_approche2/normalisers/normlaliser_formUniv.pkl','rb+'))
normaliser_formSup = pickle.load(open('orientationSystem/model/model_approche2/normalisers/normlaliser_formSup.pkl','rb+'))

def prepModel_ENS(temp):
    """
    input : ditionnary of student info 
    output: model predctions  
    """

    ## dataframe row created 
    testdata=pd.DataFrame({'x':temp}).transpose()

    testdata2 = testdata[['c1','c2','c3','c4','c5','c6']].astype(str).replace({'H14':'H00', 'H13':'H00', '711':'710', '712':'710', '713':'710','821':'820', '822':'820', '823':'820','121':'120', '122':'120', '123':'120', '841':'840', '842':'840' , '843':'840', '31':'300', '32':'300', '33':'300','21':'200', '22':'200', '23':'200', '41':'421', '42':'421', '43':'421', '44':'421', '611':'600', '612':'600', '613':'600', '614':'600', '101':'100', '102':'100', '11':'103', '12':'103', '13':'103', '14':'103','15':'103', '911':'910', '912':'910', '913':'910', '941':'940', '942':'940','721':'720', '722':'720', '723':'720','931':'930', '932':'930', '933':'930' })
    
    ###############
    #testdata[['wilaya_bac','moyenne_bac','sexe','Mention']]= testdata[['wilaya_bac','moyenne_bac','sexe','Mention']]
    ############

    if testdata.loc['x',"moyenne_bac"]<11:
        testdata['Mention'] = 0.25
    elif testdata.loc['x',"moyenne_bac"]>11 and testdata.loc['x',"moyenne_bac"]<=13 :
        testdata['Mention'] = 0.5
    elif testdata.loc['x',"moyenne_bac"]>13 and testdata.loc['x',"moyenne_bac"]<=15 :
        testdata['Mention'] = 0.75
    else :
        testdata['Mention'] = 0.90


    #### REPLACE WITH A LOADING FCT #######################
    my_dic = pd.read_excel("C:\\Users\\AzurComputer\\Downloads\\Codes de sortie (4).xlsx", sheet_name="Feuille 4", dtype={'code':str,'regroup': str}).fillna(method='ffill')
    my_dic['regroup']= my_dic['regroup'].astype(float).astype(int)
    my_dic['code '] = my_dic['code '].astype(str).apply(lambda x: x[:3])
    my_dic = my_dic.set_index('code ')
    groupDict = my_dic.to_dict()
    groupDict['regroup']['S38']=2

    ########################################################

    testdata2 =testdata2[['c1','c2','c3','c4','c5','c6']].replace(groupDict['regroup'])
    testdata2[['wilaya_bac','moyenne_bac','sexe','Mention']]= testdata[['wilaya_bac','moyenne_bac','sexe','Mention']]
    testdata2['sexe'].replace(['FEMININ', 'MASCULIN'],[0, 1], inplace=True)


    ## turn the 10 first six choices into binary data for first model 

    ## Normalisation moyenne bac
    testdata2['moyenne_bac']= normaliser_ens.transform(testdata2.moyenne_bac.to_numpy().reshape(-1, 1))

    ## model_ens ######################################################################    
    ## map intferface code to model codes 
    classes = ['66', '67', '69', '70', '71', '72', '73', '75', '76', '77', '80',   '81', '84', '85', 'OthEns']

    for col in ['c1','c2', 'c3', 'c4', 'c5', 'c6']:

        if testdata2.loc['x',col] in classes:
            pass
        else:
            testdata2.loc['x',col] = 'OTH'

    testdatafinal = testdata2[['c1','c2', 'c3', 'c4', 'c5', 'c6']].apply(encoder_ens.transform)
    
    ## map some choices to OTHs
    outputsmodel_ens= np.arange(0,15)
    #['66', '67', '69', '70', '71', '72', '73', '75', '76', '77', '80',    '81', '84', '85', 'OthEns']
    row =  []
    for i in range(1,7):


        if(testdatafinal.loc['x','c'+str(i)]) in outputsmodel_ens:

            row.append(int(testdatafinal.loc['x','c'+str(i)]))
        else:
            row.append(14)

    ## turning codes into binary vector 

    #l = testdatafinal[['c1', 'c2', 'c3', 'c4', 'c5','c6']].astype(int).values.flatten().tolist()
    l = [x-1 for x in row]

    m = np.zeros(16)


    m[l] = 1

    testdata=[]
    testdata.append(10)
    testdata.append(1)
    testdata.append(0.5)
    testdata.append(16)
    for i in m:
        testdata.append(i)
    testdata.append(np.exp2(10))

    result1 =model_ens.predict_proba(testdata)

    classes.append('OTH')

    return result1, row, classes


def prepModel_MED(temp):

    
    ## dataframe row created 
    testdata=pd.DataFrame({'x':temp}).transpose()
        
    testdata2 = testdata[['c1','c2','c3','c4','c5','c6']].astype(str).replace({'H14':'H00', 'H13':'H00', '711':'710', '712':'710', '713':'710','821':'820', '822':'820', '823':'820','121':'120', '122':'120', '123':'120', '841':'840', '842':'840' , '843':'840', '31':'300', '32':'300', '33':'300','21':'200', '22':'200', '23':'200', '41':'421', '42':'421', '43':'421', '44':'421', '611':'600', '612':'600', '613':'600', '614':'600', '101':'100', '102':'100', '11':'103', '12':'103', '13':'103', '14':'103','15':'103', '911':'910', '912':'910', '913':'910', '941':'940', '942':'940','721':'720', '722':'720', '723':'720','931':'930', '932':'930', '933':'930' })
    #testdata[['wilaya_bac','moyenne_bac','sexe','Mention']]= testdata[['wilaya_bac','moyenne_bac','sexe','Mention']]

    #### REPLACE WITH A LOADING FCT #######################
    my_dic = pd.read_excel("C:\\Users\\AzurComputer\\Downloads\\Codes de sortie (4).xlsx", sheet_name="Feuille 4", dtype={'code':str,'regroup': str}).fillna(method='ffill')
    my_dic['regroup']= my_dic['regroup'].astype(float).astype(int)
    my_dic['code '] = my_dic['code '].astype(str).apply(lambda x: x[:3])
    my_dic = my_dic.set_index('code ')
    groupDict = my_dic.to_dict()
    groupDict['regroup']['S38']=2

    ########################################################

    testdata2 =testdata2[['c1','c2','c3','c4','c5','c6']].replace(groupDict['regroup'])

    if testdata.loc['x',"moyenne_bac"]<11:
        testdata['Mention'] = 0.25
    elif testdata.loc['x',"moyenne_bac"]>11 and testdata.loc['x',"moyenne_bac"]<=13 :
        testdata['Mention'] = 0.5
    elif testdata.loc['x',"moyenne_bac"]>13 and testdata.loc['x',"moyenne_bac"]<=15 :
        testdata['Mention'] = 0.75
    else :
        testdata['Mention'] = 0.90
    testdata2[['wilaya_bac','moyenne_bac','sexe','Mention']]= testdata[['wilaya_bac','moyenne_bac','sexe','Mention']]
    testdata2['sexe'].replace(['FEMININ', 'MASCULIN'],[0, 1], inplace=True)

    
    ## turn the 10 first six choices into binary data for first model 

    ## Normalisation moyenne bac
    testdata2['moyenne_bac']= normaliser_med.transform(testdata2.moyenne_bac.to_numpy().reshape(-1, 1))


    ## model_med ######################################################################    
    ## map intferface code to model codes 
    classes = ['111', '21', '22', '23']

    for col in ['c1','c2', 'c3', 'c4', 'c5', 'c6']:

        if testdata2.loc['x',col] in classes:
            pass
        else:
            testdata2.loc['x',col] = 'OTH'
    testdatafinal = testdata2[['c1','c2', 'c3', 'c4', 'c5', 'c6']].apply(encoder_ens.transform)

    ## map some choices to OTHs
    outputsmodel_med= np.arange(0,4)
    #['111', '21', '22', '23']
    row =  []
    for i in range(1,7):

        if(testdatafinal.loc['x','c'+str(i)]) in outputsmodel_med:
            row.append(int(testdatafinal.loc['x','c'+str(i)]))
            
        else:
            row.append(4)


    ## turning codes into binary vector 

    ## l = testdatafinal[['c1', 'c2', 'c3', 'c4', 'c5','c6']].astype(int).values.flatten().tolist()
    l = [x-1 for x in row]
    m = np.zeros(5)
    m[l] = 1

    testdata=[]
    testdata.append(10)
    testdata.append(1)
    testdata.append(0.5)
    testdata.append(16)
    for i in m:
        testdata.append(i)
    testdata.append(np.exp2(10))


    Xnew = np.array(testdata).reshape((1,-1))
    result2 =model_med.predict_proba(Xnew)
    classes.append('OTH')

    return result2, row, classes


def prepModel_Prepa(temp):

    ## dataframe row created 
    testdata=pd.DataFrame({'x':temp}).transpose()

        
    testdata2 = testdata[['c1','c2','c3','c4','c5','c6']].astype(str).replace({'H14':'H00', 'H13':'H00', '711':'710', '712':'710', '713':'710','821':'820', '822':'820', '823':'820','121':'120', '122':'120', '123':'120', '841':'840', '842':'840' , '843':'840', '31':'300', '32':'300', '33':'300','21':'200', '22':'200', '23':'200', '41':'421', '42':'421', '43':'421', '44':'421', '611':'600', '612':'600', '613':'600', '614':'600', '101':'100', '102':'100', '11':'103', '12':'103', '13':'103', '14':'103','15':'103', '911':'910', '912':'910', '913':'910', '941':'940', '942':'940','721':'720', '722':'720', '723':'720','931':'930', '932':'930', '933':'930' })
    #testdata[['wilaya_bac','moyenne_bac','sexe','Mention']]= testdata[['wilaya_bac','moyenne_bac','sexe','Mention']]

    #### REPLACE WITH A LOADING FCT #######################
    my_dic = pd.read_excel("C:\\Users\\AzurComputer\\Downloads\\Codes de sortie (4).xlsx", sheet_name="Feuille 4", dtype={'code':str,'regroup': str}).fillna(method='ffill')
    my_dic['regroup']= my_dic['regroup'].astype(float).astype(int)
    my_dic['code '] = my_dic['code '].astype(str).apply(lambda x: x[:3])
    my_dic = my_dic.set_index('code ')
    groupDict = my_dic.to_dict()
    groupDict['regroup']['S38']=2

    ########################################################

    testdata2 =testdata2[['c1','c2','c3','c4','c5','c6']].replace(groupDict['regroup'])
    logging.debug(".>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
    logging.debug( testdata["moyenne_bac"])

    if testdata.loc['x',"moyenne_bac"]<11:
        testdata['Mention'] = 0.25
    elif testdata.loc['x',"moyenne_bac"]>11 and testdata.loc['x',"moyenne_bac"]<=13 :
        testdata['Mention'] = 0.5
    elif testdata.loc['x',"moyenne_bac"]>13 and testdata.loc['x',"moyenne_bac"]<=15 :
        testdata['Mention'] = 0.75
    else :
        testdata['Mention'] = 0.90

    testdata2[['wilaya_bac','moyenne_bac','sexe','Mention']]= testdata[['wilaya_bac','moyenne_bac','sexe','Mention']]
    testdata2['sexe'].replace(['FEMININ', 'MASCULIN'],[0, 1], inplace=True)

    
    ## turn the 10 first six choices into binary data for first model 

    ## Normalisation moyenne bac
    testdata2['moyenne_bac']= normaliser_prepaAll.transform(testdata2.moyenne_bac.to_numpy().reshape(-1, 1))


    ## model_prepaAll ######################################################################    
    ## map intferface code to model codes 

    classes = ['10', '11', '12', '13', '14', '15', '16', '6', '7', '8', '9']

    for col in ['c1','c2', 'c3', 'c4', 'c5', 'c6']:

        if testdata2.loc['x',col] in classes:
            pass
        else:
            testdata2.loc['x',col] = 'OTH'

    testdatafinal = testdata2[['c1','c2', 'c3', 'c4', 'c5', 'c6']].apply(encoder_ens.transform)
    
    ## map some choices to OTHs
    outputsmodel_prepaAll= np.arange(0,11)
    #['10', '11', '12', '13', '14', '15', '16', '6', '7', '8', '9']

    row =  []
    for i in range(1,7):
        if(testdatafinal.loc['x','c'+str(i)]) in outputsmodel_prepaAll:
            row.append(int(testdatafinal.loc['x','c'+str(i)]))
        else:
            row.append(11)

    ## turning codes into binary vector 

    #l = testdatafinal[['c1', 'c2', 'c3', 'c4', 'c5','c6']].astype(int).values.flatten().tolist()
    l = [x-1 for x in row]
    m = np.zeros(12)
    m[l] = 1

    testdata=[]
    testdata.append(10)
    testdata.append(1)
    testdata.append(0.5)
    testdata.append(16)
    for i in m:
        testdata.append(i)
    testdata.append(np.exp2(10))


    result3 =model_prepaAll.predict_proba(testdata)
    classes.append('OTH')


    return result3, row , classes



def prepModel_FormSup(temp):

    ## dataframe row created 
    testdata=pd.DataFrame({'x':temp}).transpose()

        
    testdata2 = testdata[['c1','c2','c3','c4','c5','c6']].astype(str).replace({'H14':'H00', 'H13':'H00', '711':'710', '712':'710', '713':'710','821':'820', '822':'820', '823':'820','121':'120', '122':'120', '123':'120', '841':'840', '842':'840' , '843':'840', '31':'300', '32':'300', '33':'300','21':'200', '22':'200', '23':'200', '41':'421', '42':'421', '43':'421', '44':'421', '611':'600', '612':'600', '613':'600', '614':'600', '101':'100', '102':'100', '11':'103', '12':'103', '13':'103', '14':'103','15':'103', '911':'910', '912':'910', '913':'910', '941':'940', '942':'940','721':'720', '722':'720', '723':'720','931':'930', '932':'930', '933':'930' })
    #testdata[['wilaya_bac','moyenne_bac','sexe','Mention']]= testdata[['wilaya_bac','moyenne_bac','sexe','Mention']]

    #### REPLACE WITH A LOADING FCT #######################
    my_dic = pd.read_excel("C:\\Users\\AzurComputer\\Downloads\\Codes de sortie (4).xlsx", sheet_name="Feuille 4", dtype={'code':str,'regroup': str}).fillna(method='ffill')
    my_dic['regroup']= my_dic['regroup'].astype(float).astype(int)
    my_dic['code '] = my_dic['code '].astype(str).apply(lambda x: x[:3])
    my_dic = my_dic.set_index('code ')
    groupDict = my_dic.to_dict()
    groupDict['regroup']['S38']=2

    ########################################################

    testdata2 =testdata2[['c1','c2','c3','c4','c5','c6']].replace(groupDict['regroup'])
    if testdata.loc['x',"moyenne_bac"]<11:
        testdata['Mention'] = 0.25
    elif testdata.loc['x',"moyenne_bac"]>11 and testdata.loc['x',"moyenne_bac"]<=13 :
        testdata['Mention'] = 0.5
    elif testdata.loc['x',"moyenne_bac"]>13 and testdata.loc['x',"moyenne_bac"]<=15 :
        testdata['Mention'] = 0.75
    else :
        testdata['Mention'] = 0.90
    testdata2[['wilaya_bac','moyenne_bac','sexe','Mention']]= testdata[['wilaya_bac','moyenne_bac','sexe','Mention']]
    testdata2['sexe'].replace(['FEMININ', 'MASCULIN'],[0, 1], inplace=True)

    
    ## turn the 10 first six choices into binary data for first model 

    ## Normalisation moyenne bac
    testdata2['moyenne_bac']= normaliser_formSup.transform(testdata2.moyenne_bac.to_numpy().reshape(-1, 1))


    ## model_prepaAll ######################################################################    
    ## map intferface code to model codes 
    
    classes = ['121', '122', '123', '124', '125', '126', '127', '128', '130',  '131', '132', '133', '134']

    for col in ['c1','c2', 'c3', 'c4', 'c5', 'c6']:

        if testdata2.loc['x',col] in classes:
            pass
        else:
            testdata2.loc['x',col] = 'OTH'
    testdatafinal = testdata2[['c1','c2', 'c3', 'c4', 'c5', 'c6']].apply(encoder_formSup.transform)
    
    ## map some choices to OTHs
    outputsmodel_FormSup= np.arange(0,13)
    #['121', '122', '123', '124', '125', '126', '127', '128', '130',  '131', '132', '133', '134']

    row =  []
    for i in range(1,7):
        if(testdatafinal.loc['x','c'+str(i)]) in outputsmodel_FormSup:
            row.append(int(testdatafinal.loc['x','c'+str(i)]))
        else:
            row.append(13)
 

    ## turning codes into binary vector 

    #l = testdatafinal[['c1', 'c2', 'c3', 'c4', 'c5','c6']].astype(int).values.flatten().tolist()
    l = [x-1 for x in row]
    m = np.zeros(15)
    m[l] = 1

    testdata=[]
    testdata.append(10)
    testdata.append(1)
    testdata.append(0.5)
    testdata.append(16)
    for i in m:
        testdata.append(i)
    testdata.append(np.exp2(10))

    result3 =model_formSup.predict_proba(testdata)
    classes.append('OTH')

    return result3, row, classes





    
def prepModel_FormUniv(temp):

    ## dataframe row created 
    testdata=pd.DataFrame({'x':temp}).transpose()

        
    testdata2 = testdata[['c1','c2','c3','c4','c5','c6']].astype(str).replace({'H14':'H00', 'H13':'H00', '711':'710', '712':'710', '713':'710','821':'820', '822':'820', '823':'820','121':'120', '122':'120', '123':'120', '841':'840', '842':'840' , '843':'840', '31':'300', '32':'300', '33':'300','21':'200', '22':'200', '23':'200', '41':'421', '42':'421', '43':'421', '44':'421', '611':'600', '612':'600', '613':'600', '614':'600', '101':'100', '102':'100', '11':'103', '12':'103', '13':'103', '14':'103','15':'103', '911':'910', '912':'910', '913':'910', '941':'940', '942':'940','721':'720', '722':'720', '723':'720','931':'930', '932':'930', '933':'930' })

    #testdata[['wilaya_bac','moyenne_bac','sexe','Mention']]= testdata[['wilaya_bac','moyenne_bac','sexe','Mention']]


    #### REPLACE WITH A LOADING FCT #######################
    my_dic = pd.read_excel("C:\\Users\\AzurComputer\\Downloads\\Codes de sortie (4).xlsx", sheet_name="Feuille 4", dtype={'code':str,'regroup': str}).fillna(method='ffill')
    my_dic['regroup']= my_dic['regroup'].astype(float).astype(int)
    my_dic['code '] = my_dic['code '].astype(str).apply(lambda x: x[:3])
    my_dic = my_dic.set_index('code ')
    groupDict = my_dic.to_dict()
    groupDict['regroup']['S38']=2

    ########################################################

    testdata2 =testdata2[['c1','c2','c3','c4','c5','c6']].replace(groupDict['regroup'])
    if testdata.loc['x',"moyenne_bac"]<11:
        testdata['Mention'] = 0.25
    elif testdata.loc['x',"moyenne_bac"]>11 and testdata.loc['x',"moyenne_bac"]<=13 :
        testdata['Mention'] = 0.5
    elif testdata.loc['x',"moyenne_bac"]>13 and testdata.loc['x',"moyenne_bac"]<=15 :
        testdata['Mention'] = 0.75
    else :
        testdata['Mention'] = 0.90

    testdata2[['wilaya_bac','moyenne_bac','sexe','Mention']]= testdata[['wilaya_bac','moyenne_bac','sexe','Mention']]
    testdata2['sexe'].replace(['FEMININ', 'MASCULIN'],[0, 1], inplace=True)

    
    ## turn the 10 first six choices into binary data for first model 

    ## Normalisation moyenne bac
    testdata2['moyenne_bac']= normaliser_formUniv.transform(testdata2.moyenne_bac.to_numpy().reshape(-1, 1))


    ## model_prepaAll ######################################################################    
    ## map intferface code to model codes 
    classes = ['1', '100', '101', '103', '108', '109', '110', '120', '24', '29',
       '3', '30', '32', '39', '40', '41', '43', '45', '46', '48', '51',
       '54', '55', '59', '60', '62', '63', '90', '91', '92', '96', '97',
       '99', 'OthUniv']

    for col in ['c1','c2', 'c3', 'c4', 'c5', 'c6']:

        if testdata2.loc['x',col] in classes:
            pass
        else:
            testdata2.loc['x',col] = 'OTH'
    testdatafinal = testdata2[['c1','c2', 'c3', 'c4', 'c5', 'c6']].apply(encoder_formUniv.transform)
    
    ## map some choices to OTHs
    outputsmodel_FormUniv= np.arange(0,34)
    """['1', '100', '101', '103', '108', '109', '110', '120', '24', '29',
       '3', '30', '32', '39', '40', '41', '43', '45', '46', '48', '51',
       '54', '55', '59', '60', '62', '63', '90', '91', '92', '96', '97',
       '99', 'OthUniv']
    """
    row =  [10]
    for i in range(1,7):
        if(testdatafinal.loc['x','c'+str(i)]) in outputsmodel_FormUniv:
            row.append(int(testdatafinal.loc['x','c'+str(i)]))
        else:
            row.append(34)
    

    ## turning codes into binary vector 

    #l = testdatafinal[['c1', 'c2', 'c3', 'c4', 'c5','c6']].astype(int).values.flatten().tolist()
    l = [x-1 for x in row]
    m = np.zeros(35)
    m[l] = 1

    testdata=[]
    testdata.append(10)
    testdata.append(1)
    testdata.append(0.5)
    testdata.append(16)
    for i in m:
        testdata.append(i)
    testdata.append(np.exp2(10))

    result3 =model_formUniv.predict_proba(testdata)
    classes.append('OTH')


    return result3, row , classes