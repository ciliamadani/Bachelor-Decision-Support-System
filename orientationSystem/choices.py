import json
import pickle
import pandas as pd
import numpy as np 
import logging

## loading models
model1=pickle.load(open('orientationSystem/model/models/H5finalized_model1_4000_.sav','rb+'))
model2=pickle.load(open('orientationSystem/model/models/H5finalized_model2_2000_4000.sav','rb+'))
model3=pickle.load(open('orientationSystem/model/models/H5finalized_model3_500_2000.sav','rb+'))
model4=pickle.load(open('orientationSystem/model/models/H5finalized_model4_200_500.sav','rb+'))
model5=pickle.load(open('orientationSystem/model/models/H5finalized_model5_100_200.sav','rb+'))

## loading encoders
encoder1 = pickle.load(open('orientationSystem/model/encoders/h5encoder1.pkl','rb+'))
encoder2 = pickle.load(open('orientationSystem/model/encoders/h5encoder2.pkl','rb+'))
encoder3 = pickle.load(open('orientationSystem/model/encoders/h5encoder3.pkl','rb+'))
encoder4 = pickle.load(open('orientationSystem/model/encoders/h5encoder4.pkl','rb+'))
encoder5 = pickle.load(open('orientationSystem/model/encoders/h5encoder5.pkl','rb+'))



## loading models
model_ens =pickle.load(open('orientationSystem/model/model_approche2/ENS_CATBOOST.pkl','rb+'))
model_med=pickle.load(open('orientationSystem/model/model_approche2/MED_CATBOOST.pkl','rb+'))
model_prepaAll=pickle.load(open('orientationSystem/model/model_approche2/PrepaAllClasses_CATBOOST.pkl','rb+'))
model_formUniv=pickle.load(open('orientationSystem/model/model_approche2/UNIV_CATBOOST.pkl','rb+'))
model_formSup=pickle.load(open('orientationSystem/model/model_approche2/FormSup_CATBOOST.pkl','rb+'))

## loading encoders
encoder_ens = pickle.load(open('orientationSystem/model/model_approche2/encoders/encoder_ENS.pkl','rb+'))
encoder_med = pickle.load(open('orientationSystem/model/model_approche2/encoders/encoder_med.pkl','rb+'))
encoder_prepaAll = pickle.load(open('orientationSystem/model/model_approche2/encoders/encoder_prepaAll.pkl','rb+'))
encoder_formUniv = pickle.load(open('orientationSystem/model/model_approche2/encoders/encoder_univ.pkl','rb+'))
encoder_formSup = pickle.load(open('orientationSystem/model/model_approche2/encoders/encoder_formSup.pkl','rb+'))

def prepModel_ENS(temp):
    """
    input : ditionnary of student info 
    output: model predctions  
    """

    ## dataframe row created 
    testdata=pd.DataFrame({'x':temp}).transpose()

    
    testdata = testdata[['c1','c2','c3','c4','c5','c6']].astype(str).replace({'H14':'H00', 'H13':'H00', '711':'710', '712':'710', '713':'710','821':'820', '822':'820', '823':'820','121':'120', '122':'120', '123':'120', '841':'840', '842':'840' , '843':'840', '31':'300', '32':'300', '33':'300','21':'200', '22':'200', '23':'200', '41':'421', '42':'421', '43':'421', '44':'421', '611':'600', '612':'600', '613':'600', '614':'600', '101':'100', '102':'100', '11':'103', '12':'103', '13':'103', '14':'103','15':'103', '911':'910', '912':'910', '913':'910', '941':'940', '942':'940','721':'720', '722':'720', '723':'720','931':'930', '932':'930', '933':'930' })
    
    ###############
    #testdata[['WILAYA_BAC','MOYENNE_BAC','sexe','Mention']]= testdata[['WILAYA_BAC','MOYENNE_BAC','sexe','Mention']]
    ############

    testdata[['WILAYA_BAC','MOYENNE_BAC','sexe','Mention']]=[16,15,1,0.5]

    #### REPLACE WITH A LOADING FCT #######################
    my_dic = pd.read_excel("C:\\Users\\AzurComputer\\Downloads\\Codes de sortie (4).xlsx", sheet_name="Feuille 4", dtype={'code':str,'regroup': str}).fillna(method='ffill')
    my_dic['regroup']= my_dic['regroup'].astype(float).astype(int)
    my_dic['code '] = my_dic['code '].astype(str).apply(lambda x: x[:3])
    my_dic = my_dic.set_index('code ')
    groupDict = my_dic.to_dict()
    groupDict['regroup']['S38']=2

    ########################################################

    testdata2 =testdata[['c1','c2','c3','c4','c5','c6']].replace(groupDict['regroup'])
    testdata2[['WILAYA_BAC','MOYENNE_BAC','sexe','Mention']]= testdata[['WILAYA_BAC','MOYENNE_BAC','sexe','Mention']]




    ## turn the 10 first six choices into binary data for first model 

    ## Normalisation moyenne bac
    pass

    ## model_ens ######################################################################    
    ## map intferface code to model codes 
    classes = ['66', '67', '69', '70', '71', '72', '73', '75', '76', '77', '80',   '81', '84', '85', 'OthEns']

    for col in ['c1','c2', 'c3', 'c4', 'c5', 'c6']:

        if testdata2.loc['x',col] in classes:
            pass
        else:
            testdata2.loc['x',col] = 'OTH'

    logging.debug("/////////////////333333333333 /////////////////")
    logging.debug(testdata2[['c1','c2', 'c3', 'c4', 'c5', 'c6']])
    testdatafinal = testdata2[['c1','c2', 'c3', 'c4', 'c5', 'c6']].apply(encoder_ens.transform)
    
    ## map some choices to OTHs
    outputsmodel_ens= np.arange(0,15)
    #['66', '67', '69', '70', '71', '72', '73', '75', '76', '77', '80',    '81', '84', '85', 'OthEns']
    row =  [10]
    for i in range(1,6):


        if(testdatafinal.loc['x','c'+str(i)]) in outputsmodel_ens:
            row.append(temp['c'+str(i)])
        else:
            row.append(5)
    logging.debug(row)
    ## turning codes into binary vector 

    l = testdatafinal[['c1', 'c2', 'c3', 'c4', 'c5','c6']].astype(int).values.flatten().tolist()
    l = [x-1 for x in l]
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

    logging.debug("fnal")
    logging.debug(testdata)
    result1 =model_ens.predict_proba(testdata)

    classes.append('OTH')

    return result1, row, classes


def prepModel_MED(temp):

    
    ## dataframe row created 
    testdata=pd.DataFrame({'x':temp}).transpose()
        
    testdata = testdata[['c1','c2','c3','c4','c5','c6']].astype(str).replace({'H14':'H00', 'H13':'H00', '711':'710', '712':'710', '713':'710','821':'820', '822':'820', '823':'820','121':'120', '122':'120', '123':'120', '841':'840', '842':'840' , '843':'840', '31':'300', '32':'300', '33':'300','21':'200', '22':'200', '23':'200', '41':'421', '42':'421', '43':'421', '44':'421', '611':'600', '612':'600', '613':'600', '614':'600', '101':'100', '102':'100', '11':'103', '12':'103', '13':'103', '14':'103','15':'103', '911':'910', '912':'910', '913':'910', '941':'940', '942':'940','721':'720', '722':'720', '723':'720','931':'930', '932':'930', '933':'930' })
    #testdata[['WILAYA_BAC','MOYENNE_BAC','sexe','Mention']]= testdata[['WILAYA_BAC','MOYENNE_BAC','sexe','Mention']]
    testdata[['WILAYA_BAC','MOYENNE_BAC','sexe','Mention']]=[16,15,1,0.5]

    #### REPLACE WITH A LOADING FCT #######################
    my_dic = pd.read_excel("C:\\Users\\AzurComputer\\Downloads\\Codes de sortie (4).xlsx", sheet_name="Feuille 4", dtype={'code':str,'regroup': str}).fillna(method='ffill')
    my_dic['regroup']= my_dic['regroup'].astype(float).astype(int)
    my_dic['code '] = my_dic['code '].astype(str).apply(lambda x: x[:3])
    my_dic = my_dic.set_index('code ')
    groupDict = my_dic.to_dict()
    groupDict['regroup']['S38']=2

    ########################################################

    testdata2 =testdata[['c1','c2','c3','c4','c5','c6']].replace(groupDict['regroup'])
    testdata2[['WILAYA_BAC','MOYENNE_BAC','sexe','Mention']]= testdata[['WILAYA_BAC','MOYENNE_BAC','sexe','Mention']]


    
    ## turn the 10 first six choices into binary data for first model 

    ## Normalisation moyenne bac
    pass

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
    row =  [10]
    for i in range(1,7):

        if(testdatafinal.loc['x','c'+str(i)]) in outputsmodel_med:
            row.append(temp['c'+str(i)])
            
        else:
            row.append(7)
    logging.debug(row)

    ## turning codes into binary vector 

    l = testdatafinal[['c1', 'c2', 'c3', 'c4', 'c5','c6']].astype(int).values.flatten().tolist()
    l = [x-1 for x in l]
    m = np.zeros(14)
    m[l] = 1

    testdata=[]
    testdata.append(10)
    testdata.append(1)
    testdata.append(0.5)
    testdata.append(16)
    for i in m:
        testdata.append(i)
    testdata.append(np.exp2(10))


    logging.debug("fnal")
    logging.debug(testdata)
    result2 =model_med.predict_proba(testdata)
    classes.append('OTH')

    return result2, row, classes


def prepModel_Prepa(temp):

    ## dataframe row created 
    testdata=pd.DataFrame({'x':temp}).transpose()

        
    testdata = testdata[['c1','c2','c3','c4','c5','c6']].astype(str).replace({'H14':'H00', 'H13':'H00', '711':'710', '712':'710', '713':'710','821':'820', '822':'820', '823':'820','121':'120', '122':'120', '123':'120', '841':'840', '842':'840' , '843':'840', '31':'300', '32':'300', '33':'300','21':'200', '22':'200', '23':'200', '41':'421', '42':'421', '43':'421', '44':'421', '611':'600', '612':'600', '613':'600', '614':'600', '101':'100', '102':'100', '11':'103', '12':'103', '13':'103', '14':'103','15':'103', '911':'910', '912':'910', '913':'910', '941':'940', '942':'940','721':'720', '722':'720', '723':'720','931':'930', '932':'930', '933':'930' })
    #testdata[['WILAYA_BAC','MOYENNE_BAC','sexe','Mention']]= testdata[['WILAYA_BAC','MOYENNE_BAC','sexe','Mention']]
    testdata[['WILAYA_BAC','MOYENNE_BAC','sexe','Mention']]=[16,15,1,0.5]

    #### REPLACE WITH A LOADING FCT #######################
    my_dic = pd.read_excel("C:\\Users\\AzurComputer\\Downloads\\Codes de sortie (4).xlsx", sheet_name="Feuille 4", dtype={'code':str,'regroup': str}).fillna(method='ffill')
    my_dic['regroup']= my_dic['regroup'].astype(float).astype(int)
    my_dic['code '] = my_dic['code '].astype(str).apply(lambda x: x[:3])
    my_dic = my_dic.set_index('code ')
    groupDict = my_dic.to_dict()
    groupDict['regroup']['S38']=2

    ########################################################

    testdata2 =testdata[['c1','c2','c3','c4','c5','c6']].replace(groupDict['regroup'])
    testdata2[['WILAYA_BAC','MOYENNE_BAC','sexe','Mention']]= testdata[['WILAYA_BAC','MOYENNE_BAC','sexe','Mention']]


    
    ## turn the 10 first six choices into binary data for first model 

    ## Normalisation moyenne bac
    pass

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

    row =  [10]
    for i in range(1,7):
        if(testdatafinal.loc['x','c'+str(i)]) in outputsmodel_prepaAll:
            row.append(temp['c'+str(i)])
        else:
            row.append(31)
    logging.debug(row)

    ## turning codes into binary vector 

    l = testdatafinal[['c1', 'c2', 'c3', 'c4', 'c5','c6']].astype(int).values.flatten().tolist()
    l = [x-1 for x in l]
    m = np.zeros(55)
    m[l] = 1

    testdata=[]
    testdata.append(10)
    testdata.append(1)
    testdata.append(0.5)
    testdata.append(16)
    for i in m:
        testdata.append(i)
    testdata.append(np.exp2(10))


    logging.debug("fnal")
    logging.debug(testdata)
    result3 =model_prepaAll.predict_proba(testdata)
    classes.append('OTH')


    return result3, row , classes



def prepModel_FormSup(temp):

    ## dataframe row created 
    testdata=pd.DataFrame({'x':temp}).transpose()

        
    testdata = testdata[['c1','c2','c3','c4','c5','c6']].astype(str).replace({'H14':'H00', 'H13':'H00', '711':'710', '712':'710', '713':'710','821':'820', '822':'820', '823':'820','121':'120', '122':'120', '123':'120', '841':'840', '842':'840' , '843':'840', '31':'300', '32':'300', '33':'300','21':'200', '22':'200', '23':'200', '41':'421', '42':'421', '43':'421', '44':'421', '611':'600', '612':'600', '613':'600', '614':'600', '101':'100', '102':'100', '11':'103', '12':'103', '13':'103', '14':'103','15':'103', '911':'910', '912':'910', '913':'910', '941':'940', '942':'940','721':'720', '722':'720', '723':'720','931':'930', '932':'930', '933':'930' })
    #testdata[['WILAYA_BAC','MOYENNE_BAC','sexe','Mention']]= testdata[['WILAYA_BAC','MOYENNE_BAC','sexe','Mention']]
    testdata[['WILAYA_BAC','MOYENNE_BAC','sexe','Mention']]=[16,15,1,0.5]

    #### REPLACE WITH A LOADING FCT #######################
    my_dic = pd.read_excel("C:\\Users\\AzurComputer\\Downloads\\Codes de sortie (4).xlsx", sheet_name="Feuille 4", dtype={'code':str,'regroup': str}).fillna(method='ffill')
    my_dic['regroup']= my_dic['regroup'].astype(float).astype(int)
    my_dic['code '] = my_dic['code '].astype(str).apply(lambda x: x[:3])
    my_dic = my_dic.set_index('code ')
    groupDict = my_dic.to_dict()
    groupDict['regroup']['S38']=2

    ########################################################

    testdata2 =testdata[['c1','c2','c3','c4','c5','c6']].replace(groupDict['regroup'])
    testdata2[['WILAYA_BAC','MOYENNE_BAC','sexe','Mention']]= testdata[['WILAYA_BAC','MOYENNE_BAC','sexe','Mention']]


    
    ## turn the 10 first six choices into binary data for first model 

    ## Normalisation moyenne bac
    pass

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

    row =  [10]
    for i in range(1,6):
        if(testdatafinal.loc['x','c'+str(i)]) in outputsmodel_FormSup:
            row.append(temp['c'+str(i)])
        else:
            row.append(135)
    logging.debug(row)

    ## turning codes into binary vector 

    l = testdatafinal[['c1', 'c2', 'c3', 'c4', 'c5','c6']].astype(int).values.flatten().tolist()
    l = [x-1 for x in l]
    m = np.zeros(55)
    m[l] = 1

    testdata=[]
    testdata.append(10)
    testdata.append(1)
    testdata.append(0.5)
    testdata.append(16)
    for i in m:
        testdata.append(i)
    testdata.append(np.exp2(10))


    logging.debug("fnal")
    logging.debug(testdata)
    result3 =model_formSup.predict_proba(testdata)
    classes.append('OTH')

    return result3, row, classes





    
def prepModel_FormUniv(temp):

    ## dataframe row created 
    testdata=pd.DataFrame({'x':temp}).transpose()

        
    testdata = testdata[['c1','c2','c3','c4','c5','c6']].astype(str).replace({'H14':'H00', 'H13':'H00', '711':'710', '712':'710', '713':'710','821':'820', '822':'820', '823':'820','121':'120', '122':'120', '123':'120', '841':'840', '842':'840' , '843':'840', '31':'300', '32':'300', '33':'300','21':'200', '22':'200', '23':'200', '41':'421', '42':'421', '43':'421', '44':'421', '611':'600', '612':'600', '613':'600', '614':'600', '101':'100', '102':'100', '11':'103', '12':'103', '13':'103', '14':'103','15':'103', '911':'910', '912':'910', '913':'910', '941':'940', '942':'940','721':'720', '722':'720', '723':'720','931':'930', '932':'930', '933':'930' })
    testdata[['WILAYA_BAC','MOYENNE_BAC','sexe','Mention']]=[16,15,1,0.5]

    testdata[['WILAYA_BAC','MOYENNE_BAC','sexe','Mention']]= testdata[['WILAYA_BAC','MOYENNE_BAC','sexe','Mention']]


    #### REPLACE WITH A LOADING FCT #######################
    my_dic = pd.read_excel("C:\\Users\\AzurComputer\\Downloads\\Codes de sortie (4).xlsx", sheet_name="Feuille 4", dtype={'code':str,'regroup': str}).fillna(method='ffill')
    my_dic['regroup']= my_dic['regroup'].astype(float).astype(int)
    my_dic['code '] = my_dic['code '].astype(str).apply(lambda x: x[:3])
    my_dic = my_dic.set_index('code ')
    groupDict = my_dic.to_dict()
    groupDict['regroup']['S38']=2

    ########################################################

    testdata2 =testdata[['c1','c2','c3','c4','c5','c6']].replace(groupDict['regroup'])
    #testdata2[['WILAYA_BAC','MOYENNE_BAC','sexe','Mention']]= testdata[['WILAYA_BAC','MOYENNE_BAC','sexe','Mention']]
    testdata[['WILAYA_BAC','MOYENNE_BAC','sexe','Mention']]=[16,15,1,0.5]

    
    ## turn the 10 first six choices into binary data for first model 

    ## Normalisation moyenne bac
    pass

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
            row.append(temp['c'+str(i)])
        else:
            row.append(31)
    logging.debug(row)

    ## turning codes into binary vector 

    l = testdatafinal[['c1', 'c2', 'c3', 'c4', 'c5','c6']].astype(int).values.flatten().tolist()
    l = [x-1 for x in l]
    m = np.zeros(55)
    m[l] = 1

    testdata=[]
    testdata.append(10)
    testdata.append(1)
    testdata.append(0.5)
    testdata.append(16)
    for i in m:
        testdata.append(i)
    testdata.append(np.exp2(10))

    logging.debug("fnal")
    logging.debug(testdata)
    result3 =model_formUniv.predict_proba(testdata)
    classes.append('OTH')


    return result3, row , classes
outputDictionary = {}


def read_choices():
    with open('orientationSystem/choices.json', 'r') as f:
        my_json_obj = json.load(f)

    return my_json_obj


def read_label_choices():
    with open("orientationSystem\model\codesDic.pkl", "rb") as f:
        dictionnary  = pickle.load(f)

    return dictionnary


def prepModel1(temp):
    """
    input : ditionnary of student info 
    output: model predctions  
    """

    logging.debug("In Model1")
    ## dataframe row created 
    testdata=pd.DataFrame({'x':temp}).transpose()

    ## turn the 10 first six choices into binary data for first model 

    ## Normalisation moyenne bac
    pass
       
    ## map some choices to OTHs
    outputsModel1= ['X03', '600', '421', '300', '103', '700']
    row =  []
    
    for i in range(1,11):

        if(testdata['c'+str(i)]['x']) in outputsModel1:
            row.append(temp['c'+i])
        else:
            row.append('OTH')

    ## map intferface code to model codes 
    encoder1 = pickle.load(open('orientationSystem/model/encoders/h5encoder1.pkl','rb+'))
    testdata[['c1','c2', 'c3', 'c4', 'c5', 'c6']]= row[:6] 
    logging.debug(testdata[['c1','c2', 'c3', 'c4', 'c5', 'c6']])

    testdatafinal = testdata[['c1','c2', 'c3', 'c4', 'c5', 'c6']].apply(encoder1.transform)
    ## turning codes into binary vector 


    l = testdatafinal[['c1', 'c2', 'c3', 'c4', 'c5','c6']].astype(int).values.flatten().tolist()
    l = [x-1 for x in l]
    m = np.zeros(7)
    m[l] = 1

    finalrow=[]
    ## moyenne apres normalisation
    finalrow.append(0.5)
    ## sexe
    finalrow.append(0)
    ## mention
    finalrow.append(0.5)

    ## wilaya
    finalrow.append(16)
    ## bin data 
    for i in m:
        finalrow.append(i) 

    ## exp2 moy 
    finalrow.append(np.exp2(0.5))

    result1 =model1.predict_proba(finalrow)

    return result1, row


def prepModel2(temp):

    logging.debug("In Model2")

    
    ## dataframe row created 
    testdata=pd.DataFrame({'x':temp}).transpose()
    
    ## turn the 10 first six choices into binary data for first model 

    ## Normalisation moyenne bac
    pass

    ## MODEL2 ######################################################################    
    ## map intferface code to model codes 
    encoder2 = pickle.load(open('orientationSystem/model/encoders/h5encoder2.pkl','rb+'))
        
    ## map some choices to OTHs
    outputsModel2= ['120', '200', '701', '710', '910', 'H00']
    row =  []
    
    for i in range(1,11):
        if(testdata['c'+str(i)]['x']) in outputsModel2:
            row.append(temp['c'+str(i)])
        else:
            row.append('OTH')


    ## map intferface code to model codes 
    encoder2 = pickle.load(open('orientationSystem/model/encoders/h5encoder2.pkl','rb+'))
    testdata[['c1','c2', 'c3', 'c4', 'c5', 'c6']]= row[:6]
    logging.debug(testdata[['c1','c2', 'c3', 'c4', 'c5', 'c6']])

    testdatafinal = testdata[['c1','c2', 'c3', 'c4', 'c5', 'c6']].apply(encoder2.transform)

    l = testdatafinal[['c1', 'c2', 'c3', 'c4', 'c5','c6']].astype(int).values.flatten().tolist()

    l = [x-1 for x in l]
    m = np.zeros(7)
    m[l] = 1

    finalrow=[]
    ## moyenne apres normalisation
    finalrow.append(0.5)
    ## sexe
    finalrow.append(0)
    ## mention
    finalrow.append(0.5)

    ## wilaya
    finalrow.append(16)
    ## bin data 
    for i in m:
        finalrow.append(i) 

    ## exp2 moy 
    finalrow.append(np.exp2(0.5))


    logging.debug("PRINTING INPUT OF MODEL2")
    
    Xnew = np.array(finalrow).reshape((1,-1))
    logging.debug(Xnew)

    result2 =model2.predict_proba(Xnew)

    return result2, row


def prepModel3(temp):

    logging.debug("In Model3")

    
    ## dataframe row created 
    testdata=pd.DataFrame({'x':temp}).transpose()
    
    ## turn the 10 first six choices into binary data for first model 

    ## Normalisation moyenne bac
    pass

    ## MODEL3 ######################################################################    
    ## map intferface code to model codes 
    encoder3 = pickle.load(open('orientationSystem/model/encoders/h5encoder3.pkl','rb+'))
        
    ## map some choices to OTHs
    outputsModel3= ['W01', '930', 'X04', '100', '940', '521', '702', '820',
       '511', '840']
    row =  []
    
    for i in range(1,11):
        if(testdata['c'+str(i)]['x']) in outputsModel3:
            row.append(temp['c'+str(i)])
        else:
            row.append('OTH')


    ## map intferface code to model codes 
    encoder3 = pickle.load(open('orientationSystem/model/encoders/h5encoder3.pkl','rb+'))
    testdata[['c1','c2', 'c3', 'c4', 'c5', 'c6']]= row[:6]
    logging.debug(testdata[['c1','c2', 'c3', 'c4', 'c5', 'c6']])

    testdatafinal = testdata[['c1','c2', 'c3', 'c4', 'c5', 'c6']].apply(encoder3.transform)

    l = testdatafinal[['c1', 'c2', 'c3', 'c4', 'c5','c6']].astype(int).values.flatten().tolist()
    l = [x-1 for x in l]
    m = np.zeros(11)
    m[l] = 1

    finalrow=[]
    ## moyenne apres normalisation
    finalrow.append(0.5)
    ## sexe
    finalrow.append(0)
    ## mention
    finalrow.append(0.5)

    ## wilaya
    finalrow.append(16)
    ## bin data 
    for i in m:
        finalrow.append(i) 

    ## exp2 moy 
    finalrow.append(np.exp2(0.5))

    Xnew = np.array(finalrow).reshape((1,-1))   
    result3 =model3.predict_proba(Xnew)

    return result3, row


def prepModel4(temp):

    logging.debug("In Model4")

    
    ## dataframe row created 
    testdata=pd.DataFrame({'x':temp}).transpose()
    
    ## turn the 10 first six choices into binary data for first model 

    ## Normalisation moyenne bac
    pass

    ## MODEL2 ######################################################################    
    ## map intferface code to model codes 
    encoder4 = pickle.load(open('orientationSystem/model/encoders/h5encoder4.pkl','rb+'))
        
    ## map some choices to OTHs
    outputsModel4= ['X13', '400', 'L01', 'X07', 'E03', 'F12', 'S04', '409',
       '415', '703', 'K01', 'EC1', 'E33', '522', 'EC2', 'E04', '720',
       'L04', 'M05', 'E32', 'EC3', 'C32', '513']
    row =  []
    
    for i in range(1,11):
        if(testdata['c'+str(i)]['x']) in outputsModel4:
            row.append(temp['c'+str(i)])
        else:
            row.append('OTH')


    ## map intferface code to model codes 
    encoder4 = pickle.load(open('orientationSystem/model/encoders/h5encoder4.pkl','rb+'))
    testdata[['c1','c2', 'c3', 'c4', 'c5', 'c6']]= row[:6]
    logging.debug(testdata[['c1','c2', 'c3', 'c4', 'c5', 'c6']])

    testdatafinal = testdata[['c1','c2', 'c3', 'c4', 'c5', 'c6']].apply(encoder4.transform)

    l = testdatafinal[['c1', 'c2', 'c3', 'c4', 'c5','c6']].astype(int).values.flatten().tolist()
    l = [x-1 for x in l]
    m = np.zeros(24)
    m[l] = 1

    finalrow=[]
    ## moyenne apres normalisation
    finalrow.append(0.5)
    ## sexe
    finalrow.append(0)
    ## mention
    finalrow.append(0.5)

    ## wilaya
    finalrow.append(16)
    ## bin data 
    for i in m:
        finalrow.append(i) 

    ## exp2 moy 
    finalrow.append(np.exp2(0.5))

    result4 =model4.predict_proba(finalrow)

    return result4, row


def prepModel5(temp):
    logging.debug("IN MODEL5")

    
    ## dataframe row created 
    testdata=pd.DataFrame({'x':temp}).transpose()
    
    ## turn the 10 first six choices into binary data for first model 

    ## Normalisation moyenne bac
    pass

    ## MODEL5 ######################################################################    
    ## map intferface code to model codes 
    encoder5 = pickle.load(open('orientationSystem/model/encoders/h5encoder5.pkl','rb+'))

        
    ## map some choices to OTHs
    outputsModel5= ['X01', 'C12', 'X05', 'C02', 'E23', '408', '143', 'M07',
       'C38', 'T10', 'E31', 'D11', 'C37', 'C33', 'E01', 'C05', '423',
       'F23', 'C35', 'EC4', 'C34', 'C31', 'F08', 'C09', 'L03', 'C07']
    row =  []

    for i in range(1,11):
        if(testdata['c'+str(i)]['x']) in outputsModel5:
            row.append(temp['c'+str(i)])
        else:
            row.append('OTH')

    ## map intferface code to model codes 
    encoder5 = pickle.load(open('orientationSystem/model/encoders/h5encoder5.pkl','rb+'))
    testdata[['c1','c2', 'c3', 'c4', 'c5', 'c6']]= row [:6]
    logging.debug(testdata[['c1','c2', 'c3', 'c4', 'c5', 'c6']])

    testdatafinal = testdata[['c1','c2', 'c3', 'c4', 'c5', 'c6']].apply(encoder5.transform)
    ## turning codes into binary vector 

    l = testdatafinal[['c1', 'c2', 'c3', 'c4', 'c5','c6']].astype(int).values.flatten().tolist()
    l = [x-1 for x in l]
    m = np.zeros(27)
    m[l] = 1

    finalrow=[]
    ## moyenne apres normalisation
    finalrow.append(0.5)
    ## sexe
    finalrow.append(0)
    ## mention
    finalrow.append(0.5)

    ## wilaya
    finalrow.append(16)
    ## bin data 
    for i in m:
        finalrow.append(i) 

    ## exp2 moy 
    finalrow.append(np.exp2(0.5))

    result5 =model5.predict_proba(finalrow)

    return result5, row
        