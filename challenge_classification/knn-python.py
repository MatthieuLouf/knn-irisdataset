# Application de l'algorithme KNN pour le challenge de classification
# Fait par Matthieu LOUF et Steve MAHOT 

#------------ IMPORTATION MODULES --------------#
from statistics import mean,stdev
from math import sqrt
import os
import numpy #pour utilisation de la loi normale

#-------- INSTALLATION DU MODULE NUMPY ---------#
# python -m pip install --user numpy

#------------ DEFINITION FONCTIONS -------------#

#lecture du data set des iris fourni
def lecture_dataset(nomFichier) :
    mon_fichier = open(nomFichier, "r")
    contenu = mon_fichier.readline()
    data_set = []
    count =0

    while contenu != '':
        data_set.append([])
        temp=""

        for i in range(len(contenu)):
            if contenu[i] == ',' or contenu[i] == '\n':
                try:
                    data_set[count].append(float(temp))
                except :
                    data_set[count].append(temp)
                temp=""
            else:
                temp += contenu[i]

        contenu = mon_fichier.readline()
        count+=1

    while data_set.count([''])>0:
        data_set.remove([''])
    return data_set

#modification des 4 premières colonnes du data set pour centrer et réduire les valeurs
def centrer_reduire_data(data_set):
    data_set_centre_reduit= [[data_set[x][y] for y in range(len(data_set[0]))] for x in range(len(data_set))]
    moy = []
    ecart_type = []

    for i in range(4):
        moy.append(mean(data_set[j][i]for j in range(len(data_set) ) ))
        ecart_type.append(stdev(data_set[j][i]for j in range(len(data_set) ) ))

    for i in range(4):
        for j in range(len(data_set)):
            data_set_centre_reduit[j][i] = (data_set[j][i] -moy[i])/ecart_type[i]
            #print(data_set_centre_reduit[j]) 

    return data_set_centre_reduit, moy,ecart_type

#on centre et réduit également la donnée test, pour la comparer au data set
def centrer_reduire_test(data_test,moyenne,ecart_type):
    data_test_centre_reduit = data_test.copy()
    for i in range(len(data_test)):
        data_test_centre_reduit[i] = (data_test[i] -moyenne[i])/ecart_type[i]

    return data_test_centre_reduit

#calcul de la distance euclidienne entre chaque donnée du data set et la donnée test
def calcul_distance(data_set,data_test):
    data_set_distance = data_set.copy()
    
    for j in range(len(data_set_distance)):
        somme_difference_carre = 0
        for i in range(len(data_set_distance[j])-1):
            somme_difference_carre += pow((data_set_distance[j][i]-data_test[i]),2)
        data_set_distance[j].append(sqrt(somme_difference_carre))
    
    return data_set_distance

#fonction secondaire pour le tri sur la 6 colonne dans trier_distance()
def takeSixth(elem):
    return elem[5]

#tri du data set selon la distance à la donnée test
def trier_distance(data_set):
    data_set_distance_triee = data_set.copy()
    data_set_distance_triee.sort(key=takeSixth)
    return data_set_distance_triee

#selection des k données les plus proches et comptage de la class la plus représentée
def prediction_class(data_set_triee,k):
    top_k_iris = []
    for i in range(k):
        top_k_iris.append(data_set_triee[i][4])

    count_iris_apparition = []
    for i in range(len(top_k_iris)):
        count_iris_apparition.append(top_k_iris.count(top_k_iris[i]))

    return top_k_iris[count_iris_apparition.index(max(count_iris_apparition))]

#fonction centrale de l'algo knn, utilise toutes les fonctions précédentes
def knn(data_set,data_test,k):

    data_set_centre_reduit,moyenne,ecart_type = centrer_reduire_data(data_set)

    data_test_centre_reduit = centrer_reduire_test(data_test,moyenne,ecart_type)

    data_set_distance = calcul_distance(data_set_centre_reduit,data_test_centre_reduit)

    data_set_distance_triee =trier_distance(data_set_distance)

    class_prediction = prediction_class(data_set_distance_triee,k)

    return class_prediction

#génération de la matrice de confusion, en générant de nouvelles données avec les moyennes 
#et ecarts-types des fleurs en utilisant un loi normale
def matrice_confusion(data_set,k, N):

    data_set_centre_reduit_setosa,moyenne_setosa,ecart_type_setosa = centrer_reduire_data(data_set[0:49])
    data_set_centre_reduit_versicolor,moyenne_versicolor,ecart_type_versicolor = centrer_reduire_data(data_set[50:99])
    data_set_centre_reduit_virginica,moyenne_virginica,ecart_type_virginica = centrer_reduire_data(data_set[100:149])

    tab_noms =['Iris-setosa','Iris-versicolor','Iris-virginica']
    mat_confusion = [[0,0,0], [0,0,0],[0,0,0]]

    i =0
    while i<=N:
        data_test_setosa = numpy.random.normal(moyenne_setosa, ecart_type_setosa, 4)
        mat_confusion[0][tab_noms.index(knn(data_set,data_test_setosa,k))] +=1

        data_test_versicolor = numpy.random.normal(moyenne_versicolor, ecart_type_versicolor, 4)
        mat_confusion[1][tab_noms.index(knn(data_set,data_test_versicolor,k))] +=1

        data_test_virginica = numpy.random.normal(moyenne_virginica, ecart_type_virginica, 4)
        mat_confusion[2][tab_noms.index(knn(data_set,data_test_virginica,k))] +=1
        
        i+=3

    return mat_confusion

#------------ DEBUT PROGRAMME -------------#
 
k=5 #nombre de plus proches voisins à sélectionner
data_set = lecture_dataset("training.csv") #lecture du data_set
#print(data_set)

data_test = lecture_dataset("predict.csv") #création d'une donnée test
#print(data_test)

nomFichier = "MahotLouf.txt"
try :
    os.remove("MahotLouf.txt")
except:
    print("Création du fichier résultat")
fichier = open(nomFichier, "a")

for i in range(len(data_test)):
    class_prediction = knn(data_set,data_test[i],k) #prédiction de la class de la donnée test
    #print("\nLa classe prédite avec k=",k," est :",class_prediction)
    fichier.write(class_prediction+"\n")

fichier.close()

print("\nPredictions effectuées dans le fichier : " ,nomFichier,"\n")