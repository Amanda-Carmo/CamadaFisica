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
import sys

# voce deverá descomentar e configurar a porta com através da qual ira fazer comunicaçao
#   para saber a sua porta, execute no terminal :
#   python -m serial.tools.list_ports
# se estiver usando windows, o gerenciador de dispositivos informa a porta

#use uma das 3 opcoes para atribuir à variável a porta usada
#serialName = "/dev/ttyACM0"           # Ubuntu (variacao de)
#serialName = "/dev/tty.usbmodem1411" # Mac    (variacao de)

serialNameT = "COM6"                  # Windows(variacao de)

def main():
    try:
        #declaramos um objeto do tipo enlace com o nome "com". Essa é a camada inferior à aplicação. Observe que um parametro
        #para declarar esse objeto é o nome da porta.
        com1 = enlace(serialNameT)
        com1.enable()

        print("Client TX enabled at: {}".format(serialNameT))
        print("---------------------")

        imageR = input("Digite o path da imagem: ")

        assert os.path.exists(imageR), "Imagem não encontrada em "+str(imageR)

        print("imagem localizada em: {}".format(imageR))


        with open(imageR, "rb") as img:
            txBuffer = img.read()

        txLen = len(txBuffer)

        header = len(txBuffer).to_bytes(2, 'big')
        header_int = int.from_bytes(header, "big")
        print("Enviando header")
               
        print("--------------------")        
        com1.sendData(np.asarray(header))
        print("enviado com sucesso!")
        print("Header: {}".format(header)) 
        print("Tamanho enviado: {}".format(header_int))
        print("--------------------")

        headerR, nHR = com1.getData(2)
        headerR_int = int.from_bytes(headerR, "big")

        print("Resposta do header: {}".format(headerR))
        print("Tamanho recebido: {}".format(headerR_int))
        print("Recebida resposta do header")
        print("--------------------")

        if header_int == headerR_int:

            print("iniciando time...")
            timeStart = time.time()
            print("---------------------")

            print("Enviando payload")
            print("--------------------")
            com1.sendData(np.asarray(txBuffer))

            print("Esperando resposta...")
            rxBuffer, nRx  = com1.getData(txLen) 
            print("Procedimento concluído") 

            tempo = time.time() - timeStart
            taxa = txLen/tempo
            
            
            print("___________________________________________________")   
            print("Tempo gasto para envio e recebimento: {}".format(tempo))
            print("Taxa de transmissão (bytes por segundo): {}".format(taxa))
            print("___________________________________________________")

            print("-------------------------")
            print("Comunicação encerrada")
            print("-------------------------")
        com1.disable()

        
    except Exception as erro:
        print("ops! :-\\")
        print(erro)
        com1.disable()
        

    #so roda o main quando for executado do terminal ... se for chamado dentro de outro modulo nao roda
if __name__ == "__main__":
    main() 