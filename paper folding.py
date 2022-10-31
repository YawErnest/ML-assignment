#!/usr/bin/env python
# coding: utf-8

# Problem 1

# In[36]:


THICKNESS=0.00008
folded_thickness=THICKNESS*(2**43)
print("Thickness:{}meters".format(folded_thickness))


# Problem 2

# In[37]:


print ("Thickness:{:2f}kilometers".format(folded_thickness/10000))


# problem 3

# In[38]:


thickness_list=[0.0008]
for i in range (43):
    thickness_list.append(thickness_list[-1]*2)
    print (thickness_list[-1])


# Problem 4

# In[39]:


import time
start=time.time()
THICKNESS=0.00008
folded_thickness=THICKNESS*(2**43)
elapsed_time=time.time()-start
print("time:{}[s]".format(elapsed_time))


# In[53]:


import time
start=time.time()
thickness_list=[0.0008]
for i in range (43):
    thickness_list.append(thickness_list[-1]*2)
    elapsed_time=time.time()-start
print("time:{}[s]".format(elapsed_time))
    


# In[15]:


get_ipython().run_cell_magic('timeit', '', 'thickness_list=[0.0008]\nfor i in range (43):\n    thickness_list.append(thickness_list[-1]*2)\n')


# problem 5

# In[61]:


for i in range (43):
    thickness_list.append(thickness_list[-1]*2)

print (thickness_list[-1])


# problem 6

# In[60]:


import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')
plt.title("THICKNESS OF FOLDED PAPER")
plt.xlabel("number of folds")
plt.ylabel("thickness[m]")
plt.plot(thickness_list)
plt.show()


# problem 7

# In[24]:


plt.title("THICKNESS OF FOLDED PAPER")
plt.xlabel("number of folds")
plt.ylabel("thickness[m]")
plt.plot(thickness_list,color='green')
plt.tick_params(labelsize = 15)
plt.show()


# In[ ]:




