import tensorflow_addons as tfa
import tensorflow as tf
import pandas as pd
from tensorflow.keras.callbacks import ModelCheckpoint, EarlyStopping,ReduceLROnPlateau
from tensorflow.keras import layers
def entity_embedding():

    num_features = ['english','french','his_geo','arabic_literature','maths','philosophy','physics',
                    'primary_module','islamic_science','MOYENNE_BAC']
    cat_features = ['c1','c2','c3','c4','c5','c6','WILAYA_BAC','SEXE','SERIE']
    inputs = []
    models =[]
    data = pd.read_csv('orientationSystem\data\data.csv')
    CLASSES = data['target'].nunique()

    for c in cat_features:
            
        num_unique_values = data[c].nunique()
        embed_dim = 50
        inp = layers.Input(shape=(1,),name='input_'+'_'.join(c.split(' ')))
        inputs.append(inp)
        embed = layers.Embedding(num_unique_values , embed_dim, name=c,
                                trainable=True,embeddings_initializer=tf.initializers.random_normal)(inp)
        embed= layers.SpatialDropout1D(0.2)(embed)
        embed_reshaped = layers.Reshape(target_shape=(50,))(embed)
        models.append(embed_reshaped)
    num_input = tf.keras.layers.Input(shape=(len(num_features)),name='input_number_features')
    inputs.append(num_input)
    models.append(num_input)
        
    merge_models= tf.keras.layers.concatenate(models)
    pre_preds = layers.BatchNormalization()(merge_models)
    pre_preds =  layers.Dense(500,activation="relu")(pre_preds)
    pre_preds = layers.Dropout(0.3)(pre_preds)
    pre_preds = tf.keras.layers.BatchNormalization()(pre_preds)
        
    pre_preds =  layers.Dense(300, activation="relu")(pre_preds)
    pre_preds = layers.Dropout(0.3)(pre_preds)
    pre_preds = tf.keras.layers.BatchNormalization()(pre_preds)    
        
    pre_preds =  layers.Dense(300, activation="relu")(pre_preds)
    pre_preds = layers.Dropout(0.3)(pre_preds)
    pre_preds = tf.keras.layers.BatchNormalization()(pre_preds)


    pred=tf.keras.layers.Dense(CLASSES,activation=tf.keras.activations.softmax)(pre_preds)
    reduce_lr = ReduceLROnPlateau(monitor='val_loss', factor=0.1,patience=5,min_lr=1e-08,verbose=1)
    
    model_full = tf.keras.models.Model(inputs= inputs,\
                                        outputs =pred)
    model_full.compile(loss='categorical_crossentropy',metrics=["accuracy"
                                                            ,tfa.metrics.F1Score(
                                                            num_classes=CLASSES,
                                                            average='macro',
                                                            name='f1_score_macro'),
                                                            tfa.metrics.F1Score(
                                                            num_classes=CLASSES,
                                                            average='weighted',
                                                            name='f1_score_weighted')], optimizer='Adam')
    model_full.load_weights("orientationSystem\models_weights\model_weights_entity_embedding.h5")
    return model_full
    