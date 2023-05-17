# This will take in M, V, W, nua, nub and energy level and then output the angles required for the state and the expectation value
import numpy as np


def ham_maker(M,V,W,nua,nub): # Will generate the LMG Hamiltonian matrix in the Fock basis
    ## Tested for a few values of M against Mathematica quickham[]. Agrees.
    main_diagonal=[(-4*k+2*M-nua+nub)/2+(W*(2*k+nua)*(2*M+nub-2*k))/(2*M+nua+nub)+W/2 for k in range(M,-1,-1)]
    off_diag=[V/(2*(2*M+nua+nub))*np.sqrt((nub+2*k+1)*(nub+2*k+2)*(2*M+nua-2*k)*(2*M+nua-2*k-1)) for k in range(0,M)] 
    # print("Main Diag is")
    # print(str(main_diagonal)+'\n')
    # print("Off diag is")
    # print(off_diag)
    return(np.diag(main_diagonal, 0) + np.diag(off_diag, -1) + np.diag(off_diag, 1))



def state_finder_fock(M,V,W,nua,nub,energy_level): # Given a hamiltonian matrix, find the (energy_level)th eigenstate and eigenvalue
    if energy_level>=M or energy_level<0:
        print("Desired energy level is not within eigenspectrum of model. Please choose a value from 0 to M-1.")
        exit()
    else:
        hamiltonian=ham_maker(M,V,W,nua,nub) # Very sparse, tridiagonal form. Can diagonalize more easily with that?
        eigs=np.linalg.eigh(hamiltonian)
        eigvals=eigs[0]
        eigvecs=eigs[1]
        eigvecs=np.transpose(eigvecs)
        return((eigvals[energy_level],eigvecs[energy_level])) # Returns a tuple of (eigenvalue, normalized eigenvector)

def angle_finder(inp_state): # Given an eigenstate to prepare, it outputs the necessary angles for the circuit.
    # Eigenvectors and -values seem to agree with Mathematica...
    inp_state=list(inp_state)
    inp_state.reverse()
    length = len(inp_state)
    pre=[2*np.arccos(inp_state[j]/np.sqrt(sum([inp_state[k]**2 for k in range(j,length)]))) for j in range(0,length-2)] # FIX
    pre.append(2*np.sign(inp_state[-1])*np.arccos(inp_state[length-2]/np.sqrt(inp_state[length-2]**2+inp_state[length-1]**2))) # FIX
    post=[]
    for ind in pre:
        if ind>=0:
            post.append(2*np.pi-ind) # Not super sure why this needs to be here, but alright.
        else:
            post.append(2*np.pi+ind) # Not super sure why this needs to be here, but alright.
    return(post) 




