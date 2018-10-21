import numpy as np

'''
Especificação:
	Valores de saída:
		¤ Tempo de retorno médio
		¤ Tempo de resposta médio
		¤ Tempo de espera médio

	Exemplo de Entrada:
		0 20
		0 10
		4 6
		4 8
	Obs:
		0 --> Tempo de Chegada
		20 --> Tempo de Duração

	Exemplo de Saída:
		FCFS 30,5 19,5 19,5
		SJF 21,5 10,5 10,5
		RR 31,5 2,0 20,5
'''

#--------------Funções-------------#

#----------Função Inicia-----------#
def start():
	input = read_input()

	average_return, average_response, average_wait = FCFS(input)
	print("FCFS", average_return, average_response, average_wait)

	average_return, average_response, average_wait = SJF(input)
	print("SJF", average_return, average_response, average_wait)

	average_return, average_response, average_wait = RR(input)
	print("RR", average_return, average_response, average_wait)	
#-------------Fim start------------#

#--------Função lê entrada---------#
def read_input():
	input = open('input.txt', 'r')
	#process = input.read().replace(' ', '\n').split()
	process = input.read().split('\n')#Separamos o input por linhas dentro da lista
	#print(process)#Resultado: ['0 20', '0 10', '4 6', '4 8']

	return process
#---------Fim lê entrada-----------#

#------------Ordena Processo(FCFS, JSF, RR)-------#
def order_process(input, operation):
	process_in = []
	pArrival = []
	pDuration = []

	for count in range(len(input)):
		process_input = input[count].split(' ')
		pArrival.append(process_input[0])#['0', '0', '4', '4']
		pDuration.append(process_input[1])#['20', '10', '6', '8']
		process_in.insert(0, process_input)#Geramos uma lista de duas dimensões para facilitar as etapas de processamento
		#print(time_in)
		#print(pArrival)
		#print(pDuration)
	#print("process_in", len(process_in))

	#FCFS = 0, Ordena por ordem de chegada
	if operation == 0:
		for count in range(len(process_in)-1, 0, -1):
			for i in range(count):
				if int(process_in[i][0]) >= int(process_in[i+1][0]):
					temp = process_in[i]
					process_in[i] = process_in[i+1]
					process_in[i+1] = temp
		#print(process_in)

	#SJF = 1, Ordena por tempo de processo
	if operation == 1:
		for count in range(len(process_in)-1, 0, -1):
			for i in range(count):
				if int(process_in[i][1]) >= int(process_in[i+1][1]):
					temp = process_in[i]
					process_in[i] = process_in[i+1]
					process_in[i+1] = temp
		#print(process_in)

	#RR = 2, Ordena por ordem de chegada e adiciona o contador do quantum
	if operation == 2:
		for count in range(len(process_in)-1, 0, -1):
			for i in range(count):
				if int(process_in[i][0]) >= int(process_in[i+1][0]):
					temp = process_in[i]
					process_in[i] = process_in[i+1]
					process_in[i+1] = temp

		for count in range(len(process_in)):
			process_in[count].append(0)#Adiciona o processo gasto

		#print(process_in)

	return process_in
#------------------Fim Ordena Processo----------------#

#----------Função FCFS-------------#
def FCFS(input):
	time_in = order_process(input, 0)
	size = len(time_in)
	time = 0
	time_wait = 0
	time_return = 0
	time_response = 0

	for process in time_in:
		#print("Process:", process)
		time_response += time - int(process[0])#Incrementa o tempo de resposta com base no tempo atual e tempo de entrada do processo atual
		time_wait = time_response#Tempo de espera igual ao tempo de resposta
		time += int(process[1])#Incrementa o tempo com o tempo de processamento do processo atual
		time_return += time - int(process[0])#Tempo de retorno é calculado com o tempo total + tempo de retorno - tempo de chegada
	
	average_return = time_return/size#Aqui temos nosso tempo médio de retorno
	average_response = time_response/size#Tempo médio de resposta
	average_wait = time_wait/size#Tempo médio de espera

	return average_return, average_response, average_wait	
#------------Fim FCFS--------------#

#----------Função SJF--------------#
def SJF(input):
	process_in = order_process(input, 1)
	size = len(process_in)
	execute = size#Verificação de execução

	process_min_time = min(process_in)#Pega o processo de menor tempo
	time = int(process_min_time[0])#Setta o tempo com o tempo do menor processo

	time_wait = 0
	time_return = 0
	time_response = 0

	#Verifica a execução do processos
	while execute:
		#Definimos um for até o final da lista de processos
		for count in range(size):
			#Verificamos se o tempo de chegada do processo atual
			#é menor ou igual ao tempo do menor processo que settamos anteriormente
			if int(process_in[count][0]) <= time:
				#print("Time:", time)
				#Seguimos o mesmo esquema do FCFS
				time_response += time - int(process_in[count][0])
				time_wait = time_response
				time += int(process_in[count][1])
				#print(int(process_in[count][0]))
				time_return += time - int(process_in[count][0])
				#Apenas nesse momento que precisamos retirar o processo que já foi executado
				#da fila
				process_in.pop(count)
				break#Usamos um break para sair totalmente da execução, devido ao .pop()
		execute -= 1#Sempre decrementamos o execute para finalizar a fila de processos

	average_return = time_return/size
	average_response = time_response/size
	average_wait = time_wait/size

	return average_return, average_response, average_wait

#------------Fim SJF---------------#

#-----------Função RR--------------#
def RR(input):
	quantum = 2
	time_in = order_process(input, 2)
	size = len(time_in)

	process_min_time = min(time_in)#Pega o processo de menor tempo
	time = int(process_min_time[0])#Setta o tempo com o tempo do menor processo

	time_wait = 0
	time_return = 0
	time_response = 0
	end_process = True
	next_process_fila = True
	back_to_fila = False
	countFila = len(time_in)
	fila = []
	next_process = []
	
	#Verifica se ainda possui processo na fila
	while end_process:
		#Verifica se ainda tem algum processo para entrar na fila 
		while next_process_fila:
			#Se o número de processos for maior que 0
			if len(time_in) > 0:
				#Vamos então rodar um for até o final da lista de processos
				for count in range(len(time_in)):
					#Caso o tempo de entrada seja menor ou igual a o tempo
					if int(time_in[count][0]) <= time:
						fila.append(time_in[count])#Então adicinamos o processo no fim da fila
						time_in.pop(count)#Agora retiramos esse processo da nossa lista de processos
						break#Encerramos a iteração
					else:
						#Caso procuremos um processo e não achamos um que possua o tempo de entrada menor ou igual ao tempo
						#Definimos uma saida do while
						next_process_fila = False
			else:
				#Caso a lista de processos seja menor que 0, não possuimos processos para a fila
				next_process_fila = False#Encerramos a execução do While

		#Iniciamos um for para começar a execução dos processos na fila
		for count in range(len(fila) + 1):
			#print("Fila:", fila)
			#Verifica se o ultimo processo precisa voltar para a fila
			if back_to_fila:
				fila.append(next_process)#Se sim, nós adicionamos ele no final da fila
				back_to_fila = False#Agora defimos que nenhum processo precisa voltar para a fil

			#Se o tempo de entrada do processo for menor ou igual ao tempo atual nós iniciamos
			if int(fila[count][0]) <= int(time):
				#Se Tempo de processamento menor que Quantum
				if int(fila[count][1]) < quantum:#Tempo de processo menor que quantum
					if int(fila[count][2]) == 0:#Verifica se já executou alguma vez
						time_response += (time - int(fila[count][0]))#Logo alteramos o tempo de resposta

					time += int(fila[count][1])#Logo o tempo é incrementado com o processamento deele
					fila[count][2] += int(fila[count][1])#Seu numero de execução quantum é igual ao seu tempo de processamento
					fila[count][1] = 0#Zeramos o tempo de processamento

				#Se tempo de processamento maior ou igual a Quantum
				if int(fila[count][1]) >= quantum:
					#Verifica se ele já executou alguma vez
					if int(fila[count][2] == 0):
						time_response += (time - int(fila[count][0]))#Logo incrementa o tempo de resposta com seu tempo de processamento
					fila[count][1] = int(fila[count][1]) - quantum#Agora nós decrementamos o tempo de processamento com o valor do quantum
					fila[count][2] = int(fila[count][2]) + quantum#Também decrementamos o contador de quantum para saber o quanto falta para esse processo terminar
					time += quantum#Normalmente incrementamos o tempo com o Quantum

				#Se o tempo de processamento já estiver zerado
				if int(fila[count][1]) == 0:
					time_return += (time - int(fila[count][0]))#Incrementamos o tempo de retorno
					time_wait += (time - int(fila[count][0]) - int(fila[count][2]))#Agora para saber seu tempo de espera, pegamos o tempo e diminuimos o tempo de espera e o contador de quantum
					#print(time_wait)
					fila.pop(count)#Agora esse processo está apto a sair da fila de processamento
					next_process_fila = True#Agora vamos buscar um novo processo
					countFila -= 1#Decrementamos o contador da fila
					break#Saimos da execução do processo

				#Se ainda possui tempo de processamento
				if int(fila[count][1]) > 0:
					next_process = fila[count]#Passamos ele para estado de pronto
					back_to_fila = True#Definimos que ele deve voltar a fila
					fila.pop(count)#Removemos ele para dar inicio  um novo processo
					next_process_fila = True#Definimos que podemos iniciar um novo processo
					break#Saimos da execução desse processo

		#Agora precisamos saber se ainda possui processos na fila
		if countFila == 0:
			end_process = False#Já que não temos mais processos na fila, encerramos a execução

	average_return = time_return/size
	average_response = time_response/size
	average_wait = time_wait/size

	return average_return, average_response, average_wait
	

#-------------Fim RR-------------#

#----------Fim Funções-----------#

#---------------Main-------------#
start()#Inicia execução
#--------------------------------#
