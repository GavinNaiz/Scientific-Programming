from sklearn.datasets import fetch_lfw_people as LFW 
import pylab
import numpy as np
import glob, Image
# import images, means, sort
ims=LFW(min_faces_per_person=20)

def order_by_brightness(images):
	pylab.gray()
	means = []
	pics = []
	
	for im in images:
		pics.append(im)
		means.append(np.mean(im))
		 
	zipped = zip(means, pics)
	print "zipped:", zipped
	sorted_zipped = sorted(zipped)
	print "sorted_zipped:", sorted_zipped
	print sorted_zipped[0][1]
	i=0
	for m in sorted_zipped:
		pylab.subplot(241+i)
		i+=1
		pylab.imshow(m[1])
	pylab.show()

order_by_brightness(ims.images[:8])

files=glob.glob('/Users/gavin/Documents/pythonprograms/katte/*')
katte = []
for im in files:
	katte.append(Image.open(im).rotate(180).transpose(Image.FLIP_LEFT_RIGHT))
order_by_brightness(katte)	

dkfiles=glob.glob('/Users/gavin/Documents/pythonprograms/DK/*')
DK = []
for im in dkfiles:
	DK.append(Image.open(im).rotate(180).transpose(Image.FLIP_LEFT_RIGHT))
order_by_brightness(DK)	


