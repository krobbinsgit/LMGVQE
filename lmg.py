import dwave.gate.operations as gt
from dwave.gate import Circuit
import numpy as np
import dwave.gate.simulator
# Run pip install dwave.gate --upgrade to upgrade to newest version of dwave.gate

# First we need to define the state-prep circuit.
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

# Now we need to write functions for the measurement diagonalization circuits

def clique_1_diag(circ,num_shots):
  with circ.context as reg:
    meas1 = gt.Measurement(reg.q) | reg.c
  dwave.gate.simulator.simulate(circ)
  samples = {}
  for qubit in range(circ.num_qubits):
      samples[qubit] = meas1.sample(qubit, num_shots)
  pre_bitstrings=[samples[key] for key in samples.keys()]
  bitstrings=list(map(list, zip(*pre_bitstrings)))
  bitstrings = [intcaststr(bitstring) for bitstring in bitstrings]
  return(bitstrings)

def clique_2_diag(circ,num_shots): # The post-prep circuit required to diagonalize the state for the measurement basis. Works with Clique 2 (see literature)
  with circ.context as (q,c):
    for k in range(circ.num_qubits):
      gt.Hadamard(q[k]) # Clique 1 is all Xs so we just apply Hadamards to each qubit.
  circ.unlock()
  with circ.context as reg:
    meas2 = gt.Measurement(reg.q) | reg.c
  dwave.gate.simulator.simulate(circ)
  samples = {}
  for qubit in range(circ.num_qubits):
      samples[qubit] = meas2.sample(qubit, num_shots)
  pre_bitstrings=[samples[key] for key in samples.keys()]
  bitstrings=list(map(list, zip(*pre_bitstrings)))
  bitstrings = [intcaststr(bitstring) for bitstring in bitstrings]
  return(bitstrings)
    
def clique_3_diag(circ,num_shots):
  if circ.num_qubits<2:
    print('Less than 2 qubits, so we do not need to measure clique 3.')
  else:
    with circ.context as (q,c):
      for k in range(0,circ.num_qubits-1,2):
        gt.Hadamard(q[k+1]) # Might be the other way around...
        gt.CNOT(q[k],q[k+1])
        gt.Hadamard(q[k])
    circ.unlock()
    with circ.context as reg:
      meas3 = gt.Measurement(reg.q) | reg.c
    dwave.gate.simulator.simulate(circ)
    samples = {}
    for qubit in range(circ.num_qubits):
        samples[qubit] = meas3.sample(qubit, num_shots)
    pre_bitstrings=[samples[key] for key in samples.keys()]
    bitstrings=list(map(list, zip(*pre_bitstrings)))
    bitstrings = [intcaststr(bitstring) for bitstring in bitstrings]
    return(bitstrings)


  
def clique_4_diag(circ,num_shots):
  if circ.num_qubits<3:
    print('Less than 3 qubits, so we do not need to measure clique 4.')
  else:
    with circ.context as (q,c):
      for k in range(1,circ.num_qubits-1,2):
        gt.Hadamard(q[k+1]) # Might be the other way around...
        gt.CNOT(q[k],q[k+1])
        gt.Hadamard(q[k])
    circ.unlock()
    with circ.context as reg:
      meas3 = gt.Measurement(reg.q) | reg.c
    dwave.gate.simulator.simulate(circ)
    samples = {}
    for qubit in range(circ.num_qubits):
        samples[qubit] = meas3.sample(qubit, num_shots)
    pre_bitstrings=[samples[key] for key in samples.keys()]
    bitstrings=list(map(list, zip(*pre_bitstrings))) # POSSIBLE FIX: IS IT TRANSPOSING CORRECTLY?
    bitstrings = [intcaststr(bitstring) for bitstring in bitstrings]
    return(bitstrings)

# def all_my_circuits(angles,num_shots):
#   # Takes in a set of angles and returns a list of the (up to) 4 separate circuits...
#   # ... required to prepare and sample the LMG state efficiently
#   # Uses a unary encoding
#   M=len(angles)
#   base1=state_prep(angles) # Makes the state prep circuit object which will have diagonalization circuits appended to it.
#   base1.unlock()
#   clique_1_diag(base1,M)
#   base2=state_prep(angles) # Uh... if I didn't make separate ones it just changed them all each time. Problem? FIX
#   base2.unlock()
#   clique_2_diag(base2,M)
#   list_of_circuits=[base1,base2]
#   if M>1: # If M>1 then clique 3 will come into play
#     base3=state_prep(angles)
#     base3.unlock()
#     clique_3_diag(base3,M)
#     list_of_circuits.append(base3)
#     if M>2: # If M>2 then clique 4 will come into play
#       base4=state_prep(angles)
#       base4.unlock()
#       clique_4_diag(base4,M)
#       list_of_circuits.append(base4)
#   return(list_of_circuits)


def all_my_circuits(angles,num_shots,out_file_name):
  # Takes in a set of angles and num_shots
  # Runs the necessary circuits (up to 4) with num_shots shots
  # outputs lists of bitstrings collected in chronological order [[clique1 bitstrings],[clique2 bitsrings],...]
  # Uses a unary encoding
  M=len(angles)
  base1=state_prep(angles) # Makes the state prep circuit object which will have diagonalization circuits appended to it.
  base1.unlock()
  bitstrings_1=clique_1_diag(base1,num_shots)
  base2=state_prep(angles) # Uh... if I didn't make separate ones it just changed them all each time. Problem? FIX
  base2.unlock()
  bitstrings_2=clique_2_diag(base2,num_shots)
  list_of_outputs=[bitstrings_1,bitstrings_2]
  if M>1: # If M>1 then clique 3 will come into play
    base3=state_prep(angles)
    base3.unlock()
    bitstrings_3=clique_3_diag(base3,num_shots)
    list_of_outputs.append(bitstrings_3)
    if M>2: # If M>2 then clique 4 will come into play
      base4=state_prep(angles)
      base4.unlock()
      bitstrings_4=clique_4_diag(base4,num_shots)
      list_of_outputs.append(bitstrings_4)
  fo=open(str(out_file_name)+'.txt','w')
  for outs in list_of_outputs:
      for bs in outs:
        fo.write(str(bs)+',')
      fo.write('\n')
  fo.close()
  return(list_of_outputs)


all_my_circuits([15,16,17,18],10,'test_dest')

# Wait! This is a state-vector simulator in a weird way. How can I make it run, measure and repeat easily? Something seems odd.
    
# Now we need to make a function which takes in a list of input angles and a number of shots
# The function will then create all the necessary circuits and run them WITH MEASUREMENT
# It will return a list of bitstrings [[strings from clique 1], [strings from clique 2]...]
