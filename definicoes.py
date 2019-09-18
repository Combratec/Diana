#from tkinter import *
class comandar():
    def read_comands_in_file():
        basic.log('definicoes.read_comands_in_file')
        lista = []
        try:
            b = basic.abrir_arquivo('comandos/arquivo')
        except Exception as e:
            try:
                a = open('comandos/arquivo','w', encoding="utf8")
                a.close()
            except Exception as e2:
                basic.log('Impossivel criar arquivo!'+str(e2))
                return lista
        else:
            if b != '':
                c = b.split('\n')
                for x in c:
                    dic = {}
                    try:
                        d = x.split(':')
                        dic[d[0]] = d[1]
                        dic[d[2]] = d[3]
                    except:
                        pass
                    else:
                        lista.append(dic)
            return lista

    def remover(item_remove):
        dic = comandar.read_comands_in_file()
        dic.pop(item_remove)
        comandar.sobrescrever(dic)

    def adicionar(item_dic_novo):
        dic = comandar.read_comands_in_file()
        dic.append(item_dic_novo)
        comandar.sobrescrever(dic)

    def sobrescrever(dic_novo):
        string = ''
        for x in dic_novo:
            try:
                string = string + 'enviar:' + str(x['enviar']) + ':' + 'comando:' + str(x['comando']) +'\n' 
            except:
                pass
        a = open('comandos/arquivo','w', encoding="utf8")
        a.write(string)
        a.close()

class musica():
    def read_musics_in_file():
        basic.log('definicoes.read_musics_in_file')
        permitido = 'nao'
        b = ''
        try:
            a = open('musica/arquivo','r', encoding="utf8")
            b = str(a.read())
            a.close()
        except Exception as e:
            try:
                a = open('musica/arquivo','w', encoding="utf8")
                a.close()
            except:
                pass
            else:
                permitido = 'sim'
        else:
            permitido = 'sim'

        lista = []
        if permitido == 'sim' and b != '':
            c = b.split('\n')
            for x in c:
                dic = {}
                try:
                    d = x.split(':')
                    dic[d[0]] = d[1]
                    dic[d[2]] = d[3]
                except:
                    pass
                else:
                    lista.append(dic)
        return lista

    def remover(item_remove):
        dic = musica.read_musics_in_file()
        dic.pop(item_remove)
        musica.sobrescrever(dic)

    def adicionar(item_dic_novo):
        dic = musica.read_musics_in_file()
        dic.append(item_dic_novo)
        musica.sobrescrever(dic)

    def sobrescrever(dic_novo):
        string = ''
        for x in dic_novo:
            try:
                string = string + 'musica:' + str(x['musica']) + ':' + 'comando:' + str(x['comando']) +'\n' 
            except:
                pass
        a = open('musica/arquivo','w', encoding="utf8")
        a.write(string)
        a.close()

class basic():
    def abrir_arquivo(link):
        arquivo = open (link,'r', encoding="utf8")
        file = str(arquivo.read())
        arquivo.close()
        return file

    # Caso o usuário pergunte que horas são
    def retornar_time():
        from datetime import datetime
        horas = datetime.now()
        return {'day':horas.day,'month':horas.month,'hour':horas.hour,'minute':horas.minute,'year':horas.year}

    # HISTÓRICO
    def load_historic():
        file = basic.abrir_arquivo('analise/histórico.txt')
        return file
    def clear_historic():
        a = open('analise/histórico.txt','w', encoding="utf8")
        a.write('')
        a.close()
    def add_historic(interacao):
        a = open('analise/histórico.txt','a', encoding="utf8")
        a.write(interacao)
        a.close()

    # CONFIGS
    def open_file_configs():
        lista = []
        file = basic.abrir_arquivo('config.txt')
        b = file.split('\n')
        for x in b:
            lista.append(x.split('='))
        return lista

    def ler_tenho_que_falar():
        lista = basic.open_file_configs()
        return lista[1][1]

    def atualizar_tenho_que_falar(novo_valor):
        lista = basic.open_file_configs()
        lista[1][1] = str(novo_valor)

        string = ''
        for x in range(len(lista)):
            if len(lista[x])>1:
                string = string + str(lista[x][0]) + '=' + str(lista[x][1]) + '\n'
        
        a = open('config.txt','w')
        a.write(string)
        a.close()
        return string

    # Serial Comands
    def ler_link_serial():
        lista = basic.open_file_configs()
        return lista[2][1]
    def atualizar_link_serial(novo_valor):
        lista = basic.open_file_configs()
        lista[2][1] = str(novo_valor)
        string = ''
        for x in range(len(lista)):
            if len(lista[x])>1:
                string = string + str(lista[x][0]) + '=' + str(lista[x][1]) + '\n'
        
        a = open('config.txt','w')
        a.write(string)
        a.close()
        return string

    # PYANALISE
    def ler_pyanalise():
        lista = basic.open_file_configs()
        return int(lista[0][1])

    def atualizar_pyanalise(novo_valor):
        lista = basic.open_file_configs()
        lista[0][1] = str(novo_valor)

        string = ''
        for x in range(len(lista)):
            if len(lista[x])>1:
                string = string + str(lista[x][0]) + '=' + str(lista[x][1]) + '\n'
        
        a = open('config.txt','w')
        a.write(string)
        a.close()
        return string
    # Outros
    def log(message):
        print(message)
    
    def abrir_site(link):
        import webbrowser
        webbrowser.open(link)

    # Comands
    def make_file_responses_comands():
        dic = comandar.read_comands_in_file()
        string = ''
        for x in dic:
            string = string + x['comando'] + '\n'
        a = open('arquivos/comandos/arduino.txt','w',encoding='utf8')
        a.write(string)
        a.close()

    # Musics
    def make_file_responses_music():
        dic = musica.read_musics_in_file()
        string = ''
        for x in dic:
            string = string + x['comando'] + '\n'
        a = open('arquivos/comandos/musica.txt','w',encoding='utf8')
        a.write(string)
        a.close()
