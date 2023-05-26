# This is the file that will take in all the functions and inputs, then output something pretty saying stuff like
## Simulation agreed with theory OR Simulation failed!
## The predicted eigenvalue should be ______
## We sampled an eigenvalue of ______ +/- ______ with __ samples
# I'd like to set it up so that it "waits" for inputs manually. I've never figured that shit out.
import numpy as np
from lmg import total_circuit_runner
from analyzer import distrfinder, distrfinder2
from state_generator import state_finder_fock, angle_finder
import random as ra
import dwave.gate.simulator
from lmg import state_prep
import matplotlib.pyplot as plt
# Gives correct answer when fed sample data from research
# Theodor has fixed the measurement issue and it now works after I cloned his dwave-gate repo


##Begin by checking the 53-qubit data and associated analyzing functions
# targ_val,targ_state=state_finder_fock(53,np.sqrt(3),np.sqrt(2),0,0,0)
# distr=distrfinder2(np.sqrt(3),np.sqrt(2),0,0)
# sampling_uncertainty = np.std(distr)/np.sqrt(len(distr))
# mean=sum(distr)/len(distr)
# print(f'\nWe can check the 53-qubit data.\nFor the test, the target energy is {np.round(targ_val,5)} while we obtained a value of {np.round(mean,5)} +/- {np.round(sampling_uncertainty,5)}')
# if abs(mean)-sampling_uncertainty<=abs(targ_val)<=abs(mean)+sampling_uncertainty:
#     print('Success!\n')
# else:
#     print('Failure!\n')


def single_run(M,V,W,nua,nub,energy_level,file_name_bitstring='test_dest',shots=10**4): 
    '''
    Will output energy and some basic data in a printed statement as well as an energy distribution graph.
    Simulates the energy_levelth eigenstate of the described LMG Hamiltonian and estimates the eigenvalue
    '''
    targ_val,targ_state=state_finder_fock(M,V,W,nua,nub,energy_level)
    angs=angle_finder(targ_state)
    total_circuit_runner(angs,file_name_bitstring,shots)
    distr=distrfinder(V,W,nua,nub,f'{file_name_bitstring}.txt')
    mean=sum(distr)/len(distr)
    standard_error=np.std(distr)/np.sqrt(shots)
    print(f'\nThe known energy value is {np.round(targ_val,4)} while we estimated {np.round(mean,4)}')
    print(f'The relative error is {abs(np.round(100*(mean-targ_val)/targ_val,1))}%\n')
    # We define bin width as bin_width= 4 * (max(distr) - min(distr)) / np.sqrt(shots)
    plt.hist(distr, density=True, bins=int(np.sqrt(shots)/4), color='b', label='Single Shot Energy Distribution')  # density=False would make counts
    plt.ylabel('Counts')
    plt.axvline(x = targ_val, color = 'g', label = 'calculated_expectation_value')
    plt.xlabel('Single Shot Estimated Energy')
    plt.show()
    # num_st_errors_away=abs(mean-targ_val)/standard_error
    # if num_st_errors_away<=1:
    #     print('The estimate was within 1 standard error')
    # else:
    #     print(f'The estimate was within {int(np.ceil(num_st_errors_away))} standard errors')
    





def mult_test2(num_tests,shots=10**4):# Runs tests and sees how many are within 100/sqrt(shots)% of the expected value
    rel_error_percents=[]
    for j in range(num_tests):
        M=ra.randint(1,5)
        V=ra.uniform(0.1,100)
        W=V*ra.random()*(-1)**ra.randint(0,1)
        nua=ra.randint(0,1)
        nub=ra.randint(0,1)
        targ_val, targ_state=state_finder_fock(M,V,W,nua,nub,0)
        angs=angle_finder(targ_state)
        total_circuit_runner(angs,'test_dest',shots)
        distr=distrfinder(V,W,nua,nub,'test_dest')
        mean=sum(distr)/len(distr)
        rel_error=abs(np.round(100*(mean-targ_val)/targ_val,2))
        rel_error_percents.append(rel_error)
    num_within_one_percent=0
    for err in rel_error_percents:
        print(f'The error was {np.round(err,2)}')
        if abs(err)<=100/np.sqrt(shots):
            num_within_one_percent+=1
    print(f'\n{np.round(100*num_within_one_percent/num_tests,2)}% were within percentile acceptability')

def mult_test3(num_tests,shots=10**4):# Runs tests and prints out relevant information if the error is beyond 5%
    for j in range(num_tests):
        M=ra.randint(1,5)
        V=ra.uniform(0.1,10)
        W=V*ra.random()*(-1)**ra.randint(0,1)
        nua=ra.randint(0,1)
        nub=ra.randint(0,1)
        targ_val, targ_state=state_finder_fock(M,V,W,nua,nub,0)
        angs=angle_finder(targ_state)
        total_circuit_runner(angs,'test_dest',shots)
        base_state0= list(dwave.gate.simulator.simulate(state_prep(angs)))
        base_state0.reverse()
        base_state=[]
        for k in base_state0:
            if np.round(k,15)!=0.0:
                base_state.append(k)
        targ_state=list(targ_state)

        targ_equal_baseq=True
        for k in range(len(targ_state)):
            if np.round(targ_state[k]-base_state[k],5)!=0:
                targ_equal_baseq=False
        distr=distrfinder(V,W,nua,nub,'test_dest')
        mean=sum(distr)/len(distr)
        rel_error=abs(np.round(100*(mean-targ_val)/targ_val,2))
        if abs(rel_error)>=5:
            print(f'Target value is {targ_val}')
            print(f'Expectation estimate is {mean}')
            print(f'Error was {rel_error}')
            print(f'M= {M}')
            print(f'V= {V}')
            print(f'W= {W}')
            print(f'nua= {nua}')
            print(f'nub= {nub}')
            if targ_equal_baseq==True:
                print('Target state equals output state from circuit')
            else:
                print(targ_state)
                print(base_state)
            print()
        else:
            print('Expectation value is within 5%')


def mult_test4(num_tests,shots=10**4):# Runs tests and prints out relevant information if the error is beyond uncertainty bounds
    num_success=0
    for j in range(num_tests):
        M=ra.randint(1,5)
        V=ra.uniform(0.1,10)
        W=V*ra.random()*(-1)**ra.randint(0,1)
        nua=ra.randint(0,1)
        nub=ra.randint(0,1)
        targ_val, targ_state=state_finder_fock(M,V,W,nua,nub,ra.randint(0,M-1))
        angs=angle_finder(targ_state)
        total_circuit_runner(angs,'test_dest',shots)
        base_state0= list(dwave.gate.simulator.simulate(state_prep(angs)))
        base_state0.reverse()
        base_state=[]
        for k in base_state0:
            if np.round(k,15)!=0.0:
                base_state.append(k)
        targ_state=list(targ_state)
        targ_equal_baseq=True
        for k in range(len(targ_state)):
            if np.round(targ_state[k]-base_state[k],5)!=0:
                targ_equal_baseq=False
        distr=distrfinder(V,W,nua,nub,'test_dest')
        unc=np.std(distr)/np.sqrt(shots)
        mean=sum(distr)/len(distr)
        rel_error=abs(np.round(100*(mean-targ_val)/targ_val,2))
        if mean-unc <= targ_val <= mean+unc:
            print('<H> estimate is within one standard error')
            num_success+=1
        else:
            print(f'\nTarget value is {np.round(targ_val,5)}')
            print(f'<H> estimate is {np.round(mean,5)}')
            print(f'Error is {rel_error}%')
            print(f'Standard error is {np.round(unc,3)}')
            print(f'<H> estimate is {np.round(abs((mean-targ_val)/unc),1)} standard errors from target value ')
            # print(f'M= {M}')
            # print(f'V= {V}')
            # print(f'W= {W}')
            # print(f'nua= {nua}')
            # print(f'nub= {nub}')
            if targ_equal_baseq==True:
                print('Target state equals output state from circuit')
            else:
                print(targ_state)
                print(base_state)
            print()
    print(f'\nOut of {num_tests} trials, {np.round(100*num_success/num_tests,1)}% were within one standard error\n')


                



def step_mult_test(num_tests):
    for M in range(1,11):
        success_count=0
        for j in range(num_tests):
            V=ra.uniform(0.1,10)
            W=V*ra.random()*(-1)*(-1)**ra.randint(0,1)
            nua=ra.randint(0,1)
            nub=ra.randint(0,1)
            shots=10**4
            targ_val,targ_state=state_finder_fock(M,V,W,nua,nub,0)
            angs=angle_finder(targ_state)
            total_circuit_runner(angs,'test_dest',shots)
            distr=distrfinder(V,W,nua,nub,'test_dest')
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
        W=-V*ra.random()*((-1)**ra.randint(0,1))
        nua=ra.randint(0,1)
        nub=ra.randint(0,1)
        shots=10**4
        targ_val,targ_state=state_finder_fock(M,V,W,nua,nub,0)
        angs=angle_finder(targ_state)
        total_circuit_runner(angs,'test_dest',shots)
        distr=distrfinder(V,W,nua,nub,'test_dest')
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

def error_perc_test(num_tests):
    percent_error=[]
    for j in range(num_tests):
        M=ra.randint(1,5)
        V=ra.uniform(0.1,10)
        W=V*ra.random()*((-1)**ra.randint(0,1))
        nua=ra.randint(0,1)
        nub=ra.randint(0,1)
        shots=10**4
        targ_val,targ_state=state_finder_fock(M,V,W,nua,nub,0)
        angs=angle_finder(targ_state)
        total_circuit_runner(angs,'test_dest',shots)
        distr=distrfinder(V,W,nua,nub,'test_dest')
        mean=sum(distr)/len(distr)
        sampling_uncertainty = np.std(distr)/np.sqrt(shots)
        #print(f'The target energy is {np.round(targ_val,5)} while we obtained a value of {np.round(mean,5)} +/- {np.round(sampling_uncertainty,5)}')
        percent_error.append(abs(100*np.round((mean-targ_val)/targ_val,3)))
    print(f'Mean percent error is {np.round(sum(percent_error)/len(percent_error),2)}')
    print(f'+/- {np.std(percent_error)/np.sqrt(len(percent_error))}')
    print(f'Max error was {max(percent_error)}')
    return((percent_error,distr))


def shots_scale_test():
    out_dict={}
    for shots in (10,10**2,10**3,10**4):
        percent_error=[]
        M=ra.randint(1,5)
        V=ra.uniform(0.1,10)
        W=V*ra.random()*((-1)**ra.randint(0,1))
        nua=ra.randint(0,1)
        nub=ra.randint(0,1)
        targ_val,targ_state=state_finder_fock(M,V,W,nua,nub,0)
        angs=angle_finder(targ_state)
        total_circuit_runner(angs,'test_dest',10**4)
        distr=distrfinder(V,W,nua,nub,'test_dest')
        mean=sum(distr)/len(distr)
        sampling_uncertainty = np.std(distr)/np.sqrt(shots)
        #print(f'The target energy is {np.round(targ_val,5)} while we obtained a value of {np.round(mean,5)} +/- {np.round(sampling_uncertainty,5)}')
        out_dict[shots]=abs(100*np.round((mean-targ_val)/targ_val,4))
        print(f'Finished with {shots} shots.')
    return(out_dict)

# master_dict={10:[],100:[],1000:[],10000:[]}
# for j in range(20):
#     out_dict=shots_scale_test()
#     temp=master_dict[10]
#     temp.append(out_dict[10])
#     master_dict[10]=temp
#     temp=master_dict[100]
#     temp.append(out_dict[100])
#     master_dict[100]=temp
#     temp=master_dict[1000]
#     temp.append(out_dict[1000])
#     master_dict[1000]=temp
#     temp=master_dict[10000]
#     temp.append(out_dict[10000])
#     master_dict[10000]=temp
# print(f'For 10**1 shots we obtained an average error of {sum(master_dict[10])/len(master_dict[10])}%')
# print(f'This is {sum(master_dict[10])/len(master_dict[10])/100*np.sqrt(10)}\n')
# print(f'For 10**2 shots we obtained an average error of {sum(master_dict[100])/len(master_dict[100])}%')
# print(f'This is {sum(master_dict[100])/len(master_dict[100])/100*np.sqrt(100)}\n')
# print(f'For 10**3 shots we obtained an average error of {sum(master_dict[1000])/len(master_dict[1000])}%')
# print(f'This is {sum(master_dict[1000])/len(master_dict[1000])/100*np.sqrt(1000)}\n')
# print(f'For 10**4 shots we obtained an average error of {sum(master_dict[10000])/len(master_dict[10000])}%')
# print(f'This is {sum(master_dict[10000])/len(master_dict[10000])/100*np.sqrt(10000)}\n')

def mult_test(num_tests): # Tests to see if the final <H> is within one sampling uncertainty unit of the expected answer.
    success_count=0
    for j in range(num_tests):
        M=ra.randint(1,10)
        V=ra.uniform(0.1,10)*(-1)**ra.randint(0,1)
        W=V*ra.random()*(-1)**ra.randint(0,1)
        nua=ra.randint(0,1)
        nub=ra.randint(0,1)
        shots=10**4
        targ_val,targ_state=state_finder_fock(M,V,W,nua,nub,ra.randint(0,M-1))
        angs=angle_finder(targ_state)
        total_circuit_runner(angs,'test_dest',shots)
        distr=distrfinder(V,W,nua,nub,'test_dest')
        mean=sum(distr)/len(distr)
        sampling_uncertainty = np.std(distr)/np.sqrt(shots)
        #print(f'The target energy is {np.round(targ_val,5)} while we obtained a value of {np.round(mean,5)} +/- {np.round(sampling_uncertainty,5)}')
        if abs(mean)-sampling_uncertainty<=abs(targ_val)<=abs(mean)+sampling_uncertainty:
            success_count+=1
    print(f'\nSuccessful in {int(100*success_count/num_tests)}% of trials.')



mult_test(10)

# SOMETIMES FAILS... TOO OFTEN
# FIGURE OUT WHY!!! First found May 11 2023
# FIX 1 (5-18-2023): The angles were wrong and producing negatives of some state vector elements. Errors average +/- 3% when they should be +/- 1% or less for 10k shots
# Angle finder agrees with an example in dissertation. Likely not the source of error.
# Found a sign/trig error in the basic state-prep circuit. Should be fixed as of now.
# Nothing is obviously incorrect in the coefficient functions like zijc, etc. Compared to thesis and rewrote several to double-check
# Output state from state-prep agrees with target state (possible reversal of list?)
# States seem a bit more uniform than what I remember, but that shouldn't matter.
# I excluded target <H> close to 0 and still got big errors, although not too big.
# mult_test4() seems to indicate that majority of failures are just beyond one standard error. Is it possible that the standard deviation of the distribution is unusually small?

# Trial notes below: 25 randomly generated problems for each row.
# In all |W| < |V|, V>0 is randomly picked from 0.1 to 10 and M is randomly picked from 1 to 10

## Is it possible failure is actually in solving for eigenvalues instead of simulation?
## In the below, % refers to percentage successful runs
## Positive W, and random nua/nub: 64% 
## Positive W, fixed nua=nub=0: 
## Positive W, fixed nua=nub=1: 
## Positive W, fixed nua=0 and nub=1: 
## Positive W, fixed nua=1 and nub=0: 
## Negative W and random nua/nub: 
## Negative W, fixed nua=nub=0: 
## Negative W, fixed nua=nub=1: 
## Negative W, fixed nua=0 and nub=1: 
## Negative W, fixed nua=1 and nub=0: 

# Trial 2: Varying M but letting everything else be random.
# 25 runs per M with 10k shots per run
## M=1: 
## M=2: 
## M=3:
## M=4: 
## M=5: 
## M=6: 
## M=7: 
## M=8: 
## M=9: 
## M=10: 

# Trial 3: How bad are the failures?
# Random everything, 50 runs, 10k shots per run
# checking ||target_val| - |data mean||/sampling_uncertainty
## Often by 10 to 100 uncertainty units (sampling uncertainty = std dev / sqrt(num shots))







