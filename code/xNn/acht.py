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
def ajout_entrees(architecture, neurones_entrees):
    for num,couche in enumerate(architecture):
        if num == 0:
            couche.update({"entrees": neurones_entrees})
        else:
            couche.update({"entrees": couche_prec["neurones"]})
        couche_prec = couche
        architecture[num] = couche
    return architecture

#   I2
def initialisation_poids(architecture, graine_fixee):
    if graine_fixee:
        np.random.seed(1)
    poids = {}
    for list,couche in enumerate(architecture):
        num = list + 1
        taille_layer = couche["neurones"]
        taille_entrees_layer = couche["entrees"]
        poids[num] = np.random.randn(taille_entrees_layer, taille_layer) * 0.1
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
    valeur_avant_act = np.dot(input, poids)
    sortie = activation(valeur_avant_act)
    return sortie, valeur_avant_act

#   F2
def propagation_avant(entrees_initiales, poids, architecture):
    valeurs = {}
    valeurs[0] = entrees_initiales
    valeur_avant_activation = {}
    for ls,couche in enumerate(architecture):
        num = ls + 1
        activation_couche = couche['activation']
        valeurs[num], valeur_avant_activation[num] = propagation_avant_par_couche(valeurs[num-1], activation_couche, poids[num])
    return valeurs, valeur_avant_activation

#       B-phase
def propagation_arriere(predictions, attentes, poids, valeurs, valeur_avant_activation, vitesse, architecture):
    erreur = {}
    for ls,couche in reversed(list(enumerate(architecture))):
        num = ls + 1
        if num == len(architecture):
            erreur[num] = derivee(valeur_avant_activation[num], couche['activation']) * attentes - predictions
        else:
            val_derivee = derivee(valeur_avant_activation[num], couche['activation'])
            erreur[num] = val_derivee * poids[num+1].dot(erreur[num+1])
    for ls,couche in enumerate(architecture):
        num = ls + 1
        # en théorie : poids[num] = poids[num] + vitesse * erreur[num+1] * valeur[num]
        #temp = erreur[num].reshape(np.shape(erreur[num])[0],1)
        #print('\ntemp :\n',temp)
        #print('erreur :\n',erreur[num])
        #print('valeur :\n',valeurs[ls])
        #print('poids :\n',poids[num])
        #print('mix :\n',(temp*valeurs[ls]).T)
        #poids[num] = poids[num] + vitesse * (temp * valeurs[ls]).T
        print(ls)
        #print(poids[num])
        #print(valeurs[ls])
        for i in range(0,np.shape(poids[num])[1]):
            for j in range(0,np.shape(poids[num])[0]):
                #print('i',i,'j',j)
                #print('poids ',i,' ; ',j,' = ',poids[num][j][i])
                #print('erreur ',i,' = ',erreur[num][i])
                #print('valeur ',j,' = ',valeurs[ls][j])
                poids[num][j][i] += vitesse * erreur[num][i] * valeurs[ls][j]
                #print('poids du neurone',j,'pour le neurone',i,' : ',poids[num][j][i])
    return poids

def derivee(x, activation):
    activation_derivee = activation + '_der'
    return eval(activation_derivee)(x)

def train(entrees, attentes, vitesse, architecture, neurones_entrees, epochs=1, graine_fixee=True):
    architecture = ajout_entrees(architecture, neurones_entrees)
    poids = initialisation_poids(architecture, graine_fixee)
    for epoch in range(0,epochs):
        #propagation avant
        print('')
        valeurs, valeur_avant_activation = propagation_avant(entrees, poids, architecture)
        predictions = valeurs[len(architecture)]
        #propagation arrière
        poids = propagation_arriere(predictions, attentes, poids, valeurs, valeur_avant_activation, vitesse, architecture)
        #impression de la sortie
        print('Epoch ',epoch+1,' : ',predictions)

if __name__ == '__main__':
    neurones_entrees = 1
    architecture = [
        {"neurones": 3, "activation": "sigmoid"},
        {"neurones": 4, "activation": "sigmoid"},
        {"neurones": 1, "activation": "sigmoid"}, # couche de sorties
    ]
    print('\n')
    train([0.5,], [0.25,], 0.1, architecture, neurones_entrees, 100)
