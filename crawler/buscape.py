# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
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

			for produto in soup.findAll('li', attrs={'class':'bui-product__container small-12 medium-4 large-4 columns js-discount'}):
				print produto.find('a')['href']
				arquivo.write(produto.find('a')['href']+";"+categoria+'\n')
		except:
			print 'Link invalido!'

#capturarItensMenu()
#capturarProdutos()