# Análise de Evasão de Clientes - TelecomX

Este projeto realiza uma análise exploratória dos dados de clientes da TelecomX, focando no comportamento de evasão (churn) e faturamento.

## Funcionalidades

- Carregamento dos dados de clientes via API (JSON)
- Normalização dos dados para facilitar a análise
- Conversão de colunas para tipos numéricos
- Remoção de valores nulos
- Cálculo do faturamento diário dos clientes
- Análise estatística e percentual de churn
- Geração de gráficos interativos (Plotly) e gráficos estáticos (Seaborn/Matplotlib)
- Exportação dos gráficos para arquivos HTML e JPG

## Como usar

1. Instale as dependências:
    ```bash
    pip install pandas plotly seaborn matplotlib
    ```

2. Execute o script `evasao_clientes.py`:
    ```bash
    python evasao_clientes.py
    ```

3. Os gráficos serão salvos na pasta do projeto.

## Principais comandos do código

- **Carregamento e normalização dos dados:**
    ```python
    df = pd.read_json(url)
    df_normalized = pd.json_normalize(df.to_dict(orient='records'))
    ```

- **Conversão de colunas e tratamento de nulos:**
    ```python
    df_normalized['account.Charges.Total'] = pd.to_numeric(df_normalized['account.Charges.Total'], errors="coerce")
    df_normalized = df_normalized.dropna(how="any", axis=0)
    ```

- **Cálculo do faturamento diário:**
    ```python
    df_normalized['contas_diarias'] = df_normalized['monthlycharges'] / 30
    ```

- **Geração de gráficos:**
    - Gráficos interativos: Plotly
    - Gráficos estáticos: Seaborn/Matplotlib

## Observações

- O script utiliza dados públicos hospedados no GitHub.
- Os gráficos são salvos automaticamente como arquivos HTML e JPG.
- O código pode ser adaptado para outras análises conforme necessário.

## Licença

Este projeto é apenas
