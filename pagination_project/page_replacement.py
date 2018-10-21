import numpy as np
import itertools

#------------------Funções-----------------#

#-------------------Start------------------#

def start():
	input, frames = read_input()

	pages_lost = fifo(input, frames)
	print('FIFO', pages_lost)

	pages_lost = otm(input, frames)
	print('OTM', pages_lost)

	pages_lost = lru(input, frames)
	print('LRU', pages_lost)

#------------------Fim Start---------------#

#--------------Função lê entrada-----------#
def read_input():
	input = open('input.txt', 'r')

	pages = input.read().split('\n')#Separamos o input por linhas dentro da lista
	#print(pages)#Resultado: Input: ['4', '1', '2', '3', '4', '1', '2', '5', '1', '2', '3', '4', '5']

	frames = pages[0]#Pegamos o primeiro elemento que será o nosso número de quadros
	pages = pages[1:]#Pega todos os elementos após o primeiro

	return pages,frames
#-------------Fim lê entrada---------------#

#------------------FIFO--------------------#

def fifo(input, frames):
	#print ("Input:", input, '\n' 'Frames:', frames)

	pages_lost = 0#Contador de falta de páginas

	#Colocamos "void" em todos os quadros da memória de acordo com a quantidade de quadros especificada
	memoryPages = ['void'] * int(frames)
	#print('MemoryPages:', memoryPages)

	#Iniciando a substituição de páginas
	for page in input:

		#Verifica se a página já existe na memória, se não...temos uma falta de página
		if page not in memoryPages:

			#Incrementamos a falta de página
			pages_lost += 1

			#Verifica se existe algum quadro vazio...
			if 'void' in memoryPages:
				#Trocamos um 'void', por uma página
				memoryPages.pop(0)
				memoryPages.append(page)

			#Caso não tenha apenas removemos o primeiro elemento e adicionamos o outro
			else:
				memoryPages.pop(0)
				memoryPages.append(page)

	return pages_lost
#----------------Fim FIFO------------------#

#----------------OTM-----------------------#
def otm(input, frames):
	#print ("Input:", input, '\n' 'Frames:', frames)

	#lista para verificar as próximas páginas
	nextPages = input.copy()

	pages_lost = 0#Contador de falta de páginas

	#Colocamos "void" em todos os quadros da memória de acordo com a quantidade de quadros especificada
	memoryPages = ['void'] * int(frames)

	#Iniciamos a substituição de páginas
	for page in input:
			#print('Page:', page)
			#print("MemoryPages:", memoryPages)
			#print('NextPages:', nextPages)
			nextPages.pop(0)#Removemos o elemento que entrou em um quadro, da nossa lista de próximo

			#Verifica se a página já está na memória
			if page not in memoryPages:

				#Incrementamos o contador de falta de página
				pages_lost += 1
				#print('Falta de páginas:', pages_lost)
				#print("MemoryPages:", memoryPages)
				#print('NextPages:', nextPages)

				#Verifica se existe algum quadro vazio
				if 'void' in memoryPages:
					#Retiramos um quadro vazio e adicionamos o elemento
					memoryPages.pop(0)
					#nextPages.pop(0)#Removemos o elemento que entrou em um quadro, da nossa lista de próximo
					memoryPages.append(page)
					#print('Entrei no void:', memoryPages)
					#print('nextPages:', nextPages)
				#Caso não exista...
				else:
					#Váriaveis de verificação
					page_not_again = False #False se não tiver página que saiu da lista de próximo
					index_to_remove = 0 #Índice de quem vai sair
					lock = True

					#Verificamos qual página no quadro não vai ser mais acessada
					for verifyPage in memoryPages:
						#Se a página não for acessada novamente, então recebe True
						#e finalizamos o for
						if lock:
							if verifyPage not in nextPages:
								page_not_again = True
								index_to_remove = memoryPages.index(verifyPage)
								#print("Página não mais acessada:", index_to_remove)
								lock = False
							
					#Verifica se alguma página não vai mais ser acessada
					if page_not_again:
						#Então removemos apenas quem não vai mais ser acessada
						memoryPages[index_to_remove] = page
						#nextPages.pop(0)#Removemos o elemento que entrou em um quadro, da nossa lista de próximo

					#Caso todas ás páginas ainda serão acessadas
					else:
						page_more_time = []

						#Verificamos o índice das páginas na memória de páginas na nossa lista de próximas páginas
						for verifyPage in memoryPages:
							page_more_time.append(nextPages.index(verifyPage))
							#print('Page_more_time:', page_more_time)

						more_time = max(page_more_time)#Maior elemento na lista de indices das páginas testadas
						#Como cada elemento entrou na ordem da mémoria de páginas, então seu indice é referente
						#Também a página na memória de páginas
						index_page_more_time = page_more_time.index(more_time)

						memoryPages[index_page_more_time] = page
						#nextPages.pop(0)
	return pages_lost				
#------------------Fim OTM-----------------#

#-----------------LRU----------------------#
def lru(input, frames):
	#print ("Input:", input, '\n' 'Frames:', frames)

	#lista para verificar as últimas páginas
	lastPages = []

	pages_lost = 0#Contador de falta de páginas

	#Colocamos "void" em todos os quadros da memória de acordo com a quantidade de quadros especificada
	memoryPages = ['void'] * int(frames)

	#Iniciamos a substituição de páginas
	for page in input:

			#print('Page:', page)
			#print("MemoryPages:", memoryPages)
			#Verificamos se uma página já apareceu na nossa lista
			#Se sim...nós removemos onde estava e adicionamos novamente ao final da lista
			if page in lastPages:
				index = lastPages.index(page)
				lastPages.pop(index)
				lastPages.append(page)#Adicionamos o elemento que entrou em um quadro ou não, na nossa lista de próximo
			#Caso não...nós apenas adicionamos ela no fim da lista
			else:
				lastPages.append(page)#Adicionamos o elemento que entrou em um quadro ou não, na nossa lista de próximo

			#print('LastPages:', lastPages)

			#Verifica se a página já está na memória
			if page not in memoryPages:

				#Incrementamos o contador de falta de página
				pages_lost += 1
				#print('Falta de páginas:', pages_lost)

				#Verifica se existe algum quadro vazio
				if 'void' in memoryPages:
					#Retiramos um quadro vazio e adicionamos o elemento
					memoryPages.pop(0)
					memoryPages.append(page)

				#Caso não exista...
				else:
					#Verificamos a página que foi acessada a mais tempo
					page_more_time = []

					#Verificamos o índice das páginas na memória de páginas na nossa lista de últimas páginas
					for verifyPage in memoryPages:
						page_more_time.append(lastPages.index(verifyPage))
						#print('Page_more_time:', page_more_time)

					more_time = min(page_more_time)#Menor elemento na lista de indices das páginas testadas

					#Como cada elemento entrou na ordem da mémoria de páginas, então seu indice é referente
					#Também a página na memória de páginas
					index_page_more_time = page_more_time.index(more_time)

					memoryPages[index_page_more_time] = page

	return pages_lost

#-----------------Fim LRU------------------#

#---------------Fim das Funções------------#


#-------MAIN-------#
start()
#------------------#
