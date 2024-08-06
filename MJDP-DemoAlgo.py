import numpy as np
import librosa
import os
import json
from moviepy.editor import VideoFileClip

# Fonction pour obtenir les chemins des fichiers à partir des DIDs
def get_filenames():
    # Récupère les DIDs depuis les variables d'environnement
    dids = os.getenv('DIDS')

    # Vérifie si les DIDs sont présents
    if not dids:
        print("No DIDs found in environment. Aborting.")
        return []

    # Charge les DIDs au format JSON
    dids = json.loads(dids)

    filenames = []
    for did in dids:
        # Construit le chemin du fichier à partir du DID
        filename = os.path.join(f'/data/inputs/{did}', '0')
        print(f"Reading asset file {filename}.")
        filenames.append(filename)

    return filenames

# Fonction pour extraire l'audio d'un fichier vidéo
def extract_audio(video_path, output_audio_path):
    # Utilise moviepy pour charger la vidéo
    video = VideoFileClip(video_path)
    # Extrait l'audio et le sauvegarde dans un fichier temporaire
    video.audio.write_audiofile(output_audio_path)

# Fonction pour calculer l'énergie du signal audio
def calculer_energie(audio_path):
    # Charge le fichier audio avec librosa
    y, sr = librosa.load(audio_path)
    
    # Calcule l'énergie comme la somme des carrés des amplitudes divisé par le nombre d'échantillons
    energie = np.sum(y**2) / len(y)
    
    return energie

# Fonction principale orchestrant le processus
def main():
    # Chemin du fichier de sortie pour les résultats
    output_path = '/data/outputs/energy_results.txt'
    # Chemin temporaire pour sauvegarder l'audio extrait
    temp_audio_path = '/data/outputs/temp_audio.wav'
    # Obtient les chemins des fichiers vidéo
    filenames = get_filenames()

    if not filenames:
        print("No files to process.")
        return

    # Ouvre le fichier de sortie en mode écriture
    with open(output_path, 'w') as output_file:
        for video_path in filenames:
            # Extrait l'audio du fichier vidéo
            extract_audio(video_path, temp_audio_path)
            # Calcule l'énergie de l'audio extrait
            energie = calculer_energie(temp_audio_path)
            # Écrit le résultat dans le fichier de sortie
            output_file.write(f"L'énergie du morceau {video_path} est : {energie:.6f}\n")
            print(f"L'énergie du morceau {video_path} est : {energie:.6f}")

# Point d'entrée du script
if __name__ == "__main__":
    main()
