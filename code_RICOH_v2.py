### PREREQUIS importants :
    # le répertoire /etc/ppd/cups/init est créé sur la machine
    # l'utilisateur a les droits sur le répertoire /etc/cups/ppd ?

### problème sous Debian : au redémarrage, pas possible d'écrire
# les droits sur le répertoire /etc/cups/ppd sont réinitialisés

import os
from tkinter import *
from tkinter.messagebox import * # boîte de dialogue

liste_codes = ["1000","1100","1200","1300"] # à compléter

def modifFichierPPD(usercode):

    # définition des chemins dans des variables
    fsave = "/etc/cups/ppd/RICOH_4504.ppd_save"
    fppd = "/etc/cups/ppd/RICOH_4504.ppd"
    ftemp = "/etc/cups/ppd/init/ppdtmp"

    if os.path.isfile(fsave): # on vérifie le ppd_save existe
        os.system("cp {} {}".format(fsave,fppd)) # utile ???
        os.system("cp {} {}".format(fsave,ftemp)) # copie du ppd_save en ppdtmp

        # ouverture du fichier ppd.tmp en lecture, copie du contenu dans une variable
        # chaine en remplaçant le code du photocopieur initialisé à 0000 par le code
        # utilisateur
        fichier_source = open(ftemp,"r")
        chaine=fichier_source.read().replace("0000",usercode)
        fichier_source.close() # fermeture du fichier

        # ouverture du fichier ppd.tmp en écriture en effaçant tout le contenu et copie
        # de la chaine à l'intérieur
        fichier_cible = open(ftemp,"w")
        fichier_cible.write(chaine)
        fichier_cible.close() # fermeture

        os.system("mv {} {}".format(ftemp,fppd)) # copie du ppd.tmp vers .ppd

        # contrôle - mode développement - A SUPPRIMER ds version prod
        fichier = open(fppd,"r")
        for ligne in fichier:
            if "*DefaultUserCode" in ligne:
                print(ligne)
        fichier.close()
    else:
        showwarning('Résultat','Erreur système !')

def limiteSaisie(saisieCode):
    # combinée avec trace, efface la saisie dès qu'on dépasse 4 caractères
    if len(saisieCode.get()) > 4:
        saisieCode.set("")

def verifCode(event):
    if saisieCode.get() in liste_codes:
        modifFichierPPD(saisieCode.get())
        fenetreDialogue.destroy() # si code correct, on ferme la fenêtre dialogue

    else:
        # le mot de passe est incorrect : on affiche une boîte de dialogue
        showwarning('Résultat','Code incorrect.\nVeuillez recommencer !')
        saisieCode.set("") #réinitialise le mot de passe

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

Champ = Entry(fenetreDialogue, textvariable = saisieCode,show="*",width=10)
Champ.focus_set()
Champ.grid(row=1,column=1)
Champ.bind("<Return>",verifCode)

fenetreDialogue.mainloop()



