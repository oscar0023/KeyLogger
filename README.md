## 🎯 Description
  Ce projet Python permet de simuler le fonctionnement d'un systeme de surveillance.
  Développé dans le cadre de mon apprentissage, il démontre comment avec un simple programme, une personne malveillante peux collecter assez d'informations sur nous et sur notre machine.

## ⚡ Fonctionnalités
  - **Keylogger** : Enregistrement des frappes clavier
  - **Capture système** : Récupération des informations hardware et software
  - **Presse-papiers** : Monitoring du contenu copié
  - **Médias** : 
    - Capture d'écran
    - Enregistrement audio (60 secondes)
    - Capture photo/vidéo via webcam
  - **Sécurité** : 
    - Chiffrement AES via Fernet
    - Envoi sécurisé par email

## 🛠️ Technologies utilisées
  - `cryptography.fernet` - Chiffrement des données
  - `pynput` - Monitoring des entrées clavier
  - `OpenCV` - Capture vidéo et photo
  - `PIL` - Capture d'écran
  - `sounddevice` - Enregistrement audio
  - `smtplib` - Envoi d'emails

## ⚠️ Attention
  **Ce projet est strictement éducatif**. Son utilisation doit se limiter à de l'**apprentissage**

## 🚀 Installation et utilisation
````bash
  # Installation des dépendances
  pip install -r requirements.txt
  
  # Génération de la clé de chiffrement
  python genere_cle.py
  
  # Lancement du monitoring
  python keylogger.py
