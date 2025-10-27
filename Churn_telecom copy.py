#%%
import pandas as pd
from sklearn import model_selection

# Carregamento e normalização da base
url = "https://raw.githubusercontent.com/alura-cursos/challenge2-data-science/refs/heads/main/TelecomX_Data.json"
df = pd.read_json(url)
df = pd.json_normalize(df.to_dict(orient='records'))
#%%
# Tratamento inicial

df.isnull().sum()
df.duplicated().sum()
print((df == '').any())
print((df == ' ').any())

#Tratando coluna de account.Charges.Total 

df["account.Charges.Total"] = pd.to_numeric(df["account.Charges.Total"], errors= "coerce")
df["account.Charges.Total"] = df["account.Charges.Total"].fillna(df["account.Charges.Total"].median())
df["account.Charges.Total"] = df["account.Charges.Total"].astype(float)

df["Churn"].unique()
df["Churn"] = df["Churn"].replace({"Yes": 1, "No": 0})
df["Churn"] = pd.to_numeric(df["Churn"], errors="coerce")
df = df.dropna(subset=['Churn'])
df["Churn"] = df["Churn"].astype(int)

#Separação de variaveis e target

features = df.columns[2::] 
target = "Churn"

X,y = df[features], df[target]

X_train, X_test, y_train, y_test = model_selection.train_test_split(X,y, random_state=42, test_size=0.2, stratify=y)


X_int = X.select_dtypes(include=["int64", "float64"]).columns
X_cat = X.select_dtypes(include="object").columns

#%% PRÉ PROCESSAMENTO
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer


X_int = X.select_dtypes(include=["int64", "float64"]).columns
X_cat = X.select_dtypes(include="object").columns

X_tranformacao = ColumnTransformer(
    transformers=[
        ("int", StandardScaler(), X_int),
        ("cat", OneHotEncoder(drop="first", handle_unknown='ignore', sparse_output=False), X_cat)
    ]
)



#"Taxa da variável resposta treino e teste
print(y_train.mean())
print(y_test.mean())
#%% Modelo para avaliar a importancia das variaveis do modelo
from sklearn.pipeline import Pipeline
from sklearn import tree
from sklearn.feature_selection import SelectFromModel
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV
from sklearn.linear_model import LogisticRegression

#model = RandomForestClassifier(random_state=42, n_jobs=-1)
model = LogisticRegression(random_state=42, class_weight= 'balanced')


#PARAMETROS RANDOM FOREST
#params = {
#    "model__min_samples_leaf": [10, 20, 35, 50],
#    "model__n_estimators": [100, 300, 600, 1000],
#    "model__criterion": ["gini", "entropy", "log_loss"]
#    "model__class_weight": [None, 'balanced']
#    }


#PARAMETROS REGRESSOA LOGISTICA
params = {
    "model__penalty": ['l1', 'l2', 'elasticnet'],
    "model__C": [0.001, 0.01, 0.1, 1.0, 10.0],
    "model__max_iter": [100, 200, 300],
}    
    
    

#
pipe_model = Pipeline(steps=[
    ("preprocesso", X_tranformacao),
    ("feature_select", SelectFromModel(tree.DecisionTreeClassifier(random_state=42), threshold=0.01)),
    ("model", model)
])

pipe_model.fit(X_train, y_train)


grid = GridSearchCV(pipe_model, param_grid=params, cv=3, scoring="roc_auc", verbose=2)
grid.fit(X_train, y_train)

print("\nMelhores parâmetros encontrados:")
print(grid.best_params_)

#%%
from sklearn import metrics
# Avaliação do modelo final
#--------------------------------------------------
y_train_predict = grid.predict(X_train) #tESTANDO A ACURACIA
y_train_proba = grid.predict_proba(X_train)[:,1] #TESTANDO A CURVA ROC

acc_train = metrics.accuracy_score(y_train, y_train_predict)
auc_train = metrics.roc_auc_score(y_train, y_train_proba)
roc_auc = metrics.roc_curve(y_train, y_train_proba)
print("Acuracia Treino: ", acc_train)
print("AUC Treino: ", auc_train)


#TESTANDO A X_TEST PARA VER SE ESTA BOM O MODELO

y_test_predict = grid.predict(X_test) #tESTANDO A ACURACIA
y_test_proba = grid.predict_proba(X_test)[:,1] #TESTANDO A CURVA ROC

roc_test = metrics.roc_curve(y_test, y_test_proba)
acc_test = metrics.accuracy_score(y_test, y_test_predict)
auc_test = metrics.roc_auc_score(y_test, y_test_proba)

roc = metrics.roc_curve(y_test_predict, y_test_proba)
print("Acuracia Teste: ", acc_test)
print("AUC Teste: ", auc_test)

# Conversão da variável resposta
# Separação entre features e target
# Identificação de tipos de variáveis
# Pré-processamento (padronização + codificação)
# Divisão treino/teste
# Modelo base para avaliar importância das variáveis
#Importância das variáveis
# Pipeline com GridSearchCV (modelo final)
# Avaliação do modelo final
