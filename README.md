# Diana 8.0
A Diana 8.0 é um chatbot que aprende, escuta, fala, toca música e pode controlar um Arduíno. Ela é feita em Python, e foi bem testada no Python3.6. Está é a versão mais recente!

## Tópicos
- [Contributing to GraphQL Zeus](#Contributing-to-GraphQL-Zeus)
  - [Table of Contents](#Como a Diana Aprende)
  - [Reporting Issues](#Reporting-Issues)
  - [Code Contribution](#Code-Contribution)
  





# Interagindo com a Diana

#Como a Diana Aprende
# Instalação de bibliotecas
# Como ativar o reconhecimento de voz
**1° instale a biblioteca PyAudio**
**2° instale a biblioteca SpeechRecognition**
**3° pratique**

# Como ativar a fala
**1° Instale o PyGame**
**2° Instale o GTTS**

# Como controlar um Arduíno?
**1° Instale a biblioteca pyfirmata**
**2° carregue a biblioteca StandartFirmata**
**3° configure a IDE**
**4° compile o programa**
**5° Programe**
**6° configure a porta**
**7° configure os comandos**
**8° pratique**
# Como tocar uma música? 

**1° instale a biblioteca do Pygame**
**2° Mova os arquivos**
**3°Configure a Diana**
**4° Pratique**
# Atualizações da versão 8.0

###Interagindo com a Diana
Ao executar a Diana, basta fazer uma pergunta que ela poderá responder.  

Você pode ativar a fala, assim ela irá usar a biblioteca Pygame e a biblioteca GTTS para gerar e executar uma fala com a resposta.  

Você também pode clicar no reconhecimento de fala, assim a Diana irá reconhecer a sua fala, atravéz da biblioteca PyAudio e da biblioteca SpeechRecognition.  

É necessário que você instale as bibliotecas manualmente.

### Como a Diana Aprende
A biblioteca pyanalise acessa um conjunto de arquivos de conversação, em cada arquivos, existe uma conversa especifica, onde cada frase está separada por ponto e virgula. Cada posição é considerada uma lista.

Usando o PyAnalise, podem acontecer 3 coisas no modo interação. A Diana pode encontrar uma frase que seja muito semelhante a que você digitou, e se a semelhança for mair que a precisaõ definida em **config>pyanalise**, a diana irá responder a posição encontrada +1. Esse é o modo responder.

Mas caso não exista a posição+1, ou seja, a frase mais semelhante a digitada é a ultima de um arquivo, então a Diana irá ativa o modo continuar assunto, ou seja, ela irá continuar aquele arquivo especifico.

Caso a melhor semelhança esteja abaixo da precisão minima definidade em **config>pyanalise**, A Diana irá ativar o modo criar_assunto. Neste modo, a Diana tenará criar um arquivo com sua pergunta e a sua resposta. Estas são as duas formas básicas da Diana Aprender.

----------

### Instalação de bibliotecas
Com o Python já instalado e devidamente pré configurado, é hora de instalar as bibliotecas. Por padrão, a Diana não vem mais com bibliotecas pré instaladas e nem tentar instalar, executando comandos de instalação em máquinas desconhecidas.  

Portanto, torna necessário a instalação manual das mesmas. Caso você esteja usando o Windows, terá que abrir o CMD para executar os comandos. Se você tiver em uma distro Linux, terá que usar o terminal.  

É super recomendado o uso do Python3.6 para a execução da Diana, algumas bibliotecas podem estar indisponíveis em versões posteriores e inferiores.  

----------
### Como ativar o reconhecimento de voz
**1° instale a biblioteca PyAudio**
É altamente recomendádo o uso do Python3.6. Outras versões, podem ainda não terem o PyAudio compartível.  
No Ubuntu  
```
sudo pip3.6 install pyaudio --no-cache  
``` 

No Windows  
```
pip3.6 install pyaudio --no-cache  
```
**2° instale a biblioteca SpeechRecognition**
No Ubuntu  
```
sudo pip3.6 install speechrecognition --no-cache  
``` 

No Windows  
```
pip3.6 install speechrecognition --no-cache  
```
**3° pratique**
O reconhecimento de voz na tela de interação, é uma funcionalidade beta, e problemas com o seu microfone, podem acontecer. Use-a sabendo que ela pode ser bem limitada!

----------
### Como ativar a fala
**1° Instale o PyGame**
No Ubuntu  
```
sudo pip3.6 install pygame --no-cache  
``` 

No Windows  
```
pip3.6 install pygame --no-cache  
```
**2° Instale o GTTS**
No Ubuntu  
```
sudo pip3.6 install gtts --no-cache  
``` 

No Windows  
```
pip3.6 install gtts --no-cache  
```
----------
### Como controlar um Arduíno?
**1° Instale a biblioteca pyfirmata**
No Ubuntu  
```
sudo pip3.6 install pyfirmata --no-cache  
``` 

No Windows  
```
pip3.6 install pyfirmata --no-cache  
```

**2° carregue a biblioteca StandartFirmata**
Carregue a biblioteca **StandartFirmata** na IDE do Arduíno. Caso você esteja no Linux, use o sudo para executar a IDE. 
**Arquivo>Exemplos>Firmata>StandartFirmata**

**3° configure a IDE**
Selecione a **Placa**, **Processador** e **Porta**, de acordo com o seu Arduíno. Salve a informação em Roxo, precisaremos da porta, em breve. No Windows 10, costuma ser  "COM"+numero, é no Ubuntu costuma ser "/dev/ttyACM"+número. **Fique atento a este detalhe.**  
![musicas][image-arduino-configurar]

**4° compile o programa**
Agora, compile o programa para o Arduino  
![musicas][image-arduino-compilar]

**5° Programe**
Caso tudo esteja funcionando, acesse o arquivo **arduino_code.py** dentro da Diana. As instruções para o Arduíno estão dentro da definição **code_instructions**, a qual ela recebe a conexão, e uma mensagem. Podemos portanto, usar uma lógica bem simples, e escrever um programa que liga ou desliga um LED. A Diana deve estar fechada neste momento.  
![musicas][image-def-programar]

**6° configure a porta**
Com o seu Arduíno conectado, abra a Diana, use o **sudo** caso você esteja em uma distro Linux, acesse **config > Comandos** e no primeiro campo, digite o endereço da sua porta, obtida no 3° passo.  
![musicas][image-diana-porta]

**7° configure os comandos**
Com o programa escrito, vamos enviar a mensagem **"ligar"** e **"desligar"**, também vamos programar qual palavra-chave a Diana usará, para enviar cada uma das mensagens. A Diana também usa o **Pyanalise** para tomar as decisões, portanto, qualquer coisa parecida com as palavras chaves, será confundida e poderá enviar a mensagem.  
![musicas][image-diana-chaves]  
Aproveite também, e faça os testes, para verificar se o comando funciona ou não!

**8° pratique**
Digite a palavra-chave na tela de interação, e veja seu Arduíno reagindo!  
![musicas][image-diana-ativar]  

----------
### Como tocar uma música? 
**1° instale a biblioteca do Pygame**
No Ubuntu   
```
sudo pip3.6 install pygame --no-cache  
```  

No Windows  
```
python -m pip install pygame --no-cache  
```  
**2° Mova os arquivos**
Mova os arquivos .mp3 para a pasta música, dentro da Diana. Alguns arquivos .mp3 podem não funcionar. Usamos músicas do Youtube Library e tudo funcionou:  
![musicas][image-music]  

**3°Configure a Diana**
Com a Diana em execução, acesse **config > Tocar música** e adicione as informações pedidas  
![configurando a diana][image-music-load]  

**4° Pratique**
No modo de interação, digite o comando escolhido, de acordo com música.  
![tocando uma música][image-music-play]   
----------
### Atualizações da versão 8.0
Objetivos: Refazer todo o conceito vigente até agora. Foco: Simplicidade	 

- [X] Refazer a lógica da Diana por completo
- [X] Adição da biblioteca PyAnalise	
- [X] Adaptação para a biblioteca PyAnalise	
- [X] Remoção da biblioteca Mipand 
- [X] Remoção de bibliotecas pesadas
- [X] Remoção de instaladores
- [X] Remoção de tela hack - ninguém usava	
- [X] Remoção das imagens hack's - peso desnecessário
- [X] Remoção da tela de avaliação - chato!	
- [X] Remover áudios salvos	
- [X] Remoção das telas de fala_esc e seus respectivos lixos	
- [X] Remoção das telas de esc_rec e seus respectivos lixos	
- [X] Remoção das telas de fala_rec e seus respectivos lixos	
- [X] Criar tela única completa	
- [X] Criar o design das novas telas	
- [X] Integrar reconhecimento de voz	
- [X] Integrar fala	
- [X] Adicionar possibilidade de tocar música	
- [X] Adicionar possibilidade se conectar com o Arduíno	
- [X] Criar menu	
- [X] Remover playsound
- [X] Adicionar Pygame
- [X] Remoção da tela de Menu
- [X] Refatoração completa do código	
- [X] Fazer documentação	
- [X] Atualizar por completo o repositório da Diana. 
- [X] Mudança na forma de análisar os arquivos
- [X] mudança na forma de ler os arquivos
- [X] Remoção de todas as interações. 1.txt, 2.txt,...450.txt
- [X] Adição de novos arquivos, com português revisadoS

[image-arduino-configurar]: https://1.bp.blogspot.com/-E1yNWD-D8To/XTcakPehJDI/AAAAAAAAA14/uuZHfViDvRY2yi8VeYdQN26LdN9A_0eNwCLcBGAs/s1600/porta%2Barduino.png  
[image-arduino-compilar]: https://1.bp.blogspot.com/-qSF25ZLyGTQ/XTcahSoQY3I/AAAAAAAAA1U/Fl9_irvvzckHvKGf4EYr6f-te57uf92bgCLcBGAs/s1600/compilar.png  
[image-def-programar]: https://1.bp.blogspot.com/-4F3n1GwPcO0/XTdNymQqlTI/AAAAAAAAA30/r5j161uXZH0h6ALGdY6vrRgT2nGE1UB2QCLcBGAs/s1600/arduino_code.png  
[image-diana-porta]: https://1.bp.blogspot.com/-Jm5m9ORKsek/XTdMbjgX-4I/AAAAAAAAA3g/ibZTB2zY0jAf_n3ntDI8-b5jujIIO6s5QCLcBGAs/s1600/conectado.png  
[image-diana-chaves]: https://1.bp.blogspot.com/-ts3tQtde1f8/XTdMbtNYxoI/AAAAAAAAA3k/K5lunyjBiMYW41XR1igqvdYa2W4h3eh2ACLcBGAs/s1600/adicionando%2Bcomandos.png  
[image-diana-ativar]: https://1.bp.blogspot.com/-I9ZFSD79nYM/XTdPqAwyymI/AAAAAAAAA4M/8zsrm7PXGL0yHiOkjoIr7BUG6WhQUQ4qACLcBGAs/s320/ligar.png  
[image-music]: https://1.bp.blogspot.com/-KPCOK6yLPmE/XTdCGiLk92I/AAAAAAAAA28/yMGBOCieQ5s5YVU2zaf9uPl76SqDNANwwCLcBGAs/s1600/musica%2Bdentro.png  
[image-music-load]: https://1.bp.blogspot.com/-zUWMDP_ZCBk/XTdCGnWAjhI/AAAAAAAAA3E/sYqPiT7wrXcrU3e18AQ8Ct6WS33bRRDrgCLcBGAs/s1600/tocar%2Bmusicas.png  
[image-music-play]: https://1.bp.blogspot.com/-MPvDSp0zVXc/XTdCGop63qI/AAAAAAAAA3A/Huu4-gBdruI3MPnxOBHnL6eqI2VRV4USQCLcBGAs/s1600/tocando%2Bm%25C3%25BAsica%2Bem%2Bpython.png  
