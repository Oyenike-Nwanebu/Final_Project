import streamlit as st
import pandas as pd
import numpy as np
import datetime
import pickle
import xgboost as xgb 
from sklearn.preprocessing import StandardScaler


primaryColor="#6eb52f"
backgroundColor="#f0f0f5"
secondaryBackgroundColor="#e0e0ef"
textColor="#262730"
font="sans serif"

st.markdown("<h1 style = 'text-align:center; color:green;'>Kickstarter Project Success Predictor</h1>", unsafe_allow_html=True)
st.image('Kickstarter_image.jpeg', caption="Image Credit: www.business2community.com")
st.header('Because dreams do come true!')
with st.form(key='my_form'):
    goal_usd = st.number_input('Please enter your project goal in USD', step = 0.10)

    #add a selectbox for staff pick
    staff_pick = st.selectbox('Is this a Staff Pick?', ('Yes', 'No'))

    #add a selectbox for Country
    country = st.selectbox('Please select your country', 
    ('AU', 'CA', 'DE', 'ES', 'FR', 'GB', 'HK', 'IT', 'MX', 'NL', 'SE', 'US', 'Other')) 

    #add a selectbox for category
    category = st.selectbox('Please select the category of your project', 
    ('Art', 'Comics', 'Crafts', 'Dance', 'Design', 'Fashion', 'Film_Video', 'Food', 
    'Games','Journalism', 'Music', 'Photography', 'Publishing', 'Technology', 'Theater'))

    #add a text input for the project name
    name = st.text_input('Please input the name of your project')

    #add a text input for project description
    blurb = st.text_input('Please input the description for your project campaign')

    #project creation date
    created_at = st.date_input('Please select project created date', 
    min_value=datetime.date(2009, 4, 28))

    #project launch date
    launched_at = st.date_input('Please select project launch date', 
    min_value=datetime.date(2009, 4, 28))

    #project deadline
    deadline = st.date_input('Please select the project deadline date', 
    min_value=datetime.date(2009, 4, 28))

    submit_button = st.form_submit_button(label='Predict')

if submit_button:
    if goal_usd == 0.00:
        st.write('Please enter the project goal in USD')
    elif launched_at < created_at:
        st.write('Please select a valid project launch date. Launch date must be greater than or equal to the project creation date')
    elif deadline < launched_at:
        st.write('Please select a valid project deadline date. Project deadline cannot be before project launch date')
    elif deadline < created_at:
        st.write('Please select a valid project deadline date. Project deadline cannot be before project creation date')
    elif name == "":
        st.write('Please enter a valid project name')
    elif blurb == "":
        st.write('Please enter a valid project description')
    else: 
        prep_time = (launched_at-created_at).days
        cam_duration = (deadline - launched_at).days
        blurb_count = len(blurb.split())
        name_count = len(name.split())

        if staff_pick == 'Yes':
            staff_pick = 1
        else:
            staff_pick = 0


        #category
        category_list = ['Art', 'Comics', 'Crafts', 'Dance', 'Design', 'Fashion', 'Film_Video', 'Food',
            'Games', 'Journalism', 'Music', 'Photography', 'Publishing', 'Technology', 'Theater']
        category_onehot = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]


        if category in category_list:
            category_onehot[category_list.index(category)] = 1

        Art, Comics, Crafts, Dance, Design, Fashion, Film_Video, Food, Games, Journalism, Music, Photography, Publishing, Technology, Theater = category_onehot


        country_onehot = [0,0,0,0,0,0,0,0,0,0,0,0,0]

        country_list = ['AU', 'CA', 'DE', 'ES', 'FR', 'GB', 'HK', 'IT', 'MX', 'NL', 'SE', 'US', 'Other']

        if country in country_list:
            country_onehot[country_list.index(country)] = 1

        AU, CA, DE, ES, FR, GB, HK, IT, MX, NL, SE, US, Other = country_onehot

        #convert user input to dataframe

        input_variables = pd.DataFrame([[staff_pick, goal_usd, name_count, blurb_count,  
            prep_time, cam_duration, AU, CA, DE, ES, FR, GB, HK, IT, MX, NL, Other, SE, US, Art, 
            Comics, Crafts, Dance, Design, Fashion, Film_Video, Food, Games, Journalism, Music, 
            Photography, Publishing, Technology, Theater]], columns=['staff_pick', 'goal_usd', 'name_count', 'blurb_count',
            'prep_time', 'cam_duration', 'country_AU', 'country_CA', 'country_DE',
            'country_ES', 'country_FR', 'country_GB', 'country_HK', 'country_IT',
            'country_MX', 'country_NL', 'country_Other', 'country_SE', 'country_US',
            'Art', 'Comics', 'Crafts', 'Dance', 'Design', 'Fashion', 'Film_Video',
            'Food', 'Games', 'Journalism', 'Music', 'Photography', 'Publishing',
            'Technology', 'Theater'],
            )

        #load the model
    
        pipeline = pickle.load(open('pipeline_model.sav', 'rb'))

        #make prediction
       
        result = pipeline.predict(input_variables)
        probas = pipeline.predict_proba(input_variables)
        probability = "{:.3f}".format(float(probas[:, 1]))
        

        #Display results of the prediction
        st.header("Result:")

        if result==1:
            st.write('Congratulations!! This campaign will likely be successful!')
            st.write ('The probability that your project will succeed is', probability)
            
        else:
            st.write('This campaign will likely fail :disappointed:')
            st.write ('The probability that your project will succeed is', probability)
            st.write('Please contact us to see how you can boost your chances!')