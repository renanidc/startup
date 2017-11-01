# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import time
import csv

itens = []
produtos = []
arquivo = open ('buscape/buscape-links.txt','a')	

#Metodo para capturar os itens (categorias de produtos) do menu
def capturarItensMenu():

	print 'Crawleando: buscape...'	

	r = requests.get('http://www.buscape.com.br/')
	soup = BeautifulSoup (r.content, 'lxml') #recebe conteúdo HTML da requisição

	menu = soup.find('header', attrs={'class':'header__bar header--home'})
	
	for item in menu.findAll('a'):
		if item.has_attr('href'):
			if item['href'] not in itens: #Não adicionar itens repetidos na lista
				itens.append(item['href'])

#Metodo para capturar produtos
def capturarProdutos():

	for produto in itens:

		categoria = produto.replace("/", "")

		try:
			r = requests.get('http://www.buscape.com.br'+produto)

			soup = BeautifulSoup (r.content, 'lxml')

			#Encontrar produtos com js-discount
			for produto in soup.findAll('li', attrs={'class':'bui-product__container small-12 medium-4 large-4 columns js-discount'}):
				print 'PRIMEIRA PAGINA DA CATEGORIA: ', produto.find('a')['href']
				arquivo.write(produto.find('a')['href']+";"+categoria+'\n')

			#Encontrar produtos com prioridade first
			for produto in soup.findAll('li', attrs={'class':'bui-product__container small-12 medium-4 large-4 columns first'}):
				print 'PRODUTO COM FIRST: ', produto.find('a')['href']
				arquivo.write(produto.find('a')['href']+";"+categoria+'\n')					

			#Encontrar produtos sem js-discount	
			for produto in soup.findAll('li', attrs={'class':'bui-product__container small-12 medium-4 large-4 columns'}):
				print 'PRODUTO SEM JS-DISCOUNT: ', produto.find('a')['href']
				arquivo.write(produto.find('a')['href']+";"+categoria+'\n')


			old_link = None #Gambiarra :)

			while(soup.find('li',attrs={'class':'bui-pagination--item next active'})!=None): #Navegar na paginação dos produtos

				link = soup.find('li',attrs={'class':'bui-pagination--item next active'})
				link = link.find('a')['href'] #Encontrar link da próxima página
				print 'PROXIMA PAGINA DE PRODUTOS: ', link

				#Evitar loop que fica repetindo o mesmo link (Bug quântico) '-'
				if(old_link!=None and old_link==link):
					break

				r = requests.get(link)

				soup = BeautifulSoup (r.content, 'lxml')

				#Encontar produtos com js-discount
				for produto in soup.findAll('li', attrs={'class':'bui-product__container small-12 medium-4 large-4 columns js-discount'}):
					print 'PRODUTO COM JS-DISCOUNT: ', produto.find('a')['href']
					arquivo.write(produto.find('a')['href']+";"+categoria+'\n')

				#Encontrar produtos com prioridade first
				for produto in soup.findAll('li', attrs={'class':'bui-product__container small-12 medium-4 large-4 columns first'}):
					print 'PRODUTO COM FIRST: ', produto.find('a')['href']
					arquivo.write(produto.find('a')['href']+";"+categoria+'\n')					

				#Encontrar produtos sem js-discount	
				for produto in soup.findAll('li', attrs={'class':'bui-product__container small-12 medium-4 large-4 columns'}):
					print 'PRODUTO SEM JS-DISCOUNT: ', produto.find('a')['href']
					arquivo.write(produto.find('a')['href']+";"+categoria+'\n')

				old_link = link #Receber link antigo

		except:
			print 'Pagina fora do formato padrao!'
		finally:
			time.sleep(1)

capturarItensMenu()
capturarProdutos()