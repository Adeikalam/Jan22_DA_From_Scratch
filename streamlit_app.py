# -*- coding: utf-8 -*-
"""
Created on Fri Feb 11 09:48:43 2022

@author: Pierre
"""

import pandas as pd
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
from datetime import datetime
import numpy as np
from streamlit_utils import load_and_filter, weekly_countplot, moving_average_plot, hourly_plot

deps = pd.read_csv("departements-france.csv")

departement = st.sidebar.selectbox("Choisir un département à étudier", options = deps['nom_departement'].unique())

dates = st.sidebar.date_input(label = "Choisir une période à analyser",
              min_value = datetime(2016, 1, 1),
              max_value = datetime(2016, 12, 31),
              value = [datetime(2016, 1, 1), datetime(2016, 12, 31)])


if len(dates) >= 2:
    df = load_and_filter(dates, departement)
    
    fig_countplot = weekly_countplot(df)
    
    st.pyplot(fig_countplot)
    
    
    window = st.slider(label = "Choisir une taille de fenêtre pour le lissage de la série",
                       min_value = 1,
                       max_value = min((dates[1] - dates[0]).days, 30),
                       value = 1)
    
    
    fig2 = moving_average_plot(df, window)
    
    st.pyplot(fig2)
    
    
    fig3 = hourly_plot(df)

    st.pyplot(fig3)
    
    
    
    