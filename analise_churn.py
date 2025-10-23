#%%
import pandas as pd
#%%
url = "https://raw.githubusercontent.com/alura-cursos/challenge2-data-science/refs/heads/main/TelecomX_Data.json"

df = pd.read_json(url)

df = pd.json_normalize(df.to_dict(orient='records'))

#TRATAMENTO INICIAL DOS DADOS

#pd.to_numeric transforma a coluna em numeric e o que não for numeric transforma em NaN
df["account.Charges.Total"] = pd.to_numeric(df["account.Charges.Total"], errors= "coerce")

df["account.Charges.Total"] = df["account.Charges.Total"].fillna(df["account.Charges.Total"].median())
df["account.Charges.Total"] = df["account.Charges.Total"].astype(float)

#Checando valores nulos e linhas duplicadas
df.isnull().sum()
df.duplicated().sum()


#Verificando a variavel e sua distribuição 
df["Churn"] = df["Churn"].replace({
                                   "Yes": 1,
                                   "No": 0,
                                   })
df["Churn"] = pd.to_numeric(df["Churn"], errors="coerce")

df = df.dropna(subset=['Churn'])
df["Churn"] = df["Churn"].astype(int)
df["Churn"].value_counts()
#%%

features = df.columns[2::] 
target = "Churn"

X,y = df[features], df[target]

numeric_features = X.select_dtypes(include=['int64', 'float64']).columns
categorical_features = X.select_dtypes(include=['object']).columns

print(numeric_features)
print(categorical_features)

#%%
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler

onehot = OneHotEncoder(drop='first', handle_unknown='ignore', sparse_output=False)

# Criando um transformador para aplicar tanto o encoder quanto o scaler
preprocessor = ColumnTransformer(
    transformers=[
        ('num', StandardScaler(), numeric_features),
        ('cat', onehot, categorical_features)
    ]
)

# Aplicando o transformador
X_processed = preprocessor.fit_transform(X)

#%%
#SAMPLE
from sklearn import model_selection 

X_train, X_test, y_train, y_teste = model_selection.train_test_split(X_processed,y, random_state= 42, test_size= 0.2, stratify=y)

#Checando a taxa da variavel resposta
print(f"Taxa da variável resposta Treino {y_train.mean()}")
print(f"Taxa da variável resposta Teste {y_teste.mean()}")

#%%

from sklearn import tree

arvore = tree.DecisionTreeClassifier(random_state=42)
arvore.fit(X_train, y_train)


#%%
arvore.feature_importances_

feature_names = preprocessor.get_feature_names_out()
# Cria a série de importâncias com esses nomes
feature_importance = pd.Series(arvore.feature_importances_, index=feature_names)
feature_importance = feature_importance.sort_values(ascending=False).reset_index()

# Renomeia as colunas para deixar mais legível
feature_importance.columns = ['Feature', 'Importance']
#%%
# Mostra as 10 mais importantes
best_features = feature_importance[feature_importance['Importance'] > 0.01]
best_features