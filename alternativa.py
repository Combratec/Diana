from  definicoes import basic
def pergunta(entrada):
    basic.log('alternativa')
    if "você conhece" in entrada.lower():
        return 'Não conheço, você conhece?'
    
    elif "você sabia" in entrada.lower():
        return 'Eu não sabia, conte-me mais!'
    
    elif "você já" in entrada.lower():
        return 'Acho que não, conte-me mais!'

    elif "você curte" in entrada.lower():
        return 'Me diga você, você curte?'
    
    elif "você gosta de" in entrada.lower():
        return 'Não sei, você gosta?'
    
    elif "o que é" in entrada.lower():
        return 'Eu não sei, o que você sabe a respeito!'
    
    elif "quando isso" in entrada.lower():
        return 'Primeiro, você sabe?'
    
    elif "você pode me recomendar" in entrada.lower():
        return 'Me recomende um primeiro, por favor!'
    
    elif "como se diz" in entrada.lower():
        return 'Por que você não me diz? '
    
    elif "você estava" in entrada.lower():
        return 'Acho que não! E você?'
    else:
        return 'O que eu poderia responder?'