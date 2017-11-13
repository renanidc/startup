# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
from selenium import webdriver
import csv
import time

#Atributos do produto
produto = ''	
categoria = ''
nome_usuario = ''
data_comentario = ''
recomendacao = ''
resumo_opiniao = ''
descricao_opiniao = ''	

#Define objeto writer para gravar no arquivo CSV
arquivo = csv.writer (open("comentarios.csv", "a"), delimiter=";")

#Escrever cabeçalho do arquivo CSV
arquivo.writerow(['produto', 'categoria', 'usuario', 'data_comentario', 
	'recomendacao', 'resumo', 'descricao'])

#Abre arquivo de links
links = open ('buscape/buscape-links.txt', 'r')

#Defina webdriver
driver = webdriver.PhantomJS(executable_path='phantomjs-2.1.1-linux-x86_64/bin/phantomjs')

#Laço para percorrer linhas do arquivo de links
for linha in links:		
	
	#Cada linha do arquivo contém um link e uma categoria
	link, categoria = linha.split(';')
	print link

	#Tenta acessar link do produto
	try:		
		driver.get(link)
		time.sleep(1)
		response = driver.page_source #recebe conteudo do response
		produto_html = BeautifulSoup(response, 'lxml')
	except:
		print 'ERRO DE CONEXÃO!'

	#Extrair e limpar dados do HTML
	try:
		produto = produto_html.find('h1').text.strip()
		produto = produto.split(' ')
		produto = produto [ :-3]
		produto = ' '.join(produto)

		qtd_comentarios = produto_html.find('small', attrs={'class':'body--gray consumer-opinion__title--small'}).text
		qtd_comentarios = qtd_comentarios.replace('(','')
		qtd_comentarios = qtd_comentarios.split(' ')
		numero_paginas = (int(qtd_comentarios[0]))/5

		#Navegar na paginação dos comentários
		for pagina in range(2, numero_paginas):

			http, comentarioURL = link.split('//')
			urlA, urlB = comentarioURL.split('/')
			comentarioURL = 'http://'+urlA+'/avaliacoes/'+urlB+'/?pagina='+str(pagina)+'#avaliacoes'
			print comentarioURL

			#Acessar link de paginacao		
			driver.get(comentarioURL)
			time.sleep(1)
			response = driver.page_source
			produto_html = BeautifulSoup(response, 'lxml')			

			#Encontrar comentários
			for comentario in produto_html.findAll('div', attrs={'class':'consumer-content'}):
				
				header = comentario.find('div', attrs={'class':'consumer-header'})
				nome_usuario = header.find('span', attrs={'class':'consumer-login--name'}).text.strip()
				data_comentario = header.find('span', attrs={'class':'consumer-login--lastAcess'}).text.strip()
				data_comentario = data_comentario.replace('Em ', '')
				recomendacao = header.find('span', attrs={'class':'consumer-recommend__true'}).text.strip()
				opiniao = comentario.find('div', attrs={'class':'consumer-opinion__content--info'})
				resumo_opiniao = opiniao.find('span', attrs={'class':'body--big consumer-description__title'}).text.strip()
				descricao_opiniao = opiniao.find('p', attrs={'class':'body--gray consumer-description__txt'}).text.strip()

				try:
					#Escreve linha no arquivo CSV com os dados do produto
					arquivo.writerow([produto.encode('utf-8'), categoria.encode('utf-8'), nome_usuario.encode('utf-8'), 
					data_comentario.encode('utf-8'), recomendacao.encode('utf-8'), resumo_opiniao.encode('utf-8'),
					descricao_opiniao.encode('utf-8')])
				except:
					print 'ERRO DE UNICODE'
	except:
			print "Página fora do formato padrão!"	


driver.close()