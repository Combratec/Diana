from  definicoes import basic
class comand_arduino():
    def start_connection(porta):
        basic.log('arduino_code.start_connection')
        from pyfirmata import Arduino,util
        global placa
        placa = Arduino(porta)
        first_conection_arduino = 1
        return placa

    def code_instructions(placa,mensagem):
        basic.log('arduino_code.code_instructions')
        if mensagem == 'ligar':
            placa.digital[12].write(1)
        elif mensagem == 'desligar':
            placa.digital[12].write(0)

    def message(placa,mensagem):
        basic.log('arduino_code.message')
        comand_arduino.code_instructions(placa,mensagem)