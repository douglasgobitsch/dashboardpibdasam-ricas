import pandas as pd
import re

#lê o arquivo CSV
input_file = "Data_America.csv"
output_file = "treatedarchive.csv"

df = pd.read_csv(input_file)

#atribui todos os objetos nulos ao valor 0
df.fillna(0, inplace=True)

#função para tratar valores não numéricos
def process_value(value):
    if isinstance(value, str):
        #remove caracteres não numéricos (exceto ponto decimal)
        value = re.sub(r'[^\d.]', '', value)
    
    return float(value)  #converte para float

#iterar pelas colunas e aplicar o tratamento
columns_to_process = ["Área do País", "População", "PIB (Dólares)"]
for col in columns_to_process:
    df[col] = df[col].apply(process_value)

#escreve os dados tratados em um novo arquivo CSV
df.to_csv(output_file, index=False)
