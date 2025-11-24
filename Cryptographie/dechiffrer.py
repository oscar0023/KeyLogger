from cryptography.fernet import Fernet

cle = " " #La clé générée 

info_saisies_chiffrer = "info_saisies_chiffrer.txt" 
info_systeme_chiffrer = "info_systeme_chiffrer.txt"
presse_papier_chiffrer = "presse_papier_chiffrer.txt"
video_chiffrer = "video_chiffrer.avi"
photo_chiffrer = "photo_chiffer.jpg"
capture_chiffrer = "capture_chiffrer.png"
enreg_chiffrer = "enreg_chiffrer.wav"

info_saisies_dechiffrer = "info_saisies_dechiffrer.txt" 
info_systeme_dechiffrer = "info_systeme_dechiffrer.txt"
presse_papier_dechiffrer = "presse_papier_dechiffrer.txt"
video_dechiffrer = "video_dechiffrer.avi"
photo_dechiffrer = "photo_dechiffer.jpg"
capture_dechiffrer = "capture_dechiffrer.png"
enreg_dechiffrer = "enreg_dechiffrer.wav"


fichier_chiffrer = [info_saisies_chiffrer, info_systeme_chiffrer, presse_papier_chiffrer, photo_chiffrer, enreg_chiffrer, video_chiffrer, capture_chiffrer]
fichier_dechiffrer = [info_saisies_chiffrer, info_systeme_dechiffrer, presse_papier_dechiffrer, photo_dechiffrer, enreg_dechiffrer, video_dechiffrer, capture_dechiffrer]

j = 0
for elt in fichier_chiffrer:

    with open(fichier_chiffrer[j], 'rb') as f:
        data = f.read()

    fernet = Fernet(cle)
    dechiffrer = fernet.decrypt(data)

    with open(fichier_dechiffrer[j], 'ab') as f:
        f.write(dechiffrer)

    j += 1


