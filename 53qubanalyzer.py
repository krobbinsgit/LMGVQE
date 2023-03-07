# Code from a side project of mine a while ago. It analyzes the 53-qubit strings from the big Qiskit simulation I used to do.
# It worked in that case.

import numpy as np

fo=open('53qub10000.txt','r')
bigstr=fo.read() # Here I'm opening the file and reading it.
fo.close()
new=bigstr.replace('\'','')
new=new.replace('[','')
new=new.replace(']','')
new=new.replace(' ','')
new=new.split(',') # In these lines I'm treating the data
tot=len(new)

cl1s= [new[i] for i in range(int(tot/4))]
cl2s= [new[i+int(tot/4)] for i in range(int(tot/4))]
cl3s= [new[i+2*int(tot/4)] for i in range(int(tot/4))]
cl4s= [new[i+3*int(tot/4)] for i in range(int(tot/4))] # In these lines I split up everything into clique data.
alldata=[cl1s,cl2s,cl3s,cl4s] # A list of all the values


### ---- NEED TO DEFINE FUNCTIONS FOR COEFFICIENTS
### ---- THEN WE CAN DO OUTPUTEATERS

def kd(i,j):
    if i==j:
        return(1)
    else:
        return(0)
def idenc(M,V,W,nua,nub): # The identity coefficient
    N=2*M+nua+nub
    return(W*M**3/(6*N)+M**2*(nub-nua+W*(1+nua+nub))/(4*N)+M*(21*(nub-nua)+W*(14+21*(nua+nub)+6*nua*nub))/(24*N)+3*(nub-nua+W*(nua+nub+2*nua*nub))/(8*N))

def z1c(M,V,W,nua,nub):
    return((4*M**2+3*nua+5*nub+M*(8-6*W+4*W*nua+4*nub)+W*(8+5*nua-3*nub+2*nua*nub))/(16*M+8*(nua+nub)))
    
def zMc(M,V,W,nua,nub):
    return((4*M**2+5*nua+3*nub+M*(8+6*W+4*nua-4*W*nub)-W*(8-3*nua+5*nub+2*nua*nub))/(16*M+8*(nua+nub)))
def zjc(k,M,V,W,nua,nub):
    return((2*(-2*M*(W-1)+nua+nub+W*(4*k+nua-nub-2)))/(8*M+4*nua+4*nub))
# def oeater1(inp):# Now I need to define the output eater function for the diagonal clique

def zijc(k,M,V,W,nua,nub):
    return((4*k-2*M-W+nua-nub-(2*W*(2*k+nua)*(2*M-2*k+nub))/(2*M+nua+nub))/8)

def xjc(k,M,V,W,nua,nub):
    return(V/(4*M+2*nua+2*nub)* (1+(kd(k,M)+kd(k,1))/2)/2*((nua+2*k)*(nua+2*k-1)*(2*M+nub-2*k+1)*(2*M+nub-2*k+2))**0.5)
    
def xzjc(k,M,V,W,nua,nub): # This perfectly agrees with Mathematica
    return(V/4/(4*M+2*nua+2*nub)*((nua+2*k)*(nua+2*k-1)*(2*M+nub-2*k+1)*(2*M+nub-2*k+2))**0.5)
def zxjc(k,M,V,W,nua,nub):
    return(-xzjc(k+1,M,V,W,nua,nub)) # Might have this backwards!

def oeater1(V,W,nua,nub,st): # The first output eater function. I think it's good!
    M=len(st)
    if M>1:
        base=idenc(M,V,W,nua,nub)+z1c(M,V,W,nua,nub)*(-1)**int(st[0])+zMc(M,V,W,nua,nub)*(-1)**int(st[M-1])
    else:
        base = idenc(1,V,W,nua,nub)+2*zjc(1,1,V,W,nua,nub)*(-1)**int(st[0])
    if M>=2:
        for j in range(1,M-1):
            base+=zjc(j+1,M,V,W,nua,nub)*(-1)**int(st[j])
        for j in range(M-1):
            base+=zijc(j+1,M,V,W,nua,nub)*(-1)**(int(st[j])+int(st[j+1]))
    return(base)

def oeater2(V,W,nua,nub,st): # This one seems to be good!
    M=len(st)
    base=0
    for j in range(M):
        base+=xjc(j+1,M,V,W,nua,nub)*(-1)**int(st[j])
    return(base)



def oeater3(V,W,nua,nub,st):  #Works!
    M=len(st)
    base=0
    if M<2:
        return(0)
    else:
        for j in range(0,M-1,2):
            base+=(xzjc(j+1,M,V,W,nua,nub)*(-1)**int(st[j]))+(zxjc(j+1,M,V,W,nua,nub)*(-1)**int(st[j+1]))
    return(base)

def oeater4(V,W,nua,nub,st): # Works!
    M=len(st)
    base=0
    if M<3:
        return(0)
    else:
        for j in range(1,M-1,2):
            base+=(xzjc(j+1,M,V,W,nua,nub)*(-1)**int(st[j]))+(zxjc(j+1,M,V,W,nua,nub)*(-1)**int(st[j+1]))
    return(base)

def distrfinder(V,W,nua,nub,inp_data): # Finds the distribution of single-shot estimates of <H>
    M=len(inp_data[0][0])
    h_distr=[(oeater1(V,W,nua,nub,inp_data[0][j])+oeater2(V,W,nua,nub,inp_data[1][j])+oeater3(V,W,nua,nub,inp_data[2][j])+oeater4(V,W,nua,nub,inp_data[3][j])) for j in range(len(inp_data[0]))]
    return(h_distr)

    
dis=distrfinder(np.sqrt(3),np.sqrt(2),0,0,alldata)
var=np.std(dis)/np.sqrt(len(dis))
mn=sum(dis)/len(dis)
print("The mean is %f +/- %f " % (mn,var))


## That's pretty close if not right on.