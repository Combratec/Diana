class comand_arduino():
    def start_connection():
        from pyfirmata import Arduino,util
        import time
        global placa
        global first_conection_arduino
        placa = Arduino('COM5')
        first_conection_arduino = 1

    def code_instructions(mensagem):
        if mensagem == 'ligar':
            placa.digital[12].write(1)
        elif mensagem == 'desligar':
            placa.digital[12].write(0)

    def message(mensagem,reboot):
        if reboot == 'sim':
            comand_arduino.start_connection()
        comand_arduino.code_instructions(mensagem)