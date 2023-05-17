# This is the file that will take in all the functions and inputs, then output something pretty saying stuff like
## Simulation agreed with theory OR Simulation failed!
## The predicted eigenvalue should be ______
## We sampled an eigenvalue of ______ +/- ______ with __ samples
# I'd like to set it up so that it "waits" for inputs manually. I've never figured that shit out.
import numpy as np
from lmg import all_my_circuits
from analyzer import distrfinder, distrfinder2
from state_generator import state_finder_fock, angle_finder
import random as ra
# Gives correct answer when fed sample data from research
# Theodor has fixed the measurement issue and it now works after I cloned his dwave-gate repo


##Begin by checking the 53-qubit data and associated analyzing functions
targ_val,targ_state=state_finder_fock(53,np.sqrt(3),np.sqrt(2),0,0,0)
distr=distrfinder2(np.sqrt(3),np.sqrt(2),0,0)
sampling_uncertainty = np.std(distr)/np.sqrt(len(distr))
mean=sum(distr)/len(distr)
print(f'\nWe can check the 53-qubit data.\nFor the test, the target energy is {np.round(targ_val,5)} while we obtained a value of {np.round(mean,5)} +/- {np.round(sampling_uncertainty,5)}')
if abs(mean)-sampling_uncertainty<=abs(targ_val)<=abs(mean)+sampling_uncertainty:
    print('Success!\n')
else:
    print('Failure!\n')


# M=5
# V=ra.uniform(0.1,10)
# W=-V*ra.random() 
# nua=0
# nub=0
# shots=10**4
# targ_val,targ_state=state_finder_fock(M,V,W,nua,nub,0)
# angs=angle_finder(targ_state)
# all_my_circuits(angs,shots,'test_dest')
# distr=distrfinder(V,W,nua,nub,'test_dest.txt')
# mean=sum(distr)/len(distr)
# sampling_uncertainty = np.std(distr)/np.sqrt(shots)
# print(f'The target energy is {np.round(targ_val,5)} while we obtained a value of {np.round(mean,5)} +/- {np.round(sampling_uncertainty,5)}')
# if abs(mean)-sampling_uncertainty<=abs(targ_val)<=abs(mean)+sampling_uncertainty:
#     print('Success!')
# else:
#     print('Failure!')

def mult_test(num_tests):
    success_count=0
    for j in range(num_tests):
        M=ra.randint(1,10)
        V=ra.uniform(0.1,10)
        W=V*ra.random()*(-1)**ra.randint(0,1)
        nua=ra.randint(0,1)
        nub=ra.randint(0,1)
        shots=10**4
        targ_val,targ_state=state_finder_fock(M,V,W,nua,nub,0)
        angs=angle_finder(targ_state)
        all_my_circuits(angs,shots,'test_dest')
        distr=distrfinder(V,W,nua,nub,'test_dest.txt')
        mean=sum(distr)/len(distr)
        sampling_uncertainty = np.std(distr)/np.sqrt(shots)
        #print(f'The target energy is {np.round(targ_val,5)} while we obtained a value of {np.round(mean,5)} +/- {np.round(sampling_uncertainty,5)}')
        if abs(mean)-sampling_uncertainty<=abs(targ_val)<=abs(mean)+sampling_uncertainty:
            success_count+=1
    print(f'\nSuccessful in {int(100*success_count/num_tests)}% of trials.')

def step_mult_test(num_tests):
    for M in range(1,11):
        success_count=0
        for j in range(num_tests):
            V=ra.uniform(0.1,10)
            W=V*ra.random() **((-1)**ra.randint(0,1))
            nua=ra.randint(0,1)
            nub=ra.randint(0,1)
            shots=10**4
            targ_val,targ_state=state_finder_fock(M,V,W,nua,nub,0)
            angs=angle_finder(targ_state)
            all_my_circuits(angs,shots,'test_dest')
            distr=distrfinder(V,W,nua,nub,'test_dest.txt')
            mean=sum(distr)/len(distr)
            sampling_uncertainty = np.std(distr)/np.sqrt(shots)
            #print(f'The target energy is {np.round(targ_val,5)} while we obtained a value of {np.round(mean,5)} +/- {np.round(sampling_uncertainty,5)}')
            if abs(mean)-sampling_uncertainty<=abs(targ_val)<=abs(mean)+sampling_uncertainty:
                success_count+=1
        print(f'\nFor M={M} it was successful in {int(100*success_count/num_tests)}% of trials.')


def error_quant_test(num_tests):
    success_count=0
    for j in range(num_tests):
        M=ra.randint(1,10)
        V=ra.uniform(0.1,10)
        W=-V*ra.random() #**((-1)**ra.randint(0,1))
        nua=ra.randint(0,1)
        nub=ra.randint(0,1)
        shots=10**4
        targ_val,targ_state=state_finder_fock(M,V,W,nua,nub,0)
        angs=angle_finder(targ_state)
        all_my_circuits(angs,shots,'test_dest')
        distr=distrfinder(V,W,nua,nub,'test_dest.txt')
        mean=sum(distr)/len(distr)
        sampling_uncertainty = np.std(distr)/np.sqrt(shots)
        #print(f'The target energy is {np.round(targ_val,5)} while we obtained a value of {np.round(mean,5)} +/- {np.round(sampling_uncertainty,5)}')
        if abs(mean)-sampling_uncertainty<=abs(targ_val)<=abs(mean)+sampling_uncertainty:
            continue
        else:
            print(abs(mean)-sampling_uncertainty)
            print(abs(targ_val))
            print(abs(mean)+sampling_uncertainty)
            print()
    


mult_test(100)

# SOMETIMES FAILS... TOO OFTEN
# FIGURE OUT WHY!!! DATED MAY 11 2023
# Angle finder agrees with an example in dissertation. Likely not the source of error.
# Nothing is obviously incorrect in the coefficient functions like zijc, etc. Rewriting some seems to have helped a bit


# Trial notes below: 25 randomly generated problems for each row.
# In all |W| < |V|, V>0 is randomly picked from 0.1 to 10 and M is randomly picked from 1 to 10

## Is it possible failure is actually in solving for eigenvalues instead of simulation?
## Positive W, and random nua/nub: 40% success (seems to be anomalously high upon re-running)
## Positive W, fixed nua=nub=0: 20% success
## Positive W, fixed nua=nub=1: 28% success
## Positive W, fixed nua=0 and nub=1: 24% success
## Positive W, fixed nua=1 and nub=0: 24% success
## Negative W and random nua/nub: 64% success (I thought it was the opposite?)
## Negative W, fixed nua=nub=0: 76% success
## Negative W, fixed nua=nub=1: 52% success
## Negative W, fixed nua=0 and nub=1: 72% success
## Negative W, fixed nua=1 and nub=0: 72% success

# Trial 2: Varying M but letting everything else be random.
# 25 runs per M with 10k shots per run
## M=1: 60% success
## M=2: 4% success
## M=3: 20% success
## M=4: 12% success
## M=5: 12% success
## M=6: 4% success
## M=7: 12% success
## M=8: 16% success
## M=9: 28% success
## M=10: 12% success

# Trial 3: How bad are the failures?
# Random everything, 50 runs, 10k shots per run
# checking ||target_val| - |data mean||/sampling_uncertainty
## Often by 10 to 100 uncertainty units.







