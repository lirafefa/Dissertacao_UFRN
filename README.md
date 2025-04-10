# Dissertação

## Sobre o Projeto

Este repositório foi desenvolvido no contexto da dissertação de mestrado em Direito da Universidade Federal do Rio Grande do Norte (UFRN), por **Fernanda Lira**.

O objetivo central é a **classificação automática de casos de cumprimento de sentença de ações coletivas no âmbito do TRF5 (Tribunal Regional Federal da 5ª Região)**. Para isso, utilizamos a técnica de **Positive-Unlabeled Learning (PU Learning)** com base no método proposto por **Elkan e Noto (2008)**.



## Etapas da Modelagem

A modelagem segue as etapas principais:

1. **Extração de Dados**
2. **Rotulação Manual de Casos**
3. **Processamento de Texto e Geração de Vetores**
4. **Treinamento do Modelo PU Learning**
5. **Validação e Avaliação dos Resultados**



## Execução do Projeto

###Extração de Dados

Para iniciar o processo de modelagem, é necessário executar o script `01-extracao.py`, responsável por extrair e preparar os dados brutos.

Antes de rodar o script, **crie um arquivo `.env`** na raiz do projeto com a seguinte variável de ambiente: PATH_DADOS=/caminho/para/salvar/os/dados



### Rotulação Manual

Após a extração, foi realizada uma amostragem de processos para rotulagem manual. Foram selecionados **3.000 processos**, dos quais os casos identificados como **cumprimento de sentença de ações coletivas** receberam o rótulo `1`, enquanto os demais foram rotulados como `0`.

Esses rótulos são fundamentais para treinar o classificador positivo-não rotulado.



### Processamento de Texto e Geração de Vetores

Os textos dos processos são transformados em vetores de características utilizando um modelo pré-treinado da Hugging Face (`ModernBERT-base`).

Esse processo é realizado nos scripts intermediários, que:

- Tokenizam os textos com `AutoTokenizer`
- Extraem embeddings com `AutoModel`
- Calculam a média dos estados ocultos como vetores representativos de cada processo

Os vetores são então salvos nos arquivos `caracteristicas_treino.parquet`, `caracteristicas_validacao.parquet` e `caracteristicas_teste.parquet`.


### Treinamento com PU Learning (Elkan & Noto)

O classificador utilizado é o `ElkanotoPuClassifier`, da biblioteca `pulearn`. Ele é treinado com:

- Amostras **positivas rotuladas** (`1`)
- Amostras **não rotuladas** (`-1`)

A estimativa da probabilidade de uma amostra ser positiva é ajustada com base na proporção de exemplos rotulados, conforme o método proposto por **Elkan e Noto**.

Foi utilizado tanto o `RandomForestClassifier` quanto o `MLPClassifier` como estimadores base.


### Avaliação

A performance do classificador é avaliada com base em:

- **Acurácia**
- **Relatório de Classificação (`classification_report`)**
- **Coeficiente de Correlação de Matthews (MCC)**

Essas métricas ajudam a entender o desempenho do modelo mesmo com a ausência de exemplos negativos rotulados.

###Bibliotecas Necessárias

As seguintes bibliotecas são requeridas para a execução completa do projeto:

- `pandas` – Manipulação de dados tabulares com DataFrames.
- `numpy` – Operações matemáticas com arrays e matrizes.
- `scikit-learn` – Algoritmos de machine learning, PCA e métricas.
- `transformers` – Tokenização e uso de modelos pré-treinados da Hugging Face.
- `torch` – Framework de deep learning (necessário para os modelos Hugging Face).
- `tqdm` – Barra de progresso para loops demorados.
- `matplotlib` – Visualização de gráficos, incluindo gráficos 3D.
- `seaborn` – Visualizações estatísticas com estilo aprimorado.
- `python-dotenv` – Carregamento de variáveis de ambiente a partir de arquivos `.env`.
- `pulearn` – Framework para Positive-Unlabeled Learning (PU Learning).





