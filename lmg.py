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

def clique1_diag(circ,num_shots): # A new version of diagonal circuit 1
  # used for testing Theodor's new sample() function which should fix entanglement issue
  with circ.context as reg:
    meas1 = gt.Measurement(reg.q) | reg.c
  st=dwave.gate.simulator.simulate(circ)
  qubs=[qubit for qubit in range(circ.num_qubits)]
  samples = meas1.sample(qubs, num_shots,as_bitstring=True)
  return((samples,st))

def clique2_diag(circ,num_shots): # The post-prep circuit required to diagonalize the state for the measurement basis. Works with Clique 2 (see literature)
  with circ.context as (q,c):
    for k in range(circ.num_qubits):
      gt.Hadamard(q[k]) # Clique 2 is all Xs so we just apply Hadamards to each qubit.
  circ.unlock()
  with circ.context as reg:
    meas2 = gt.Measurement(reg.q) | reg.c
  dwave.gate.simulator.simulate(circ)
  qubs=[qubit for qubit in range(circ.num_qubits)]
  samples = meas2.sample(qubs, num_shots,as_bitstring=True)
  return(samples)
    
def clique3_diag(circ,num_shots):
  if circ.num_qubits<2:
    print('Less than 2 qubits, so we do not need to measure clique 3.\n')
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
    qubs=[qubit for qubit in range(circ.num_qubits)]
    samples = meas3.sample(qubs, num_shots,as_bitstring=True)
    return(samples)


  
def clique4_diag(circ,num_shots):
  if circ.num_qubits<3:
    print('Less than 3 qubits, so we do not need to measure clique 4.\n')
  else:
    with circ.context as (q,c):
      for k in range(1,circ.num_qubits-1,2):
        gt.Hadamard(q[k+1]) # Might be the other way around...
        gt.CNOT(q[k],q[k+1])
        gt.Hadamard(q[k])
    circ.unlock()
    with circ.context as reg:
      meas4 = gt.Measurement(reg.q) | reg.c
    dwave.gate.simulator.simulate(circ)
    qubs=[qubit for qubit in range(circ.num_qubits)]
    samples = meas4.sample(qubs, num_shots,as_bitstring=True)
    return(samples)
  


def total_circuit_runner(angles,out_file_name,num_shots=10**4):
  # Takes in a set of angles and num_shots
  # Runs the necessary circuits (up to 4) with num_shots shots
  # outputs lists of bitstrings collected in chronological order [[clique1 bitstrings],[clique2 bitsrings],...]
  # Uses a unary encoding
  M=len(angles)
  base1=state_prep(angles) # Makes the state prep circuit object which will have diagonalization circuits appended to it.
  base1.unlock()
  bitstrings_1,base_state=clique1_diag(base1,num_shots)
  base2=state_prep(angles) # Uh... if I didn't make separate ones it just changed them all each time. Problem? FIX
  base2.unlock()
  bitstrings_2=clique2_diag(base2,num_shots)
  list_of_outputs=[bitstrings_1,bitstrings_2]
  if M>1: # If M>1 then clique 3 will come into play
    base3=state_prep(angles)
    base3.unlock()
    bitstrings_3=clique3_diag(base3,num_shots)
    list_of_outputs.append(bitstrings_3)
    if M>2: # If M>2 then clique 4 will come into play
      base4=state_prep(angles)
      base4.unlock()
      bitstrings_4=clique4_diag(base4,num_shots)
      list_of_outputs.append(bitstrings_4)
  fo=open(str(out_file_name)+'.txt','w')
  for outs in list_of_outputs:
      for bs in outs:
        fo.write(str(bs)+',')
      fo.write('\n')
  fo.close()
  #return(base_state)
