# -*- coding: utf-8 -*-
import os
from bs4 import BeautifulSoup # pip install bs4

# Diretório dos arquivos HTML gerados pelo IPED
diretorio_do_html = './'

# Percorre todos os arquivos no diretório
for nome_arquivo in os.listdir(diretorio_do_html):
    if nome_arquivo.endswith('.html'):
        caminho_arquivo = os.path.join(diretorio_do_html, nome_arquivo)

        # Abre o arquivo HTML e lê o seu conteúdo
        with open(caminho_arquivo, 'r', encoding='utf-8') as arquivo:
            conteudo = arquivo.read()

        # Analisa o conteúdo HTML com BeautifulSoup
        soup = BeautifulSoup(conteudo, 'html.parser')
        
        # Encontra todas as divs com a classe "audioImg iped-audio" dentro de uma tag <a>
        divs_audio = soup.select('a div.audioImg.iped-audio')
        
        # Itera sobre as divs encontradas
        for div_audio in divs_audio:
            # Obtém o valor do atributo "data-src2"
            data_src2 = div_audio['data-src2']
            
            # Cria um novo elemento <span> para conter o valor
            span_tag = soup.new_tag('span')
            span_tag.string = data_src2
            
            # Encontra o elemento pai <a> da div e insere o novo elemento <span> após o fechamento
            a_tag = div_audio.parent
            
            caminho_opus = span_tag.string[8:]
            caminho_txt = caminho_arquivo[:-5] + "_arquivos/" + str(caminho_opus[:-5].split('/')[-1]) + ".txt"

            if (os.path.isfile(caminho_txt) == True):
                ref_arquivo = open(caminho_txt,"r")
                for linha in ref_arquivo:
                    span_tag.string = '[transcricao] ' + linha
                ref_arquivo.close()
                print(f'achei o {caminho_txt}')

                a_tag.insert_after(span_tag)

        # Salva as alterações no arquivo HTML
        with open(caminho_arquivo, 'w', encoding='utf-8') as arquivo:
            arquivo.write(str(soup))