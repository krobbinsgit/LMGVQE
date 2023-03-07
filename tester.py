import dwave.gate.operations as gt
from dwave.gate import Circuit
import dwave.gate.simulator
import numpy as np

### ------------- WHAT TO DO
### ------------- The bitstrings come out "wrong" even at the point of measurement.

def intcaststr(bitlist): # Taken from Stack Exchange
    return("".join(str(i) for i in bitlist))

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

def clique_1_diag(circ,num_shots):
    with circ.context as reg:
        meas1 = gt.Measurement(reg.q) | reg.c
    dwave.gate.simulator.simulate(circ)
    # Need to run simulator for each measurement.
    samples = {}
    for qubit in range(circ.num_qubits):
        samples[qubit] = meas1.sample(qubit, num_shots)
    pre_bitstrings=[samples[key] for key in samples.keys()]
    bitstrings=list(map(list, zip(*pre_bitstrings)))
    bitstrings = [intcaststr(bitstring) for bitstring in bitstrings]
    return(bitstrings)

def circ1(angles,num_shots,out_file_name):
    M=len(angles)
    base1=state_prep(angles) # Makes the state prep circuit object which will have diagonalization circuits appended to it.
    base1.unlock()
    bitstrings_1=clique_1_diag(base1,num_shots)

circ1([3,2],10,'big_test')