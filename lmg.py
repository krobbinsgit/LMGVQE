import dwave.gate.operations as gt
from dwave.gate import Circuit
from dwave.gate.simulator import simulate
import numpy as np

# First we need to define the state-prep circuit.

def state_prep(angles):
  M=len(angles) # The total number of qubits required which is roughly equal to the number of particles N/2
  blank=Circuit(M,M) #A blank circuit with M qubits and M bits. Not sure if we need the bits.
  with blank.context as (q,c):
    gt.RY(angle[0],q[0]) # Apply a rotation gate to the first qubit
    for k in range(1,len(angles)): # Apply controlled rotation gates to the rest of the qubits (control one below)
      gt.CRY(angles[k],q[k-1],q[k]) # Unsure if this is the syntax
  return(blank)

# Now we need to write functions for the measurement diagonalization circuits

def clique_2_diag(circ,num_qubits): # The post-prep circuit required to diagonalize the state for the measurement basis. Works with Clique 2 (see literature)
  with circ.context as (q,c):
    for k in range(num_qubits):
      gt.H(q[k]) # Clique 1 is all Xs so we just apply Hadamards to each qubit.
  return(circ)
    
def clique_3_diag(circ,num_qubits):
  
def clique_3_diag(circ,num_qubits):
    
# After that we need to write a master function which creates all four circuits for a given M and set of angles.
