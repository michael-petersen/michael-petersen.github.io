#!/usr/bin/env python
# coding: utf-8

# # Demystifying Multichannel Singular Spectral Analysis
# ### Mike Petersen, 16 May 2022
# 
# A visual approach to the linear algebra steps of MSSA. This tutorial follows Weinberg & Petersen (2021) -- hereafter WP21 -- with some modest changes that will appear in Johnson et al. (2022).
# 
# With 9 worked examples.
# 

# Goals:
# 1. Use numpy to perform linear algebra steps
# 2. Run pedagogical examples
# 3. Build a playground for intuition development
# 4. Let you loose on (small) MSSA problems!

# Outline:
# 1. As MSSA is complicated, start with *SSA*, where we consider a single input stream.
# 2. Develop a range of examples to showcase different use cases for SSA.
# 3. Move to an MSSA implementation.
# 4. Introduce the more powerful C++ tools.

# In[ ]:


# standard python modules
import numpy as np;import time;import copy

# plotting utilities
import matplotlib.pyplot as plt;import matplotlib as mpl;import matplotlib.cm as cm;import matplotlib.colors as colors
get_ipython().run_line_magic('matplotlib', 'inline')
cmap = mpl.cm.inferno;mpl.rcParams['xtick.labelsize'] = 12;mpl.rcParams['ytick.labelsize'] = 12;mpl.rcParams['font.weight'] = 'medium';mpl.rcParams['axes.linewidth'] = 1.5;mpl.rcParams['xtick.major.width'] = 1.5;mpl.rcParams['xtick.minor.width'] = 0.75;mpl.rcParams['xtick.minor.visible'] = True;mpl.rcParams['ytick.major.width'] = 1.5;mpl.rcParams['ytick.minor.width'] = 0.75;mpl.rcParams['ytick.minor.visible'] = True


# ### Example 0
# Let's start with a very simple case: a single sinusoid.

# In[ ]:


ndim = 1   # as this is SSA, we only have one dimension of data
N    = 200 # set the length of the data

data = np.zeros([ndim,N])
data[0] = np.cos(np.arange(0,N,1)*np.pi/12.)

plt.figure(figsize=(5,3))
plt.plot(data[0],color='black')
plt.title('input data series')
plt.ylabel('amplitude')
_ = plt.xlabel('sample number (N)')


# The first ingredient is some prescription to _embed_ the data. At this step, we are creating a trajectory matrix that is comprised of _lagged_ copies of the input data stream. This constructs a matrix where the antidiagonals have the same value. We will call this matrix $T$, following WP21, equation 10.

# In[ ]:


def embed_data(data,L,K,ndim=1,norm=False):
    """
    Build embedded time series, Y.
    Follows the embedding strategy of Weinberg \& Petersen (2021)
    Augmented vectors are the rows.
    
    inputs
    ---------
    data     : (array) data streams, set up as data[0],data[1],data[2]...
    L        : (int) the window length
    K        : (int) the length of augmented vectors
    ndim     : (int, default 1) number of data streams to consider
    norm     : (bool, default False) detrend the data?
    
    returns
    ---------
    Y        : (array) the trajectory matrix
    """
    Y = np.zeros([L,K*ndim])
    for n in range(0,ndim):
        for j in range(0,K):
            for i in range(0,L):
                if norm:
                    Y[i, K*n+j] = (data[n][i + j] - np.nanmean(data[n]))/np.nanstd(data[n])
                else:
                    Y[i, K*n+j] = data[n][i + j]
    print('Shape of Y:',Y.shape)
    return Y


# In[ ]:


L = 50   # set the window length
K = N-L+1 # calculate the length of the lagged series

#embed the data
Y = embed_data(data,L,K,1)

plt.figure()
plt.imshow(Y,cmap=cm.coolwarm)
plt.title('trajectory matrix')
plt.colorbar(label='amplitude')
plt.ylabel('rows are windowed (length L)')
_ = plt.xlabel('columns are lagged vectors (length K)')


# The second step is to construct the lag-covariance matrix. We have two choices here:
# 1. Reconstruct the full dimensionality, $C = \frac{1}{K}T^T\cdot T$, where the matrix is $K\times K$.
# 2. Reconstruct the reduced dimensionality, $C = \frac{1}{K}T\cdot T^T$, where the matrix is $L\times L$.
# 
# We will here choose option 1, but will note the differences below. This is equation 11 in WP21.

# In[ ]:


def make_covariance(Y,K,full=True):
    """
    estimate the covariance matrix C_X, using the formula in eq 9
    
    inputs
    ---------
    Y     : (array) the trajectory matrix
    K     : (array) the length of the augmented vectors
    
    returns
    ---------
    C     : (array) the covariance matrix
    
    """
    if full:
        C = np.dot(Y.T,Y)/K
    else:
        C = np.dot(Y,Y.T)/K
    print('C shape:',C.shape)
    return C


# In[ ]:


C = make_covariance(Y,K)

plt.figure()
plt.imshow(C,cmap=cm.coolwarm)
plt.title('covariance matrix')
plt.colorbar(label='amplitude')
plt.ylabel('dim 1 (length K)')
_ = plt.xlabel('dim 2 (length K)')


# Now we get to the magic: making the principal components, singular vectors, and empirical orthogonal functions. This is accomplished by a singular value decomposition step.
# 
# Following equation 12 of WP21, use SVD: $$C = U\cdot \Lambda \cdot V.$$ SVD takes as an input $C$ and returns $U$, $\Lambda$, and $V$. The columns of $U$ are the eigenvectors (or empirical orthogonal functions EOF, $L$ with length $K$), which we immediately use to construct the principal components (with length $K$) by projecting the time series onto the EOF: $$P = Y\cdot U.$$
# 

# Other notes:
# 1. $\Lambda$ are the singular values. These are typicall ordered largest to smallest by SVD algorithms.
# 2. $U = V^T$, to SVD approximation precision.

# In[ ]:



def make_pcs(C,Y,ndim=1):
    """perform the SVD on the covariance matrix to construct the PCs.
    
    inputs
    ---------
    C     : (array) the covariance matrix   
    Y     : (array) the trajectory matrix
    ndim  : (int, default 1) the number of MSSA dimensions
    
    returns
    ---------
    PCs   : (array) the principal components (in rows)
    U     : (array)
    S     : (vector) the list of singular vectors
    
    
    
    """
    U,SV,V = np.linalg.svd(C, full_matrices=True)
    
    #print(U.shape,SV.shape,V.shape)

    # the columns of U are the left singular vectors
    # the columns of V are the right singular vectors
    # SV are the singular values
    
    # to recover the PCs, dot the trajectory matrix and the left singular vectors
    # the projection of the time series Y onto the EOF (eigenvectors), U
    PCs = np.dot(Y,U)

    print('PC shape:',PCs.shape)
    print('Left singular vector shape:',U.shape)
    return PCs,U,SV


# In[ ]:


# run it!
PC,EOF,SV = make_pcs(C,Y)


# In[ ]:


# the columns of EOFs are the set of empirical orthogonal vectors: plot them!
plt.figure()
for i in range(9,-1,-1):
    plt.plot(EOF[:,i],color=cm.viridis(i/9.))
    
plt.title('empirical orthogonal functions')
plt.ylabel('EOF value')
_ = plt.xlabel('abscissa (length K)')


# In[ ]:


# the columns of PCs are the set of principal components: plot them!
plt.figure()
for i in range(9,-1,-1):
    plt.plot(PC[:,i],color=cm.viridis(i/9.))
    
plt.title('principal components')
plt.ylabel('PC value')
_ = plt.xlabel('abscissa (length K)')


# In[ ]:


# plot the run of singular values
plt.figure()
SVnonoise = np.copy(SV) # save these for later...
plt.plot(np.log10(SV),color='black')
plt.title('singular value curve')
plt.ylabel('singular value value')
_ = plt.xlabel('PC number (length K)')


# We aren't quite done yet: we want to reconstruct the contribution to the input time series from each PC. This is accomplished through an _antidiagonal average_ of the transformed PCs. In WP21, we explicitly write the element reconstruction; in this implementation we will play a numpy trick to accomplish the antidiagonal average:
# 1. Select the PC to use for reconstruction, $P$, and the corresponding EOF, $E$.
# 2. Calculate $A = P^T\cdot E$.
# 3. Compute the antiagonal average of $A$ by reversing the matrix and using numpy's built in .diagonal call to compute the average.

# In[ ]:


def reconstruct(PC,EOF,pcnum,K,nd=1):
    """Average antidiagonal elements of a 2d array
    
    inputs
    -----------
    PC    : (array) PCs
    EOF   : (array) empirical orthogonal functions
    pcnum : (int) which PC to consider
    K     : (int) length of the augmented vectors
    ndim  : (int, default 0) which MSSA dimension to consider

    returns
    -------
    x1d   : (np.array) 1d numpy array representing averaged antidiangonal elements of A

    thanks to: https://codereview.stackexchange.com/questions/195635/numpy-2d-array-anti-diagonal-averaging
    """
    A = np.dot(np.array([PC[:,pcnum]]).T,np.array([EOF[K*nd:K*(nd+1),pcnum]]))
    
    x1d = [np.mean(A[::-1, :].diagonal(i)) for i in range(-A.shape[0] + 1, A.shape[1])]

    return np.array(x1d)


# In[ ]:


O = reconstruct(PC,EOF,0,K,0)

plt.figure()
plt.plot(O,color='black')
plt.plot(data[0],color='grey',linestyle='dashed')
plt.title('first PC reconstruction')
plt.xlabel('sample number (length $N$)')
plt.ylabel('amplitude')


# In[ ]:


O = reconstruct(PC,EOF,0,K,0)
O += reconstruct(PC,EOF,1,K,0)

plt.figure()
plt.plot(O,color='black')
plt.plot(data[0],color='grey',linestyle='dashed')
plt.title('first PC $group$ reconstruction')
plt.xlabel('sample number (length $N$)')
plt.ylabel('amplitude')


# That's it! SSA in a nutshell. We followed four steps:
# 1. _embed_ the data
# 2. _lag_ the data
# 3. _decompose_ the covariance matrix
# 4. _reconstruct_ the decomposition (selectively!)

# The final step, reconstruction, is where much interpretation creeps in, and is the primary subject of automation research in the group.

# Extensions: 
# 
# 1. How do the results change with window length?
# 2. What happens when we detrend (and are there other schemes)?

# ### Example 1
# 
# Let's go through another example to show one of the MSSA power points: removing noise.
# 
# This time, we'll construct a noisy data stream.

# In[ ]:


ndim = 1
N = 200
L = 50
K = N-L+1

data = np.zeros([ndim,N])

data[0] = np.cos(np.arange(0,N,1)*np.pi/12.) # start with a simple sinusoid
cleandata = np.copy(data[0]) # record the clean data

# add some gaussian noise, at the level of the signal!
noiselevel = 1.0
data[0] += np.random.normal(0.,noiselevel,size=data[0].size)

plt.figure(figsize=(5,3))
plt.plot(data[0],color='black')
plt.title('input data series')
plt.ylabel('amplitude')
_ = plt.xlabel('sample number (N)')


# In[ ]:


# perform the SSA steps
Y = embed_data(data,L,K,1)
C = make_covariance(Y,K)
PC,EOF,SV = make_pcs(C,Y)
O = reconstruct(PC,EOF,0,K,0)
O += reconstruct(PC,EOF,1,K,0)

plt.figure()
plt.plot(O,color='black')
plt.plot(cleandata,color='gray',linestyle='dashed')
plt.plot(data[0],color='red',linestyle='dashed')
plt.title('first PC $group$ reconstruction')
plt.xlabel('sample number (length $N$)')
plt.ylabel('amplitude')


# In[ ]:


O = reconstruct(PC,EOF,2,K,0)
for pc in range(3,45):
    O += reconstruct(PC,EOF,pc,K,0)

plt.figure()
plt.plot(O,color='black')
plt.plot(cleandata,color='gray',linestyle='dashed')
plt.plot(data[0],color='red',linestyle='dashed')
plt.title('second PC $group$ reconstruction')
plt.xlabel('sample number (length $N$)')
plt.ylabel('amplitude')


# We've shown that we can separate the signal from the noise very efficiently using MSSA.
# 
# Extensions: 
# 1. What does a pure noise field look like on reconstruction?
# 2. How large can the noise level be before we cannot recover the signal?
# 3. How does biased noise affect the results?

# In[ ]:


# check in on the SV curve
plt.figure()
plt.plot(np.log10(SV),color='black')
plt.plot(np.log10(SVnonoise),color='gray',linestyle='dashed')
plt.title('singular value curve')
plt.ylabel('singular value value')
_ = plt.xlabel('PC number (length K)')


# ### Example 2
# 
# What about an example with a second component: slow growth over time? Can we reconstruct that?
# 
# We'll keep noise for this example.

# In[ ]:


ndim = 1
N = 200
L = 50
K = N-L+1

data = np.zeros([ndim,N])

data[0] = np.cos(np.arange(0,N,1)*np.pi/12.) # start with a simple sinusoid

# add a quadratic (slow) trend
data[0] += 0.0001*(np.arange(0,N,1)**2.)

cleandata = np.copy(data[0]) # record the clean data


# add some gaussian noise, at the level of the signal!
noiselevel = 1.0
data[0] += np.random.normal(0.,noiselevel,size=data[0].size)

plt.figure(figsize=(5,3))
plt.plot(data[0],color='black')
plt.title('input data series')
plt.ylabel('amplitude')
_ = plt.xlabel('sample number (N)')


# In[ ]:


# perform the SSA steps
Y = embed_data(data,L,K,1)
C = make_covariance(Y,K)
PC,EOF,SV = make_pcs(C,Y)
O = reconstruct(PC,EOF,0,K,0)

plt.figure()
plt.plot(O,color='black')
plt.plot(cleandata,color='gray',linestyle='dashed')
plt.plot(data[0],color='red',linestyle='dashed')
plt.title('first PC reconstruction')
plt.xlabel('sample number (length $N$)')
plt.ylabel('amplitude')


# In[ ]:


#O = reconstruct(PC,EOF,0,K,0)
O = reconstruct(PC,EOF,1,K,0)
O += reconstruct(PC,EOF,2,K,0)

plt.figure()
plt.plot(O,color='black')
plt.plot(cleandata,color='gray',linestyle='dashed')
plt.plot(data[0],color='red',linestyle='dashed')
plt.title('second PC $group$ reconstruction')
plt.xlabel('sample number (length $N$)')
plt.ylabel('amplitude')


# This is a good time to introduce a tool for interpretation: the $w$-correlation matrix. We won't go in to the calculation details -- see WP21 eq 19 -- but the $w$-correlation matrix tries to find similarity between PCs, which often indicate that they are a group.

# In[ ]:


def wCorr(R):
    """
    make the w-correlation matrix.
    
    inputs
    --------
    R     : (array) the reconstructed elements, stacked.
    
    returns
    -----------
    wcorr : (array) the w-correlation matrix
    """
    
    numT   = R.shape[0]
    numW   = R.shape[1]
    Lstar  = np.nanmin([numT - numW, numW]);
    Kstar  = np.nanmax([numT - numW, numW]);

    wcorr = np.zeros([numW, numW])
    for m in range(0,numW):
        for n in range(m,numW):
            for i in range(0,numT):
                if   (i < Lstar): w = i;
                elif (i < Kstar): w = Lstar;
                else            : w = numT - i + 1;
                
                wcorr[m, n] += w * R[i, m]*R[i, n];

    #// Normalize
    for m in range(0,numW):
        for n in range(m+1,numW):
            if (wcorr[m, m]>0.0 and wcorr[n, n]>0.0):
                wcorr[m, n] /= np.sqrt(wcorr[m, m]*wcorr[n, n]);


    #// Unit diagonal
    for m in range(0,numW): 
        wcorr[m, m] = 1.0;

    #// Complete
    for m in range(0,numW):
        for n in range(0,m):
            wcorr[m, n] = wcorr[n, m];

    return wcorr;


# In[ ]:


# select a maximum PC to consider
pcmax = 10

# build a reconstruction matrix (PC contributions stacked on top of one another)
RC = np.zeros([N,pcmax])
for i in range(0,pcmax):
    RC[:,i] = reconstruct(PC,EOF,i,K,nd=0)
    
# compute the w-correlation matrix
R = wCorr(RC)

plt.imshow(np.log10(np.abs(R)),cmap=cm.Greys)
plt.colorbar(label='log correlation (higher is more correlated)')
plt.xlabel('PC number')
_ = plt.ylabel('PC number')


# Note that the $w$-correlation matrix doesn't tell us about significance -- just which PCs are likely to be related.

# ### Example 3 (optional)
# 
# What about two sinusoidal signals on top of each other?
# 
# No noise in this example.

# In[ ]:


ndim = 1
N = 200
L = 50
K = N-L+1

data = np.zeros([ndim,N])

data[0] = np.cos(np.arange(0,N,1)*np.pi/12.) # start with a simple sinusoid
sample1data = np.copy(data[0]) # record the first signal

# add a chirp
omega2 = 0.05; chirp = 4.
omega = omega2*(1.0 + chirp*np.arange(0,N,1)/N);
data[0] += 0.5*np.cos(np.arange(0,N,1)*omega)

sample2data = 0.5*np.cos(np.arange(0,N,1)*omega) # record the second signal

cleandata = np.copy(data[0]) # record the clean data

plt.figure(figsize=(5,3))
plt.plot(data[0],color='black')
plt.plot(sample1data,color='gray',lw=1.)
plt.plot(sample2data,color='gray',lw=1.)

plt.title('input data series')
plt.ylabel('amplitude')
_ = plt.xlabel('sample number (N)')


# In[ ]:


# perform the SSA steps
Y = embed_data(data,L,K,1)
C = make_covariance(Y,K)
PC,EOF,SV = make_pcs(C,Y)
O = reconstruct(PC,EOF,0,K,0)
O += reconstruct(PC,EOF,1,K,0)

plt.figure()
plt.plot(O,color='black')
plt.plot(cleandata,color='gray',linestyle='dashed')
plt.plot(data[0],color='red',linestyle='dashed')
plt.title('first PC $group$ reconstruction')
plt.xlabel('sample number (length $N$)')
plt.ylabel('amplitude')


# In[ ]:


O = reconstruct(PC,EOF,2,K,0)
O += reconstruct(PC,EOF,3,K,0)
O += reconstruct(PC,EOF,4,K,0)
O += reconstruct(PC,EOF,5,K,0)

plt.figure()
plt.plot(O,color='black')
plt.plot(cleandata,color='gray',linestyle='dashed')
plt.plot(data[0],color='red',linestyle='dashed')
plt.title('second PC $group$ reconstruction')
plt.xlabel('sample number (length $N$)')
plt.ylabel('amplitude')


# In[ ]:


# select a maximum PC to consider
pcmax = 10

# build a reconstruction matrix (PC contributions stacked on top of one another)
RC = np.zeros([N,pcmax])
for i in range(0,pcmax):
    RC[:,i] = reconstruct(PC,EOF,i,K,nd=0)
    
# compute the w-correlation matrix
R = wCorr(RC)

plt.imshow(np.log10(np.abs(R)),cmap=cm.Greys)
plt.colorbar(label='log correlation (higher is more correlated)')
plt.xlabel('PC number')
_ = plt.ylabel('PC number')


# Extensions: 
# 1. What happens when the signals do not have different amplitudes?
# 2. How can we get better separation of the signals?

# ### Example 4 (optional)
# 
# An example of _how_ SSA works: sawtooth reconstruction.

# In[ ]:


ndim = 1
N = 100
L = 50
K = N-L+1

data = np.zeros([ndim,N])

data[0] = (np.arange(0,N,1)*0.01) % 0.3

cleandata = np.copy(data[0]) # record the clean data

plt.figure(figsize=(5,3))
plt.plot(data[0],color='black')
plt.title('input data series')
plt.ylabel('amplitude')
_ = plt.xlabel('sample number (N)')


# In[ ]:


# perform the SSA steps
Y = embed_data(data,L,K,1)
C = make_covariance(Y,K)
PC,EOF,SV = make_pcs(C,Y)


plt.figure()

for i in range(0,20,2):
    if i == 0:
        O = reconstruct(PC,EOF,0,K,0)
        O += reconstruct(PC,EOF,1,K,0)
    else:
        O += reconstruct(PC,EOF,i,K,0)
        O += reconstruct(PC,EOF,i+1,K,0)
    
    plt.plot(O,color=cm.viridis_r(i/9.))


plt.plot(data[0],color='red',linestyle='dashed')
plt.title('first PC $group$ reconstruction')
plt.xlabel('sample number (length $N$)')
plt.ylabel('amplitude')


# ### Example 5
# 
# We haven't even discussed the _M_ in MSSA yet: what can we do with multiple dimensions?
# 
# Luckily, we've set up the definitions above to be MSSA-aware, so we can just throw a couple of switches and perform MSSA. Let's start with the simplest case: duplicating the sine wave twice as the input.

# In[ ]:


ndim = 2   # as this is SSA, we only have one dimension of data
N    = 200 # set the length of the data

data = np.zeros([ndim,N])
data[0] = np.cos(np.arange(0,N,1)*np.pi/12.)
data[1] = np.cos(np.arange(0,N,1)*np.pi/12.)
cleandata = np.copy(data[0])

plt.figure(figsize=(5,3))
plt.plot(data[0],color='black')
plt.title('input data series')
plt.ylabel('amplitude')
_ = plt.xlabel('sample number (N)')


# In[ ]:



L = 50   # set the window length
K = N-L+1 # calculate the length of the lagged series

#embed the data
Y = embed_data(data,L,K,ndim)

plt.figure()
plt.imshow(Y,cmap=cm.coolwarm)
plt.title('trajectory matrix')
plt.colorbar(label='amplitude')
plt.ylabel('rows are windowed (length L)')
_ = plt.xlabel('columns are lagged vectors (length K)')


# In[ ]:


# perform the additional SSA steps
C = make_covariance(Y,K)  # not aware of dimensions
PC,EOF,SV = make_pcs(C,Y) # not aware of dimensions

# pick the dimension to reconstruct
reconstruct_stream = 1
O = reconstruct(PC,EOF,0,K,reconstruct_stream)
O += reconstruct(PC,EOF,1,K,reconstruct_stream)

plt.figure()
plt.plot(O,color='black')
plt.plot(cleandata,color='gray',linestyle='dashed')
plt.plot(data[0],color='red',linestyle='dashed')
plt.title('first PC $group$ reconstruction, stream 1')
plt.xlabel('sample number (length $N$)')
plt.ylabel('amplitude')


# This exercise is totally trivial, but it can remind us that we have compressed the information from both streams into a single pair of eigenvectors! This would be true no matter how many times we fed in the series in duplicate.

# ### Example 6
# 
# What about extracting the series from a two noisy (with uncorrelated noise) streams?

# In[ ]:


ndim = 2   # as this is SSA, we only have one dimension of data
N    = 200 # set the length of the data

data = np.zeros([ndim,N])
data[0] = np.cos(np.arange(0,N,1)*np.pi/12.)
data[1] = np.cos(np.arange(0,N,1)*np.pi/12.)
cleandata = np.copy(data[0])

noiselevel = 2.5
data[0] += np.random.normal(0.,noiselevel,size=data[0].size)
data[1] += np.random.normal(0.,noiselevel,size=data[0].size)

plt.figure(figsize=(5,3))
plt.plot(data[0],color='black',lw=1.)
plt.plot(data[1],color='blue',lw=1.)
plt.title('input data series')
plt.ylabel('amplitude')
_ = plt.xlabel('sample number (N)')


# In[ ]:


L = 50   # set the window length
K = N-L+1 # calculate the length of the lagged series
Y = embed_data(data,L,K,ndim)
C = make_covariance(Y,K)  # not aware of dimensions
PC,EOF,SV = make_pcs(C,Y) # not aware of dimensions

# pick the dimension to reconstruct
reconstruct_stream = 1
O = reconstruct(PC,EOF,0,K,reconstruct_stream)
O += reconstruct(PC,EOF,1,K,reconstruct_stream)

plt.figure()
plt.plot(O,color='black')
plt.plot(data[reconstruct_stream],color='grey',linestyle='dashed')
plt.title('first PC $group$ reconstruction, stream 1')
plt.xlabel('sample number (length $N$)')
plt.ylabel('amplitude')


# We are able to dig (the correct) signal out of a noise field with **2.5x** the amplitude of the signal!

# You are now ready to MSSA a bigger, wilder dataset, or to continue playing in this sandbox, using the code we developed above!

# ### Example 7
# 
# How about some real EXP simulation data?
# 
# Let's try looking at some bar coefficients in the simulation we explored in WP21.

# In[ ]:


# bring in some processed data. columns are
# 0: time
# 1-2: m=1, n=0
# 3-4: m=2, n=0
# 5-6: m=1, n=1
# ...etc
indir = ''
prefix = 'processed/seriesm1m2.'
Data = np.genfromtxt(indir+prefix+'data') 
Data[:,0] *= 0.004 # put in simulation times

ndim = 2   # as this is SSA, we only have one dimension of data
N    = Data.shape[0] # set the length of the data

data = np.zeros([ndim,N])
data[0] = Data[:,3]
data[1] = Data[:,4]

plt.figure(figsize=(5,3))
plt.plot(data[0],color='black',lw=1.)
plt.plot(data[1],color='blue',lw=1.)
plt.title('input data series')
plt.ylabel('amplitude')
_ = plt.xlabel('sample number (N)')


# In[ ]:



# only do the expensive steps once!!
L = 200   # set the window length
K = N-L+1 # calculate the length of the lagged series
Y = embed_data(data,L,K,ndim)
C = make_covariance(Y,K)  # not aware of dimensions
PC,EOF,SV = make_pcs(C,Y) # not aware of dimensions


# In[ ]:


# pick the dimension to reconstruct
reconstruct_stream = 1
O = reconstruct(PC,EOF,0,K,reconstruct_stream)
O += reconstruct(PC,EOF,1,K,reconstruct_stream)

plt.figure()
plt.plot(O,color='black')
plt.plot(data[reconstruct_stream],color='grey',linestyle='dashed')
plt.title('first PC $group$ reconstruction, stream 1')
plt.xlabel('sample number (length $N$)')
plt.ylabel('amplitude')


# ### Example 8
# 
# What about the correlation of $m=1$ and $m=2$?

# In[ ]:


# bring in some processed data. columns are
# 0: time
# 1-2: m=1, n=0
# 3-4: m=2, n=0
# 5-6: m=1, n=1
# ...etc
indir = ''
prefix = 'processed/seriesm1m2.'
Data = np.genfromtxt(indir+prefix+'data') 
Data[:,0] *= 0.004 # put in simulation times

ndim = 4   # as this is SSA, we only have one dimension of data
N    = Data.shape[0] # set the length of the data

data = np.zeros([ndim,N])
data[0] = Data[:,1]
data[1] = Data[:,2]
data[2] = Data[:,3]
data[3] = Data[:,4]

plt.figure(figsize=(5,3))
plt.plot(data[0],color='black',lw=1.)
plt.plot(data[1],color='blue',lw=1.)
plt.title('input data series')
plt.ylabel('amplitude')
_ = plt.xlabel('sample number (N)')


# In[ ]:



# only do the expensive steps once!!
L = 200   # set the window length
K = N-L+1 # calculate the length of the lagged series
Y = embed_data(data,L,K,ndim)
C = make_covariance(Y,K)  # not aware of dimensions
PC,EOF,SV = make_pcs(C,Y) # not aware of dimensions


# In[ ]:


# pick the dimension to reconstruct
reconstruct_stream = 1
O = reconstruct(PC,EOF,0,K,reconstruct_stream)
O += reconstruct(PC,EOF,1,K,reconstruct_stream)

plt.figure()
plt.plot(O,color='black')
plt.plot(data[reconstruct_stream],color='grey',linestyle='dashed')
plt.title('first PC $group$ reconstruction, stream 1')
plt.xlabel('sample number (length $N$)')
plt.ylabel('amplitude')


# Okay, that last one was painful -- we need production MSSA!
# 
# See Alex's code, which we are finishing the user interface for.
