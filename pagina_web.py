import os
import subprocess
import csv
import json
import streamlit as st
import streamlit.components.v1 as components
from streamlit_modal import Modal
import pandas as pd
import pydotplus
import re


def verifica_dados(dataset):
    padrao_pasta = r'^(?:[a-zA-Z]:[\\\/]|\\\\)(?:[a-zA-Z0-9]+[\\\/])*[a-zA-Z0-9]'
    padrao_id = set()
    dados_limpos = []
    if(len(dataset) > 0):
        for row in dataset:
            # Limpa as entradas
            id_ = row['ID'].strip()  # Renomeado para 'id_' para evitar conflito com a função id() do Python
            nome = row['Nome'].strip()
            pasta_origem = row['PastaOrigem'].strip()
            pasta_destino = row['PastaDestino'].strip()
            pasta_backup = row['PastaBackup'].strip()
            if not id_:
                st.session_state["erro"] = 1
                st.write("ID vazio encontrado.")
            
            if not nome:
                st.session_state["erro"] = 1
                if(id_):
                    st.write(f"Nome vazio encontrado. ID: {id_}")
                else:
                    st.write("Nome vazio encontrado.")

            if not pasta_origem:
                st.session_state["erro"] = 1
                if(id_):
                    st.write(f"Origem vazia encontrada.ID: {id_}")
                else:
                    st.write("Origem vazia encontrada.")
            # Verifica IDs repetidos
            if id_ in padrao_id:
                if(id_ != ""):
                    st.write(f"ID repetido encontrado: {id_}")
                    st.session_state["erro"] = 1
            else:
                padrao_id.add(id_)
                # Adiciona os dados limpos à lista de dados
                dados_limpos.append(row)
            
            # Verifica se origem = destino/backup
            if pasta_origem == pasta_destino:
                st.write(f"A pasta de origem é igual à pasta de destino. ID: {id_}")
                st.session_state["erro"] = 1
            
            if pasta_origem == pasta_backup:
                st.write(f"A pasta de origem é igual à pasta de backup. ID: {id_}")   
                st.session_state["erro"] = 1
            
            # Verifica se as pastas seguem o padrão
            if not re.match(padrao_pasta, pasta_origem) and pasta_origem != "":
                
                st.write(f"A pasta de origem não segue o padrão. ID: {id_}")
                st.session_state["erro"] = 1
            
            if not re.match(padrao_pasta, pasta_destino) and pasta_destino != "":
                
                st.write(f"A pasta de destino não segue o padrão. ID: {id_}")
                st.session_state["erro"] = 1
            
            if not re.match(padrao_pasta, pasta_backup) and pasta_backup != "":
                
                st.write(f"A pasta de backup não segue o padrão. ID: {id_}")
                st.session_state["erro"] = 1
                
    else:
        st.session_state["erro"] = 1
    return dados_limpos


def dot_to_json(dot_file):
    graph = pydotplus.graph_from_dot_file(dot_file)
    nodes = []
    edges = []

    for node in graph.get_nodes():


        try:
            node_id = node.get_name().strip('"')
        
            label = node.get_label().strip('"')
            nodes.append({"id": int(node_id), "label": label, "title": int(node_id), "shape": "box", "size": 10})
        except:
            pass

    for edge in graph.get_edges():
        source = edge.get_source().strip('"')
        target = edge.get_destination().strip('"')
        label = edge.get_label().strip('"')
        edges.append({"from": int(source), "to": int(target), "weight": 1, "title": label})

    graph_data = {"nodes": nodes, "edges": edges}
    return json.dumps(graph_data, indent=4)


def move_uploaded_file(uploaded_file):
    file_path = os.path.join("csv/", uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return file_path

def clear_output_directory():
    output_dir = "output"
    if os.path.exists(output_dir):
        files = os.listdir(output_dir)
        for file in files:
            if(file != ".gitkeep"):
                file_path = os.path.join(output_dir, file)
                os.remove(file_path)


def main():

    st.set_page_config(page_title="Hiperstream", page_icon="web_custom/Logo_hi.png")

    col1, col2 = st.columns([3,1])

    with col1:
        st.title("Hiperstream Hackathon")
    with col2:

        st.write("")
        st.write("")
        if st.button("Precisa de Ajuda?",key="help_button"):
            modal = Modal(key="tutorial_key",title="Tutorial")
            with modal.container():
                st.title('Video')
                video_file = open('web_custom/tutorial.mp4', 'rb')
                video_bytes = video_file.read()
                st.video(video_bytes)
                st.write("Se o vídeo não carregar clique [aqui](https://youtu.be/Xy8BK6DnmbU)")
                st.title('Escrito')
                st.write("1- Escolha um arquivo da lista ou faça upload do seu próprio.")
                st.write("2- Clique em \"Analisar dados\" para fazer a análise do arquivo escolhido.")
                st.write("3- Após a análise será um grafo e um texto resposta.")
                st.write("4- O grafo é interativo, ou seja, você pode navegar e edita-lo.")
                st.write("5- Se você parar o mouse sobre um vertice, será mostrado o ID.")
                st.write("6- Se você parar o mouse sobre uma aresta, será mostrado o diretorio e tipo da relação.")
                st.write("7- As mudanças feitas no grafo não são refletidas no CSV ou texto.")
                st.write("8- Ao interagir com um botão a página recarrega.")
    st.title("Análise de Arquivos CSV")

    uploaded_file = st.file_uploader("Faça o upload de um arquivo CSV")

   
    if uploaded_file is not None:
        
        st.write(f"Arquivo '{uploaded_file.name}' foi carregado com sucesso.")
        move_uploaded_file(uploaded_file)


    
    files = [file for file in os.listdir("csv/") if file.endswith(".csv")]
    
    if len(files) == 0:
        st.write("Nenhum arquivo CSV encontrado na pasta do código.")
    else:
        st.write("Ou use um dos arquivos CSV abaixo")
        selected_file = st.selectbox("Selecione um arquivo CSV:", files)
        selected_file = os.path.join("csv/", selected_file)


        try:
            df = pd.read_csv(selected_file, sep=';')
            st.write("Preview da Tabela:")

            st.dataframe(df)
        

            if st.button("Analisar Dados"):
                clear_output_directory()
                st.title("Resultados")
                data = []
                if 'erro' not in st.session_state:
                    st.session_state["erro"] = 0
                else:
                    st.session_state["erro"] = 0
                if 'disponivel' not in st.session_state:
                    st.session_state["disponivel"] = 0
                else:
                    st.session_state["disponivel"] = 0
                with open(selected_file, 'r') as file:
                    reader = csv.reader(file)
                    contador = 0
                    for row in reader:
                        try:
                            labels = [label.strip() for label in row[0].split(';')]  
                            row_dict = {'ID': labels[0],
                                        'Nome': labels[1],
                                        'PastaOrigem': labels[2],
                                        'PastaDestino': labels[3],
                                        'PastaBackup': labels[4]}  
                            if(contador != 0):
                                data.append(row_dict)
                            else:
                                contador+=1
                        except IndexError:
                            try:
                                labels = [label.strip() for label in row[0].split(',')]  
                                row_dict = {'ID': labels[0],
                                            'Nome': labels[1],
                                            'PastaOrigem': labels[2],
                                            'PastaDestino': labels[3],
                                            'PastaBackup': labels[4]}  
                                if(contador != 0):
                                    data.append(row_dict)
                                else:
                                    contador+=1
                            except IndexError:
                                    st.session_state["erro"] = 1
                                    break                       

                    
                data = verifica_dados(data)

                if 'disponivel' not in st.session_state:
                    if(st.session_state["erro"] == 1):
                        st.session_state["disponivel"] = 0
                else:
                    if(st.session_state["erro"] == 1):
                        st.session_state["disponivel"] = 0
                if(st.session_state["erro"] == 0):
                    if 'disponivel' not in st.session_state:
                        st.session_state["disponivel"] = 1
                    else:
                        st.session_state["disponivel"] = 1
                    output_file = 'output/func_data.csv'
                    with open(output_file, 'w', newline='') as file:
                        writer = csv.DictWriter(file, fieldnames=['ID', 'Nome', 'PastaOrigem', 'PastaDestino', 'PastaBackup'], delimiter=';')
                        writer.writeheader()  
                        writer.writerows(data)  
                    # Chama o código em C para analisar os dados
                    subprocess.run(["gcc", "-o", "./source/main", "./source/main.c"])

                    # Execute o programa compilado
                    subprocess.run(["./source/main"])
                else:
                    st.write("Arquivo Invalido")   
                if(st.session_state["disponivel"] == 1):
                

                            
                            if os.path.exists("output/grafo.dot") and os.path.exists("output/dados.txt"):
                                tab1, tab2 = st.tabs(["Grafo", "Dados"])
                                dot_file = "output/grafo.dot"
                                json_data = dot_to_json(dot_file)

                                with tab1:
                                    st.subheader("Grafo gerado")

                                    components.html( """          
                                    <html>
                                    <head>
                                    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/vis/4.16.1/vis.css" type="text/css" />
                                    <script type="text/javascript" src="https://cdnjs.cloudflare.com/ajax/libs/vis/4.16.1/vis-network.min.js"> </script>
                                    <center>
                                    <h1></h1>
                                    </center>
                                    <!-- <link rel="stylesheet" href="../node_modules/vis/dist/vis.min.css" type="text/css" />
                                    <script type="text/javascript" src="../node_modules/vis/dist/vis.js"> </script>-->
                                    <style type="text/css">
                                            #mynetwork {
                                                width: 100%;
                                                height: 100%;
                                                background-color: #ffffff;
                                                position: absolute;
                                                float: left;
                                            }       
                                    </style>
                                    </head>
                                    <body>
                                    <div id = "mynetwork"></div>
                                    <div id = "config"></div>
                                    <script type="text/javascript">
                                        var edges;
                                        var nodes;
                                        var network; 
                                        var container;
                                        var options, data;
                                        function drawGraph() {
                                            var container = document.getElementById('mynetwork');
                                            var dotObject = JSON.parse(`"""+ json_data + """`);
                                            var nodes = new vis.DataSet(dotObject.nodes);
                                            var edges = new vis.DataSet(dotObject.edges);
                                            data = {nodes: nodes, edges: edges};
                                            var options = {
                                            "manipulation": {
                                                "enabled": true,
                                                },
                                                "layout": {
                                                "hierarchical": {
                                                    "nodeSpacing": 300,
                                                    "direction": "UD",
                                                    "sortMethod": "directed",
                                                }
                                            },
                                            "nodes":{
                                                "shape": "box",
                                            },
                                            edges:{
                                            "arrows": {
                                            "to": { enabled: true, scaleFactor: 1, type: "arrow" }
                                            }
                                        },
                                            "interaction": {
                                                "dragNodes": true,
                                                "hideEdgesOnDrag": false,
                                                "hideNodesOnDrag": false,
                                                "hover": true,
                                                "keyboard":{enabled: true},
                                                "multiselect": true,
                                            },
                                            "physics": false
                                    };
                                            network = new vis.Network(container, data, options);
                                            return network;
                                        }
                                        drawGraph();
                                    </script>
                                    </body>
                                    </html>
                                    """, height = 900,width=900)
                                with tab2:
                                    st.subheader("Dados gerados")
                                    
                                    with open("output/dados.txt", "r", encoding="utf-8") as file:
                                        st.text(file.read())
        except:
            st.write("Arquivo inválido")
                

if __name__ == "__main__":
    main()
    
