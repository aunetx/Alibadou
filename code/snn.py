#           sNN - simplified Neural Network

#       Début de programme
import numpy as np
import time

#       Définitions des fonctions secondaires
#   Initialisation du NN
def nn_init(arch, graine = 99):
    np.random.seed(graine) # On donne une graine pour fixer le hasard (pour faciliter le déboguage)
    layer_nb = len(arch) # Nombre de layers

    #   Initialisation de la variable 'matrices'
    matrices = {}

    #   On initialise layer par layer :
    for list_id, layer in enumerate(arch):
        layer_id = str(list_id + 1)
        # layer_id : numéro du layer (str)
        # layer : informations à son propos

        taille_layer = layer["neurons"]
        taille_entrees_layer = layer["entrees"]

        #   Poids :
        matrices['W' + layer_id] = np.random.randn(taille_layer, taille_entrees_layer) * 0.1
        #   Bias :
        matrices['b' + layer_id] = np.random.randn(taille_layer) * 0.1

    return matrices #   En réalité les matrices ne sont pas stockées indépendamment pour simplifier l'écriture du programme :
                    #   les matrices W (poids) et b (pondération, bias (en)) sont stockées dans le même tableau,
                    #   sous la forme : matrice_poids_layer_1, matrice_bias_layer_1, matrice_poids_layer_2, matrice_bias_layer_2...
                    #   Les matrice poids de chaque layer ont deux axes (le nombre de neurones et les entrées du layer).
                    #   Les matrices bias de chaque layer ont un axe (le nombre de neurones du layer)
                    #
                    #                                C'EST ICI TOUTE LA MEMOIRE A LONG TERME DU RESEAU NEURONAL
                    #   Afin d'enregistrer l'avancement de l'apprentissage du nn, il suffit d'enregistrer ce retour une fois l'apprentissage effectué ;
                    #   Afin d'importer un apprentissage précédemment effectué, il suffit d'importer une telle valeur compatible avec l'architecture du nn.


#   Fonctions d'activation
def sigmoid(Z):
    val = 1/(1+np.exp(-Z))
    return val

def relu(Z):
    val = np.maximum(0,Z)
    return val

#   Et leurs dérivées
def sigmoid_backward(dA, Z):
    val = dA * sigmoid(Z) * (1 - sigmoid(Z))
    return val

def relu_backward(dA, Z):
    dZ = np.array(dA, copy = True)
    dZ[Z <= 0] = 0;
    return dZ;

#   Propagation des valeurs à travers le reseau : Forward Propagation
# Pour chaque layer
def single_layer_forward_propagation(A_prev, W_curr, b_curr, activation="relu"):
    Z_curr = np.dot(W_curr, A_prev) + b_curr #  z = (poids * valeur) + bias

    if activation is "relu":
        activation_func = relu
    elif activation is "sigmoid":
        activation_func = sigmoid
    else:
        raise Exception('Non-supported activation function')

    #      a = g(z)
    return activation_func(Z_curr), Z_curr

# En entier
def full_forward_propagation(X, matrices, sNn_arch):
    memoire = {}
    A_courant = X

    #   On initialise layer par layer :
    for list_id, layer in enumerate(sNn_arch):
        layer_id = str(list_id + 1)
        # layer_id : numéro du layer (str)
        # layer : informations à son propos
        A_prec = A_courant

        activation_courante = layer["activation"] # On trouve l'activation du layer courant
        W_courant = matrices['W' + layer_id] # On stocke les valeurs des poids de la couche présente
        b_courant = matrices['b' + layer_id] # On stocke les valeurs des bias de la couche présente

        A_courant, Z_courant = single_layer_forward_propagation(A_prec, W_courant, b_courant, activation_courante)

        memoire["A" + str(list_id)] = A_prec
        memoire["Z" + str(layer_id)] = Z_courant

    return A_courant, memoire


#   Cost et tout
def convert_prob_into_class(probs):
    probs_ = np.copy(probs)
    probs_[probs_ > 0.5] = 1
    probs_[probs_ <= 0.5] = 0
    return probs_

def get_cost_value(Y_hat, Y):
    m = Y_hat.shape[1]
    cost = -1 / m * (np.dot(Y, np.log(Y_hat).T) + np.dot(1 - Y, np.log(1 - Y_hat).T))
    return np.squeeze(cost)

def get_accuracy_value(Y_hat, Y):
    Y_hat_ = convert_prob_into_class(Y_hat)
    return (Y_hat_ == Y).all(axis=0).mean()

#   Backward propagation : propagation inverse
# Pour une couche de neurones
def single_layer_backward_propagation(dA_courant, W_courant, b_courant, Z_courant, A_prec, activation="relu"):
    m = A_prec.shape[1]

    if activation is "relu":
        backward_activation_func = relu_backward
    elif activation is "sigmoid":
        backward_activation_func = sigmoid_backward
    else:
        raise Exception('Non-supported activation function')

    dZ_curr = backward_activation_func(dA_curr, Z_curr)
    dW_curr = np.dot(dZ_curr, A_prev.T) / m
    db_curr = np.sum(dZ_curr, axis=1, keepdims=True) / m
    dA_prev = np.dot(W_curr.T, dZ_curr)

    return dA_prev, dW_curr, db_curr


def full_backward_propagation(Y_hat, Y, memoire, params_values, sNn_arch):
    grads_values = {}
    m = Y.shape[1]
    Y = Y.reshape(Y_hat.shape)

    dA_prec = - (np.divide(Y, Y_hat) - np.divide(1 - Y, 1 - Y_hat));

    for list_id, layer in reversed(list(enumerate(sNn_arch))):
        layer_id = str(list_id + 1)
        activation_courante = layer["activation"]
        dA_courant = dA_prec

        A_prec = memoire["A" + list_id]
        Z_courant = memoire["Z" + layer_id]
        W_courant = params_values["W" + layer_id]
        b_courant = params_values["b" + layer_id]

        dA_prec, dW_courant, db_courant = single_layer_backward_propagation(
            dA_courant, W_courant, b_courant, Z_courant, A_prec, activation_courante)

        grads_values["dW" + layer_id] = dW_courant
        grads_values["db" + layer_id] = db_courant

    return grads_values


def update(params_values, grads_values, sNn_arch, learning_rate):
    for list_id, layer in enumerate(sNn_arch):
        layer_id = str(list_id)
        params_values["W" + layer_id] -= learning_rate * grads_values["dW" + layer_id]
        params_values["b" + layer_id] -= learning_rate * grads_values["db" + layer_id]

    return params_values;


def train(X, Y, sNn_arch, epochs, learning_rate):
    params_values = nn_init(sNn_arch, 2)
    cost_history = []
    accuracy_history = []

    for i in range(epochs):
        Y_hat, cashe = full_forward_propagation(X, params_values, sNn_arch)
        cost = get_cost_value(Y_hat, Y)
        cost_history.append(cost)
        accuracy = get_accuracy_value(Y_hat, Y)
        accuracy_history.append(accuracy)

        grads_values = full_backward_propagation(Y_hat, Y, cashe, params_values, sNn_arch)
        params_values = update(params_values, grads_values, sNn_arch, learning_rate)

    return params_values, cost_history, accuracy_history



if __name__ == '__main__':
    sNn_arch = [
        {"entrees": 1, "neurons": 16, "activation": "relu"}, # input layer
        {"entrees": 16, "neurons": 12, "activation": "relu"},
        {"entrees": 12, "neurons": 12, "activation": "relu"},
        {"entrees": 12, "neurons": 5, "activation": "sigmoid"}, # output layer
    ]
    print("\n","Randomised matrix : \n",nn_init(sNn_arch),)
    print("<b>Result : </b>",full_forward_propagation([0.3], nn_init(sNn_arch), sNn_arch))

# Copyright aunetx 2018
