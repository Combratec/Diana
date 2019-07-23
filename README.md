# Diana Tecnologia
Chatbot com um método de aprendizado.

[![Build Status][image-arduino-configurar]][]  
# Bibliotecas

## Como controlar um Arduino?
#### 1° passo
Instale a biblioteca pyfirmata
No Ubuntu  
```
sudo pip3.6 install pyfirmata --no-cache  
``` 

No Windows  
```
pip3.6 install pyfirmata --no-cache  
```

#### 2° passo
Carregue a biblioteca **StandartFirmata** na IDE do Arduino. Caso você esteja no Linux, use o sudo para executar a IDE. 
**Arquivo>Exemplos>Firmata>StandartFirmata**

#### 3° passo
Selecione a **Placa**, **Processador** e **Porta**, de acordo com o seu arduino. Salve a informação em Roxo, precisaremos da porta, em breve. No Windows 10, costuma ser  "COM"+numero, é no Ubuntu costuma ser "/dev/ttyACM"+número. **Fique atento a este detalhe.**
[![musicas][image-arduino-configurar]]

#### 4° passo
Agora, compile o programa para o Arduino
[musicas][image-arduino-compilar]

#### 5° passo
Caso tudo esteja funcionando, acesse o arquivo **arduino_code.py** dentro da Diana. As instruções para o Arduino estão dentro da definição **code_instructions**, a qual ela recebe a conexão, e uma mensagem. Podemos portanto, usar uma lógica bem simples, e escrever um programa que liga ou desliga um LED. A Diana deve estar fechada neste momento.
![musicas][image-def-programar]

#### 6° passo
Com o seu Arduino conectado, abra a Diana, use o **sudo** caso você esteja em uma distro linux, acesse **config > Comandos** e no primeiro campo, digite o endereço da sua porta, obitida no 3° passo. 
![musicas][image-diana-porta]

#### 7° passo
Com o programa escrito, vamos enviar a mensagem **"ligar"** e **"desligar"**, também vamos programar qual palavra chave a Diana irá usar, para enviar cada uma das mensagens. A Diana também usa o **Pyanalise** para tomar as decisões, portanto, qualquer coisa parecida com as palavras chaves, será confundida e poderá enviar a mensagem.
![musicas][image-diana-chaves]
Aproveite também, e faça os testes, para verificar se o comando funciona ou não!

#### 8° passo
Digite a palavra chave na tela de interação, e veja seu Arduino reagindo!
![musicas][image-diana-ativar]
- - - 

## Como tocar uma música? 
#### 1° passo
Instale a biblioteca do Pygame
No Ubuntu  
```
sudo pip3.6 install pygame --no-cache
```  

No Windows  
```
python -m pip install pygame --no-cache
```  
#### 2° passo 
Mova os arquivos .mp3 para a pasta música, dentro da Diana:
![musicas][image-music]

#### 3° passo 
Com a Diana em execução, acesse **config > Tocar música** e adicione as informações pedidas
![configurando a diana][image-music-load]

#### 4° passo 
No modo de interação, digite o comando escolhido, de acordo com música.
![tocando uma música][image-music-play] 
- - -

# Versão 8.0  - Atualizações
Objetivos: Refazer todo o conceito vigente até agora. Foco: Simplicidade	

- [X] Refazer a lógica da Diana por completo - Lógica novinha em folha	
- [X] Adição da biblioteca PyAnalise	
- [X] Adaptação para a biblioteca PyAnalise	
- [X] Remoção da biblioteca Mipand 	
- [X] Remoção de bibliotecas pesadas 	
- [X] Remoção de instaladores - Não quero executar dezenas de comandos em uma máquina desconhecida!	
- [X] Remoção de tela hack - ninguém usava	
- [X] Remoção das imanges hack - peso desnecessário	
- [X] Remoção da tela de avaliação - chato!	
- [X] Remover audios salvos	

- - - 	

- [X] Remoção das telas de fala_esc e seus respectivos lixos	
- [X] Remoção das telas de esc_rec e seus respectivos lixos	
- [X] Remoção das telas de fala_rec e seus respectivos lixos	
- [X] Criar tela unica completa	
- [X] Criar o design das novas telas	
- [X] Integrar reconhecimento de voz	
- [X] Integrar fala	
- [X] Adicionar possibilidade de tocar música	
- [X] Adicionar possibilidade se conectar com o arduino	
- [X] Criar novo menu	
- [X] Remover playsound
- [X] Adicionar Pygame
- [X] Remoção da tela de Menu - Vamos direto ao ponto, telas são legais, mas o foco sempre foi conversar com a voz!	
- [X] Remoção da tela de histórico - Eu gosto, mas não vejo muita utilidade agora	

- - - 	

- [X] Refatoração completa do código	
- [ ] Fazer documentação	
- [ ] Atualizar por completo o respositório da Diana. Versões offline por enquanto!
[image-arduino-configurar]: https://1.bp.blogspot.com/-E1yNWD-D8To/XTcakPehJDI/AAAAAAAAA14/uuZHfViDvRY2yi8VeYdQN26LdN9A_0eNwCLcBGAs/s1600/porta%2Barduino.png  
[image-arduino-compilar]: https://1.bp.blogspot.com/-qSF25ZLyGTQ/XTcahSoQY3I/AAAAAAAAA1U/Fl9_irvvzckHvKGf4EYr6f-te57uf92bgCLcBGAs/s1600/compilar.png  
[image-def-programar]: https://1.bp.blogspot.com/-4F3n1GwPcO0/XTdNymQqlTI/AAAAAAAAA30/r5j161uXZH0h6ALGdY6vrRgT2nGE1UB2QCLcBGAs/s1600/arduino_code.png  
[image-diana-porta]: https://1.bp.blogspot.com/-Jm5m9ORKsek/XTdMbjgX-4I/AAAAAAAAA3g/ibZTB2zY0jAf_n3ntDI8-b5jujIIO6s5QCLcBGAs/s1600/conectado.png  
[image-diana-chaves]: https://1.bp.blogspot.com/-ts3tQtde1f8/XTdMbtNYxoI/AAAAAAAAA3k/K5lunyjBiMYW41XR1igqvdYa2W4h3eh2ACLcBGAs/s1600/adicionando%2Bcomandos.png  
[image-diana-ativar]: https://1.bp.blogspot.com/-I9ZFSD79nYM/XTdPqAwyymI/AAAAAAAAA4M/8zsrm7PXGL0yHiOkjoIr7BUG6WhQUQ4qACLcBGAs/s320/ligar.png  
[image-music]: https://1.bp.blogspot.com/-KPCOK6yLPmE/XTdCGiLk92I/AAAAAAAAA28/yMGBOCieQ5s5YVU2zaf9uPl76SqDNANwwCLcBGAs/s1600/musica%2Bdentro.png  
[image-music-load]: https://1.bp.blogspot.com/-zUWMDP_ZCBk/XTdCGnWAjhI/AAAAAAAAA3E/sYqPiT7wrXcrU3e18AQ8Ct6WS33bRRDrgCLcBGAs/s1600/tocar%2Bmusicas.png  
[image-music-play]: https://1.bp.blogspot.com/-MPvDSp0zVXc/XTdCGop63qI/AAAAAAAAA3A/Huu4-gBdruI3MPnxOBHnL6eqI2VRV4USQCLcBGAs/s1600/tocando%2Bm%25C3%25BAsica%2Bem%2Bpython.png  
