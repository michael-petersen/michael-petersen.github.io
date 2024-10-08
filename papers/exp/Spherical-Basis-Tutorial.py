#!/usr/bin/env python
# coding: utf-8

# # Building a basis
# ### Mike Petersen, 18 May
# 
# Updates since the last time we built a spherical basis.

# Old tools:
# 1. makemodel (slight upgrade with addition of makemodel_empirical)
# 2. haloprof
# 3. (slcheck, other tools for basis inspection) 

# The tutorial material mostly holds; I'm going to introduce two new tools:
# 1. simpleSL (Python tool)
# 2. modelfit (smoothing strategy for empirical bases)

# ### Step 1
# 
# 1. Install **EXP**: review?
# 2. export PYTHONPATH=$HOME/lib/python3.8 (or where you installed it)
# 3. python -> import simpleSL

# ### Some definitions

# In[1]:


# standard python modules
import numpy as np;import time;import copy

# plotting utilities
import matplotlib.pyplot as plt;import matplotlib as mpl;import matplotlib.cm as cm;import matplotlib.colors as colors
get_ipython().run_line_magic('matplotlib', 'inline')

import scipy.interpolate as interpolate;import subprocess;from astropy.io import fits

cmap = mpl.cm.inferno;mpl.rcParams['xtick.labelsize'] = 10;mpl.rcParams['ytick.labelsize'] = 10;mpl.rcParams['font.weight'] = 'medium';mpl.rcParams['axes.linewidth'] = 1.5;mpl.rcParams['xtick.major.width'] = 1.5;mpl.rcParams['xtick.minor.width'] = 0.75;mpl.rcParams['xtick.minor.visible'] = True;mpl.rcParams['ytick.major.width'] = 1.5;mpl.rcParams['ytick.minor.width'] = 0.75;mpl.rcParams['ytick.minor.visible'] = True


# In[2]:


def return_density(logr,weights=1.,rangevals=[-2, 6],bins=500,d2=False):
    """return_density
    
    simple binned density using logarithmically spaced bins
    
    inputs
    ---------
    logr        : (array) log radii of particles to bin
    weights     : (float or array) if float, single-mass of particles, otherwise array of particle masses
    rangevals   : (two value list) minimum log r, maximum log r
    bins        : (int) number of bins
    d2          : (bool) if True, compute surface density
    
    returns
    ---------
    rcentre     : (array) array of sample radii (NOT LOG)
    density     : (array) array of densities sampled at rcentre (NOT LOG)
    
    """
    
    # assume evenly spaced logarithmic bins
    dr      = (rangevals[1]-rangevals[0])/bins
    rcentre = np.zeros(bins)
    density = np.zeros(bins)
    
    # check if single mass, or an array of masses being passed
    # construct array of weights
    if isinstance(weights,np.float):
        w = weights*np.ones(logr.size)
    else:
        w = weights
    
    for indx in range(0,bins):
        
        # compute the centre of the bin (log r)
        rcentre[indx] = rangevals[0] + (indx+0.5)*dr
        
        # compute dr (not log)
        rmin,rmax = 10.**(rangevals[0] + (indx)*dr),10.**(rangevals[0] + (indx+1)*dr)
        if d2:
            shell = np.pi*(rmax**2-rmin**2)
        else:
            shell = (4./3.)*np.pi*(rmax**3.-rmin**3.)
            
        # find all particles in bin
        inbin = np.where((logr>=(rangevals[0] + (indx)*dr)) & (logr<(rangevals[0] + (indx+1)*dr)))
        
        # compute M/V for the bin
        density[indx] = np.nansum(w[inbin])/shell
        
    # return
    return 10.**rcentre,density



# In[3]:



def makemodel(func,M,funcargs,rvals = 10.**np.linspace(-2.,4.,2000),pfile='',plabel = '',verbose=True):
    """make an EXP-compatible spherical basis function table
    
    inputs
    -------------
    func        : (function) the callable functional form of the density
    M           : (float) the total mass of the model, sets normalisations
    funcargs    : (list) a list of arguments for the density function.
    rvals       : (array of floats) radius values to evaluate the density function
    pfile       : (string) the name of the output file. If '', will not print file
    plabel      : (string) comment string
    verbose     : (boolean)
    outputs
    -------------
    R           : (array of floats) the radius values
    D           : (array of floats) the density
    M           : (array of floats) the mass enclosed
    P           : (array of floats) the potential
    
    """
    
    R = np.nanmax(rvals)
    
    # query out the density values
    dvals = func(rvals,*funcargs)

    # make the mass and potential arrays
    mvals = np.zeros(dvals.size)
    pvals = np.zeros(dvals.size)
    pwvals = np.zeros(dvals.size)

    # initialise the mass enclosed an potential energy
    mvals[0] = 1.e-15
    pwvals[0] = 0.

    # evaluate mass enclosed and potential energy by recursion
    for indx in range(1,dvals.size):
        mvals[indx] = mvals[indx-1] +          2.0*np.pi*(rvals[indx-1]*rvals[indx-1]*dvals[indx-1] +                 rvals[indx]*rvals[indx]*dvals[indx])*(rvals[indx] - rvals[indx-1]);
        pwvals[indx] = pwvals[indx-1] +           2.0*np.pi*(rvals[indx-1]*dvals[indx-1] + rvals[indx]*dvals[indx])*(rvals[indx] - rvals[indx-1]);
    
    # evaluate potential (see theory document)
    pvals = -mvals/(rvals+1.e-10) - (pwvals[dvals.size-1] - pwvals)

    # get the maximum mass and maximum radius
    M0 = mvals[dvals.size-1]
    R0 = rvals[dvals.size-1]

    # compute scaling factors
    Beta = (M/M0) * (R0/R);
    Gamma = np.sqrt((M0*R0)/(M*R)) * (R0/R);
    if verbose:
        print("! Scaling:  R=",R,"  M=",M)

    rfac = np.power(Beta,-0.25) * np.power(Gamma,-0.5);
    dfac = np.power(Beta,1.5) * Gamma;
    mfac = np.power(Beta,0.75) * np.power(Gamma,-0.5);
    pfac = Beta;

    if verbose:
        print(rfac,dfac,mfac,pfac)

    # save file if desired
    if pfile != '':
        f = open(pfile,'w')
        print('! ',plabel,file=f)
        print('! R    D    M    P',file=f)

        print(rvals.size,file=f)

        for indx in range(0,rvals.size):
            print('{0} {1} {2} {3}'.format( rfac*rvals[indx],              dfac*dvals[indx],              mfac*mvals[indx],              pfac*pvals[indx]),file=f)
    
        f.close()
    
    return rvals*rfac,dfac*dvals,mfac*mvals,pfac*pvals


# In[4]:



def makemodel_empirical(rvals,dvals,pfile='',plabel = '',verbose=True):
    """make an EXP-compatible spherical basis function table
    
    inputs
    -------------
    rvals       : (array of floats) radius values to evaluate the density function
    pfile       : (string) the name of the output file. If '', will not print file
    plabel      : (string) comment string
    verbose     : (boolean)
    outputs
    -------------
    R           : (array of floats) the radius values
    D           : (array of floats) the density
    M           : (array of floats) the mass enclosed
    P           : (array of floats) the potential
    
    """
    M = 1.
    R = np.nanmax(rvals)
    
    # query out the density values
    #dvals = D#func(rvals,*funcargs)
    #print(R.size,)

    # make the mass and potential arrays
    mvals = np.zeros(dvals.size)
    pvals = np.zeros(dvals.size)
    pwvals = np.zeros(dvals.size)

    # initialise the mass enclosed an potential energy
    mvals[0] = 1.e-15
    pwvals[0] = 0.

    # evaluate mass enclosed and potential energy by recursion
    for indx in range(1,dvals.size):
        mvals[indx] = mvals[indx-1] +          2.0*np.pi*(rvals[indx-1]*rvals[indx-1]*dvals[indx-1] +                 rvals[indx]*rvals[indx]*dvals[indx])*(rvals[indx] - rvals[indx-1]);
        pwvals[indx] = pwvals[indx-1] +           2.0*np.pi*(rvals[indx-1]*dvals[indx-1] + rvals[indx]*dvals[indx])*(rvals[indx] - rvals[indx-1]);
    
    # evaluate potential (see theory document)
    pvals = -mvals/(rvals+1.e-10) - (pwvals[dvals.size-1] - pwvals)

    # get the maximum mass and maximum radius
    M0 = mvals[dvals.size-1]
    R0 = rvals[dvals.size-1]

    # compute scaling factors
    Beta = (M/M0) * (R0/R);
    Gamma = np.sqrt((M0*R0)/(M*R)) * (R0/R);
    if verbose:
        print("! Scaling:  R=",R,"  M=",M)

    rfac = np.power(Beta,-0.25) * np.power(Gamma,-0.5);
    dfac = np.power(Beta,1.5) * Gamma;
    mfac = np.power(Beta,0.75) * np.power(Gamma,-0.5);
    pfac = Beta;

    if verbose:
        print(rfac,dfac,mfac,pfac)

    # save file if desired
    if pfile != '':
        f = open(pfile,'w')
        print('! ',plabel,file=f)
        print('! R    D    M    P',file=f)

        print(rvals.size,file=f)

        for indx in range(0,rvals.size):
            print('{0} {1} {2} {3}'.format( rfac*rvals[indx],              dfac*dvals[indx],              mfac*mvals[indx],              pfac*pvals[indx]),file=f)
    
        f.close()
    
    return rvals*rfac,dfac*dvals,mfac*mvals,pfac*pvals


# ### First strategy: Build a Plummer basis
# 
# (Also recovers the Clutton-Brock basis set!)

# In[5]:



def plummer_density(radius,scale_radius=1.0,mass=1.0,astronomicalG=1.0):
    """basic plummer density profile"""
    return ((3.0*mass)/(4*np.pi))*(scale_radius**2.)*((scale_radius**2 + radius**2)**(-2.5))

plummer_b = 1.0
R,D,M,P = makemodel(plummer_density,1.,[plummer_b],rvals = 10.**np.linspace(-3.,1.,2000),pfile='SLPlummer.dat')

plt.figure(figsize=(4,3))
plt.plot(np.log10(R),np.log10(D),color='black')
plt.xlabel('log r')
plt.ylabel('log rho')
plt.title('Plummer model')


# In[7]:


get_ipython().system('head -100 SLPlummer.dat')


# ### Second strategy: Making an empirical basis
# 
# Let's try the model of GSE from Naidu et al. (2021)

# In[8]:


from astropy.io import fits
fits_image_filename = '/Users/mpetersen/Downloads/GSEz0snapshot.fits'

hdul = fits.open(fits_image_filename)
#_=hdul.info()

# compute 3d radius
R = np.sqrt((hdul[1].data['X'])**2.+(hdul[1].data['Y'])**2.+((hdul[1].data['Z'])**2.))
print(np.nanmin(R),np.nanmax(R))


# In[15]:


plt.figure(figsize=(6,6))
plt.scatter(hdul[1].data['X'],hdul[1].data['Z'],facecolor='black',edgecolor='none',s=1.,alpha=0.3)
plt.xlabel('X (kpc)')
plt.ylabel('Z (kpc)')
_ = plt.axis([-50,50,-50,50])


# In[22]:


rbins,dreturn = return_density(np.log10(R),1.,rangevals=[0., 2.],bins=100)
plt.figure(figsize=(6,6))
plt.plot(np.log10(rbins),np.log10(dreturn),color='black')
plt.xlabel('log r (kpc)')
plt.ylabel('log rho')


# In[23]:


# call the empirical model maker
R,D,M,P = makemodel_empirical(rbins,dreturn,pfile='GSEbasis_empirical.txt')


# In[28]:


get_ipython().system('head -102 GSEbasis_empirical.txt')


# ### Build the basis!
import simpleSL

E = simpleSL.slfunctions('/home/mpetersen/GSEbasis_empirical.txt',2,6,0.,2.,2000)
# In[25]:


from exptool.utils import halo_methods

sph_file = '.slGSE_cache'
mod_file = 'GSEbasis_empirical.txt'

lmax,nmax,numr,cmap,rmin,rmax,scale,ltable,evtable,eftable = halo_methods.read_cached_table(sph_file)
xi,rarr,p0,d0 = halo_methods.init_table(mod_file,numr,rmin,rmax,cmap,scale)


# In[30]:


# plot the first 5 potential functions
plt.figure(figsize=(6,4))
for n in range(0,5): plt.plot(np.log10(rarr),eftable[0][n]*p0,color=cm.viridis(n/4.,1.))
plt.xlabel('log radius (kpc)')
plt.ylabel('function value')

E = simpleSL.coefsl(A[:,0],A[:,1],A[:,2],A[:,3],'/home/mpetersen/GSEbasis_empirical.txt',2,10)
>>> E[0]
array([ 4.13228848e+04, -9.67864595e+01, -5.35207119e+01,  2.56910430e+00,
       -6.52886971e+00,  2.98285971e+00, -9.29453752e+00,  4.29659946e+00,
        3.21584556e+00,  8.41393555e-01])
# ### modelfit utility
# 
# Strategies for smoothing: still up for discussion!

# modelfit --data=/disk01/mpetersen/Disk080/SLGridSph.NFW77 --type=TwoPowerTrunc --iterations=100
# 
# 
# 

# ### workflow examples
# 
# These are specific to my machine, so approach with care!
import numpy as np;import matplotlib.pyplot as plt

import simpleSL

E = simpleSL.slfunctions('/home/mpetersen/GSEbasis_empirical.txt',2,6,0.,2.,2000)
xvals = 10.**(np.linspace(0.,2.,2000))

# plot the first 5 potential functions
for n in range(0,5): plt.plot(xvals,E[0][n],color='black')

plt.savefig('/home/mpetersen/testfig.png')

import numpy as np;import matplotlib.pyplot as plt

import simpleSL

E = simpleSL.slfunctions('/home/mpetersen/SLGridEmpirical1.dat',2,6,-1.2,2.5,2000)
xvals = 10.**(np.linspace(-1.2,2.5,4000))


E = simpleSL.slfunctions('/disk01/mpetersen/Disk080/SLGridSph.NFW77',4,10,-3,0.5,4000)
xvals = 10.**(np.linspace(-3,0.5,4000))

# plot the first 5 potential functions
for n in range(0,5): plt.plot(xvals,E[0][n],color='black')

plt.savefig('/home/mpetersen/testfig.png')


from exptool.io import particle
O = particle.Input('/disk01/mpetersen/Disk080/OUT.system1_3m.00048','mw')

E = simpleSL.coefsl(O.mass,O.xpos-np.nanmean(O.xpos),O.ypos-np.nanmean(O.ypos),O.zpos-np.nanmean(O.zpos),'/disk01/mpetersen/Disk080/SLGridSph.NFW77',2,10)

# this workflow will also save the cache

mpirun haloprof  --LMAX=4 --NMAX=16 --MODFILE=/disk01/mpetersen/Disk080/SLGridSph.NFW77 --dir=/disk01/mpetersen/Disk080/ --beg=0 --end=1 --prefix=OUT  --filetype=PSPout --RMAX=1 --RSCALE=0.067 --CONLY -v --runtag=system1_3m --compname="mw"
