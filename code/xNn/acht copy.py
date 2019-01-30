# acht.py - module principal du réseau de neurones
#
#   Tête du programme : importation des modules : T1
#
#   Initialisation phase : on initialise les bases (matrices, activations...) : I
#       définition du nn (ou récupérées par variables) : I0
#   ->  ajout des entrées à l'architecture du réseau : I1
#   ->  création des matrice de : poids (weight) :  I2.1 & pondération (bias) : I2.2
#   ->  définition des activations  : relu, sigmoid : I3.11, I3.12 & leurs dérivées : relu_der, sigmoid_der : I3.21, I3.22
#
#   Forward phase : on feedforward le réseau (on le nourrit et on fait une propagation avant : les neurones sont activées depuis la couche d'entrée jusqu'à la couche de sortie) : F
#       activation par couche : on multiplie les sorties de la couche précédente pour les poids, on ajoute la pondération et on effectue l'activation de la couche sur le résultat : F1
#           => valeur[L] = activation( valeur[L-1] * poids + bias )
#       propager l'activation : on effectue F1 pour chaque couche de neurones, les une à la suite des autres : F2
#
#   Backward phase : on détermine les erreurs de la phase F comparé au résultat attendu, puis on corrige les matrices de poids et de pondération afin de se rapprocher du résultat : B
#       calcul du loss : fonction mathématique déterminant l'écart entre le résultat donné et le résultat attendu : B1
#       calcul de la dérivée de notre activation :
#
#

'''acht.py - réseau de neurones'''

import numpy as np

#       I-phase
#   I0
entrees = 2
architecture = [
    {"neurones": 4, "activation": "relu"}, # couche d'entrée
    {"neurones": 3, "activation": "relu"},
    {"neurones": 2, "activation": "sigmoid"}, # couche de sorties
]

#   I1
def ajout_entrees(architecture):
    for num,couche in enumerate(architecture):
        if num == 0:
            couche.update({"entrees": entrees})
        else:
            couche.update({"entrees": couche_prec["neurones"]})
        couche_prec = couche
        architecture[num] = couche
    return architecture
architecture = ajout_entrees(architecture)

#   I2.1
def initialisation_poids(architecture, graine, debug):
    np.random.seed(graine)
    poids = {}
    if debug:
        print('\n    Poids :')
    for list,couche in enumerate(architecture):
        num = list + 1
        taille_layer = couche["neurones"]
        taille_entrees_layer = couche["entrees"]
        poids[num] = np.random.randn(taille_layer, taille_entrees_layer) * 0.1
        if debug:
            print('Matrice poids couche ',num,' :\n',poids[num])
    return poids

#   I2.2
def initialisation_ponderation(architecture, is_ponderation, graine, debug):
    np.random.seed(graine)
    ponderation = {}
    if debug and is_ponderation:
        print('\n    Pondération :')
    elif debug:
        print('\n    Matrices de pondération initialisées à zéro.')
    for list,couche in enumerate(architecture):
        num = list + 1
        taille_layer = couche["neurones"]
        if is_ponderation:
            ponderation[num] = np.random.randn(taille_layer) * 0.1
            if debug:
                print('Matrice pondération couche ',num,' :\n',ponderation[num])
        else:
            ponderation[num] = np.zeros(taille_layer)
    return ponderation

#   I3.11
def relu(x):
    return np.maximum(0,x)

#   I3.12
def sigmoid(x):
    return 1/(1+np.exp(-x))

#   I3.21
def relu_der(x):
    x[x <= 0] = 0
    x[x > 0] = 1
    return x

#   I3.22
def sigmoid_der(x):
    return sigmoid(x) * (1 - sigmoid(x))


#       F-phase
#           Sake for clarity : on entre la matrice 'entrees_initiales', on devra ressortir la matrice 'sortie_effective'
#   F1
def propagation_avant_par_couche(input, activation_couche, poids, ponderation):
    activation = eval(activation_couche)
    temp = np.dot(input, poids.T) + ponderation
    sortie_effective = activation(temp)
    return sortie_effective

#   F2
def propagation_avant(entrees_initiales, poids, ponderation, architecture, debug=False):
    valeur_couche = {}
    valeur_couche[0] = entrees_initiales
    if debug:
        print('\n    Entrées du réseau :')
        print(valeur_couche)
        print('\n    Valeurs après propagation avant :')
    for list,couche in enumerate(architecture):
        num = list + 1
        activation_couche = couche['activation']
        valeur_couche[num] = propagation_avant_par_couche(valeur_couche[list], activation_couche, poids[num], ponderation[num])
        sortie_effective = valeur_couche[num]
        if debug:
            print('Valeurs couche ',num,' :\n',sortie_effective)
    if debug:
        print('Sortie du réseau :\n',sortie_effective)
    return sortie_effective, valeur_couche

#       B-phase
#           Sake for clarity : on entre la matrice 'sortie_effective', 'sorties_attendues', ''

def calcul_erreur_modele(sorties_attendues, sortie_effective, erreurs, num):
    erreurs[]

#   Il nous faut comme sortie : l'augmentation/diminution des poids, leurs valeurs
def propagation_arriere(sortie_effective, sorties_attendues, poids, ponderation, valeur_couche, learning_rate, debug):
    erreurs = {}
    if debug:
        print('\n    Erreurs et corrections (delta) :')
    for ls,couche in reversed(list(enumerate(architecture))):
        num = ls + 1
        # On calcul les erreurs du modèle
        if num == len(architecture):
            erreur_sortie = sorties_attendues - sortie_effective
        erreurs[num] = np.dot(poids[num], valeur_couche[ls]) # peut-être avec erreurs[ls] ?
        if debug:
            print('Erreur totale du modèle :\n',erreur_sortie)
            print('Erreurs couche ',num,' :\n',erreurs)
        # On a maintenant : erreur_sortie (erreur totale du modèle sur la sortie attendue), erreurs (erreur de chaque couche de neurones)
        # On veut obtenir delta
        delta = relu_der(valeur_couche[num]) * (erreurs[num])
        if debug:
            print('Delta couche ',num,' :\n',delta)
    if debug:
        print('\n    Poids avant correction :\n',poids)
    # On veut maintenant corriger le réseau à l'aide de 'delta'
    for ls,couche in enumerate(architecture):
        num = ls + 1
        poids[num] -= learning_rate * delta[num]
    if debug:
        print('\n    Poids après correction :\n',poids)
    return 'fait'

def train(entrees_initiales, sorties_attendues, architecture, learning_rate, epochs=1, is_ponderation=True, debug=False):
    poids = initialisation_poids(architecture, 1, debug=debug)
    ponderation = initialisation_ponderation(architecture, is_ponderation, 1, debug=debug)
    for epoch in range(0,epochs):
        sortie_effective, valeur_couche = propagation_avant(entrees_initiales, poids, ponderation, architecture, debug)
        print(sortie_effective)
        print(propagation_arriere(sortie_effective, sorties_attendues, poids, ponderation, valeur_couche, learning_rate, debug))

#   debug
# On veut f(x)=x*x

#   Pour backpropagrate le bias, on utilise la même valeur qu'avec le poids.
#   bias[j] -= learning_rate * delta[j]
#   Où 'delta[j]' est l'erreur dérivée

train([0.5,0.5], [0.7,0.7], architecture, 1, 10000, False, False)

#   !debug
