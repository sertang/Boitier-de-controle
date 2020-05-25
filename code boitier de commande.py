#importation des diffrentes librairies
from microbit import * 
import microbit
import radio

#mise a 0 de la variable correction_time
correction_time = 0

#définition des pins 0 et 1 commes entrées en PULLUP (reliés a une résistance)
pin0.set_pull(pin0.PULL_UP)
pin1.set_pull(pin1.PULL_UP)

#démarage du module radiofréquence
radio.on()

#boucle infinie
while True:
    liste = [0,0,0,0,0,0,0,0,0,0] #définition d'une liste avec 10 valeurs dedans toutes égales a 0
    #boucles while qui s'éxécute 10 fois
    i = 0
    while i <= 9:
        valx = microbit.accelerometer.get_y() #lecture de la valeur de l'accelerometre sur l'axe y (valeur entre -1023 et +1023 en fonction de l'accélération)
        liste[i] = valx
        i += 1
        sleep(5)#intervalles entres les boucles de 5 millisecondes
    x = (liste[0]+liste[1]+liste[2]+liste[3]+liste[4]+liste[5]+liste[6]+liste[7]+liste[8]+liste[9])/10 #moyenne des 10 valeurs de la liste 1
    sleep(300) #delais de 300 millisecondes
    liste2 = [0,0,0,0,0,0,0,0,0,0] #définition d'une liste avec 10 valeurs dedans toutes égales a 0*
    #boucles while qui s'éxécute 10 fois
    j = 0
    while j <= 9:
        valx = microbit.accelerometer.get_y() #lecture de la valeur de l'accelerometre sur l'axe y (valeur entre -1023 et +1023 en fonction de l'accélération)
        liste2[j] = valx
        j += 1
        sleep(5)#intervalles entres les boucles de 5 millisecondes
    y = (liste2[0]+liste2[1]+liste2[2]+liste2[3]+liste2[4]+liste2[5]+liste2[6]+liste2[7]+liste2[8]+liste2[9])/10 #moyenne des 10 valeurs de la liste 2
    
    if y < x -100: # si la moyenne 2 est plus petite que la moyenne 1 - 100 alors... Détéction du freinage
        radio.send("S") # envois du charactere "s" par radio
        correction_time = running_time() #récuperation de la valeur actuelle de la fonction running_time()

    if y > x+200:# si la moyenne 2 est plus grande que la moyenne 1 + 200 alors... Détéction de l'accélération
        calc_time = running_time() - correction_time #calcul de la difference entre la valeur actuelle de running_time() et correction_time permet de calculer le temp écoulé entre l'execution du freinage et la détéction de l'accélération
        if calc_time > 500: #si calc_time est superieur a 500 alors ... permet de verifier qu'il y a eu 500 millisecondes entre la detection du freinage et la detection de l'accélération , empeche l'effet rebond de l'accelerometre
            radio.send("A")# envois du charactere "a" par radio
    
    b1 = pin0.read_digital()#lecture de l'état du pin 0 (pullup donc valeur inversé)
    b2 = pin1.read_digital()#lecture de l'état du pin 1 (pullup donc valeur inversé)
    
    if b1 == 0:#si b1 est égale a 0 alors...
        radio.send("G")# envois du charactere "g" par radio
        
    if b2 == 0:#si b2 est égale a 0 alors...
        radio.send("D")# envois du charactere "d" par radio