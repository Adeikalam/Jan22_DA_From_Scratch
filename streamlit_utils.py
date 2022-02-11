# -*- coding: utf-8 -*-
"""
Created on Fri Feb 11 11:22:23 2022

@author: Pierre
"""


import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

def load_and_filter(dates, departement):
    
    df = pd.read_csv("caracteristiques.csv")
    
    df['date_full'] = pd.to_datetime('2016-' + df['month'].astype(str) + '-' + df['day'].astype(str))
    
    df = df[(df['date_full'].dt.date > dates[0]) & (df['date_full'].dt.date < dates[1])]
    
    deps = pd.read_csv("departements-france.csv")

    deps['code_departement'] = deps['code_departement'].replace(['2A', '2B'], ['20', '20']).astype(int)
    
    df = df.merge(deps[['code_departement', 'nom_departement', 'nom_region']],
             left_on = 'dep',
             right_on = 'code_departement',
             how = 'left')
    
    df = df[df['nom_departement'] == departement]
    
    return df


def weekly_countplot(df):
    
    fig, ax = plt.subplots()
    
    sns.countplot(df['weekday'], ax = ax)    
    
    return fig

def moving_average_plot(df, window):
    
    fig2, ax2 = plt.subplots()
    
    num_acc_per_day = df.groupby('monthday').count()['Num_Acc'].reset_index()

    num_acc_per_day = num_acc_per_day.merge(df[['monthday', 'weekday', 'month', 'day']],
                                            on = 'monthday', how = 'left' ).drop_duplicates()
    
    num_acc_per_day = num_acc_per_day.sort_values(by = ['month', 'day'])
    
    plt.plot(num_acc_per_day['monthday'], num_acc_per_day['Num_Acc'], alpha = 0.3)
    
    MA = num_acc_per_day['Num_Acc'].rolling(window, center = True).mean()
    
    plt.plot(num_acc_per_day['monthday'], MA, linewidth = 5)
    
    plt.xticks(num_acc_per_day['monthday'][::30], label = "Moyenne Mobile calculée sur une fenêtre centrée de 20 valeurs");
    
    plt.title("Nombre d'accidents quotidiens pendant l'année 2016")
    
    plt.xlabel("Date")
    plt.ylabel("Nombre d'accidents")
    
    fig2.set_size_inches(16, 9)
    
    return fig2


def hourly_plot(df):
    
    fig3, ax3 = plt.subplots()
    
    df['heure'] = df['hrmn'] // 100

    num_acc_heure = df.groupby(['month', 'day', 'heure']).count()['Num_Acc'].reset_index()
    
    num_acc_heure['monthday'] = num_acc_heure['month'].astype(str) + '-' + num_acc_heure['day'].astype(str)
    
    for day in num_acc_heure['monthday'].unique():
        data = num_acc_heure[num_acc_heure['monthday'] == day]
        
        for i in range(5):
            heure = data['heure']
            heure = heure + np.random.rand(len(heure))
    
            n_acc = data['Num_Acc']
            n_acc = n_acc + np.random.rand(len(n_acc))
        
            plt.plot(heure, n_acc, alpha = 0.015, color = 'black')
        
        
    plt.title("Nombres d'accidents quotidiens par heure")
        
    plt.xlabel("Heure de la journée")
    plt.ylabel("Nombre d'accidents")
    
    fig3.set_size_inches(16, 9)
    
    return fig3