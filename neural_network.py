# -*- coding: utf-8 -*-
"""neural network.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/16pDH6v9mRPLI8Rp3dTNKU70Bb_tQ-auJ
"""

import numpy as np
import matplotlib.pyplot as plt

from sklearn.metrics import accuracy_score
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score
from sklearn.metrics import f1_score

from keras.datasets import mnist
(x_train,y_train),(x_test,y_test)=mnist.load_data()

print(x_train.shape
      )
print(x_test.shape)
print(x_train[0].dtype)

x_train=x_train.reshape(-1,784)
x_test=x_test.reshape(-1,784)
print(x_train.shape)
print(x_test.shape)

# Commented out IPython magic to ensure Python compatibility.
import matplotlib.pyplot as plt
# %matplotlib inline
index=0
image=x_train[index].reshape(28,28)
plt.imshow(image,'gray')
plt.title('label :{}'.format(y_train[index]))
plt.show()

x_train=x_train.astype(np.float)
x_test=x_test.astype(np.float)
x_train/=255
x_test/=255
print(x_train.max())
print(x_test.min())

from sklearn.model_selection import train_test_split

x_train,x_val,y_train,y_val=train_test_split(x_train,y_train,test_size=0.2)
print(x_train.shape)
print(x_val.shape)

from sklearn.preprocessing import OneHotEncoder
enc=OneHotEncoder(handle_unknown='ignore',sparse=False)
y_train_one_hot =enc.fit_transform(y_train[:,np.newaxis])
y_val_one_hot=enc.transform(y_val[:,np.newaxis])
print(y_train.shape)
print(y_train_one_hot.shape)
print(y_train_one_hot.dtype)

class GetMiniBatch:
    """
    ミニバッチを取得するイテレータ

    Parameters
    ----------
    X : 次の形のndarray, shape (n_samples, n_features)
      訓練データ
    y : 次の形のndarray, shape (n_samples, 1)
      正解値
    batch_size : int
      バッチサイズ
    seed : int
      NumPyの乱数のシード
    """
    def __init__(self, X, y, batch_size = 20, seed=0):
        self.batch_size = batch_size
        np.random.seed(seed)
        shuffle_index = np.random.permutation(np.arange(X.shape[0]))
        self._X = X[shuffle_index]
        self._y = y[shuffle_index]
        self._stop = np.ceil(X.shape[0]/self.batch_size).astype(np.int)

    def __len__(self):
        return self._stop

    def __getitem__(self,item):
        p0 = item*self.batch_size
        p1 = item*self.batch_size + self.batch_size
        return self._X[p0:p1], self._y[p0:p1]        

    def __iter__(self):
        self._counter = 0
        return self

    def __next__(self):
        if self._counter >= self._stop:
            raise StopIteration()
        p0 = self._counter*self.batch_size
        p1 = self._counter*self.batch_size + self.batch_size
        self._counter += 1
        return self._X[p0:p1], self._y[p0:p1]

get_mini_batch = GetMiniBatch(x_train, y_train, batch_size=20)

print(len(get_mini_batch)) # 2400
print(get_mini_batch[5]) # 5番目のミニバッチが取得できる
for mini_x_train, mini_y_train in get_mini_batch:
    # このfor文内でミニバッチが使える
    pass

class ScratchSimpleNeuralNetrowkClassifier():
    
    def __init__(self, n_epoch=50, n_features=784, n_nodes1=400, n_nodes2=200, 
                 n_output=10, sigma=0.01, n_batch=20, 
                 activate_function_key='tanh', lr = 0.01, verbose = False):
        
        self.n_epoch = n_epoch
        self.n_features = n_features
        self.n_nodes1 = n_nodes1
        self.n_nodes2 = n_nodes2
        self.n_output = n_output
        self.sigma = sigma
        self.n_batch = n_batch
        self.activate_function_key = activate_function_key
        self.lr = lr
        self.verbose = verbose
        
    def initial_weight(self):
        self.W1 = self.sigma * np.random.randn(self.n_features, self.n_nodes1)
        self.b1 = np.zeros(self.n_nodes1)
        self.W2 = self.sigma * np.random.randn(self.n_nodes1, self.n_nodes2)
        self.b2 = np.zeros(self.n_nodes2)
        self.W3 = self.sigma * np.random.randn(self.n_nodes2, self.n_output)
        self.b3 = np.zeros(self.n_output)
        
    def activation_function(self,X):
        if self.activate_function_key == 'sigmoid':
            return 1/(1+np.exp(-X))
        
        elif self.activate_function_key == 'tanh':
            return np.tanh(X)
    
    def softmax(self,X):
        
        return np.exp(X-np.max(X))/np.sum(np.exp(X-np.max(X)),axis=1,keepdims=True)
    
    def loss_function(self,y,yt):
        delta = 1e-7
        return -np.mean(yt*np.log(y+delta))
    
    def gradient_descent(self,X,y,yt):
        
            # 3rd layer
            delta_a3 = (y-yt)/self.n_batch
            delta_b3 = np.sum(delta_a3,axis=0)
            delta_W3 = np.dot(self.z2.T,delta_a3)
            delta_z2 = np.dot(delta_a3,self.W3.T)
        
            self.W3 -= self.lr*delta_W3
            self.b3 -= self.lr*delta_b3
        
            # 2nd layer
            if self.activate_function_key == 'sigmoid':
                delta_a2 = delta_z2*(1-self.activation_function(self.z2))*self.activation_function(self.z2)
            
            elif self.activate_function_key == 'tanh':
                delta_a2 = delta_z2*(1-np.tanh(self.z2)**2)
            
            delta_b2 = np.sum(delta_a2,axis=0)
            delta_W2 = np.dot(self.z1.T,delta_a2)
            delta_z1 = np.dot(delta_a2,self.W2.T)
        
            self.W2 -= self.lr*delta_W2
            self.b2 -= self.lr*delta_b2
        
            # 1st layer
            if self.activate_function_key == 'sigmoid':
                delta_a1 = delta_z1*(1-self.activation_function(self.z1))*self.activation_function(self.z1)
            
            elif self.activate_function_key == 'tanh':
                delta_a1 = delta_z1*(1-np.tanh(self.z1)**2)
                
            delta_b1 = np.sum(delta_a1,axis=0)
            delta_W1 = np.dot(X.T,delta_a1)
        
            self.W1 -= self.lr*delta_W1
            self.b1 -= self.lr*delta_b1
                
    def fit(self, X, y, X_val=False, y_val=False):
       
        # Initialize weights
        self.initial_weight()
        
        # List to record the loss_function for each epoch
        self.log_loss = []
        self.log_loss_val = []
        
        # Evaluate the estimation of Train data per epoch: Accuracy
        self.log_acc = []
        self.log_acc_val = []
        
        for epoch in range(self.n_epoch):
            # Mini-batch processing
            get_mini_batch = GetMiniBatch(X, y, batch_size=self.n_batch)
            
            self.loss = 0
            self.true_y = np.array([])
            self.pred_y = np.array([])
            
            for mini_X_train, mini_y_train in get_mini_batch:
            
                # 1st layer
                self.z1 = self.activation_function(np.dot(mini_X_train,self.W1) + self.b1)
            
                # 2nd layer
                self.z2 = self.activation_function(np.dot(self.z1,self.W2) + self.b2)
            
                # 3rd layer (softmax function)
                yhat = self.softmax(np.dot(self.z2,self.W3) + self.b3)
                
                # Backpropagation (stochastic gradient descent method)）
                self.gradient_descent(mini_X_train,yhat,mini_y_train)
                
                # Record correct and estimated values for mini-batch data
                self.true_y = np.concatenate([self.true_y,np.argmax(mini_y_train,axis=1)])
                self.pred_y = np.concatenate([self.pred_y,np.argmax(yhat,axis=1)])
                
                # Loss function
                self.loss += self.loss_function(yhat,mini_y_train)
            
            # Record the loss function for each epoch
            self.log_loss.append(self.loss/len(get_mini_batch))
            
            # Accuracy
            acc = accuracy_score(self.true_y, self.pred_y)
            self.log_acc.append(acc)
            
            # Calculate once Val data has been entered
            if (type(X_val) != bool):
                # 1st layer
                self.z1_val = self.activation_function(np.dot(X_val,self.W1) + self.b1)
            
                # 2nd layer
                self.z2_val = self.activation_function(np.dot(self.z1_val,self.W2) + self.b2)
            
                # 3rd layer (softmax function)
                yhat_val = self.softmax(np.dot(self.z2_val,self.W3) + self.b3)
                
                # Loss function
                self.loss_val = self.loss_function(yhat_val,y_val)
                self.log_loss_val.append(self.loss_val)
                
                # Accuracy
                
                acc_val = accuracy_score(np.argmax(y_val,axis=1), np.argmax(yhat_val,axis=1))
                self.log_acc_val.append(acc_val)
            
            #When verbose is set to true, output the learning process and other information.
            if self.verbose:
                print('epoch:{:>3} loss:{:>8,.3f} acc:{:>5,.3f}'.format(epoch,self.loss/self.n_batch,acc))
            
    def predict(self, X):
       
        # 1st layer
        self.pred_z1 = self.activation_function(np.dot(X,self.W1) + self.b1)
            
        # 2nd layer
        self.pred_z2 = self.activation_function(np.dot(self.pred_z1,self.W2) + self.b2)
        
        return np.argmax(np.dot(self.pred_z2,self.W3) + self.b3, axis=1)

import numpy as np
n_features=784
n_nodes1=400
n_nodes2=200
n_outputs=10
sigma=0.01
w1=sigma*np.random.randn(n_features,n_nodes1)
print('w1',w1.shape)

w1=sigma*np.random.randn(n_features,n_nodes1)
b1=sigma*np.random.randn(n_nodes1)
w2=sigma*np.random.randn(n_nodes1,n_nodes2)
b2=sigma*np.random.randn(n_nodes2)
w3=sigma*np.random.randn(n_nodes2,n_outputs)
b3=sigma*np.random.randn(n_outputs)
print('w1',w1.shape)
print('b1',b1.shape)
print('w2',w2.shape)
print('b2',b2.shape)
print('w3',w3.shape)
print('b3',b3.shape)

x=x_train[0:20]

z1 = np.dot(x,w1)# + b1
print('z1.shape:',z1.shape)
print(z1)

sig1 = 1/(1+np.exp(-z1))
print('sig1.shape:',sig1.shape)
print(sig1)

z2=np.dot(sig1,w2)+b2
print('z2.shape',z2.shape)
print(z2)

sig2 = 1/(1+np.exp(-z2))
print('sig2.shape:',sig2.shape)
print(sig2)

z3=np.dot(sig2,w3)+b3
print('z3.shape',z3.shape)
print(z3)

sfmax=np.zeros([len(x),10])
for i in range(20):
    sfmax[i]=np.exp(z3[i])/np.sum(np.exp(z3[i]),axis=0)
print('sfmax.shape',sfmax.shape)
print(sfmax) 
print(np.sum(sfmax))

softmax=np.exp(z3).T/np.sum(np.exp(z3),axis=1)
print('softmax.shape',softmax.shape)
print(softmax.T)
print(np.sum(softmax))

softmax=np.exp(z3)/np.sum(np.exp(z3),axis=1,keepdims=True)
print('softmax.shape',softmax.shape)
print(softmax)
print(np.sum(softmax))

np.tanh(z1)

(np.exp(z1)-np.exp(-z1))/(np.exp(z1)+np.exp(-z1))

y=y_train_one_hot[0:20]
loss=-y*np.log(sfmax)/len(y)
print('shape:\n',loss.shape)
print(loss)

delta_a3=sfmax-y
delta_b3=np.sum(delta_a3,axis=0)
delta_w3=np.dot(z2.T,delta_a3)
delta_z2=np.dot(delta_a3,w3.T)

print(delta_a3.shape)
print(delta_b3.shape)
print(delta_w3.shape)
print(delta_z2.shape)

delta_a2=delta_z2*(-np.tanh(z2)**2)
delta_b2=np.sum(delta_a2,axis=0)
delta_w2=np.dot(z1.T,delta_a2)
delta_z1=np.dot(delta_a2,w2.T)

print(delta_a2.shape)
print(delta_b2.shape)
print(delta_w2.shape)
print(delta_z1.shape)

delta_a1=delta_z1*(1-np.tanh(z1)**2)
delta_b1=np.sum(delta_a1,axis=0)
delta_w1=np.dot(x.T,delta_a1)

print(delta_a1.shape)
print(delta_b1.shape)
print(delta_w1.shape)

clf=ScratchSimpleNeuralNetrowkClassifier(n_epoch=30,n_features=784,n_nodes1=400,n_nodes2=200,n_output=10,sigma=0.01,n_batch=100,activate_function_key='tanh',lr=0.01, verbose = True)
clf.fit(x_train,y_train_one_hot,x_val,y_val_one_hot)
y_pred=clf.predict(x_val)

print(y_pred)

accuracy=accuracy_score(y_val,y_pred)
print('accuracy:{:.3f}'.format(accuracy))

fig=plt.subplots(figsize=(12,8))
plt.rcParams["font.size"]=20
plt.plot(clf.log_loss,'rs--')
plt.plot(clf.log_loss_val,'bo--');

fig=plt.subplots(figsize=(12,8))
plt.rcParams["font.size"]=20
plt.plot(clf.log_acc,'rs--')
plt.plot(clf.log_acc_val,'bo--');

import numpy as np
import matplotlib.pyplot as plt

num=5
print('Estimation Reseult/correct results')

true_false=y_pred==y_val
false_list=np.where(true_false==False)[0].astype(np.int)
if false_list.shape[0]<num:
   num=false_list[0]
fig=plt.figure(figsize=(6,6))
fig.subplots_adjust(left=0, right=0.8, bottom=0, top=0.8, hspace=1, wspace=0.3)
for i in range(num):
    ax=fig.add_subplot(6,6,i+1,xticks=[],yticks=[])
    ax.set_title("{}/{}".format(y_pred[false_list[i]],y_val[false_list[i]]))
    ax.imshow(x_val.reshape(-1,28,28)[false_list[i]],cmap='gray')