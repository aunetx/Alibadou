# acht.py - module principal du réseau de neurones
#
#   Tête du programme : importation des modules : T1
#
#   Initialisation phase : on initialise les bases (matrices, activations...) : I
#       définition du nn (ou récupérées par variables) : I0
#   ->  ajout des entrées à l'architecture du réseau : I1
#   ->  création des matrice de : poids (weight) :  I2
#   ->  définition des activations  : relu, sigmoid : I3.1, I3.2
#   ->  définition de leurs dérivées : relu_der, sigmoid_der : I4.1, I4.2
#
#   Forward phase : on feedforward le réseau (on le nourrit et on fait une propagation avant : les neurones sont activées depuis la couche d'entrée jusqu'à la couche de sortie) : F
#       activation par couche : on multiplie les sorties de la couche précédente pour les poids et on effectue l'activation de la couche sur le résultat : F1
#           => valeur[L] = activation( valeur[L-1] * poids )
#       propager l'activation : on effectue F1 pour chaque couche de neurones, les une à la suite des autres : F2
#
#   Backward phase : on détermine les erreurs de la phase F comparé au résultat attendu, puis on corrige les matrices de poids afin de se rapprocher du résultat : B
#       calcul du loss : fonction mathématique déterminant l'écart entre le résultat donné et le résultat attendu : B1
#       calcul de la dérivée de notre activation :
#
#

'''acht.py - réseau de neurones'''

import numpy as np

#       I-phase
#   I1
def ajout_entrees():
    if debug:
        print("Architecture du réseau :")
    for num,couche in enumerate(architecture):
        if num == 0:
            couche.update({"entrees": neurones_entrees})
        else:
            couche.update({"entrees": couche_prec["neurones"]})
        couche_prec = couche
        architecture[num] = couche
        if debug:
            print("Couche",num+1," : ",architecture[num])
    return architecture

#   I2
def initialisation_poids(graine_fixee):
    if graine_fixee:
        np.random.seed(1)
        if debug:
            print("\nGraine fixée à 1 pour l'initialisation.")
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

#   I3.1
def relu(x):
    return np.maximum(0,x)

#   I3.2
def sigmoid(x):
    return 1/(1+np.exp(-x))

#   I4.1
def relu_der(x):
    x[x <= 0] = 0
    x[x > 0] = 1
    return x

#   I4.2
def sigmoid_der(x):
    return sigmoid(x) * (1 - sigmoid(x))


#       F-phase
#   F1
def propagation_avant_par_couche(input, activation_couche, poids):
    activation = eval(activation_couche)
    valeur_avant_act = np.dot(input, poids.T)
    sortie = activation(valeur_avant_act)
    return sortie, valeur_avant_act

#   F2
def propagation_avant(entrees_initiales, poids):
    valeurs = {}
    valeurs[0] = entrees_initiales
    valeur_avant_activation = {}
    if debug:
        print('\n    Entrées du réseau :')
        print(valeurs[0])
        print('\n    Valeurs après propagation avant :')
    for ls,couche in enumerate(architecture):
        num = ls + 1
        activation_couche = couche['activation']
        valeurs[num], valeur_avant_activation[num] = propagation_avant_par_couche(valeurs[num-1], activation_couche, poids[num])
        if debug:
            print('Valeurs couche ',num,' :\n',valeurs[num])
    if debug:
        print('Sortie du réseau :\n',valeurs[len(architecture)])
    return valeurs, valeur_avant_activation

#       B-phase
def propagation_arriere(predictions, attentes, poids, valeurs, valeur_avant_activation, vitesse):
    erreur = {}
    if debug:
        print('\n    Poids avant propagation arrière :')
    for ls,couche in reversed(list(enumerate(architecture))):
        num = ls + 1
        if num == len(architecture):
            erreur[num] = derivee(valeur_avant_activation[num], couche['activation']) * attentes - predictions
        else:
            temp = derivee(valeur_avant_activation[num], couche['activation'])
            erreur[num] = temp * poids[num+1].T.dot(erreur[num+1])
            # anciennement : erreur[num] = temp * poids[num+1].dot(erreur[num+1])
    p = {}
    for ls,couche in reversed(list(enumerate(architecture))):
        num = ls + 1
        print('\nPoids couche ',num,' avant correction :\n',poids[num])
        p[num] = poids[num]
        # en théorie : poids[num] = poids[num] + vitesse * erreur[num+1] * valeur[num]
        #print(erreur[num+1])
        #print(valeurs[num])
        temp = erreur[num].reshape(np.shape(erreur[num])[0],1)
        poids[num] = poids[num] + vitesse * temp * valeurs[ls]
        print('Poids couche ',num,' après correction :\n',poids[num])
        print('Correction couche ',num,' :\n',p[num] - poids[num])
    return poids

def derivee(x, activation):
    activation_derivee = activation + '_der'
    return eval(activation_derivee)(x)

def train(entrees, attentes, vitesse, epochs=1, graine_fixee=True):
    #init
    global debug
    global architecture
    global neurones_entrees
    architecture = ajout_entrees()
    poids = initialisation_poids(graine_fixee)
    #boucle epochs
    for epoch in range(0,epochs):
        #propagation avant
        valeurs, valeur_avant_activation = propagation_avant(entrees, poids)
        predictions = valeurs[len(architecture)]
        #propagation arrière
        #poids = propagation_arriere(sortie_effective, sorties_attendues, poids, valeur_couche, learning_rate, debug)
        poids = propagation_arriere(predictions, attentes, poids, valeurs, valeur_avant_activation, vitesse)
        #impression de la sortie
        print('Epoch ',epoch+1,' : ',predictions)


if __name__ == '__main__':
    neurones_entrees = 1
    architecture = [
        {"neurones": 3, "activation": "sigmoid"},
        {"neurones": 4, "activation": "sigmoid"},
        {"neurones": 1, "activation": "sigmoid"}, # couche de sorties
    ]
    debug=False
    print('\n')
    train([0.5,], [0.25,], 0.1, 200)
