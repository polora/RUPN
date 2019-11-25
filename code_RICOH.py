### PREREQUIS importants :
    # python installé
    # tkinter installé (apt-get install python3-tk)
    # créer le répertoire /etc/ppd/cups/init 
    # chmod 777 /etc/cups/ppd/*
    # copier le script Python dans /etc/opt et changer les droits root:root
    # créer un bash ou un lanceur contenant (python3 /opt/code_RICOH.py)
    
    # dans le code ci-dessous le fichier de configuration de notre imprimante se nomme copieur_SPD.ppd, le renommer si nécessaire

import os
from tkinter import *
from tkinter.messagebox import * # boîte de dialogue

def modifFichierPPD(usercode):

    # définition des chemins dans des variables
    fsave = "/etc/cups/ppd/copieur_SDP.ppd_save"
    fppd = "/etc/cups/ppd/copieur_SDP.ppd"
    ftemp = "/etc/cups/ppd/init/ppdtmp"

    if os.path.isfile(fsave): # on vérifie le ppd_save existe
        os.system("cp {} {}".format(fsave,fppd)) # rénitialisation du ppd
        os.system("cp {} {}".format(fsave,ftemp)) # copie du ppd_save en ppdtmp

        # ouverture du fichier ppd.tmp en lecture, copie du contenu dans une variable
        # chaine en remplaçant le code du photocopieur initialisé à 0000 par le code
        # utilisateur
        fichier_source = open(ftemp,"r")
        remplacement = "*DefaultUserCode: "
        remplacement+= usercode
        chaine=fichier_source.read().replace("%*DefaultUserCode: 0000",remplacement)
        fichier_source.close() # fermeture du fichier

        # ouverture du fichier ppd.tmp en écriture en effaçant tout le contenu et copie
        # de la chaine à l'intérieur
        fichier_cible = open(ftemp,"w")
        fichier_cible.write(chaine)
        fichier_cible.close() # fermeture

        os.system("cp {} {}".format(ftemp,fppd)) # copie du ppd.tmp vers .ppd

    else:
        showwarning('Résultat','Erreur système !')

def limiteSaisie(saisieCode):
    # combinée avec trace, efface la saisie dès qu'on dépasse 4 caractères
    if len(saisieCode.get()) > 4:
        saisieCode.set("")

def verifCode(event):
    modifFichierPPD(saisieCode.get())
    fenetreDialogue.destroy()

# Création fenêtre principale
fenetreDialogue = Tk()
fenetreDialogue.title('Saisie code imprimante')

# Label info utilisateur
Label1 = Label(fenetreDialogue, text = 'Saisir votre code et valider en appuyant sur la touche Entrée').grid(row=0,columnspan=2,padx=30,pady=10)
# Label saisie de code
Label2 = Label(fenetreDialogue,text = "Code").grid(row=1,column=0,padx=30,pady=10)

# Création d'un widget Entry (champ de saisie)
saisieCode = StringVar(fenetreDialogue)
saisieCode.trace("w", lambda *args: limiteSaisie(saisieCode))

Champ = Entry(fenetreDialogue, textvariable = saisieCode, width=10)
Champ.focus_set()
Champ.grid(row=1,column=1)
Champ.bind("<Return>",verifCode) # association de la touche Entrée à verifCode

fenetreDialogue.mainloop()



