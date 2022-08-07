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
        