""" Ouvre les fichiers .tcx du répertoire sources
    Lit le contenu pour en proposer des représentations graphiques : Evolution de l'allure, de l'altitude ...

    TODO : Interface graphique
    * Choix du fichier
    * Choix des paramètres (zoom, grandeurs à représenter, couleurs ...)
    TUTO : https://matplotlib.org/stable/gallery/user_interfaces/embedding_in_tk_sgskip.html
    https://pythonprogramming.net/how-to-embed-matplotlib-graph-tkinter-gui/
"""

import matplotlib.pyplot as plt
from extraction_fichiers import *
from exploitation import *
from traitement import *


if __name__ == "__main__":
    COULEURS = créer_dégradé()
    request = cimgt.OSM()
    dossier = "Sources"
    liste_tcx = lister_fichiers(dossier)
    if len(liste_tcx) == 0:
        print("Aucun fichier .tcx dans le dossier sources")

    else:
        fichier = choix_fichier(liste_tcx)
        entete, activite = lire_tcx(dossier + "/" + fichier)
        dico_entete = construire_dico_entete(entete)
        liste_trackpoints = construire_activite(activite)
        print("Nombre de points de l'activité : ", len(liste_trackpoints))

        # Construit les listes de valeurs à exploiter
        temps = [dico["Time"] for dico in liste_trackpoints]
        temps_secondes = temps_iso_vers_sec(
            temps
        )  # Conversion de la liste des temps en secondes
        altitudes = [float(dico["AltitudeMeters"]) for dico in liste_trackpoints]
        distances = [float(dico["DistanceMeters"]) for dico in liste_trackpoints]
        cadence = [float(dico["RunCadence"]) for dico in liste_trackpoints]
        vitesses = [float(dico["Speed"]) for dico in liste_trackpoints]
        #
        latitudes = [float(dico["LatitudeDegrees"]) for dico in liste_trackpoints]
        longitudes = [float(dico["LongitudeDegrees"]) for dico in liste_trackpoints]
        extent, zoom = construire_carte(latitudes, longitudes)
        # Calcul des dénivelés lissés sur 30 points
        pentes = calculer_pentes(altitudes, distances, 30)
        pente_min, pente_max = extremum(pentes)
        couleurs = []
        tailles = []
        for i in range(len(pentes)):
            indice_couleur = int(
                255 * (pentes[i] - pente_min) / (pente_max - pente_min)
            )
            couleurs.append(COULEURS[indice_couleur])
            tailles.append((indice_couleur) / 3)
        # Dessins
        plt.figure(figsize=(40, 30))
        ax = plt.axes(projection=request.crs)
        ax.set_extent(extent)
        ax.add_image(request, zoom)
        plt.scatter(
            longitudes,
            latitudes,
            transform=ccrs.PlateCarree(),
            s=tailles,
            c=couleurs,
        )
        """
        plt.figure(figsize=(20, 10))
        v = lisser(vitesses, 30)
        # Dessine la courbe colorée de l'évolution de v
        for i in range(len(temps_secondes) - 1):
            tps1 = temps_secondes[i]
            tps2 = temps_secondes[i + 1]
            v1 = v[i]
            v2 = v[i + 1]
            plt.plot([tps1, tps2], [v1, v2], color=couleurs[i])
        plt.title("Evolution de la vitesse")
        plt.xlabel("Temps")
        plt.ylabel("Vitesse (m/s)")
        """
        plt.show()
