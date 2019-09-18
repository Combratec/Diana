from tkinter import SUNKEN
from tkinter import FLAT
from tkinter import GROOVE
from tkinter import RAISED

class design_principal():
    def config_main_btns(): 
        return {
            'highlightbackground':'blue',
            'border':0,
            'bg':'blue',
            'relief':SUNKEN,
            'activebackground':'blue'
            ,'highlightthickness':0}

    def config_main_entr(): 
        return {
            'fg':'white',
            'bg':'blue',
            'highlightbackground':'white',
            'highlightcolor':'white',
            'font':("",14)}

    def config_main_text(): 
        return {
            'bg':'white',
            'fg':'black',
            'highlightthickness':0,
            'border':0,
            'font':("consolas", 12),
            'undo':True,
            'wrap':'word'}

    def config_main_titl(): 
        return {
            'bg':'blue',
            'fg':'white',
            'font':("Arial",20,'bold')}

class design_opcoes():
    def config_options_btns(): 
        return {
            'relief':GROOVE,
            'highlightthickness':0,
            'border':0,
            'bg':'white'}

    def config_options_txts(): 
        return {
            'font':("Sans",20,'bold'),
            'bg':'white'}

    def config_options_icon(): 
        return {
            'bg':'white'}

    def config_options_opti(): 
        return {
            'font':("Sans",17,'bold'),
            'bg':'blue',
            'fg':'white'}

    def config_options_retu(): 
        return {
            'relief':GROOVE,
            'highlightthickness':0,
            'border':0,
            'bg':'blue',
            'activebackground':'blue'}

class design_historico():
    def config_historic_tops():
        return {
            'background':'#00cccb',
            'highlightbackground':'#00cccb',
            'foreground':'#222',
            'font':("",14)}

    def config_historic_titl():
        return {
            'background':'#1976d3',
            'font':("Sans",17,'bold'),
            'highlightbackground':"#1976d3",
            'foreground':'#fff'}

    def config_historic_text():
        return {
            'background':'white',
            'highlightbackground':'#fff',
            'border':2,
            'foreground':'black',
            'font':("consolas", 12),
            'undo':True,
            'wrap':'word'}

    def config_historic_scrl():
        return {
            'background':'white',
            'activebackground':'#f9f9f9',
            'highlightbackground':'white',
            'highlightcolor':'white'}

    def config_historic_retu():
        return {
            'background':'#009899',
            'foreground':'white',
            'activebackground':'#009899',
            'activeforeground':'#fff',
            'highlightbackground':'#009899',
            'relief':FLAT,
            'font':("Arial",12)}

    def config_historic_clea():
        return {
            'background':'#fe0000',
            'foreground':'white',
            'activebackground':'#fe0000',
            'activeforeground':'#fff',
            'highlightbackground':'#fe0000',
            'relief':FLAT,
            'font':("Arial",12)}

class design_pyanalise():
    def config_pyanalise_icon(): 
        return {
            'font':("Sans",17,'bold'),
            'bg':'DarkGreen',
            'activebackground':'DarkGreen',
            'relief':GROOVE,
            'highlightthickness':0,
            'border':0}

    def config_pyanalise_fras(): 
        return {
            'font':("Sans",10,'bold'),
            'bg':'white',
            'fg':'black'}

    def config_pyanalise_titl(): 
        return {
            'font':("Sans",17,'bold'),
            'bg':'DarkGreen',
            'fg':'white'}

    def config_pyanalise_desc(): 
        return {
            'font':("Sans",12,'bold'),
            'bg':'green',
            'fg':'white'}

    def config_pyanalise_scal(): 
        return {
            'highlightbackground':'white',
            'troughcolor':'green',
            'bd':1,
            'bg':'green',
            'fg':'white',
            'highlightthickness':0}

    def config_pyanalise_comp(): 
        return {
            'relief':GROOVE,
            'border':3,
            'font':('Sans',15,'bold')}

    def config_pyanalise_resu(): 
        return {
            'font':('Sans',40,'bold'),
            'fg':'blue',
            'bg':'#eee'}


class design_musica():
    def config_music_retu(): 
        return {
            'relief':GROOVE,
            'highlightthickness':0,
            'border':0,
            'bg':'blue',
            'activebackground':'blue'}

    def config_music_btns(): 
        return {
            'relief':GROOVE,
            'highlightthickness':1,
            'border':0,
            'bg':'white',
            'activebackground':'white'}

    def config_music_desc(): 
        return {
            'font':("Sans",10,'bold'),
            'bg':'white',
            'fg':'#777'}

    def config_music_toca(): 
        return {
            'font':("Sans",17,'bold'),
            'bg':'blue', 
            'fg':'white'}

    def config_music_spac(): 
        return {
            'bg':'white'}

    def config_music_entr(): 
        return {
            'relief':GROOVE,
            'border':2}

    def config_music_fram():
    	return {
    		'bg':'white',
    		'padx':6}



class design_comando():
    def config_command_retu(): 
        return {
            'relief':GROOVE,
            'highlightthickness':0,
            'border':0,
            'bg':'blue',
            'activebackground':'blue'}

    def config_command_addi(): 
        return {
            'relief':GROOVE,
            'highlightthickness':0,
            'border':0,
            'bg':'white',
            'activebackground':'white'}

    def config_command_expl(): 
        return {
            'font':("Sans",10,'bold'),
            'bg':'white',
            'fg':'black'}

    def config_command_titl(): 
        return {
            'font':("Sans",17,'bold'),
            'bg':'blue',
            'fg':'white'}

    def config_command_help(): 
        return {
            'relief':RAISED,
            'border':4,
            'padx':5,
            'pady':5,
            'bg':'purple',
            'fg':'white',
            'font':('Sans',13,'bold'),
            'activebackground':'purple',
            'activeforeground':'white'}

    def config_command_desc(): 
        return {
            'bg':'white'}

    def config_command_seri(): 
        return {
            'state':'normal',
            'relief':GROOVE,
            'border':2}

    def config_command_test(): 
        return {
            'highlightthickness':0,
            'bg':'white',
            'activebackground':'white',
            'relief':RAISED,
            'border':1,
            'padx':1}

    def config_command_entr(): 
        return {
            'relief':GROOVE,
            'border':2}
