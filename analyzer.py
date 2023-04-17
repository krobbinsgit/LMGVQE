# This is the file which will have the python code to interpret my results.
# This will be based on the 53qubanalyzer.py file
import numpy as np


def kd(i,j): # Kronecker Delta
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

def distrfinder(V,W,nua,nub,inp_data_filename): # Finds the distribution of single-shot estimates of <H> FIX TEST AGAINST KNOWN SOLUTIONS
    fo=open(inp_data_filename,'r')
    bigstr=fo.readlines() # Here I'm opening the file and reading it.
    fo.close()
    inp_data=[(lilstr.split(','))[0:-1] for lilstr in bigstr]
    M=len(inp_data[0][0])
    if M==1:
        h_distr=[(oeater1(V,W,nua,nub,inp_data[0][j])+oeater2(V,W,nua,nub,inp_data[1][j])) for j in range(len(inp_data[0]))]
    elif M==2:
        h_distr=[(oeater1(V,W,nua,nub,inp_data[0][j])+oeater2(V,W,nua,nub,inp_data[1][j])+oeater3(V,W,nua,nub,inp_data[2][j])) for j in range(len(inp_data[0]))]
    else:
        h_distr=[(oeater1(V,W,nua,nub,inp_data[0][j])+oeater2(V,W,nua,nub,inp_data[1][j])+oeater3(V,W,nua,nub,inp_data[2][j])+oeater4(V,W,nua,nub,inp_data[3][j])) for j in range(len(inp_data[0]))]
    return(h_distr)

def distrfinder2(V,W,nua,nub): # Just changing the input to the 53 qubits data gives the exactly correct answer. This is likely NOT the problem.
    fo=open('53qublines2.txt','r')
    bigstr=fo.readlines() # Here I'm opening the file and reading it.
    out=[bigstr[2*k] for k in range(0,40000)]
    out=[elem.replace(",","") for elem in out]
    out= [elem.replace("\"","") for elem in out]
    out= [elem.replace(" ","") for elem in out]
    out= [elem[0:-1] for elem in out]
    inp_data=[out[0:10**4],out[10**4:2*10**4],out[2*10**4:3*10**4],out[3*10**4:4*10**4]]
    M=len(inp_data[0][0])
    if M==1:
        h_distr=[(oeater1(V,W,nua,nub,inp_data[0][j])+oeater2(V,W,nua,nub,inp_data[1][j])) for j in range(len(inp_data[0]))]
    elif M==2:
        h_distr=[(oeater1(V,W,nua,nub,inp_data[0][j])+oeater2(V,W,nua,nub,inp_data[1][j])+oeater3(V,W,nua,nub,inp_data[2][j])) for j in range(len(inp_data[0]))]
    else:
        h_distr=[(oeater1(V,W,nua,nub,inp_data[0][j])+oeater2(V,W,nua,nub,inp_data[1][j])+oeater3(V,W,nua,nub,inp_data[2][j])+oeater4(V,W,nua,nub,inp_data[3][j])) for j in range(len(inp_data[0]))]
    return(h_distr)

#print(distrfinder(3,1.2,0,0,'test_dest.txt'))
#distr=distrfinder2(np.sqrt(3),np.sqrt(2),0,0)
#print(sum(distr)/len(distr))

# fo=open('53qublines2.txt','r')
# bigstr=fo.readlines() # Here I'm opening the file and reading it.
# out=[bigstr[2*k] for k in range(0,40000)]
# out=[elem.replace(",","") for elem in out]
# out= [elem.replace("\"","") for elem in out]
# out= [elem.replace(" ","") for elem in out]
# out= [elem[0:-1] for elem in out]
# print(out[0])
# print(out[1])
# inp_data=[out[0:10**4],out[10**4:2*10**4],out[2*10**4:3*10**4],out[3*10**4:4*10**4]]
# lens=[]
# for k in range(len(inp_data[0])):
#     if len(inp_data[0][k]) not in lens:
#         lens.append(len(inp_data[0][k]))
#         print(k)
# print(lens)

