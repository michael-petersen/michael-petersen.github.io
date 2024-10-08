#!/usr/bin/env python
# coding: utf-8

# # Demystifying multichannel Singular Spectral Analysis (mSSA)
# ### Mike Petersen, 16 May 2022
# ### updated for 19 September 2024
# 
# A visual approach to the linear algebra steps of mSSA. This tutorial follows Weinberg & Petersen (2021) -- hereafter WP21 -- with some modest changes that appeared in Johnson et al. (2023), and some things that I've learned since then.
# 
# With ~~9~~ ~~10~~ 12 worked examples.
# 

# Goals:
# 1. Use numpy to perform linear algebra steps
# 2. Run pedagogical examples
# 3. Build a playground for intuition development
# 4. Let you loose on (small) mSSA problems!

# Outline:
# 1. As mSSA is complicated, start with *SSA*, where we consider a single input stream.
# 2. Develop a range of examples to showcase different use cases for SSA.
# 3. Move to an *mSSA* implementation.
# 4. Look ahead to what else can be done with *mSSA*.

# In[1]:


# standard python modules
import numpy as np;import time;import copy

# plotting utilities
import matplotlib.pyplot as plt;import matplotlib as mpl;import matplotlib.cm as cm;import matplotlib.colors as colors
get_ipython().run_line_magic('matplotlib', 'inline')
cmap = mpl.cm.inferno;mpl.rcParams['xtick.labelsize'] = 12;mpl.rcParams['ytick.labelsize'] = 12;mpl.rcParams['font.weight'] = 'medium';mpl.rcParams['axes.linewidth'] = 1.5;mpl.rcParams['xtick.major.width'] = 1.5;mpl.rcParams['xtick.minor.width'] = 0.75;mpl.rcParams['xtick.minor.visible'] = True;mpl.rcParams['ytick.major.width'] = 1.5;mpl.rcParams['ytick.minor.width'] = 0.75;mpl.rcParams['ytick.minor.visible'] = True


# ### Example 0
# Let's start with a very simple case: a single sinusoid.

# In[2]:


ndim = 1   # as this is SSA, we only have one dimension of data
N    = 200 # set the length of the data

data = np.zeros([ndim,N])
data[0] = np.cos(np.arange(0,N,1)*np.pi/12.)

plt.figure(figsize=(4,3),facecolor='white')
plt.plot(data[0],color='black')
plt.title('input data series')
plt.ylabel('amplitude')
_ = plt.xlabel('sample number (N)')
plt.tight_layout()


# The first ingredient is some prescription to _embed_ the data. At this step, we are creating a trajectory matrix that is comprised of _lagged_ copies of the input data stream. This constructs a matrix where the antidiagonals have the same value. We will call this matrix $T$, following WP21, equation 10.

# In[3]:


def embed_data(data,L,K,ndim=1,norm=False):
    """
    Construct an embedded time series (trajectory matrix) based on the input data.
    This function embeds the input time series following the strategy outlined by Weinberg & Petersen (2021). The trajectory matrix `Y` is formed by arranging augmented vectors as rows, with an option to normalize each data stream by removing the mean and scaling by the standard deviation.

    Parameters
    ----------
    data : (array-like) The input time series data streams. Each data stream should be structured as data[n], where `n` is the index for each stream.
    L    : (int) The window length, which determines the number of rows in the trajectory matrix.
    K    : (int) The length of the augmented vectors (number of columns per data stream).
    ndim : (int, optional) The number of data streams to include in the embedding process. Default is 1.
    norm : (bool, optional) If True, each data stream is normalized by removing the mean and dividing by the standard deviation. If False, the raw data values are used. Default is False.

    Returns
    -------
    Y    : (ndarray) The trajectory matrix of shape (L, K * ndim), where each row represents an augmented vector from the input data streams.

    Notes
    -----
    - If `norm=True`, the data are standardized (mean-subtracted and divided by the standard deviation) to remove trends and variations in scale.
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


# In[5]:


L = 60   # set the window length
K = N-L+1 # calculate the length of the lagged series

#embed the data
T = embed_data(data,L,K,1)

plt.figure(figsize=(4,3),facecolor='white')
plt.imshow(T,cmap=cm.coolwarm,aspect='equal')
plt.title('trajectory matrix')
plt.colorbar(label='amplitude')
plt.ylabel('rows are windowed (length L)')
_ = plt.xlabel('columns are lagged vectors (length K)')


# The second step is to construct the lag-covariance matrix. We have two choices here:
# 1. Reconstruct the full dimensionality, $C = \frac{1}{K}T^T\cdot T$, where the matrix is $K\times K$.
# 2. Reconstruct the reduced dimensionality, $C = \frac{1}{K}T\cdot T^T$, where the matrix is $L\times L$.
# 
# We will here choose option 1, but will note the differences below. This is equation 11 in WP21, and is denoted in this code as `full=True`. Throughout this notebook, we can set `full=False` to get option 2.

# In[6]:


def make_covariance(T,K,full=True):
    """
    Estimate the covariance matrix for a given trajectory matrix.
    This function computes the covariance matrix C_X based on the provided trajectory matrix using the formula in Equation 9. The output can be either the full covariance matrix or a reduced version, depending on the `full` parameter.

    Parameters
    ----------
    T    : (array-like) The trajectory matrix, representing time series data with delayed coordinates.
    K    : (int) The length of the augmented vectors, which corresponds to the number of columns in the trajectory matrix.
    full : (bool, optional) If True, computes the full covariance matrix as T^T * T / K. If False, computes a reduced covariance matrix as T * T^T / K. Default is True.

    Returns
    -------
    C    : (ndarray) The covariance matrix of shape (K, K) if `full=True`, or of shape (M, M), where M is the number of rows in T, if `full=False.
    """
    if full:
        C = np.dot(T.T,T)/K
    else:
        C = np.dot(T,T.T)/K
    print('C shape:',C.shape)
    return C


# In[7]:


C = make_covariance(T,K)

plt.figure(figsize=(4,3),facecolor='white')

plt.imshow(C,cmap=cm.coolwarm)
plt.title('covariance matrix')
plt.colorbar(label='amplitude')
plt.ylabel('dim 1 (length K)')
_ = plt.xlabel('dim 2 (length K)')


# Now we get to the magic: making the principal components, singular vectors, and empirical orthogonal functions. This is accomplished by a singular value decomposition step.
# 
# Following equation 12 of WP21, use SVD: $$C = U\cdot \Lambda \cdot V.$$ SVD takes as an input $C$ and returns $U$, $\Lambda$, and $V$. The columns of $U$ are the eigenvectors (or empirical orthogonal functions [EOF], $L$ with length $K$), which we immediately use to construct the principal components $P$ (with length $K$) by projecting the time series onto the EOF: $$P = T\cdot U.$$ 
# 
# 

# Other notes:
# 1. The principal components are in _lag_ space, which cannot be directly interpreted as series time. Instead, they encode the time of maximum correlated amplitude, but these only have meaning on the input timescale the after the reconstruction step.
# 2. The principal components will most often come in pairs when periodic signals are present in the dataset, in order to reconstruct phase information.
# 3. $\Lambda$ are the singular values. These are typically ordered largest to smallest by SVD algorithms.
# 4. $U = V^T$, to SVD approximation precision.
# 5. One can think of this step as hunting for structure in the covariance matrix.

# In[8]:


def make_pcs(C,T,ndim=1,full=True):
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
    SV    : (vector) the list of singular vectors
    """
    U,SV,V = np.linalg.svd(C, full_matrices=True)
    # the columns of U are the left singular vectors
    # the columns of V are the right singular vectors
    # SV are the singular values
    
    # to recover the PCs, dot the trajectory matrix and the left singular vectors
    # the projection of the time series Y onto the EOF (eigenvectors), U
    if full:
        PCs = np.dot(T,U)
    else:
        PCs = np.dot(V,T).T

    print('PC shape:',PCs.shape)
    
    if full:
        print('Left singular vector shape:',U.shape)
        return PCs,U,SV
    else:
        print('Left singular vector shape:',V.shape)
        return PCs,V.T,SV


# In[9]:


# run it!
PC,EOF,SV = make_pcs(C,T)


# In[10]:


# the columns of EOFs are the set of empirical orthogonal vectors: plot them!
plt.figure(figsize=(4,3),facecolor='white')

for i in range(K-1,-1,-1):
    plt.plot(EOF[:,i],color=cm.viridis(i/9.))
    
plt.title('empirical orthogonal functions')
plt.ylabel('EOF value')
_ = plt.xlabel('zero origin time (length K)')


# In[11]:


# the columns of PCs are the set of principal components: plot them!
plt.figure(figsize=(4,3),facecolor='white')

for i in range(9,-1,-1):
    plt.plot(PC[:,i],color=cm.viridis(i/9.))
    
plt.title('principal components')
plt.ylabel('PC value')
_ = plt.xlabel('abscissa (length K)')


# In[12]:


# plot the run of singular values
plt.figure(figsize=(4,3),facecolor='white')

SVnonoise = np.copy(SV) # save these for later...
plt.plot(np.log10(SV),color='black')
plt.title('singular value curve')
plt.ylabel('log$_{10}$ singular value value')
_ = plt.xlabel('PC number (length K)')


# We aren't quite done yet: we want to reconstruct the contribution to the input time series from each PC. This is accomplished through an _antidiagonal average_ of the transformed PCs. In WP21, we explicitly write the element reconstruction; in this implementation we will play a numpy trick to accomplish the antidiagonal average:
# 1. Select the PC to use for reconstruction, $P$, and the corresponding EOF, $E$. Both $P$ and $E$ are single vectors of length $K$. $E$ is a column of $U$.
# 2. Calculate $A = P^T\cdot E$.
# 3. Compute the antiagonal average of $A$ by reversing the matrix and using numpy's built in .diagonal call to compute the average.

# In[13]:


def reconstruct(PC,EOF,pcnum,K,nd=0):
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


# In[14]:


O = reconstruct(PC,EOF,0,K)

plt.figure(figsize=(4,3),facecolor='white')
plt.plot(O,color='black')
plt.plot(data[0],color='grey',linestyle='dashed')
plt.title('first PC reconstruction')
plt.xlabel('sample number (length $N$)')
plt.ylabel('amplitude')
plt.tight_layout()


# In[15]:


O = reconstruct(PC,EOF,0,K)
O += reconstruct(PC,EOF,1,K) # this adds PC1

plt.figure(figsize=(4,3),facecolor='white')

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
# 2. Should we detrend (and are there other schemes)? Under what circumstances?
# 3. How much can we stride the data (subsample) and still maintain robust results?

# ### Example 1
# 
# Let's go through another example to show one of the MSSA power points: removing noise.
# 
# This time, we'll construct a noisy data stream by injecting white noise (important distinction!) onto the sinusoidal series.

# In[16]:


ndim = 1
N = 200
L = 70
K = N-L+1

data = np.zeros([ndim,N])

data[0] = np.cos(np.arange(0,N,1)*np.pi/12.) # start with a simple sinusoid
cleandata = np.copy(data[0]) # record the clean data

# add some gaussian noise, at the level of the signal!
noiselevel = 1.5
data[0] += np.random.normal(0.0,noiselevel,size=data[0].size)

plt.figure(figsize=(4,3),facecolor='white')

plt.plot(data[0],color='black')
plt.plot(cleandata,color='gray',linestyle='dashed')
plt.title('input data series');plt.ylabel('amplitude');plt.xlabel('sample number (N)')
plt.tight_layout()


# In[17]:


# perform the SSA steps
T = embed_data(data,L,K,1)
C = make_covariance(T,K)
PC,EOF,SV = make_pcs(C,T)
O = reconstruct(PC,EOF,0,K,0)
O = reconstruct(PC,EOF,1,K,0)

plt.figure(figsize=(4,3),facecolor='white')

plt.plot(2*O,color='black')
plt.plot(cleandata,color='gray',linestyle='dashed')
#plt.plot(data[0],color='red',linestyle='dashed')
plt.title('first PC $group$ reconstruction');plt.xlabel('sample number (length $N$)');plt.ylabel('amplitude');plt.tight_layout()


# We can also compare to the Discrete Fourier Transformation to see some of the real interpretive power of SSA: SSA makes the signal stand out to high significance.

# In[18]:


def make_dft(data):
    freqs = np.fft.fftfreq(len(data), d=1.0)
    DFT = np.fft.fft(data, axis=-1)

    nfreqs = int(np.floor(len(data)/2.))
    return freqs[0:nfreqs],np.abs(DFT)[0:nfreqs]

ff,ftD = make_dft(data[0])
ff,ftR = make_dft(O)

plt.figure(figsize=(4,3),facecolor='white')
plt.plot(ff,ftD,color='gray',linestyle='dashed')
plt.plot(ff,ftR,color='black')
plt.title('DFT frequency recovery');plt.xlabel('frequency (inverse time)');  plt.ylabel('amplitude')


# In[19]:


O = reconstruct(PC,EOF,2,K,0)
for pc in range(3,45):
    O += reconstruct(PC,EOF,pc,K,0)

plt.figure(figsize=(4,3),facecolor='white')

plt.plot(O,color='black')
plt.plot(cleandata,color='gray',linestyle='dashed')
plt.title('second PC $group$ reconstruction')
plt.xlabel('sample number (length $N$)')
plt.ylabel('amplitude')


# We've shown that we can separate the signal from the noise very efficiently using MSSA.
# 
# Extensions: 
# 1. What happens when you test $L$ and $N$?
# 2. What does a pure noise field look like on reconstruction?
# 3. How large can the noise level be before we cannot recover the signal?
# 4. How does biased noise affect the results?

# In[20]:


# check in on the SV curve
plt.figure(figsize=(4,3),facecolor='white')

plt.plot(np.log10(SV),color='black')
plt.plot(np.log10(SVnonoise),color='gray',linestyle='dashed')
plt.title('singular value curve')
plt.ylabel('singular value value')
_ = plt.xlabel('PC number (length K)')


# ### Example 2
# 
# What about an example with a second component: slow growth over time? Can we reconstruct that?
# 
# Bonus: how does separation of signal change with window length (try adjusting $L$!)?
# 
# We'll keep noise for this example.

# In[21]:


ndim = 1
N = 200
L = 50
K = N-L+1

data = np.zeros([ndim,N])
data[0] = np.cos(np.arange(0,N,1)*np.pi/12.) # start with a simple sinusoid

plt.figure(figsize=(4,3))#,facecolor='white')
plt.plot(data[0],color='grey',linestyle='dotted',label='periodic trend')

# add a quadratic (slow) trend
quadratictrend = 0.0001*(np.arange(0,N,1)**2.)
data[0] += quadratictrend
plt.plot(quadratictrend,color='grey',linestyle='dashed',label='growing trend')

cleandata = np.copy(data[0]) # record the clean data
# add some gaussian noise, at the level of the signal!
noiselevel = 1.0
data[0] += np.random.normal(0.,noiselevel,size=data[0].size)

plt.plot(data[0],color='black',label='measured signal')
plt.ylabel('amplitude');_ = plt.xlabel('sample number (N)');plt.legend(frameon=False);plt.tight_layout()


# In[22]:


# perform the SSA steps
T = embed_data(data,L,K,1)
C = make_covariance(T,K)
PC,EOF,SV = make_pcs(C,T)


plt.figure(figsize=(4,3))#,facecolor='white')
plt.plot(data[0],color='black',label='measured signal')

O = reconstruct(PC,EOF,0,K,0)
plt.plot(O,color='red',linestyle='dashed',label='first group')
 
O = reconstruct(PC,EOF,1,K,0)
O += reconstruct(PC,EOF,2,K,0)
plt.plot(O,color='red',linestyle='dotted',label='second group')

O = reconstruct(PC,EOF,3,K,0)
for k in range(4,50):
    O += reconstruct(PC,EOF,k,K,0)
#plt.plot(O,color='red',linestyle='solid',lw=0.5,label='nullity')

plt.xlabel('sample number (length $N$)');plt.ylabel('amplitude');plt.legend(frameon=False);plt.tight_layout()


# In[23]:


plt.figure(figsize=(4,3))#,facecolor='white')
plt.plot(data[0],color='black',label='measured signal')

O = reconstruct(PC,EOF,3,K,0)
for k in range(4,50):
    O += reconstruct(PC,EOF,k,K,0)
plt.plot(O,color='red',linestyle='solid',lw=0.5,label='nullity')

plt.xlabel('sample number (length $N$)');plt.ylabel('amplitude');plt.legend(frameon=False);plt.tight_layout()


# In[24]:


# now compare to the original series
plt.figure(figsize=(4,3))#,facecolor='white')

O = reconstruct(PC,EOF,0,K,0)
plt.plot(O,color='red',linestyle='dashed',label='first group')

O = reconstruct(PC,EOF,1,K,0)
O += reconstruct(PC,EOF,2,K,0)
plt.plot(O,color='red',linestyle='dotted',label='second group')

data = np.zeros([ndim,N])
data[0] = np.cos(np.arange(0,N,1)*np.pi/12.) # start with a simple sinusoid
plt.plot(data[0],color='grey',linestyle='dotted',label='periodic trend')

# add the quadratic (slow) trend
data[0] += quadratictrend
plt.plot(0.0001*(np.arange(0,N,1)**2.),color='grey',linestyle='dashed',label='growing trend')

plt.xlabel('sample number (length $N$)');plt.ylabel('amplitude');plt.legend(frameon=False);plt.tight_layout()


# In[25]:


# reconstruct the second group
O = reconstruct(PC,EOF,1,K,0)
O += reconstruct(PC,EOF,2,K,0)

# check on the DFT recovery
plt.figure(figsize=(4,3),facecolor='white')

ff,ft = make_dft(data[0])
plt.plot(ff,ft,color='gray',linestyle='dashed')

ff,ft = make_dft(O)
plt.plot(ff,ft,color='black')

plt.title('DFT frequency recovery');plt.xlabel('frequency (inverse time)');plt.ylabel('amplitude')


# This is a good time to introduce a tool for interpretation: the $w$-correlation matrix. We won't go in to the calculation details -- see WP21 eq 19 -- but the $w$-correlation matrix tries to find similarity between PCs, which often indicate that they are a group.

# In[26]:


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
                else            : w = numT - i + 1
                
                wcorr[m, n] += w * R[i, m]*R[i, n]

    #// Normalize
    for m in range(0,numW):
        for n in range(m+1,numW):
            if (wcorr[m, m]>0.0 and wcorr[n, n]>0.0):
                wcorr[m, n] /= np.sqrt(wcorr[m, m]*wcorr[n, n])


    #// Unit diagonal
    for m in range(0,numW): 
        wcorr[m, m] = 1.0

    #// Complete
    for m in range(0,numW):
        for n in range(0,m):
            wcorr[m, n] = wcorr[n, m]

    return wcorr


# In[27]:


# select a maximum PC to consider
pcmax = 10

# build a reconstruction matrix (PC contributions stacked on top of one another)
RC = np.zeros([N,pcmax])
for i in range(0,pcmax):
    RC[:,i] = reconstruct(PC,EOF,i,K,nd=0)
    
# compute the w-correlation matrix
R = wCorr(RC)

plt.figure(figsize=(4,3),facecolor='white')


plt.imshow(np.log10(np.abs(R)),cmap=cm.Greys)
plt.colorbar(label='log correlation (higher is more correlated)')
plt.xlabel('PC number')
_ = plt.ylabel('PC number')


# Note that the $w$-correlation matrix doesn't tell us about significance -- just which PCs are likely to be related.
# 
# We can also look at $F$ and $G$ matrices, but those will be described elsewhere.

# ### Example 3 (optional)
# 
# What about two sinusoidal signals on top of each other?
# 
# No noise in this example.

# In[28]:


ndim = 1
N = 200
L = 50
K = N-L+1

data = np.zeros([ndim,N])

data[0] = np.cos(np.arange(0,N,1)*np.pi/12.) # start with a simple sinusoid
sample1data = np.copy(data[0]) # record the first signal

# add a chirp
omega2 = 0.04; chirp = 6.
omega = omega2*(1.0 + chirp*np.arange(0,N,1)/N);
data[0] += 0.5*np.cos(np.arange(0,N,1)*omega)
sample2data = 0.5*np.cos(np.arange(0,N,1)*omega) # record the second signal
cleandata = np.copy(data[0]) # record the clean data

plt.figure(figsize=(4,3),facecolor='white')

plt.plot(data[0],color='black')
plt.plot(sample1data,color='gray',lw=1.)
plt.plot(sample2data,color='gray',lw=1.)

plt.title('input data series')
plt.ylabel('amplitude')
_ = plt.xlabel('sample number (N)')


# In[29]:


# perform the SSA steps
T = embed_data(data,L,K,1)
C = make_covariance(T,K)
PC,EOF,SV = make_pcs(C,T)
O = reconstruct(PC,EOF,0,K,0)
O += reconstruct(PC,EOF,1,K,0)

plt.figure(figsize=(4,3),facecolor='white')

plt.plot(O,color='black')
plt.plot(sample1data,color='gray',linestyle='dashed')
plt.plot(data[0],color='red',linestyle='dashed')
plt.title('first PC $group$ reconstruction')
plt.xlabel('sample number (length $N$)')
plt.ylabel('amplitude')


# In[30]:


O = reconstruct(PC,EOF,2,K,0)
O += reconstruct(PC,EOF,3,K,0)
O += reconstruct(PC,EOF,4,K,0)
O += reconstruct(PC,EOF,5,K,0)

plt.figure(figsize=(4,3),facecolor='white')

plt.plot(O,color='black')
plt.plot(sample2data,color='gray',linestyle='dashed')
plt.plot(data[0],color='red',linestyle='dashed')
plt.title('second PC $group$ reconstruction')
plt.xlabel('sample number (length $N$)')
plt.ylabel('amplitude')


# In[31]:


plt.figure(figsize=(4,3),facecolor='white')

# check on the DFT recovery
ff,ft = make_dft(data[0])
plt.plot(ff,ft,color='gray',linestyle='dashed')

ff,ft = make_dft(O)
plt.plot(ff,ft,color='black')

plt.title('DFT frequency recovery')
plt.xlabel('frequency (inverse time)')
plt.ylabel('amplitude')


# In[33]:


# select a maximum PC to consider
pcmax = 10

# build a reconstruction matrix (PC contributions stacked on top of one another)
RC = np.zeros([N,pcmax])
for i in range(0,pcmax):
    RC[:,i] = reconstruct(PC,EOF,i,K,nd=0)
    
# compute the w-correlation matrix
R = wCorr(RC)

plt.figure(figsize=(4,3),facecolor='white')


plt.imshow(np.log10(np.abs(R)),cmap=cm.Greys)
plt.colorbar(label='log correlation (higher is more correlated)')
plt.xlabel('PC number')
_ = plt.ylabel('PC number')



# Extensions: 
# 1. What happens when the signals do not have different amplitudes?
# 2. How can we get better separation of the signals?

# ### Example 4 (optional)
# 
# An example of _how_ SSA works: sawtooth reconstruction. This example demonstrates that when a linear recurrence relation doesn't exist for the signal being reconstructed, SSA will require many PCs to recover the signal.

# In[ ]:


ndim = 1
N = 100
L = 50
K = N-L+1

data = np.zeros([ndim,N])

data[0] = (np.arange(0,N,1)*0.01) % 0.3

cleandata = np.copy(data[0]) # record the clean data

plt.figure(figsize=(4,3),facecolor='white')

plt.plot(data[0],color='black')
plt.title('input data series')
plt.ylabel('amplitude')
_ = plt.xlabel('sample number (N)')


# In[ ]:


# perform the SSA steps
T = embed_data(data,L,K,1)
C = make_covariance(T,K)
PC,EOF,SV = make_pcs(C,T)
plt.figure(figsize=(4,3),facecolor='white')


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

# In[34]:


ndim = 2   # as this is SSA, we only have one dimension of data
N    = 200 # set the length of the data

data = np.zeros([ndim,N])
data[0] = np.cos(np.arange(0,N,1)*np.pi/12.)
data[1] = np.cos(np.arange(0,N,1)*np.pi/12.)
cleandata = np.copy(data[0])
plt.figure(figsize=(4,3),facecolor='white')

plt.plot(data[0],color='black')
plt.title('input data series')
plt.ylabel('amplitude')
_ = plt.xlabel('sample number (N)')


# In[35]:


L = 50   # set the window length
K = N-L+1 # calculate the length of the lagged series

#embed the data
T = embed_data(data,L,K,ndim)

plt.figure(figsize=(4,3),facecolor='white')

plt.imshow(T,cmap=cm.coolwarm)
plt.title('trajectory matrix')
plt.colorbar(label='amplitude')
plt.ylabel('rows are windowed (length L)')
_ = plt.xlabel('columns are lagged vectors (length K)')


# In[36]:


# take a look at the covariance matrix: lots of block structure here!
C = make_covariance(T,K)  # not aware of dimensions

plt.figure(figsize=(4,3),facecolor='white')

plt.imshow(C,cmap=cm.coolwarm)
plt.title('covariance matrix')
plt.colorbar(label='amplitude')
plt.ylabel('dim 1 (length K)')
_ = plt.xlabel('dim 2 (length K)')


# In[38]:


# perform the additional SSA steps
PC,EOF,SV = make_pcs(C,T) # not aware of dimensions

# pick the dimension to reconstruct
reconstruct_stream = 0
O = reconstruct(PC,EOF,0,K,reconstruct_stream)
O += reconstruct(PC,EOF,1,K,reconstruct_stream)

plt.figure(figsize=(4,3),facecolor='white')

plt.plot(O,color='black')
plt.plot(cleandata,color='gray',linestyle='dashed')
plt.plot(data[0],color='red',linestyle='dashed')
plt.title('first PC $group$ reconstruction, stream 1')
plt.xlabel('sample number (length $N$)')
plt.ylabel('amplitude')


# This exercise is totally trivial, but it can remind us that we have compressed the information from both streams into a single pair of eigenvectors! This would be true no matter how many times we fed in the series in duplicate.

# ### Example 6
# 
# What about extracting the series from a two noisy (with uncorrelated white noise) streams?

# In[39]:


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


# In[42]:


L = 100   # set the window length
K = N-L+1 # calculate the length of the lagged series
T = embed_data(data,L,K,ndim)
C = make_covariance(T,K)  # not aware of dimensions
PC,EOF,SV = make_pcs(C,T) # not aware of dimensions

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
# 
# (Note that this is specific to this problem and should not be considered a general result!)

# You are now ready to MSSA a bigger, wilder dataset, or to continue playing in this sandbox, using the code we developed above!

# ### Example 7
# 
# How about some real EXP simulation data?
# 
# Let's try looking at some bar coefficients in the simulation we explored in WP21.

# In[43]:


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
T = embed_data(data,L,K,ndim)
C = make_covariance(T,K)  # not aware of dimensions
PC,EOF,SV = make_pcs(C,T) # not aware of dimensions


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

stride = 1
inputlength = Data[::stride,1].size
data = np.zeros([ndim,inputlength])

data[0] = Data[::stride,1]
data[1] = Data[::stride,2]
data[2] = Data[::stride,3]
data[3] = Data[::stride,4]

plt.figure(figsize=(5,3))
plt.plot(data[0],color='black',lw=1.)
plt.plot(data[1],color='blue',lw=1.)
plt.title('input data series')
plt.ylabel('amplitude')
_ = plt.xlabel('sample number (N)')


# In[ ]:


# only do the expensive steps once!!
L = 30   # set the window length
K = N-L+1 # calculate the length of the lagged series
#K = inputlength-L+1
T = embed_data(data,L,K,ndim)
C = make_covariance(T,K)  # not aware of dimensions
PC,EOF,SV = make_pcs(C,T) # not aware of dimensions


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


# In[ ]:


# select a maximum PC to consider
pcmax = 10

# build a reconstruction matrix (PC contributions stacked on top of one another)
RC = np.zeros([N,pcmax])
#RC = np.zeros([inputlength,pcmax])
for i in range(0,pcmax):
    RC[:,i] = reconstruct(PC,EOF,i,K,0)
    
# compute the w-correlation matrix
R = wCorr(RC)

plt.imshow(np.log10(np.abs(R)),cmap=cm.Greys)
plt.colorbar(label='log correlation (higher is more correlated)')
plt.xlabel('PC number')
_ = plt.ylabel('PC number')



# Okay, that last one was painful -- we need production mSSA!
# 
# A more advanced interface is available in pyEXP.

# ### Example 9: What about missing data?
# 
# There are a few strategies for missing data. The simplest is to just ignore and let SSA try to find the connective values. That's what we'll do in this example: take a sinusoid, remove some fraction of the data
# 
# (One can also place dummy data and use the reconstruction to refine.)
# 

# In[44]:


N=200 # set the initial number of data points
R=100 # set the number of data points to remove
ndim=1
testrange = np.arange(0,N,1)
testdata = np.cos(np.arange(0,N,1)*np.pi/12.)

exclude = np.unique(np.random.randint(0,N,R)) # pick samples to remove

R = len(exclude)
data = np.zeros([ndim,N-R])
dtime = np.zeros(N-R)


i = 0
for v in range(0,N):
    if v not in exclude:
        data[0][i] = testdata[v]
        dtime[i] = testrange[v]
        i+=1
        
plt.plot(dtime,data[0],color='grey',linestyle='dashed')
#plt.plot(testrange,testdata,color='black')


# In[45]:


# now perform SSA steps

N = len(data[0])

L = 100   # set the window length
K = N-L+1 # calculate the length of the lagged series
Y = embed_data(data,L,K,ndim)
C = make_covariance(Y,K)  # not aware of dimensions
PC,EOF,SV = make_pcs(C,Y) # not aware of dimensions


# In[46]:


# examine the reconstruction
O = reconstruct(PC,EOF,0,K,0)
O += reconstruct(PC,EOF,1,K,0)

plt.figure()
plt.plot(dtime,O,color='black')
plt.plot(testrange,testdata,color='grey',linestyle='dashed')
plt.title('first PC reconstruction')
plt.xlabel('sample number (length $N$)')
plt.ylabel('amplitude')


# In the end, we can see that the reconstruction is able to pick up the period quite well, even with a large number of missing data samples!

# ### Example 10: Nothing from nothing
# 
# One possible issue with mSSA is the correlation of noise into (supposed) signal. This can -- and will -- happen because mSSA is looking to pick up any correlation, even if it is just noise. This is still an area of ongoing research, 

# In[49]:


ndim = 1
N = 200
L = 70
K = N-L+1

# set up some gaussian noise
data = np.zeros([ndim,N])
noiselevel = 1.5
data[0] = np.random.normal(0.0,noiselevel,size=data[0].size)

plt.figure(figsize=(4,3),facecolor='white')
plt.plot(data[0],color='black')
plt.title('input data series');plt.ylabel('amplitude');plt.xlabel('sample number (N)')
plt.tight_layout()


# In[50]:


# perform the SSA steps
T = embed_data(data,L,K,1)
C = make_covariance(T,K)
PC,EOF,SV = make_pcs(C,T)
O = reconstruct(PC,EOF,0,K,0)
O += reconstruct(PC,EOF,1,K,0)

plt.figure(figsize=(4,3),facecolor='white')

plt.plot(O,color='black')
plt.plot(data[0],color='grey',linestyle='dashed')
plt.title('first PC $group$ reconstruction')
plt.xlabel('sample number (length $N$)')
plt.ylabel('amplitude')


# Two things are working in our favour to mitigate this concern: 
# 
# 1. The correlation tends to be at very high frequency (higher than any frequency in the system), which outs it as false. 
# 2. When correlating multiple series, it is harder to make a false signal -- because it would have to be common noise in different time series.
# 
# But worth being careful!

# ### Example 11: Linear Recurrence Relations
# 
# mSSA is fundamentally built on the idea that a time series can be represented by some (as yet undiscovered) linear recurrence relation that describes the time series. 

# 
# We'll follow the Recurrent SSA Forecasting (SSA-R) strategy from Kalantari et al. (2019). The idea is to represent the time series as a linear recurrence relation, i.e.
# $$ y_{i+d} = \sum_{k=1}^d a_ky_{i+d-k}$$
# where $1\le i\le N-d$, $a_d\ne0$, and $d<N$. The $R = a_1,...a_{L-1}$ values are the LRR coefficients, of which there will be $L-1$.
# 
# Using the empirical orthogonal functions (left singular vectors) as an orthonormal basis in the trajectory space, we can calculate the $R$ values as
# $$R = \frac{1}{1-v^2}\sum \pi_i U_i$$
# where $U_i$ is the first $L-1$ components of a group of EOF, and $\pi_i$ and $v$ are normalisations (see Kalantari for definition).
# 

# We'll go all the way back to the first sinusoid example to see this in action.

# In[51]:


ndim = 1   # as this is SSA, we only have one dimension of data
N    = 200 # set the length of the data
L = 40   # set the window length
K = N-L+1 # calculate the length of the lagged series
full=False # note that the strategy only works with (full=True,Lw=K) or (full=False,Lw=L). We'll choose the former because it is quicker.

data = np.zeros([ndim,N])
data[0] = np.cos(np.arange(0,N,1)*np.pi/12.)
Y = embed_data(data,L,K,1)
C = make_covariance(Y,K,full=full)
PC,EOF,SV = make_pcs(C,Y,full=full)
O = reconstruct(PC,EOF,0,K,0)
O = reconstruct(PC,EOF,1,K,0)


# In[52]:


def recurrencecoefficients(P,I,L):
    # try implementing the recursion strategy to get R
    # the verticality coefficient of Lr (the linear space defined by the eigenanalysis)
    nu2 = np.sum([P[-1,i]**2 for i in range(0,I)])
    print(nu2)
    R = np.sum([(1/(1-nu2))*P[-1,i]*P[0:(L),i] for i in range(0,I)],axis=0)
    return R

# two components should be sufficient to recover the dynamics
I = 2
Lw = L
R = recurrencecoefficients(EOF,I,Lw)
plt.plot(R,color='black',label='minimum LR')

# what happens if we add another group?
I = 3
R = recurrencecoefficients(EOF,I,Lw)
plt.plot(R,color='red',label='noisy LR')
plt.legend(frameon=False);plt.xlabel('linear recurrence term (length $L$)');_=plt.ylabel('amplitude')


# In[53]:


I = 2 # use the minimum LR
Lw = L

O = reconstruct(PC,EOF,0,K)
for i in range(1,I): O += reconstruct(PC,EOF,i,K)
tvals = np.arange(0,len(O),1)

# compute the recurrence coefficients
R = recurrencecoefficients(EOF,I,Lw)

# how many forecasting steps should we take?
h = 100

# take the first forecasting step
lrecent = O[-(Lw):];ttime = tvals[-1];Z = np.concatenate([O,np.array([np.sum(R*lrecent)])]); totalT = np.concatenate([tvals,np.array([ttime])])

for ih in range(1,h):
    lrecent = Z[-(Lw):];ttime += 1;Z = np.concatenate([Z,np.array([np.sum(R*lrecent)])]);totalT = np.concatenate([totalT,np.array([ttime])])

plt.plot(totalT,Z,color='red',label='Extended Series');plt.plot(tvals,O,color='black',label='Original Series');plt.legend(frameon=False)
plt.legend(frameon=False);plt.xlabel('sample number');_=plt.ylabel('amplitude')


# Not bad! But maybe using the full covariance matrix would be better?

# ### A final question I'm thinking about.
# 
# Can we make some sort of uncertainty estimate on the shape of the PCs?
# 

# ## Thanks for trying out mSSA!
# 
# Feel free to get in touch with any recommendations, questions, or just general thoughts.

# In[ ]:




