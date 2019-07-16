class comand_arduino():
    def start_connection(porta):
        from pyfirmata import Arduino,util
        import time
        global placa
        global first_conection_arduino
        placa = Arduino(porta)
        first_conection_arduino = 1
        return placa

    def code_instructions(placa,mensagem):
        if mensagem == 'ligar':
            placa.digital[12].write(1)
        elif mensagem == 'desligar':
            placa.digital[12].write(0)

    def message(placa,porta,mensagem,reboot):
        if reboot == 'sim':
            comand_arduino.start_connection(porta)
        comand_arduino.code_instructions(placa,mensagem)