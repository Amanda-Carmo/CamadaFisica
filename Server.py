#####################################################
# Camada Física da Computação
#Carareto
#11/08/2020
#Aplicação
####################################################


#esta é a camada superior, de aplicação do seu software de comunicação serial UART.
#para acompanhar a execução e identificar erros, construa prints ao longo do código! 


from enlace import *
import time
import numpy as np
import os
import io
import subprocess
import logging
import PIL.Image as Image
import Client

# voce deverá descomentar e configurar a porta com através da qual ira fazer comunicaçao
#   para saber a sua porta, execute no terminal :
#   python -m serial.tools.list_ports
# se estiver usando windows, o gerenciador de dispositivos informa a porta

#use uma das 3 opcoes para atribuir à variável a porta usada
#serialName = "/dev/ttyACM0"           # Ubuntu (variacao de)
#serialName = "/dev/tty.usbmodem1411" # Mac    (variacao de)

serialNameR = "COM3"                  # Windows(variacao de)


def main():
    try:
        #declaramos um objeto do tipo enlace com o nome "com". Essa é a camada inferior à aplicação. Observe que um parametro
        #para declarar esse objeto é o nome da porta.
        print("A recepção vai começar")        
        
        com2 = enlace(serialNameR)

        # Ativa comunicacao. Inicia os threads e a comunicação seiral 
        com2.enable()

        imageW = './img/' + input('Nomeie a imagem que vai receber! ') + 'Copia.jpg'

        #Se chegamos até aqui, a comunicação foi aberta com sucesso. Faça um print para informar.
        print('comunicação aberta com sucesso')
        print("Server Rx habilitado em: {}".format(serialNameR))
        print("---------------------")

        print("local da imagem a ser salva: {}".format(imageW))
        print("---------------------")        

        print("Esperando Header...")
        
        header, nHr = com2.getData(2)      
        
        print("---------------------")
        print("Header recebido com sucesso!")
        print("---------------------")
        time.sleep(1)


        print("Enviando resposta do header para o cliente...")  
        com2.sendData(np.asarray(header))
        print("---------------------")

        HeadR = int.from_bytes(header, "big")

        print("Esperando dados do payload do cliente...")
        print("--------------------")    

        rxBuffer, nRx = com2.getData(HeadR)     

        print("Payload recebido!")
        print("--------------------")

        print("Pasasando os dados para o cliente...")
        com2.sendData(np.asarray(rxBuffer))
        time.sleep(1)
        print("--------------------")             
              

        print("Salvando imagem em: {}".format(imageW))   
        print(" - {}".format(imageW))


        f = open(imageW, 'wb')
        f.write(rxBuffer)

       
        print("-------------------------")
        print("Comunicação encerrada")
        print("-------------------------")
        com2.disable()

        
    except Exception as erro:
        print("ops! :-\\")
        print(erro)
        com2.disable()
        

    #so roda o main quando for executado do terminal ... se for chamado dentro de outro modulo nao roda
if __name__ == "__main__":
    main()
