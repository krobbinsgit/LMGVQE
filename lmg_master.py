# This is the file that will take in all the functions and inputs, then output something pretty saying stuff like
## Simulation agreed with theory OR Simulation failed!
## The predicted eigenvalue should be ______
## We sampled an eigenvalue of ______ +/- ______ with __ samples
# I'd like to set it up so that it "waits" for inputs manually. I've never figured that shit out.
import numpy as np
from lmg import all_my_circuits
from analyzer import distrfinder, distrfinder2
from state_generator import state_finder_fock, angle_finder
# FIX FAILING PRETTY BADLY
# Gives correct answer when fed sample data from research
# On closer look, examining the measurement from clique 1 results in bad bitstrings
# Something is wrong with entanglement in the measurement system!
# I spoke with Theodor and I need to clone something or other to do it.


# Begin by checking the 53-qubit data and associated analyzing functions
targ_val,targ_state=state_finder_fock(53,np.sqrt(3),np.sqrt(2),0,0,0)
distr=distrfinder2(np.sqrt(3),np.sqrt(2),0,0)
sampling_uncertainty = np.std(distr)/np.sqrt(len(distr))
mean=sum(distr)/len(distr)
print(f'\nWe can check the 53-qubit data.\nFor the test, the target energy is {np.round(targ_val,5)} while we obtained a value of {np.round(mean,5)} +/- {np.round(sampling_uncertainty,5)}')
if abs(mean)-sampling_uncertainty<=abs(targ_val)<=abs(mean)+sampling_uncertainty:
    print('Success!\n')
else:
    print('Failure!\n')


M=5
V=3.2
W=-1.5
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




