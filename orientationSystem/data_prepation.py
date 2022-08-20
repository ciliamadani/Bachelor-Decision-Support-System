from pickle import load, dump
import tensorflow as tf
def prep_entity_embedding_model(student_information):
        
    """
        input : ditionnary of student info 
        output: model predctions  
    """
    #load choice encoder
    encoder = load(open('orientationSystem\data_preparatio_object\categorical_encoder_entity_embedding.pkl', 'rb'))
    # load scaler
    scaler = load(open('orientationSystem\data_preparatio_object\scaler_marks_entity_embedding.pkl', 'rb'))
    sample= {
            'input_c1':encoder.transform(student_information['c1']),
            "input_c2":encoder.transform(student_information['c2']),
            "input_c3":encoder.transform(student_information['c3']),
            "input_c4":encoder.transform(student_information['c4']),
            "input_c5":encoder.transform(student_information['c5']),
            "input_c6":encoder.transform(student_information['c6']),
            "input_WILAYA_BAC":encoder.transform(student_information['annee_bac']),
            "input_SEXE":encoder.transform(student_information['sexe']),
            "input_SERIE":encoder.transform(student_information['serie']),
            "input_number_features": scaler.transform([student_information['english'],
                                                       student_information['french'],
                                                       student_information['his_geo'],
                                                       student_information['arabic_literature'],
                                                       student_information['maths'],
                                                       student_information['philosophy'],
                                                       student_information['physics'],
                                                       student_information['primary_module'],
                                                       student_information['islamic_science']
                                                       ])
            }
    input_dict = {name: tf.convert_to_tensor([value]) for name, value in sample.items()}
    return sample
def create_student_dictionary(list_choice, etudiant):
    student_information = {
                'matricule':etudiant['matricule'],
                'moyenne_bac':etudiant['moyenne_bac'],
                'serie_bac':etudiant['serie_bac'],
                'annee_bac':etudiant['annee_bac'],
                'sexe':etudiant['sexe'],
                'english':etudiant['english'],
                'french':etudiant['french'],
                'his_geo':etudiant['his_geo'],
                'arabic_literature':etudiant['arabic_literature'],
                'maths':etudiant['maths'],
                'philosophy':etudiant['philosophy'],
                'physics':etudiant['physics'],
                'primary_module':etudiant['primary_module'],
                'islamic_science':etudiant['islamic_science'],
                'c1':list_choice[0],
                'c2':list_choice[1],
                'c3':list_choice[2],
                'c4':list_choice[3],
                'c5':list_choice[4],
                'c6':list_choice[5]
                    }
    return student_information