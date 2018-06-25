from numpy import *

def loadDataSet(fileName):
	dataMat = []
	fr = open(fileName)
	for line in fr.readlines():
		curLine = line.strip().split('\t')
		fltLine = list(map(float, curLine))
		dataMat.append(fltLine)
	return dataMat

def distEclud(vectA, vectB):
	return sqrt(sum(power(vectA - vectB, 2)))

def randCent(dataSet, k):
	n = shape(dataSet)[1]
	centroids = mat(zeros((k,n)))
	for j in range(n):
		minJ = min(dataSet[:,j])
		rangeJ = float(max(dataSet[:,j]) - minJ)
		centroids[:,j] = minJ + rangeJ * random.rand(k,1)
	return centroids

def kMeans(dataSet, k, distMeas=distEclud, createCent=randCent):
	m = shape(dataSet)[0]
	clusterAssment = mat(zeros((m,2)))
	centroids = createCent(dataSet, k)
	clusterChanged = True
	while clusterChanged:
		clusterChanged = False
		for i in range(m):
			minDist = inf
			minIndex = -1
			for j in range(k):
				distJI = distMeas(centroids[j,:], dataSet[i,:])
				if distJI < minDist:
					minDist = distJI
					minIndex = j
			if clusterAssment[i,0] != minIndex:
				clusterChanged = True
				clusterAssment[i,:] = minIndex, minDist**2
		print(centroids)
		for cent in range(k):
			ptsInClust = dataSet[nonzero(clusterAssment[:,0].A==cent)[0]]
			centroids[cent,:] = mean(ptsInClust, axis=0)
	return centroids, clusterAssment


import matplotlib.pyplot as plt   
def showCluster(dataSet, k, centroids, clusterAssment):
    m, dim = shape(dataSet)

    if dim != 2:  
        print ("Sorry! I can not draw because the dimension of your data is not 2!")  
        return 1  

    mark = ['or', 'ob', 'og', 'ok', '^r', '+r', 'sr', 'dr', '<r', 'pr'] 
    if k > len(mark):  
        print ("Sorry! Your k is too large! ")  
        return 1 
    
    #draw all samples
    for i in range(m):
        markIndex = int(clusterAssment[i,0]) #为样本指定颜色
        plt.plot(dataSet[i,0], dataSet[i,1], mark[markIndex])
            
    #draw the centroids
    for i in range(k):
        plt.plot(centroids[i,0], centroids[i,1], marker = 'x', color = 'purple', markersize=12)
        #用marker来指定质心样式，用color和markersize来指定颜色和大小
            
    plt.show()


#test
dataSet = mat(loadDataSet('data.txt'))
print(dataSet)
k = 3
centroids, clusterAssment = kMeans(dataSet, k)
print(centroids)
print(clusterAssment)
showCluster(dataSet, k, centroids, clusterAssment)