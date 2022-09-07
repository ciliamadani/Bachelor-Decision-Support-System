from django.http import HttpResponse
from django.shortcuts import render, redirect
from .form import NameForm
import logging
import pickle
from .model_ml import entity_embedding
import tensorflow as tf
from pickle import load, dump
from .models import Bachelier
from django.contrib.auth.models import User, auth
from django.contrib import messages
from .data_prepation import prep_entity_embedding_model,create_student_dictionary

from .prepModels import prepModel_ENS, prepModel_MED, prepModel_FormUniv, prepModel_FormSup, prepModel_Prepa
from .choices import read_choices, read_label_choices




# Create your views here.
def index(request):
    etudiant_test = Bachelier.objects.create(matricule=171731088156,serie_bac="N03",wilaya_bac='15',
                                            moyenne_bac=15.03,sexe='FEMININ',english=14.5,
                                            french=12,his_geo=17.5,arabic_literature=16,maths=19,
                                            philosophy=17,primary_module=14,islamic_science=13
                                       )
    etudiant_test.save()
    if request.method=='POST':
        matricule = request.POST["matricule"]
        mdp = request.POST["mdp"]
        mdp_confirmer = request.POST["mdp_confirmer"]
        if mdp == mdp_confirmer:
            if User.objects.filter(username=matricule).exists():
                messages.info(request, 'Matricule déjà utilsé par un autre étudiant')
                return redirect('/')
            else :
                user = User.objects.create_user(matricule, password=mdp)
                user.save()
                return redirect('login')
        else :
            messages.info(request,'Password Not The same')
            return redirect('/')
    else :
        return render(request, 'index.html')

def login(request):
    if request.method=='POST':
        matricule= request.POST['matricule']
        password= request.POST['password']

        
        user = auth.authenticate(username=matricule,password=password)
        logging.debug("////////////////////////////////")
        logging.debug(user)
        logging.debug("////////////////////////////////")
        if user is not None :
            auth.login(request,user)
            if Bachelier.objects.filter(matricule=matricule).exists():
                etudiant = Bachelier.objects.filter(matricule=matricule).values()[0]
                context = {
                'matricule':etudiant['matricule'],
                'moyenne_bac':etudiant['moyenne_bac'],
                'serie_bac':etudiant['serie_bac'],
                'wilaya_bac':etudiant['wilaya_bac'],
                'sexe':etudiant['sexe'],
                'english':etudiant['english'],
                'french':etudiant['french'],
                'his_geo':etudiant['his_geo'],
                'arabic_literature':etudiant['arabic_literature'],
                'maths':etudiant['maths'],
                'philosophy':etudiant['philosophy'],
                'physics':etudiant['physics'],
                'primary_module':etudiant['primary_module'],
                'islamic_science':etudiant['islamic_science']
                    }

                logging.debug(context)
                request.session["moyenne_bac"] = str(etudiant['moyenne_bac'])
                request.session["wilaya_bac"] = str(etudiant['wilaya_bac'])
                request.session["sexe"] = str(etudiant['sexe'])
                request.session.modified = True



                

                return render(request,'profile.html',context)

        return render(request, 'profile.html')
    else:
        return render(request, 'login.html')

def get_name(request):
    form = NameForm()
    if request.method =='POST':

        ## save form using a session 
        #request.session.save()
        request.session["c1"] = str(request.POST.get('choice1'))  
        request.session["c2"] =str(request.POST.get('choice2')) 
        request.session["c3"] =str(request.POST.get('choice3')) 
        request.session["c4"] = str(request.POST.get('choice4')) 
        request.session["c5"] = str(request.POST.get('choice5')) 
        request.session["c6"] = str(request.POST.get('choice6')) 
        request.session.modified = True


        logging.debug("LOADING MODEL")
                #retrieve choices from FORM
        if request.user.is_authenticated:
            matricule=request.user.username
            logging.debug(matricule)
            if Bachelier.objects.filter(matricule=matricule).exists():
                etudiant = Bachelier.objects.filter(matricule=matricule).values()[0]
                list_choice=[
                    str(request.POST.get('choice1')),
                    str(request.POST.get('choice2')),
                    str(request.POST.get('choice3')), 
                    str(request.POST.get('choice4')),  
                    str(request.POST.get('choice5')),  
                    str(request.POST.get('choice6')),  
                ]
                student_information=create_student_dictionary(list_choice, etudiant)
                input_dict=prep_entity_embedding_model(student_information)
                model_full=entity_embedding()
                prediction_result=model_full.predict(input_dict)
                context={'probability_choice1':prediction_result[0,0],
                    'probability_choice2':prediction_result[0,1],
                    'probability_choice3':prediction_result[0,2],
                    'probability_choice4':prediction_result[0,3],
                    'probability_choice5':prediction_result[0,4],
                    'probability_choice6':prediction_result[0,5]
                    }
                logging.debug(context)
                return render(request, 'evaluation.html',context)
    return render(request, 'evaluation.html', {'form': form})
    
def predict(request):

    if request.method =='POST':
                #load choice encoder
        encoder = load(open('orientationSystem\data_preparatio_object\choices_encoder_label_encoder_entity_embedding.pkl', 'rb'))

        # load scaler
        scaler = load(open('orientationSystem\data_preparatio_object\scaler_marks_entity_embedding.pkl', 'rb'))

        if request.user.is_authenticated:
            matricule=request.user.username
            logging.debug(matricule)
            if Bachelier.objects.filter(matricule=matricule).exists():
                etudiant = Bachelier.objects.filter(matricule=matricule).values()[0]
                list_choice=[
                    str(request.POST.get('choice1')),
                    str(request.POST.get('choice2')),
                    str(request.POST.get('choice3')), 
                    str(request.POST.get('choice4')),  
                    str(request.POST.get('choice5')),  
                    str(request.POST.get('choice6')),  
                ]
                student_information=create_student_dictionary(list_choice, etudiant)
                input_dict=prep_entity_embedding_model(student_information)
                model_full=entity_embedding()
                prediction_result=model_full.predict(input_dict)
                context={'probability_choice1':prediction_result[0,0],
                    'probability_choice2':prediction_result[0,1],
                    'probability_choice3':prediction_result[0,2],
                    'probability_choice4':prediction_result[0,3],
                    'probability_choice5':prediction_result[0,4],
                    'probability_choice6':prediction_result[0,5]
                    }
            return render(request,'evaluation.html', context)



def profile(request):
    return render(request, 'profile.html')



def diplayVis(request):

    ## Get the form from session 
    temp={}
    temp['c1']=str(request.session.get("c1"))
    logging.debug(temp['c1'])
    temp['c2']=str(request.session.get("c2"))
    logging.debug(temp['c2'])
    temp['c3']=str(request.session.get("c3"))
    temp['c4']=str(request.session.get("c4"))
    temp['c5']=str(request.session.get("c5"))
    temp['c6']=str(request.session.get("c6"))
    temp['wilaya_bac'] = str(request.session.get("wilaya_bac"))
    temp['moyenne_bac'] = float(request.session.get("moyenne_bac"))
    temp['sexe'] = str(request.session.get("sexe"))

    logging.debug('????????????????????????????????')
    logging.debug(temp['wilaya_bac'])
    logging.debug(temp['moyenne_bac'])
    logging.debug(temp['sexe'])
    



 
    ## Get the dropdown list value
    btn = request.POST.get('typeForm')

    if btn == 'ens':
        result,row, classes           =prepModel_ENS(temp)
        ## load labels dictionnary 
        dict = pickle.load(open("orientationSystem\model\models\labels\dictEns.pkl", 'rb+'))

        labels = []
        for c in classes:
            if c == 'OTH':
                labels.append('Autres types de formation')
            elif c == 'OthEns':
                labels.append('Autres ENS')
            else:
                labels.append(dict[int(c)])

        
    elif btn == 'med':        
        result,row, classes           =prepModel_MED(temp)
        ## load labels dictionnary 
        dict = pickle.load(open("orientationSystem\model\models\labels\dictMed.pkl", 'rb+'))

        labels = []
        for c in classes:
            if c == 'OTH':
                labels.append('Autres types de formation')
            else:
                labels.append(dict[int(c)])
        logging.debug(labels)


        
    elif btn == 'formSup':
        result,row, classes   =prepModel_FormSup(temp)
        ## load labels dictionnary 
        dict = pickle.load(open("orientationSystem\model\models\labels\dictFormSup.pkl", 'rb+'))

        labels = []
        for c in classes:
            if c == 'OTH':
                labels.append('Autres types de formation')
            else:
                labels.append(dict[int(c)])
        
    elif btn == 'formUniv':
                
        result,row, classes =prepModel_FormUniv(temp)
        ## load labels dictionnary 
        dict = pickle.load(open("orientationSystem\model\models\labels\dictFormUniv.pkl", 'rb+'))

        labels = []
        for c in classes:
            if c == 'OTH':
                labels.append('Autres types de formation')
            elif c == 'OthUniv':
                labels.append('Autres formations universitaires')
            else:
                labels.append(dict[int(c)])

    else :
        result,row, classes       =prepModel_Prepa(temp)
        ## load labels dictionnary 
        dict = pickle.load(open("orientationSystem\model\models\labels\dictPrepa.pkl", 'rb+'))
        labels = []
        for c in classes:
            if c == 'OTH':
                labels.append('Autres types de formation')
            else:
                labels.append(dict[int(c)])
    


    ## connecter les resultat a l'interface 

   
    context={'result':result, 
                 'row':row, 
                 'classes': labels
                }

    return render(request,'evaluation_model2.html', context)

def logout(request):
    auth.logout(request)
    return render(request, 'login.html')