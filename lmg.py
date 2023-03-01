import dwave.gate.operations as gt
from dwave.gate import Circuit
from dwave.gate.simulator import simulate
import numpy as np
# Run pip install dwave.gate --upgrade to upgrade to newest version of dwave.gate

# First we need to define the state-prep circuit.

def state_prep(angles):
  M=len(angles) # The total number of qubits required which is roughly equal to the number of particles N/2
  blank=Circuit(M,M) #A blank circuit with M qubits and M bits. Not sure if we need the bits.
  if M==1:
    with blank.context as (q,c):
      gt.RY(angles[0],q[0]) # Apply a rotation gate to the first qubit
  else:
    with blank.context as (q,c):
      gt.RY(angles[0],q[0]) # Apply a rotation gate to the first qubit
      for k in range(1,len(angles)): # Apply controlled rotation gates to the rest of the qubits (control one below)
        gt.CRY(angles[k],q[k-1],q[k]) # Unsure if this is the syntax
  return(blank)

# Now we need to write functions for the measurement diagonalization circuits

def clique_2_diag(circ,num_qubits): # The post-prep circuit required to diagonalize the state for the measurement basis. Works with Clique 2 (see literature)
  with circ.context as (q,c):
    for k in range(num_qubits):
      gt.Hadamard(q[k]) # Clique 1 is all Xs so we just apply Hadamards to each qubit.
  return(circ)
    
def clique_3_diag(circ,num_qubits):
  if num_qubits<2:
    print('Less than 2 qubits, so we do not need to measure clique 3.')
  else:
    with circ.context as (q,c):
      for k in range(0,num_qubits-1,2):
        gt.Hadamard(q[k+1]) # Might be the other way around...
        gt.CNOT(q[k],q[k+1])
        gt.Hadamard(q[k])
  return(circ)


  
def clique_4_diag(circ,num_qubits):
  if num_qubits<3:
    print('Less than 3 qubits, so we do not need to measure clique 4.')
  else:
    with circ.context as (q,c):
      for k in range(1,num_qubits,2):
        gt.Hadamard(q[k+1]) # Might be the other way around...
        gt.CNOT(q[k],q[k+1])
        gt.Hadamard(q[k])
  return(circ)

def all_my_circuits(angles):
  # Takes in a set of angles and returns a list of the (up to) 4 separate circuits...
  # ... required to prepare and sample the LMG state efficiently
  # Uses a unary encoding
  M=len(angles)
  base1=state_prep(angles) # Makes the state prep circuit object which will have diagonalization circuits appended to it.
  base2=state_prep(angles) # Uh... if I didn't make separate ones it just changed them all each time. Problem? FIX
  base2.unlock()
  clique_2_diag(base2,M)
  list_of_circuits=[base1,base2]
  if M>1: # If M>1 then clique 3 will come into play
    base3=state_prep(angles)
    base3.unlock()
    clique_3_diag(base3,M)
    list_of_circuits.append(base3)
    if M>2: # If M>2 then clique 4 will come into play
      base4=state_prep(angles)
      base4.unlock()
      clique_4_diag(base4,M)
      list_of_circuits.append(base4)
  return(list_of_circuits)




    
# Now we need to make a function which takes in a list of input angles and a number of shots
# The function will then create all the necessary circuits and run them WITH MEASUREMENT
# It will return a list of bitstrings [[strings from clique 1], [strings from clique 2]...]
