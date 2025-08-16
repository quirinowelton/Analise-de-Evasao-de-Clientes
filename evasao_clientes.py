#%%
import pandas as pd
import plotly.express as px

url = 'https://raw.githubusercontent.com/alura-cursos/challenge2-data-science/refs/heads/main/TelecomX_Data.json'
df = pd.read_json(url)

df_normalized = pd.json_normalize(df.to_dict(orient='records'))
#%%
df_normalized.columns = df_normalized.columns.str.lower()
df_normalized.columns = df_normalized.columns.str.replace(r'\.', '_', regex=True)
df_normalized = df_normalized[df_normalized['churn'].notna() & (df_normalized['churn'] != '')]
df_normalized['contas_diarias'] = round(df_normalized['account_charges_monthly'] / 30,2)
#%%
'''
#substituindo Yes por 1 e No por 0, mas decidi não usar aqui
#df_normalized['churn'] = df_normalized['churn'].apply(lambda x: 1 if x == 'Yes' else 0) #todas as opções abaixo fazem essa mesma função
#df_normalized['churn'] = df_normalized['churn'].map({'Yes': 1, 'No': 0})
#df_normalized['churn'] = np.where(df_normalized['churn'] == 'Yes', 1, 0)
#df_normalized['churn'] = df_normalized['churn'].replace({'Yes': 1, 'No': 0})
distribuicao_genero = df_normalized.groupby('churn').agg({'customer_gender':'count'}).reset_index()
distribuicao_contrato = df_normalized.groupby('churn').agg({'account_contract':'count'}).reset_index()
distribuicao_pagamento = df_normalized.groupby('churn').agg({'account_paymentmethod':'count'}).reset_index()
distribuicao_contas_diarias = df_normalized.groupby('churn').agg({'contas_diarias':'count'}).reset_index()
distribuicao_customer_partner = df_normalized.groupby('churn').agg({'customer_partner':'count'}).reset_index()'''
distribuicao_churn = df_normalized.groupby('churn').agg({'customerid':'count'}).reset_index()
distribuicao_genero = df_normalized.groupby(['customer_gender', 'churn']).size().reset_index(name='count')
distribuicao_contrato = df_normalized.groupby(['account_contract', 'churn']).size().reset_index(name='count')
distribuicao_pagamento = df_normalized.groupby(['account_paymentmethod', 'churn']).size().reset_index(name='count')
distribuicao_customer_partner = df_normalized.groupby(['customer_partner', 'churn']).size().reset_index(name='count')

#%%

def gerando_grafico_barra(dados,x,y):
    fig = px.bar(
    dados,
    x=x,  # eixo X: male/female
    y=y,            # altura da barra
    color='churn',        # divide por 'sim' e 'não'
    barmode='group',      # 'group' para barras lado a lado, 'stack' para empilhadas
    text=y          # mostra o valor no topo da barra
)

    fig.update_traces(textposition='outside')
    fig.write_html(f"{x}_churn.html")

gerando_grafico_barra(distribuicao_genero, "customer_gender", "count")
gerando_grafico_barra(distribuicao_contrato, "account_contract", "count")
gerando_grafico_barra(distribuicao_pagamento, "account_paymentmethod", "count")
gerando_grafico_barra(distribuicao_customer_partner, "customer_partner", "count")