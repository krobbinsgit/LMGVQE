# This is the file that will take in all the functions and inputs, then output something pretty saying stuff like
## Simulation agreed with theory OR Simulation failed!
## The predicted eigenvalue should be ______
## We sampled an eigenvalue of ______ +/- ______ with __ samples
# I'd like to set it up so that it "waits" for inputs manually. I've never figured that shit out.
import numpy as np
from lmg import all_my_circuits
from analyzer import distrfinder
from state_generator import state_finder_fock, angle_finder
# FIX FAILING PRETTY BADLY
M=5
V=3.2
W=-1
nua=0
nub=0
shots=10**4
targ_val,targ_state=state_finder_fock(M,V,W,nua,nub,0)
angs=angle_finder(targ_state)
all_my_circuits(angs,shots,'test_dest')
distr=distrfinder(V,W,nua,nub,'test_dest.txt')
mean=sum(distr)/len(distr)
sampling_uncertainty = np.std(distr)/np.sqrt(shots)
print(f'The target energy is {np.round(targ_val,5)} while we obtained a value of {np.round(mean,5)} +/- {np.round(sampling_uncertainty,5)}')
if abs(mean)-sampling_uncertainty<=abs(targ_val)<=abs(mean)+sampling_uncertainty:
    print('Success!')
else:
    print('Failure!')
