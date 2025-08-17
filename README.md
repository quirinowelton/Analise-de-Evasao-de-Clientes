# Análise de Churn de Clientes em Telecomunicações

Este projeto tem como objetivo analisar o comportamento de **churn** (abandono) de clientes em uma empresa de telecomunicações e desenvolver modelos de **machine learning** para identificar clientes com maior risco de saída.

## Sobre o Dataset

O dataset utilizado contém informações de clientes de uma empresa de telecomunicações, incluindo:

- **Churn:** indica se o cliente saiu no último mês (variável alvo).  
- **Serviços:** tipo de serviço contratado (telefone, internet, streaming, etc.).  
- **Conta:** informações da conta do cliente (tempo de cliente, tipo de contrato, forma de pagamento, etc.).  
- **Demografia:** dados demográficos do cliente (sexo, idade, parceiros, dependentes).  

## Tarefas Realizadas

1. **Análise Exploratória dos Dados (EDA):**  
   - Análise das features para entender a distribuição dos dados e identificar padrões.

2. **Tratamento de Valores Faltantes:**  
   - Identificação e tratamento dos valores nulos na coluna `TotalCharges`.

3. **Balanceamento de Classes:**  
   - Aplicação de técnicas de **oversampling** e **undersampling** para lidar com o desbalanceamento da variável alvo (`Churn`).

4. **Pré-processamento:**  
   - Transformação da variável alvo para formato numérico.  
   - Divisão dos dados em conjuntos de treino e teste.  
   - Codificação de variáveis categóricas e escalonamento de variáveis numéricas utilizando um pipeline.

5. **Modelagem:**  
   - Treinamento e avaliação de diferentes modelos de classificação:  
     - Árvore de Decisão  
     - Floresta Aleatória  
     - XGBoost  
     - Regressão Logística  
     - SVC  

6. **Tunagem de Hiperparâmetros:**  
   - Utilização de `RandomizedSearchCV` para otimizar hiperparâmetros dos modelos de Floresta Aleatória e SVC, buscando melhorar a performance, especialmente o **recall**.

7. **Avaliação dos Modelos:**  
   - Comparação das métricas de performance (`accuracy`, `precision`, `recall`, `f1-score`).  
   - Análise da matriz de confusão e das curvas ROC e Precision-Recall.

## Resultados

Os resultados foram apresentados através de gráficos e tabelas, comparando a performance dos modelos antes e depois da tunagem e do balanceamento de classes. O foco principal foi na métrica de **recall**, importante para identificar corretamente os clientes que irão sair (churn).

### Principais Insights

- A análise exploratória revelou desbalanceamento significativo da variável alvo.  
- Undersampling e oversampling foram aplicados para mitigar o impacto do desbalanceamento.  
- A tunagem de hiperparâmetros melhorou a performance, principalmente o **recall** no caso do SVC tunado.  
- A matriz de confusão e as curvas ROC/PR forneceram uma avaliação detalhada da performance de cada modelo.

Este projeto demonstra um fluxo completo para análise e modelagem de **churn** de clientes, desde a exploração dos dados até a avaliação e otimização dos modelos.
