#%%
import pandas as pd
import plotly.express as px
import seaborn as sns
import seaborn as sns
import matplotlib.pyplot as plt

url = 'https://raw.githubusercontent.com/alura-cursos/challenge2-data-science/refs/heads/main/TelecomX_Data.json'
df = pd.read_json(url)

df_normalized = pd.json_normalize(df.to_dict(orient='records'))
df_normalized.head()

df_normalized['account.Charges.Total'] = pd.to_numeric(df_normalized['account.Charges.Total'], errors="coerce")
# "coerce" faz com que as células com letras ou caracteres especieais fiquem vazias.

df_normalized = df_normalized.drop("customerID", axis=1)
# Comando alternativo à esse ultimo:
# df_normalized = df_normalized.dropna(how="all", axis=1)
# "dropna" é usada para excluir células vazias.

# ordenar em ordem decrescente as variáveis por seus valores ausentes
percentual_nulos = (df_normalized.isnull().sum() / df_normalized.shape[0]).sort_values(ascending=False)
df_normalized = df_normalized.dropna(how="any", axis=0)#Excluindo valores nulos na base
#verificando se ainda existem valores nulos na base
print(percentual_nulos)
print(df_normalized.isna().any())

df_normalized.describe()

#porcentagens de sim e não
analise_churn_total = df_normalized["Churn"].value_counts()
analise_churn_percent =df_normalized["Churn"].value_counts(normalize=True).map("{:.2%}".format) # "map("{:.2%}".format" é usado para formatar o número.
print(f'Analise de churn total:\n{analise_churn_total}')
print(f'Analise de churn percentual:\n{analise_churn_percent}')

coluna_excluida = ['account.Charges.Total']

for coluna in df_normalized.columns:
    if coluna not in coluna_excluida:
        fig = px.histogram(
            df_normalized,
            x=coluna,
            color="Churn",
            text_auto=True,
            title=f"Distribuição de {coluna} por Churn"
        )
        # Salva cada gráfico em um HTML com o nome da coluna
        fig.write_html(f"{coluna}_churn.html")


# gerando um gráfico de distribuição para a coluna 'TotalCharges'
fig, ax = plt.subplots(figsize = (10, 4))
sns.set_style('dark')
sns.histplot(df_normalized['account.Charges.Total'], ax = ax, bins = 40, kde=True)
ax.set_xlabel('')
ax.set_title('Cobranças Totais')
plt.tight_layout()
plt.savefig('total-charge.jpg')
plt.show()