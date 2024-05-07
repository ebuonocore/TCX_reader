# ***** Fonctions sur les traitements des données

import cartopy.crs as ccrs
import cartopy.io.img_tiles as cimgt
import numpy as np
from math import floor, ceil


def extremum(coordonnées: list):
    """Renvoie les coordonnées GPS extrêmes de la liste de float"""
    coord_min = coordonnées[0]
    coord_max = coordonnées[0]
    for coord in coordonnées:
        if coord < coord_min:
            coord_min = coord
        if coord > coord_max:
            coord_max = coord
    return coord_min, coord_max


def calculer_pentes(altitudes: list, distances: list, delta: int = 30) -> list:
    """Renvoie la liste des dénivelés calculés sur delta points"""
    if delta > len(altitudes):
        return altitudes
    pente = (altitudes[delta] - altitudes[0]) / (distances[delta] - distances[0])
    pentes = [pente] * (floor(delta / 2))
    for i in range(0, len(altitudes) - delta):
        pente = (altitudes[i + delta] - altitudes[i + 0]) / (
            distances[i + delta] - distances[i + 0]
        )
        pentes.append(pente)
    for _ in range(ceil(delta / 2)):
        pentes.append(pente)
    return pentes


def lisser(valeurs: list, delta: int):
    """Lisse les valeurs de la liste sur un intervale de delta valeurs."""
    if len(valeurs) < delta or delta < 2:
        return valeurs
    nb_début = floor(delta / 2)
    nb_fin = ceil(delta / 2)
    somme = 0
    _valeurs = []
    for i in range(nb_début):
        somme = sum(valeurs[: (nb_début + i)])
        _valeurs.append(somme / (nb_début + i))
    for i in range(nb_début + 1, len(valeurs) - nb_fin):
        somme += valeurs[i + nb_fin] - valeurs[i - nb_début]
        _valeurs.append(somme / delta)
    for i in range(nb_fin, -1, -1):
        somme = sum(valeurs[(len(valeurs) - nb_fin - i) :])
        _valeurs.append(somme / (nb_fin + i))
    return _valeurs


def créer_dégradé():
    """Crée un dégradé de couleur du rouge au vert sur 256 valeurs"""
    from math import sin

    couleurs = []
    for i in range(256):
        G = 255 - i
        R = i
        B = int(sin(i * 0.025 - 1.6) * 127 + 128)
        couleurs.append("#{:02x}{:02x}{:02x}".format(R, G, B))
    return couleurs


def zoomlevel_from_deg(delta):
    "Calculate OSM zoom level from a span in degrees.  Adjust +/-1 as desired"
    from numpy import log2, clip, floor

    zoomlevel = int(clip(floor(log2(360) - log2(delta)), 0, 20))
    return zoomlevel


def construire_carte(latitudes: list, longitudes: list):
    lat_min, lat_max = extremum(latitudes)
    long_min, long_max = extremum(longitudes)
    delta_lat = lat_max - lat_min
    delta_long = long_max - long_min
    lat_min -= delta_lat / 10
    lat_max += delta_lat / 10
    long_min -= delta_long / 10
    long_max += delta_long / 10
    zoom = zoomlevel_from_deg(delta_lat) + 1
    extent = [long_min, long_max, lat_min, lat_max]
    return extent, zoom
