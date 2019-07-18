from playsound import playsound
import threading
from time import sleep
def tocar_musica():
	playsound('musica/Atlanta.mp3')

def iniciar_thread():
	th = threading.Thread(target=tocar_musica,daemon=True)
	th._stop_flag = True

	th.start()
	i = input('pausar')
	#th._stop_flag = True
	#th.daemon=False
	print(th)
	#th.daemon.stop()

#_stop_flag