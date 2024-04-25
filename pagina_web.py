import streamlit as st
import os
import subprocess
import csv
import pandas as pd
from ctypes import *
import pydot
from PIL import Image
import plotly.graph_objects as go
import numpy as np

import networkx as nx
import matplotlib.pyplot as plt

def move_uploaded_file(uploaded_file):
    file_path = os.path.join("csv", uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return file_path

def clear_output_directory():
    output_dir = "output"
    if os.path.exists(output_dir):
        files = os.listdir(output_dir)
        for file in files:
            file_path = os.path.join(output_dir, file)
            os.remove(file_path)


def main():
    os.environ["PATH"] += os.pathsep + (os.path.dirname(os.path.abspath(__file__)) + '\\Graphviz-10.0.1-win64\\bin')
    st.set_page_config(page_title="Hiperstream", page_icon="web_custom/Logo_hi.png")
   
    st.title("Análise de Arquivos CSV")

    # Verifica se o arquivo CSV foi carregado
    uploaded_file = st.file_uploader("Faça o upload de um arquivo CSV")

    # Se um arquivo foi carregado, move-o para a pasta do código
    if uploaded_file is not None:
        #file_path = move_uploaded_file(uploaded_file)
        st.write(f"Arquivo '{uploaded_file.name}' foi carregado com sucesso.")

    # Lista os arquivos CSV na pasta do código
    
    files = [file for file in os.listdir("csv/") if file.endswith(".csv")]
    st.write("Ou use um dos arquivos CSV abaixo")
    if len(files) == 0:
        st.write("Nenhum arquivo CSV encontrado na pasta do código.")
    else:
        selected_file = st.selectbox("Selecione um arquivo CSV:", files)
        selected_file = os.path.join("csv/", selected_file)

        df = pd.read_csv(selected_file, sep=';')



        st.write("Preview da Tabela:")

        st.dataframe(df)

        if st.button("Analisar Dados"):
            clear_output_directory()
            
            data = []
            if 'erro' not in st.session_state:
                st.session_state["erro"] = 0
            else:
                st.session_state["erro"] = 0
            
            with open(selected_file, 'r') as file:
                reader = csv.reader(file)
                next(reader)  # Skip the header
                for row in reader:
                    try:
                        labels = [label.strip() for label in row[0].split(';')]  # Strip whitespace and newline characters
                        row_dict = {'ID': labels[0],
                                    'Nome': labels[1],
                                    'PastaOrigem': labels[2],
                                    'PastaDestino': labels[3],
                                    'PastaBackup': labels[4]}  # Create dictionary
                        data.append(row_dict)
                    except IndexError:
                       
                        st.session_state["erro"] = 1
                        if 'disponivel' not in st.session_state:
                            st.session_state["disponivel"] = 0
                        else:
                            st.session_state["disponivel"] = 0
                        break
            if(st.session_state["erro"] == 0):
                if 'disponivel' not in st.session_state:
                    st.session_state["disponivel"] = 1
                else:
                    st.session_state["disponivel"] = 1
                output_file = 'output/func_data.csv'
                with open(output_file, 'w', newline='') as file:
                    writer = csv.DictWriter(file, fieldnames=['ID', 'Nome', 'PastaOrigem', 'PastaDestino', 'PastaBackup'], delimiter=';')
                    writer.writeheader()  # Write the header
                    writer.writerows(data)  # Write the data rows
                # Chama o código em C para analisar os dados
                subprocess.run(["gcc", "-o", "./source/main", "./source/main.c"])

                # Execute o programa compilado
                subprocess.run(["./source/main"])
            else:
                 st.write("Arquivo Invalido")   
            if(st.session_state["disponivel"] == 1):
              

                        
                        if os.path.exists("output/grafo.dot") and os.path.exists("output/dados.txt"):


                            command = f"dot -Tpng output/grafo.dot -o output/grafo.png"
                            subprocess.run(command, shell=True)
                            teste = ""
                            with open("output/dados.txt", "r", encoding="utf-8") as file:
                                teste = teste + file.read()
                            teste = teste.split("Alturas:\n")

                         
                            alturas = teste[1].split('\n')
                            alturas.pop()
                            print(alturas)
                            alturas = [(int(pair.split(',')[0]), int(pair.split(',')[1])) for pair in alturas]
                            G = nx.drawing.nx_pydot.read_dot('output/grafo.dot')
                            print(G.nodes)
                            for node_id, altura in alturas:
                                G.nodes[str(node_id)]["altura"] = altura


                            
                            # Desenhar o grafo usando Matplotlib
                            nx.draw_shell(G, with_labels=True, node_color='skyblue', node_size=500, font_size=12, font_color='black')

                            # Salvar o gráfico como um arquivo .png
                            plt.savefig('output/grafo.png', format='png')

                            imagem = np.array(Image.open('output/grafo.png'))


                            # Carregar a imagem PNG
                            fig = go.Figure()

                            # Adicionar a imagem como um trace de imagem
                            fig.add_trace(go.Image(z=imagem))

                            # Configurar o layout do gráfico
                            fig.update_layout(
                                
                                xaxis=dict(visible=False),
                                yaxis=dict(visible=False),
                            )

                           
                            st.write("Análise concluída. Verifique os resultados.")
                            st.write("Grafo gerado:")
                            st.plotly_chart(fig)

                        
                            st.write("Dados gerados:")
                            
                            st.text(teste[0])
                        
            

if __name__ == "__main__":
    main()
