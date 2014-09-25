from sklearn import datasets
from sklearn.neighbors import KNeighborsClassifier as Knn
from sklearn.naive_bayes import GaussianNB
from sklearn.feature_extraction.text import CountVectorizer as vectorizer # makes bow
import matplotlib.pyplot as plt 
import numpy as np 
import pylab
from scipy import stats

# store final accuracy scores to input in bar chart
knn_full_data = []
nb_full_data = []

def learning_curves(my_data, title, istext=False):

	X = my_data.data 
	y = my_data.target
	knn_resultlist=[]
	nb_resultlist=[]

	# changes split
	splitpoint=0.1 
	splitpointlist=[]
	while splitpoint < 0.91:
		split = int(len(X)*splitpoint)
		test_split = int(len(X)*0.1)
		X_train, X_test = X[:split], X[test_split:] 
		y_train, y_test = y[:split], y[test_split:] 
		if istext==True:
			vec = vectorizer()
			vec.fit(X_train, y_train)
			X_train = vec.transform(X_train).toarray()
			X_test = vec.transform(X_test).toarray()

		# applies knn
		clf = Knn(n_neighbors=5) 
		clf.fit(X_train, y_train)
		knn_resultlist.append(clf.score(X_test,y_test))
		
		splitpointlist.append(splitpoint)
		splitpoint+=0.05
		print splitpoint

		#apply Naive Bayes
		gnb = GaussianNB()
		gnb.fit(X_train, y_train)
		nb_resultlist.append(gnb.score(X_test,y_test))

	# print results to check
	print "knn results:", knn_resultlist
	#store final score
	knn_full_data.append(knn_resultlist[-1]*100)
	

	# same as above for nb
	print "nb results:", nb_resultlist
	nb_full_data.append(nb_resultlist[-1]*100)
	
	

	# creates learning curve plots
	plt.plot(splitpointlist, knn_resultlist, c='g', lw=3, label='KNN')
	plt.plot(splitpointlist, nb_resultlist, c='m', lw=3, label='Naive Bayes')
	plt.ylabel('Accuracy')
	plt.xlabel('Training split')
	plt.axis([0.1, 0.9, 0, 1])
	plt.title(title)
	plt.legend(loc='best')
	plt.show()



# apply learning curves to 5 datasets

learning_curves(datasets.load_iris(), 'iris')

learning_curves(datasets.load_digits(), 'digits')
   
path = 'my_books'
data = datasets.load_files(path, charset='latin-1', shuffle=True)
learning_curves(data, 'my_books', istext=True)

path = 'my_electronics'
data = datasets.load_files(path, charset='latin-1', shuffle=True)
learning_curves(data, 'my_electronics', istext=True)

path = 'sports'
data = datasets.load_files(path, charset='latin-1', shuffle=True)
learning_curves(data, 'sports', istext=True)

print knn_full_data
print nb_full_data

# Bar chart
N = 5
KNN = knn_full_data
ind = np.arange(N)
width = 0.35
pylab.bar(ind, KNN, width, color='g', label='KNN')
NB = nb_full_data
pylab.bar(ind+width, NB, width, color='m', label='NB')
pylab.ylabel("Accuracy (%)")
pylab.xticks(ind+width, ['Iris', 'Digits', 'My_books', 'My_electronics', 'Sports'])
pylab.legend(loc="best")
pylab.show()

# apply Wilcoxon

print "Wilcoxon results:", stats.wilcoxon(knn_full_data, nb_full_data,)





