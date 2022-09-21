# -*- coding: utf-8 -*-
"""
Created on Thu Aug 11 17:18:29 2022

@author: est.gustavopietruza

Script para filtro da base de dados das tarifas de distribuição de gás natural, para comparação por meio de gráficos

Legenda das colunas:
AGENCIA: Agência Reguladora do Estado de interesse
CONCESSIONARIA: Concessionária provedora dos serviços de distribuição de gás no Estado de interesse
SEGMENTO: Segmento econômico utilizador do gás natural
FAIXA: Faixa de consumo referente à tarifa cobrida
P: Preço do gás cobrado
UM_P: Unidade de Mensuração do preço do gás
TF: Tarifa Fixa cobrada pelo consumo de gás (Sem Impostos)
TF_I: Tarifa Fixa cobrada pelo consumo de gás (Com Impostos)
UM_TF: Unidade de Mensuração da Tarifa Fixa
TV: Tarifa Variável cobrada pelo consumo de gás (Sem Impostos)
TV_I: Tarifa Variável cobrada pelo consumo de gás (Com Impostos)
UM_TV: Unidade de Mensuração da Tarifa Variável
MMBTU: Preço de um Milhão de BTU (Sem Impostos)
MMBTU_I: Preço de um Milhão de BTU (Com Impostos)
UM_MMBTU: Unidade de Mensuração do preço do MMBTU
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import re

np.set_printoptions(linewidth=np.inf)
pd.set_option('display.max_columns', 25)
pd.set_option('display.max_rows', 450)
pd.set_option('display.width', 1000)
pd.set_option('display.max_colwidth', 100)
pd.set_option("display.precision", 3)
# Don't wrap repr(DataFrame) across additional lines
pd.set_option("display.expand_frame_repr", False)

def input_dados(col):
    #Apresenta uma lista de opções da coluna de interesse, e retorna uma lista de dados selecionados pelo usuário
    print('')
    #Apresenta uma lista de opções disponíveis
    print(list(col.unique()))
    print('')
    print('Selecione os dados de interesse:')
    print('Digite ALL para selecionar todos os dados')
    print('Pressione ENTER para encerrar a escolha')
    #Lista vazia
    lista = []
    #Referencial inicial nulo (para prevenir um STOP de imediato)
    var = 0
    while True:
        #Input dos dados
        var = str(input()).upper().strip()
        if var == 'ALL':
            #Seleciona todos os dados
            lista = list(col.unique())
            break
        elif var == '':
            #Para o loop
            break
        #Confere se o estado existe na lista    
        elif var in list(col.unique()):
            lista.append(var)
        else:
            print('Estado não existe, digite novamente')
    return lista

def filtro(df_ref, lista, nome_col):
    #Cria uma lista de inputs, seleciona os DataFrames de interesse e junta-os em um único
    lista_df = []
    for i in lista:
        #Filtra o DataFrame de acordo com a informação fornecida
        df_var = df_ref[df_ref.loc[:, nome_col] == i]
        #Coloca o DataFrame filtrado em uma lista
        lista_df.append(df_var)
    #Junta todos os DataFrames em um único
    df_ref = pd.concat(lista_df)
    return df_ref

def filtra_dados(df_ref):
    #Cria uma cópia do DataFrame
    df_aux = df_ref.copy()
    
    #Input dos Estados de interesse
    lista_estados = input_dados(df_aux.loc[:, 'ESTADO'])
    #Filtra a base de dados de acordo com a lista de estados selecionados
    df_aux = filtro(df_aux, lista_estados, 'ESTADO')
    
    #Verifica se há mais de uma opção de concessionária no Estado
    if len(df_aux.loc[:,'CONCESSIONARIA'].unique()) > 1:
        #Input das Concessionárias de interesse
        lista_concessao = input_dados(df_aux.loc[:,'CONCESSIONARIA'])
    else:
        #Se for único, retorna somente ele
        lista_concessao = list(df_aux.loc[:,'CONCESSIONARIA'].unique())
    #Filtra o DataFrame para incluir somente os dados das concessionárias de interesse
    df_aux = filtro(df_aux, lista_concessao, 'CONCESSIONARIA')  
    
    #Verifica a existência de dados sobre as tarifas de gás
    if len(df_aux.loc[:,'SEGMENTO'].unique()) > 1:
        #Há dados de gás
        #Input dos Segmentos de interesse
        lista_seg = input_dados(df_aux.loc[:, 'SEGMENTO'])
        #Filtra o DataFrame para incluir somente os dados dos segmentos de interesse
        df_aux = filtro(df_aux, lista_seg, 'SEGMENTO')
    else:
        #Não há dados de gás
        df_aux = df_aux.reset_index(drop = True)
        #Retorna o DataFrame com as informações disponíveis
        if df_aux.loc[0,'SEGMENTO'] == df_aux.loc[0,'SEGMENTO']:        
            segmento = df_aux.loc[:,'SEGMENTO'].unique()[0]
            df_aux = df_aux[df_aux.loc[:,'SEGMENTO'] == segmento]  
            
    #Remove as colunas que não possuem dados e reinicia o índice
    df_aux = df_aux.dropna(how='all', axis=1).reset_index(drop = True)
    print(df_aux)
    return df_aux

#_____________________________________TRATAMENTO INICIAL DA BASE DE DADOS___________________________________

#Importa a base de dados do Excel
path = r'C:/Users/est.gustavopietruza/Desktop/Python Scripts/Formatação Tarifas/Tarifas/Tarifas Gás Natural Brasil - atualizado até agosto 2022.xlsx'
df_base = pd.read_excel(path, sheet_name = 'BASE DE DADOS', usecols = 'A:P').replace('-',np.nan)

#Renomeia as colunas para siglas
cols = ['ESTADO', 'AGENCIA', 'CONCESSIONARIA', 'SEGMENTO', 'FAIXA', 'P', 'UM_P', 'TF', 'TF_I', 'UM_TF', 'TV', 'TV_I', 'UM_TV', 'MMBTU', 'MMBTU_I', 'UM_MMBTU']
df_base.columns = cols

#__________________________________________________FILTRAGEM__________________________________________________

#DataFrame com os dados filtrados
#df_filtro = filtra_dados(df_base)

#___________________________________________________GRÁFICOS____________________________________________________
'''
for seg in df_filtro.SEGMENTO.unique():
    fig, ax1 = plt.subplots()
    df = df_filtro[df_filtro.SEGMENTO == seg]
    df = df.reset_index(drop=True)
    val_x = df.FAIXA
    val_y = df.TV
    plt.plot(val_x, val_y, color='darkgreen', marker='o', alpha=0.5)
    ax1.spines['top'].set_color('white')
    ax1.spines['right'].set_color('white')
    ax1.set_xticklabels(labels=val_x, size=7, rotation=-15)
    plt.xlabel('FAIXA DE CONSUMO')
    plt.ylabel('TARIFA DO GÁS')
    plt.title(seg, fontsize=7)
    plt.legend(loc='best')
'''

#cols_ref = ['ESTADO','AGENCIA','CONCESSIONARIA','SEGMENTO','FAIXA','TF','UM_TF','TV','UM_TV']
#df_ref = df_base.loc[:,cols_ref]

    


