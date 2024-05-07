""" Opérations sur les fichiers sources
"""

import os
from datetime import datetime


def lister_fichiers(dossier: str) -> list:
    """Renvoie la liste des fichiers .tcx du dossier sources"""
    liste_fichiers = os.listdir(dossier)
    liste_tcx = [fichier for fichier in liste_fichiers if fichier.endswith(".tcx")]
    return liste_tcx


def choix_fichier(liste_tcx: list) -> str:
    """Propose à l'utilisateur de choisir un fichier dans la liste des fichiers .tcx"""
    print("Choisissez un fichier dans la liste suivante :")
    for i, fichier in enumerate(liste_tcx):
        print(f"{i} : {fichier}")
    choix = int_input("Votre choix : ")
    return liste_tcx[choix]


def int_input(texte: str) -> int:
    print(texte, end="")
    choix = input()
    if choix.isdigit():
        return int(choix)
    else:
        return 0


def lire_tcx(chemin: str) -> tuple:
    """Lit le contenu du fichier
    Renvoie dans un tuple les données de l'entête et les données de l'activité
    """
    with open(chemin, "r") as f:
        contenu = f.read()
    entete, activite = contenu.split("<Track>")
    return entete, activite


def segementer_iso_time(iso_time: str) -> float:
    """, Convertit une date ISO 8601 en secondes depuis le 1er janvier 1970"""
    # Identifie le caractère central (Lettre)
    date = None
    heure = None
    i = 0
    while i < len(iso_time) and date is None:
        if ord(iso_time[i]) >= 65:
            date = iso_time[:i]
            heure = iso_time[i + 1 :][:8]
        i += 1
    return date, heure


def iso_time_vers_sec(iso_time: str) -> float:
    """Convertit une date ISO 8601 en secondes"""
    date, heure = segementer_iso_time(iso_time)
    annee, mois, jour = [int(x) for x in date.split("-")]
    heure, minute, seconde = [int(x) for x in heure.split(":")]
    dt = datetime(annee, mois, jour, heure, minute, seconde)
    return dt.timestamp()


def temps_iso_vers_sec(temps: list) -> list:
    """Convertit une liste de temps iso en temps en secondes en prenant le premier temps comme référence."""
    temps_ref = iso_time_vers_sec(temps[0])
    temps_sec = []
    for tempo in temps:
        delta_temps = iso_time_vers_sec(tempo) - temps_ref
        temps_sec.append(delta_temps)
    return temps_sec
