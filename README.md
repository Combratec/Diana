# Diana 8.0
A Diana 8.0 é um chatbot que aprende, escuta, fala, toca música e pode controlar um Arduíno. Ela é feita em Python, e foi bem testada no [Python3.6](https://www.python.org/downloads/), está é a versão que recomendamos para o uso da Diana.

----------

## Tópicos
- [Interagindo com a Diana](#Interagindo-com-a-Diana)
- [Como a Diana Aprende](#Como-a-Diana-Aprende)
- [Como a Diana Aprende](# Funções especiais)
- [Instalação de bibliotecas](#Instalação-de-bibliotecas)
- [Como ativar o reconhecimento de voz](#Como-ativar-o-reconhecimento-de-voz)
- [Como ativar a fala](#Como-ativar-a-fala)
- [Como controlar um Arduíno?](#Como-controlar-um-Arduíno)
- [Como tocar uma música?](#Como-tocar-uma-música)
- [Atualizações da versão 8.0](#Atualizações-da-versão-8)

----------

### Interagindo com a Diana
Ao executar a Diana, basta fazer uma pergunta, e ela irá responder.  

Você pode [ativar a fala](#Como-ativar-a-fala), assim ela usará a biblioteca [Pygame](https://pypi.org/project/pygame/) e a biblioteca [GTTS](https://pypi.org/project/gTTS/) para gerar e executar uma fala com a resposta.

Você também pode clicar no [reconhecimento de fala](#Como-ativar-o-reconhecimento-de-voz), assim a Diana reconhecerá a sua fala, através da biblioteca [PyAudio](https://pypi.org/project/PyAudio/) e da biblioteca [SpeechRecognition](https://pypi.org/project/SpeechRecognition/).  

É necessário que você instale as bibliotecas manualmente.

----------

### Como a Diana Aprende
A biblioteca [pyanalise](https://github.com/gabrielogregorio/pyanalise) recebe centenas de frases, localizadas em um conjunto de arquivos de conversação, e retorna uma semelhança entre a pergunta feita pelo usuário, e cada frase nos arquivos de conversação.

Estas frases, estão organizados desta forma dentro de cada arquivo:
frase_1;frase_2;frase_3  

Cada arquivo possui algumas frases, de forma que elas estão de alguma forma relacionadas, como se fosse uma conversa. Ou seja, cada arquivo é como se fosse uma conversa diferente. O que a Diana faz, é ler todas as frases, seguindo o exemplo acima, é como se ela pegasse a frase digitada pelo usuário, e comparasse com a frase_1, depois com a frase_2 e depois com a frase_3. Caso a frase_2 tenha uma boa semelhança com a pergunta do usuário, ela responderá com a frase_3

Mas, e se a pergunta for muito semelhante a frase_3?

Bom, não existe a frase_4, nesse caso, a frase mais semelhante a digitada, é a última deste arquivo, então a Diana ativará o modo continuar_assunto, ou seja, ela continuará aquele arquivo específico,dando um retorno para o usuário. A resposta do usuário, será adicionada como frase_4 naquele arquivo especifico.

Caso a melhor semelhança entre o conteudo digitado pelo usuário, em relação a cada uma das frases localizadas em cada arquivo, esteja abaixo da precisão mínima definida em **config>pyanalise**, A Diana ativará o modo criar_assunto. Neste modo, a Diana tentará criar um arquivo com sua pergunta e a sua resposta. Estas são as duas formas básicas da Diana Aprender.

### Funções especiais
Caso a Diana não esteja executando a funcionalidade de continuar ou de criar assunto, ela tentará ver se existe alguma semelhança entre o conteudo que o usuário digitou, e os comandos pré-programados para [tocar a música](#Como-tocar-uma-música) e para [Como controlar um Arduíno?](#Como-controlar-um-Arduíno). Caso exista, e ele seja maior que a precisão mínima definida pelo usuário em **config>pyanalise**, ela responderá de acordo com o que foi programado nestas etapas. Caso não exista, ela simplismente vai continuar a fazer sua análise normal.

----------

### Instalação de bibliotecas
Com o Python já instalado e devidamente pré configurado, é hora de instalar as bibliotecas. Por padrão, a Diana não vem mais com bibliotecas pré instaladas e nem tentar instalar, já que não é muito legal executar comandos de instalação em máquinas desconhecidas.  

Portanto, torna necessário a instalação manual das mesmas. Caso você esteja usando o Windows, terá que abrir o CMD para executar os comandos. Se você tiver em uma distro Linux, em especial o Ubuntu, terá que usar o terminal. Caso você use outra distro, deverá checar em outras fontes, se o seu SO também funciona desta forma.  

É recomendado o uso do [Python3.6](https://www.python.org/downloads/) para a execução da Diana, já que algumas bibliotecas podem estar indisponíveis em versões posteriores e inferiores.  

----------

### Como ativar o reconhecimento de voz
**1° instale a biblioteca PyAudio**  
É altamente recomendado o uso do [Python3.6](https://www.python.org/downloads/). Outras versões, podem ainda não terem o PyAudio compartível, e isso pode ser uma grande dor de cabeça,portando, vamos aos comandos.  
Ele será responsável por acessar o microfone
No Ubuntu  
```console
$ sudo pip3.6 install pyaudio --no-cache 
```  
No Windows  
```console
$ python -m pip install pyaudio --no-cache 
```  

**2° instale a biblioteca SpeechRecognition**  
Ele será responsável por fazer o reconhecimento
No Ubuntu  
```console
$ sudo pip3.6 install speechrecognition --no-cache 
```  
No Windows  
```console
$ python -m pip install speechrecognition --no-cache 
```  

**3° tente usar**  
O reconhecimento de voz na tela de interação, é uma funcionalidade beta, e problemas com o seu microfone, podem acontecer. use-a sabendo que ela pode ser bem limitada, já que ainda não dominamos totalmente a biblioteca!

----------

### Como ativar a fala
**1° Instale o PyGame**  
Ele será responsável por executar os arquivos de áudio
No Ubuntu  
```console
$ sudo pip3.6 install pygame --no-cache 
```  
No Windows  
```console
$ python -m pip3.6 install pygame --no-cache
```  

**2° Instale o GTTS**  
Ele será responsável por gerar os arquivos de áudio
No Ubuntu  
```console
$ sudo pip3.6 install gtts --no-cache  
```  
No Windows  
```console
$ python -m pip3.6 install gtts --no-cache  
```  

----------

### Como controlar um Arduíno
**1° Instale a biblioteca pyfirmata**  
Ela será responsável por permitir o controle remoto do Arduino
No Ubuntu  
```console
$ sudo pip3.6 install pyfirmata --no-cache  
```   
No Windows    
```console
$ python -m pip3.6 install pyfirmata --no-cache  
```  

**2° carregue a biblioteca StandartFirmata**  
Carregue a biblioteca **StandartFirmata** na IDE do seu Arduíno. Caso você esteja usando uma distro Linux, use o sudo para executar a IDE.  
**Arquivo>Exemplos>Firmata>StandartFirmata**  

**3° configure a IDE**  
Selecione a **Placa**, **Processador** e **Porta**, de acordo com o seu Arduíno. Salve a informação em Roxo, precisaremos da porta, em breve. No Windows 10, costuma ser  "COM"+numero, é no Ubuntu costuma ser "/dev/ttyACM"+número. E então, compile o programa.
![musicas][image-arduino-configurar]

**4° Programe**  
Caso tudo esteja funcionando, acesse o arquivo **arduino_code.py** dentro da Diana. As instruções para o Arduíno estão dentro da definição **code_instructions**, a qual ela recebe a conexão, e uma mensagem. Podemos portanto, usar uma lógica bem simples, e escrever um programa que liga ou desliga um LED. A Diana deve estar fechada neste momento.  
![musicas][image-def-programar]

**5° configure a porta**  
Com o seu Arduíno conectado, abra a Diana, use o **sudo** caso você esteja em uma distro Linux, acesse **config > Comandos** e no primeiro campo, digite o endereço da sua porta, obtida no 3° passo. Execute um teste para verificar se está tudo bem.  
![musicas][image-diana-porta]

**6° configure os comandos**  
Com o programa escrito, vamos enviar a mensagem **"ligar"** e **"desligar"**, também vamos programar qual palavra-chave a Diana usará, para enviar cada uma das mensagens. A Diana também usa o **Pyanalise** para tomar as decisões, portanto, qualquer coisa parecida com as palavras chaves, será confundida e poderá enviar a mensagem, isso significa que coisas podem ser acionadas sem que você tenha sido claro sobre isso, cuidado!  
![musicas][image-diana-chaves]  
Aproveite também, e faça os testes, para verificar se o comando funciona ou não!

**7° pratique**  
Digite a palavra-chave na tela de interação, e veja seu Arduíno reagindo!  

----------  

### Como tocar uma música  
**1° instale a biblioteca do Pygame**  
Ela seria a responsável por tocar as músicas
No Ubuntu    
```console
$ sudo pip3.6 install pygame --no-cache 
```   
No Windows  
```console
$ python -m pip install pygame --no-cache  
```   

**2° Mova os arquivos**  
Mova os arquivos .mp3 para a pasta música, dentro da Diana. Alguns arquivos .mp3 podem não funcionar. Usamos músicas do [Youtube /audiolibrary/](https://www.youtube.com/audiolibrary/music) e tudo funcionou, porém, aúdios .mp3 de clipes extraidos do Youtube não apresentaram bons resultados:  
![musicas][image-music]  

**3°Configure a Diana**  
Com a Diana em execução, acesse **config > Tocar música** e adicione as informações pedidas  
![configurando a diana][image-music-load]  

**4° Teste**    
No modo de interação, digite o comando escolhido, de acordo com música e veja se a música toca ou não.   

----------

### Atualizações da versão 8  
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
[image-music]: https://1.bp.blogspot.com/-KPCOK6yLPmE/XTdCGiLk92I/AAAAAAAAA28/yMGBOCieQ5s5YVU2zaf9uPl76SqDNANwwCLcBGAs/s1600/musica%2Bdentro.png  
[image-music-load]: https://1.bp.blogspot.com/-zUWMDP_ZCBk/XTdCGnWAjhI/AAAAAAAAA3E/sYqPiT7wrXcrU3e18AQ8Ct6WS33bRRDrgCLcBGAs/s1600/tocar%2Bmusicas.png  
