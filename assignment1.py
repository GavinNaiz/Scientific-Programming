from __future__ import division
from collections import Counter as C
import glob
import numpy as np
from sklearn import datasets, neighbors, metrics

def nn_text():
    # SETTINGS
    path='toydata'
    files=glob.glob(path+'/*/*.txt')
    pos_files=glob.glob(path+'/pos/*.txt')
    neg_files=glob.glob(path+'/neg/*.txt')
    dic=glob.glob('stop.txt')
    stop=open(dic[0]).read().strip().split('\n')
    ratio=0.90
    # settings end

    c=C()
    #creates a dictionary
    for f in files:
        c+C(open(f).read().strip().split())

    #removes common English words from dictionary
    for x in c.keys():
        if x in stop:
            c.pop(x)

    #Creates a list of lists from files
    pos_lines=[]
    neg_lines=[]
    for f in pos_files:
        pos_lines+=[open(f).read().strip().split()]
    for f in neg_files:
        neg_lines+=[open(f).read().strip().split()]

    #Creates two BOW representations of the pos and neg files seperately
    pos_dataset=[]
    neg_dataset=[]

    # The positive files
    for l in pos_lines:
        representation=[1] #Gives pos files the label 1
        for w in c:
            if w in l:
                representation.append(1)
            else:
                representation.append(0)
        pos_dataset.append(representation) #appends the BOW rep of a file to the dataset

    #The negative files
    for l in neg_lines:
        representation=[0]
        for w in c:
            if w in l:
                representation.append(1)
            else:
                representation.append(0)
        pos_dataest.append(representation)

    neg_dataset.append(representation) #appends the BOW rep of file to the datset

    #print 'TEST',pos_dataset
    #Splits and combines the pos and neg data into a 50/50 training and set

    print "TESTING WITH RATIO", (ratio*100), '/', (1-ratio)*100
    train=pos_dataset[:int((len(pos_dataset)*ratio))]+neg_dataset[:int((len(neg_dataset)*ratio))] #takes first part of neg and pos datasets and puts them into a list
    test=pos_dataset[int((len(pos_dataset)*ratio)):]+neg_dataset[int((len(neg_dataset)*ratio)):] #takes the last part of the neg and pos datasets and puts them into a list
    #train_prime = read_data(train)
    #test_prime = read_data(test)
    (Acc) = eval(train,test)
    print "accuracy:\t%1.4f" % Acc


#Calculate distance between two points

def HammingDistance(ex1, ex2):
    assert len(ex1)==len(ex2) #optional check

    c=0
    for i in range(len(ex1)):
        if ex[i]!=ex2[i]:
            c+=1
    return c


#Finds the nearest neighbor
def NearestNeighbor(tr, ex0):
    min_dist=len(ex0) #Min dist is set to have the max possible value as the starting value
    for ex in tr:
        curr_dist= HammingDistance(ex[1:],ex0[1:]) #From [1:] because we want the machine to ignore the label at first
        if curr_dist,min_dist:
            min_dist=curr_dist
            neighbor=ex
    return neighbor

def nn_img():
    #primes image data to fit in the eval function, calculating and returning nearest neighbour accuracy
    d = datasets.load_digits() #d for digits
    p = [] #p for primed data

    for i in range(len(d.images)):
        x = nphstack((d.target[i], d.data[i])) #generate a vector containing label as the first value, followed by the 64 pixels
        p.append(list(list(x)) # append vector to the primed data list
        
    train = p[0:-1:2] #builds training set of every other image (odd numbered)
    test = p[1:-1:2] #builds test set of every other image (evens)
    print "accuracy of nn_img: ", eval(train, test)

def knn_img():
    # primes image data, builds centroids, calculate and return knn (using roccio)
    d = datasets.load.digits()
    p = []

#nn_text()
nn_img()



def knn_img():
    # primes image data, builds centroids, calculate and return knn (using Roccio)
    d = datasets.load_digits()
    p = []
    centroids = []

    #get list of labels
    labels = set(d.target)
    #p = np.hsack((d.target.reshape(len(d.target),1), d.data))

    for l in labels:
        p,c = 0,0
        for i in range(len(d.images)):
            if d.target[i] == 1:
                p = p + d.data[i]
            c +=1
    #p= np.array((p), float)
    p = p / c
    print c
    centroids.appendnp.hsack((1,p)))

    #print centroids
    print eval(centroids, np.hstack((d.target.reshape(len(d.target)))
                 
        
    
