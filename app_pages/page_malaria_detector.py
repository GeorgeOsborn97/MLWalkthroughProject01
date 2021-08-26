import streamlit as st
from PIL import Image
import numpy as np


def page_page_malaria_detector_body():
    st.info(
        f"* The client is interested to tell whether or not a given cell is parasitized "
        f"with malaria or not."
        )


    img_file_buffer = st.file_uploader('Upload the blood smear sample', type='png')
    st.write("---")
    if img_file_buffer is not None:

        img = np.array((Image.open(img_file_buffer)))
        st.write("* Blood Smear Sample")
        st.image(img, caption=f"Image Size: Width {img.shape[1]}px x Height {img.shape[0]}px")

        my_image = resize_input_image(img)

        pred_proba, pred_class = load_model_and_predict(my_image)

        plot_predictions_probabilities(pred_proba, pred_class)



import pandas as pd
import plotly.express as px
def plot_predictions_probabilities(pred_proba, pred_class):


    prob_per_class= pd.DataFrame(data=[0,0],index={'Parasitized': 0, 'Uninfected': 1}.keys(), columns=['Probability'])

    prob_per_class.loc[pred_class] = pred_proba


    for x in prob_per_class.index.to_list():
        if x not in pred_class: prob_per_class.loc[x] = 1 - pred_proba

    prob_per_class = prob_per_class.round(3)
    prob_per_class['Diagnostic'] = prob_per_class.index
    import plotly.express as px
    fig = px.bar(
            prob_per_class,
            x = 'Diagnostic',
            y = prob_per_class['Probability'],
            range_y=[0,1],
            width=600, height=400,template='presentation')

    st.plotly_chart(fig)





import cv2      
def resize_input_image(img):        
    img_resized = cv2.resize(img,(132,133)) 
    my_image = np.expand_dims(img_resized, axis=0)
    return my_image


from tensorflow.keras.models import load_model
def load_model_and_predict(my_image):
    model = load_model('outputs/model/my_model.h5')
    pred_proba = model.predict(my_image)[0,0]

    target_map = {v: k for k, v in {'Parasitized': 0, 'Uninfected': 1}.items()}
    pred_class =  target_map[pred_proba > 0.5]  
    st.write(
        f"* The predictive analysis indicates the sample cell is "
        f"{pred_class.lower()} with malaria.")
    
    if pred_class == target_map[0]: pred_proba = 1 - pred_proba

    return pred_proba, pred_class