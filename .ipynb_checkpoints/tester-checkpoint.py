import dwave.gate.operations as gt
from dwave.gate import Circuit
import dwave.gate.simulator
import numpy as np
import random as ra
from lmg import total_circuit_runner, state_prep
from state_generator import state_finder_fock, angle_finder, ham_maker
from analyzer import distrfinder

# What's wrong (5-18-2023)?
# -- The estimated value of <H> is too far off in too many trials.
# -- for some settings it's only a 20% success rate! Should be really close to 100%
# -- Appears to be some correlation between - W values and higher success probability
# -- Checked and retyped coefficient functions. All seem good.
# -- I inverted the diagonalizer circuits for cliques 3 and 4. No improvement.
# -- I could check the outputeaters, but they're identical to the 53qubit one and that works perfectly.
# -- I checked the output state. It agreed with the target state (up to possible reversal but I'm pretty sure it agrees)
# -- Some of the states seem more uniform than I remember them being.
# -- All of this together indicates the issue is likely in steps before analysis:
# # Finding the eigenvalues and eigenvectors with numpy
# # Finding the angles to plug into the circuits... needs more thorough checks. # Found a bug and now it's flawless
# # The circuits themselves # At least state_prep is fine
# # Measuring and treating the bitstrings
# # The code counting successes and failures. # I checked this in multiple ways.
# # It's possible that I'm not pairing eigenvalues with the proper eigenstates? NOPE PERFECT
# # Some of the states' coefficients were negative when they should be positive. Fixed as of 5-18-2023
# # Even with 1000 randomly generated problems, the output state agreed with the target state to 10 decimal places.

inc_len=0
inc_vals=0
for j in range(1000):
  vals = []
  M = ra.randint(1, 10)
  V = ra.uniform(0.1, 10)
  W = V*ra.random()*(-1)*(-1)**ra.randint(0, 1)
  nua = ra.randint(0, 1)
  nub = ra.randint(0, 1)
  # shots=10**4
  targ_val, targ_state = state_finder_fock(M, V, W, nua, nub, 0)
  angs = angle_finder(targ_state)
  out_state = dwave.gate.simulator.simulate(state_prep(angs))
  out_state = np.flip(out_state)
  out = []
  for k in range(len(out_state)):
      if np.round(out_state[k], 20) != 0.0j:
          out.append(out_state[k])

  # negq='negative'
  # if W>=0:
  #   negq='positive'
  # if np.round(targ_state[1]+out[1],10)==0.j:
  #    print(f'Sign error! W is {negq}\n')

  for k in range(len(out)):
      vals.append(np.round((out[k]-targ_state[k]), 5))
  for entry in vals:
      if entry!=0.0:
          print('WRONG STATE')
          inc_vals+=1
print(f'\n{inc_len} had the incorrect length\n')
print(f'\n{inc_vals} had the incorrect values\n')
