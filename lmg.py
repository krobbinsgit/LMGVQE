import dwave.gate.operations as gt
from dwave.gate import Circuit
from dwave.gate.simulator import simulate
import numpy as np

# First we need to define the state-prep circuit.

def state_prep(angles):
  M=len(angles)
  blank=Circuit(M)
  with blank.context as (q,c):
    gt.RY(angle[0],q[0])
    for k in range(1,len(angles)):
      gt.CRY(angles[k],q[k-1],q[k]) # Unsure if this is the syntax
  return(blank)

# Now we need to write functions for the measurement diagonalization circuits

def clique_2_diag(circ,num_qubits):
  with circ.context as (q,c):
    for k in range(num_qubits):
      gt.H(q[k])
  return(circ)
    
def clique_3_diag(circ,num_qubits):
  
def clique_3_diag(circ,num_qubits):
    
# After that we need to write a master function which creates all four circuits for a given M and set of angles.
