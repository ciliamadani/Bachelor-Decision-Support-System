
from django.http import HttpResponse
from django.shortcuts import render
import math
import pandas as pd
import pickle
from .form import NameForm
import logging
import numpy as np
from .choices import prepModel_ENS, prepModel_MED, prepModel_FormUniv, prepModel_FormSup, prepModel_Prepa, read_label_choices, prepModel1, prepModel2, prepModel3, prepModel4, prepModel5

choices =read_label_choices()
CODE_CHOICES= []
outputDictionary = {}


## loading encoders
encoder1 = pickle.load(open('orientationSystem/model/encoders/h5encoder1.pkl','rb+'))
encoder2 = pickle.load(open('orientationSystem/model/encoders/h5encoder2.pkl','rb+'))
encoder3 = pickle.load(open('orientationSystem/model/encoders/h5encoder3.pkl','rb+'))
encoder4 = pickle.load(open('orientationSystem/model/encoders/h5encoder4.pkl','rb+'))
encoder5 = pickle.load(open('orientationSystem/model/encoders/h5encoder5.pkl','rb+'))

outputsModel1= ['X03', '600', '421', '300', '103', '700']
outputsModel2= ['H00', '200', '701', '710', '910', '120']
outputsModel3= ['W01', '930', 'X04', '100', '940', '521', '702', '820',
       '511', '840']

       
outputsModel4= ['X13', '400', 'L01', 'X07', 'E03', 'F12', 'S04', '409',
       '415', '703', 'K01', 'EC1', 'E33', '522', 'EC2', 'E04', '720',
       'L04', 'M05', 'E32', 'EC3', 'C32', '513']
outputsModel5= ['X01', 'C12', 'X05', 'C02', 'E23', '408', '143', 'M07',
       'C38', 'T10', 'E31', 'D11', 'C37', 'C33', 'E01', 'C05', '423',
       'F23', 'C35', 'EC4', 'C34', 'C31', 'F08', 'C09', 'L03', 'C07', 'OTH']


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def get_name(request):
    # if this is a POST request we need to process the form data
        # create a form instance and populate it with data from the request:
    form = NameForm()
    logging.debug("................................................")

    """    if form.is_valid():
            logging.debug("VALIIIID.....................")"""
    ##if request.method =='POST':   
    if request.POST.get('NameOfYourButton') == 'YourValue':


                ## save form using a session 
        #request.session.save()
        request.session["c1"] = str(request.POST.get('choice1'))  
        request.session["c2"] =str(request.POST.get('choice2')) 
        request.session["c3"] =str(request.POST.get('choice3')) 
        request.session["c4"] = str(request.POST.get('choice4')) 
        request.session["c5"] = str(request.POST.get('choice5')) 
        request.session["c6"] = str(request.POST.get('choice6')) 
        request.session["c7"] = str(request.POST.get('choice7'))  
        request.session["c8"] = str(request.POST.get('choice8')) 
        request.session["c9"] = str(request.POST.get('choice9')) 
        request.session["c10"] = str(request.POST.get('choice10')) 
        request.session.modified = True


        c1 = request.session.get("c1")
        c2 = request.session.get("c2")
        c3 = request.session.get("c3")
        c4 = request.session.get("c4")
        c5 = request.session.get("c5")
        c6 = request.session.get("c6")
        c7 = request.session.get("c7")
        c8 = request.session.get("c8")
        c9 = request.session.get("c9")
        c10 = request.session.get("c10")

        """        ## test session
                logging.debug("TESTING THE SESSION2")
                logging.debug(c1)
                logging.debug(c2)
                logging.debug(c3)
                logging.debug("END OF TESTING THE SESSION2")"""

        print('user clicked button')  
        logging.debug("LOADING MODEL")
        #model=pickle.load(open('orientationSystem/model/finalized_model.sav','rb+'))
        temp={}
        temp['c1']=str(request.POST.get('choice1'))  
        logging.debug(temp['c1'])
        temp['c2']=str(request.POST.get('choice2')) 
        logging.debug(temp['c2'])
        temp['c3']=str(request.POST.get('choice3')) 
        temp['c4']=str(request.POST.get('choice4')) 
        temp['c5']=str(request.POST.get('choice5')) 
        temp['c6']=str(request.POST.get('choice6')) 
        temp['c7']=str(request.POST.get('choice7')) 
        temp['c8']=str(request.POST.get('choice8')) 
        temp['c9']=str(request.POST.get('choice9'))  
        temp['c10']=str(request.POST.get('choice10'))
        temp['moy'] = 10 
        logging.debug(temp)
        logging.debug("END...........")



        other = {'H14':'H00', 'H13':'H00', '711':'710', '712':'710', '713':'710','821':'820', '822':'820', '823':'820','121':'120', '122':'120', '123':'120', '841':'840', '842':'840' , '843':'840', '31':'300', '32':'300', '33':'300','21':'200', '22':'200', '23':'200', '41':'421', '42':'421', '43':'421', '44':'421', '611':'600', '612':'600', '613':'600', '614':'600', '101':'100', '102':'100', '11':'103', '12':'103', '13':'103', '14':'103','15':'103', '911':'910', '912':'910', '913':'910', '941':'940', '942':'940','721':'720', '722':'720', '723':'720','931':'930', '932':'930', '933':'930' }
        for key, val in temp.items():
            for key2, val2 in other.items():
                if  val == key2:
                    ## replace val in temp by key2
                    temp[key]= key2
                    break

        logging.debug("PRINTING THE CHOICES LIST AFTER GROUPING")
        logging.debug(temp)



        """
        ## dataframe row created 
        testdata=pd.DataFrame({'x':temp}).transpose()
        ## turn the 10 first six choices into binary data for first model 
        ## Normalisation moyenne bac

        ## encoding codes 
        encoder1 = pickle.load(open('orientationSystem/model/model1Encoder.sav','rb+'))
        testdatafinal = testdata[['c1','c2', 'c3', 'c4', 'c5', 'c6']].apply(encoder1.transform)
        testdatafinal['MOYENNE_BAC']= 10
        
        ## turning codes into binary vector 

        l = testdatafinal[['c1', 'c2', 'c3', 'c4', 'c5','c6']].astype(int).values.flatten().tolist()
        l = [x-1 for x in l]
        m = np.zeros(19)
        m[l] = 1
        m= np.insert(m, 0, 10) 
        logging.debug("prinitng m ")
        logging.debug(m)
        result=model.predict_proba(m)
        logging.debug("Printing result")
        logging.debug(result)"""

        ## get results from the 3 models 
        result1,row1 = prepModel1(temp)
        logging.debug("Printing result1")
        logging.debug(result1)

        result2,row2 = prepModel2(temp)
        logging.debug("Printing result2")
        logging.debug(result2)

        result3,row3 = prepModel3(temp)
        logging.debug("Printing result3")
        logging.debug(result3)

        result4,row4 = prepModel4(temp)
        logging.debug("Printing result4")
        logging.debug(result4)

        result5,row5 = prepModel5(temp)
        logging.debug("Printing result5")
        logging.debug(result5)
        logging.debug("Printing row1,2,3,4,5..........")


        #### 
        logging.debug("arrounding resultssssss ..................")
        result1 =np.around(result1, decimals=2)
        result2 =np.around(result2, decimals=2)
        result3 =np.around(result3, decimals=2)
        result4 =np.around(result4, decimals=2)
        result5 =np.around(result5, decimals=2)

        logging.debug(row1)
        logging.debug(row2)
        logging.debug(row3)
        logging.debug(row4)
        logging.debug(row5)


        
    ## verifier si l'utilisateur a rentrer un une ou plusieurs classes traitees par le modele 
        for classe in row1[:6]:
            logging.debug(classe)
            if classe in outputsModel1:
                ## not so sure about the index 
                outputDictionary['model1',classe]=result1[list(encoder3.classes_).index(classe)]

        for classe in row2[:6]:
            logging.debug(classe)
            if classe in outputsModel2:
                ## not so sure about the index 
                outputDictionary['model2',classe]=result2[0][list(encoder2.classes_).index(classe)]

        
        for classe in row3[:6]:
            logging.debug(classe)
            if classe in outputsModel3:
                ## not so sure about the index 
                outputDictionary['model3',classe]=result3[0][list(encoder3.classes_).index(classe)]

        
        for classe in row4[:6]:
            logging.debug(classe)
            if classe in outputsModel4:
                ## not so sure about the index 
                outputDictionary['model4',classe]=result4[list(encoder4.classes_).index(classe)]

        for classe in row5[:6]:
            logging.debug(classe)
            if classe in outputsModel5:
                ## not so sure about the index 
                outputDictionary['model5',classe]=result5[list(encoder5.classes_).index(classe)]

        logging.debug("VIEWS.PY PRINTING THE FINAL OUTPUT OOOF THE 3 MODELS")
        logging.debug(outputDictionary)


        import re
        ## filter the output and order for display 
        finalDisplay = {}
        logging.debug("This is a test of the dict keys")
        result = ([ a for a,b in outputDictionary.keys() ], [ b for a,b in outputDictionary.keys() ])
        
        #logging.debug(result[0][result[1].index('OTH')])
        #logging.debug(result[1])
        
        logging.debug("LOOOOOP")

        for classe in list(temp.values())[:10]:
            logging.debug(classe)
            if classe in result[1]:   
                ## check for which model 
                finalDisplay[classe, result[0][result[1].index(classe)]]= outputDictionary[result[0][result[1].index(classe)],classe]

            elif classe in other.keys(): ## cas groupement 
                finalDisplay[classe, result[0][result[1].index(classe)]] = outputDictionary[result[0][result[1].index(classe)],other[classe]]
            else: ## cas option other
                finalDisplay[classe, result[0][result[1].index('OTH')]] = outputDictionary['model5','OTH']

        logging.debug("ORDERED AND READY TO CONNECT TO UI")
        logging.debug(finalDisplay)


        resultModel1, resultModel2, resultModel3,resultModel4,resultModel5  = [],[],[],[],[]

        for key, val in finalDisplay.items():
            logging.debug("TEST")

            if key[1] ==  'model1':
                resultModel1.append(val)
                resultModel2.append('nan')
                resultModel3.append('nan')
                resultModel4.append('nan')
                resultModel5.append('nan')
            elif key[1] ==  'model2':
                resultModel2.append(val)
                resultModel1.append('nan')
                resultModel3.append('nan')
                resultModel4.append('nan')
                resultModel5.append('nan')
            elif key[1] ==  'model3':
                resultModel3.append(val)
                resultModel1.append('nan')
                resultModel2.append('nan')
                resultModel4.append('nan')
                resultModel5.append('nan')

            elif key[1] ==  'model4':
                resultModel4.append(val)
                resultModel3.append('nan')
                resultModel1.append('nan')
                resultModel2.append('nan')
                resultModel5.append('nan')

            elif key[1] ==  'model5':
                resultModel5.append(val)
                resultModel4.append('nan')
                resultModel3.append('nan')
                resultModel1.append('nan')
                resultModel2.append('nan')

        logging.debug("FINAL RESULTS")
        logging.debug(resultModel1)
        logging.debug(resultModel2)
        logging.debug(resultModel3)
        logging.debug(resultModel4)
        logging.debug(resultModel5)

        logging.debug("ML1"+"     |    "+"ML2"+"    |    "+"ML3"+"    |    "+"ML4"+"    |    "+"ML5")

        for j in range(len(resultModel5)):
            logging.debug(str(resultModel1[j])+"     |    "+str(resultModel2[j])+"    |    "+str(resultModel3[j])+"    |    "+str(resultModel4[j])+"    |    "+str(resultModel5[j]))

        ## connecter les resultat a l'interface 


        context={'result1':resultModel1, 
                'result2':resultModel2, 
                'result3':resultModel3,  
                'result4':resultModel4,  
                'result5':resultModel5,  
                'form' : form # pass the form in the context
                }
        
        ## orginal: result.html
        return render(request,'evaluation_model1.html', context)


            

    return render(request, 'evaluation_model1.html', {'form': form})




def predict(request):
    
    if request.method =='POST':   
        ## save form using a session 
        request.session.save()
        request.session["c1"] = temp['c1']=str(request.POST.get('choice1'))  
        request.session["c2"] = temp['c2']=str(request.POST.get('choice2')) 
        request.session["c3"] = temp['c3']=str(request.POST.get('choice3')) 
        request.session["c4"] = temp['c4']=str(request.POST.get('choice4')) 
        request.session["c5"] = temp['c5']=str(request.POST.get('choice5')) 
        request.session["c6"] = temp['c6']=str(request.POST.get('choice6')) 
        request.session["c7"] = temp['c7']=str(request.POST.get('choice7'))  
        request.session["c8"] = temp['c8']=str(request.POST.get('choice8')) 
        request.session["c9"] = temp['c9']=str(request.POST.get('choice9')) 
        request.session["c10"] = temp['c10']=str(request.POST.get('choice10')) 
        request.session.modified = True


        c1 = request.session.get("c1")
        c2 = request.session.get("c2")
        c3 = request.session.get("c3")
        c4 = request.session.get("c4")
        c5 = request.session.get("c5")
        c6 = request.session.get("c6")
        c7 = request.session.get("c7")
        c8 = request.session.get("c8")
        c9 = request.session.get("c9")
        c10 = request.session.get("c10")

        ## test session
        logging.debug("TESTING THE SESSION2")
        logging.debug(c1)
        logging.debug(c2)
        logging.debug(c3)
        logging.debug("END OF TESTING THE SESSION2")



        logging.debug("LOADING MODEL")
        #model=pickle.load(open('orientationSystem/model/finalized_model.sav','rb+'))
        temp={}
        temp['c1']=str(request.POST.get('choice1'))  
        logging.debug(temp['c1'])
        temp['c2']=str(request.POST.get('choice2')) 
        logging.debug(temp['c2'])
        temp['c3']=str(request.POST.get('choice3')) 
        temp['c4']=str(request.POST.get('choice4')) 
        temp['c5']=str(request.POST.get('choice5')) 
        temp['c6']=str(request.POST.get('choice6')) 
        temp['c7']=str(request.POST.get('choice7')) 
        temp['c8']=str(request.POST.get('choice8')) 
        temp['c9']=str(request.POST.get('choice9'))  
        temp['c10']=str(request.POST.get('choice10'))
        temp['moy'] = 10 


        other = {'H14':'H00', 'H13':'H00', '711':'710', '712':'710', '713':'710','821':'820', '822':'820', '823':'820','121':'120', '122':'120', '123':'120', '841':'840', '842':'840' , '843':'840', '31':'300', '32':'300', '33':'300','21':'200', '22':'200', '23':'200', '41':'421', '42':'421', '43':'421', '44':'421', '611':'600', '612':'600', '613':'600', '614':'600', '101':'100', '102':'100', '11':'103', '12':'103', '13':'103', '14':'103','15':'103', '911':'910', '912':'910', '913':'910', '941':'940', '942':'940','721':'720', '722':'720', '723':'720','931':'930', '932':'930', '933':'930' }
        for key, val in temp.items():
            for key2, val2 in other.items():
                if  val == key2:
                    ## replace val in temp by key2
                    temp[key]= key2
                    break

        logging.debug("PRINTING THE CHOICES LIST AFTER GROUPING")
        logging.debug(temp)



        """
        ## dataframe row created 
        testdata=pd.DataFrame({'x':temp}).transpose()
        ## turn the 10 first six choices into binary data for first model 
        ## Normalisation moyenne bac

        ## encoding codes 
        encoder1 = pickle.load(open('orientationSystem/model/model1Encoder.sav','rb+'))
        testdatafinal = testdata[['c1','c2', 'c3', 'c4', 'c5', 'c6']].apply(encoder1.transform)
        testdatafinal['MOYENNE_BAC']= 10
        
        ## turning codes into binary vector 

        l = testdatafinal[['c1', 'c2', 'c3', 'c4', 'c5','c6']].astype(int).values.flatten().tolist()
        l = [x-1 for x in l]
        m = np.zeros(19)
        m[l] = 1
        m= np.insert(m, 0, 10) 
        logging.debug("prinitng m ")
        logging.debug(m)
        result=model.predict_proba(m)
        logging.debug("Printing result")
        logging.debug(result)"""

        ## get results from the 3 models 
        result1,row1 = prepModel1(temp)
        logging.debug("Printing result1")
        logging.debug(result1)
        result2,row2 = prepModel2(temp)
        logging.debug("Printing result2")
        logging.debug(result2)
        result3,row3 = prepModel3(temp)
        logging.debug("Printing result3")
        logging.debug(result3)
        logging.debug("Printing row1,2,3..........")

        logging.debug(row1)
        logging.debug(row2)
        logging.debug(row3)


        
    ## verifier si l'utilisateur a rentrer un une ou plusieurs classes traitees par le modele 
        for classe in row1[:6]:
            logging.debug(classe)
            if classe in outputsModel1:
                ## not so sure about the index 
                outputDictionary['model1',classe]=result1[list(encoder3.classes_).index(classe)]

        for classe in row2[:6]:
            logging.debug(classe)
            if classe in outputsModel2:
                ## not so sure about the index 
                outputDictionary['model2',classe]=result2[list(encoder2.classes_).index(classe)]

        
        for classe in row3[:6]:
            logging.debug(classe)
            if classe in outputsModel3:
                ## not so sure about the index 
                outputDictionary['model3',classe]=result3[list(encoder3.classes_).index(classe)]

        logging.debug("VIEWS.PY PRINTING THE FINAL OUTPUT OOOF THE 3 MODELS")
        logging.debug(outputDictionary)


        import re
        ## filter the output and order for display 
        finalDisplay = {}
        logging.debug("This is a test of the dict keys")
        result = ([ a for a,b in outputDictionary.keys() ], [ b for a,b in outputDictionary.keys() ])
        logging.debug(result[0][result[1].index('OTH')])
        logging.debug(result[1])
        

        for classe in list(temp.values())[:10]:
            if classe in result[1]:   
                ## check for which model 
                
                finalDisplay[classe, result[0][result[1].index(classe)]]= outputDictionary[result[0][result[1].index(classe)],classe]

            elif classe in other.keys(): ## cas groupement 
                finalDisplay[classe, result[0][result[1].index(classe)]] = outputDictionary[result[0][result[1].index(classe)],other[classe]]
            else: ## cas option other
                finalDisplay[classe, result[0][result[1].index('OTH')]] = outputDictionary['model3','OTH']

        logging.debug("ORDERED AND READY TO CONNECT TO UI")
        logging.debug(finalDisplay)


        resultModel1, resultModel2, resultModel3  = [],[],[]

        for key, val in finalDisplay.items():

            if key[1] ==  'model1':
                resultModel1.append(val)
                resultModel2.append('')
                resultModel3.append('')
            elif key[1] ==  'model2':
                resultModel2.append(val)
                resultModel1.append('')
                resultModel3.append('')
            elif key[1] ==  'model3':
                resultModel3.append(val)
                resultModel1.append('')
                resultModel2.append('')
        logging.debug(resultModel1)
        logging.debug(resultModel2)
        logging.debug(resultModel3)

        ## connecter les resultat a l'interface 

   
        context={'result1':result1, 
                 'result2':result2, 
                 'result3':result3,  
                }
        
        ## orginal: result.html

        return render(request,'evaluation_model1.html', context)


def diplayVis(request):


    ## get dropdown list value 

    c1 = request.session.get("c1")
    c2 = request.session.get("c2")
    c3 = request.session.get("c3")
    c4 = request.session.get("c4")
    c5 = request.session.get("c5")
    c6 = request.session.get("c6")
    c7 = request.session.get("c7")
    c8 = request.session.get("c8")
    c9 = request.session.get("c9")
    c10 = request.session.get("c10")

    ## test session
    logging.debug("TESTING THE SESSION")
    logging.debug(c1)
    logging.debug(c2)
    logging.debug(c3)
    logging.debug(c5)
    logging.debug(c6)
    logging.debug(c7)
    logging.debug("END OF TESTING THE SESSION")


    ## check the value of drop list 
    pass
    pass
    pass


    temp={}
    temp['c1']=str(c1)
    logging.debug(temp['c1'])
    temp['c2']=str(c2)
    logging.debug(temp['c2'])
    temp['c3']=str(c3)
    temp['c4']=str(c4)
    temp['c5']=str(c5)
    temp['c6']=str(c6)
    temp['c7']=str(c7)
    temp['c8']=str(c8) 
    temp['c9']=str(c9)
    temp['c10']=str(c10)
    temp['moy'] = 10 
    ## call the models 

    logging.debug("////////////////////////////////////")
    logging.debug("Printing TEMP")
    logging.debug(temp)


    btn = request.POST.get('typeForm')
    logging.debug("*****************************************************")
    logging.debug(btn)
    logging.debug("*****************************************************")

    if btn == 'ens':
        logging.debug('ENS CLICKED')
        result,row, classes           =prepModel_ENS(temp)
        logging.debug("ccccccccccccccccccccccccccccc")
        logging.debug(classes)
        logging.debug("I CALLED MODEL ENS")


        ## load labels dictionnary 
        dict = pickle.load(open("orientationSystem\dictEns.pkl", 'rb+'))

        labels = []
        for c in classes:
            if c == 'OTH':
                labels.append('Autres types de formation')
            elif c == 'OthEns':
                labels.append('Autres ENS')
            else:
                labels.append(dict[int(c)])


        logging.debug(result)
        
    elif btn == 'med':
        logging.debug('MED CLICKED')
        
        result,row, classes           =prepModel_MED(temp)
        logging.debug("I CALLED MODEL MED")
        logging.debug("ccccccccccccccccccccccccccccc")

                ## load labels dictionnary 
        dict = pickle.load(open("orientationSystem\dictMed.pkl", 'rb+'))

        labels = []
        for c in classes:
            if c == 'OTH':
                labels.append('Autres types de formation')
            else:
                labels.append(dict[int(c)])

        logging.debug(result)
        
    elif btn == 'formSup':
        logging.debug('SUP CLICKED')
        result,row, classes   =prepModel_FormSup(temp)
        logging.debug("I CALLED MODEL FormSup")
        logging.debug("ccccccccccccccccccccccccccccc")

                ## load labels dictionnary 
        dict = pickle.load(open("orientationSystem\dictFormSup.pkl", 'rb+'))

        labels = []
        for c in classes:
            if c == 'OTH':
                labels.append('Autres types de formation')
            else:
                labels.append(dict[int(c)])

        logging.debug(result)
        
    elif btn == 'formUniv':
        logging.debug('UNIV CLICKED')
                
        result,row, classes =prepModel_FormUniv(temp)
        logging.debug("I CALLED MODEL FormUniv")
                ## load labels dictionnary 
        dict = pickle.load(open("orientationSystem\dictFormUniv.pkl", 'rb+'))

        labels = []
        for c in classes:
            if c == 'OTH':
                labels.append('Autres types de formation')
            elif c == 'OthUniv':
                labels.append('Autres formations universitaires')
            else:
                labels.append(dict[int(c)])

        logging.debug("ccccccccccccccccccccccccccccc")
        logging.debug(result)
    

    else :
        logging.debug('PREPA CLICKED')
        result,row, classes       =prepModel_Prepa(temp)
        logging.debug("I CALLED MODEL prep")
        logging.debug("ccccccccccccccccccccccccccccc")

                        ## load labels dictionnary 
        dict = pickle.load(open("orientationSystem\dictPrepa.pkl", 'rb+'))

        labels = []
        for c in classes:
            if c == 'OTH':
                labels.append('Autres types de formation')
            else:
                labels.append(dict[int(c)])

        
        logging.debug(result)

    """
    ## WORKS ######################################







    """




    ## connecter les resultat a l'interface 

   
    context={'result':result, 
                 'row':row, 
                 'classes': labels
                }
        
        ## orginal: result.html

    return render(request,'evaluation_model2.html', context)