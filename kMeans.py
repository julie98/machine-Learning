from numpy import *

def loadDataSet(fileName):
	dataMat = []
	fr = open(fileName)
	for line in fr.readlines():
		curLine = line.strip().split('\t')
		fltLine = list(map(float, curLine))
		dataMat.append(fltLine)
	return dataMat	#格式为列表嵌套

def distEclud(vectA, vectB):
	return sqrt(sum(power(vectA - vectB, 2)))

def randCent(dataSet, k):	#随机初始化质心
	n = shape(dataSet)[1]	#列数
	centroids = mat(zeros((k,n)))
	for j in range(n):
		minJ = min(dataSet[:,j])
		rangeJ = float(max(dataSet[:,j]) - minJ)
		centroids[:,j] = minJ + rangeJ * random.rand(k,1)	#随机生成的质心在数据边界内
	return centroids

def kMeans(dataSet, k, distMeas=distEclud, createCent=randCent):
	m = shape(dataSet)[0]	#行数
	clusterAssment = mat(zeros((m,2)))	#簇分配结果矩阵，第一列为簇index，第二列为距离
	centroids = createCent(dataSet, k)
	clusterChanged = True
	while clusterChanged:	#反复迭代，直到所有数据点的簇分配结果不再改变
		clusterChanged = False
		for i in range(m):
			minDist = inf	#infinity
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

#show plot
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

print(clusterAssment)
showCluster(dataSet, k, centroids, clusterAssment)