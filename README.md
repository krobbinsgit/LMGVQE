# LMG Variational Quantum Eigensolver (VQE)
## IP Notice 
In this we run my own version of the Variational Quantum Eigensolver (VQE) for the exactly-solvable Lipkin-Meshkov-Glick (LMG) model. This work has been published in my own dissertation and is in the process of being written up for publication in a journal with my old advisor. As such the circuit design and implementation and advantages therein are not intellectual property of D-Wave because I invented them a months to years before joining D-Wave

## Summary
Herein we demonstrate running an efficient non-optimizing derivative of VQE to find energy eigenvalues of the exactly-solvable Lipkin-Meshkov-Glick (LMG) model. Because of the innate symmetries of the LMG model we can leverage the power of quantum mechanics to ensure that the number of measurements required does not exceed $4$ for any number of particles $N$. FIX INSERT CITATIONS OF SELF?

We can use the structure of the LMG model to easily calculate its eigenstates and eigenvalues classically and then determine what the parameters should be in a simulation circuit. After running the circuit we can make measurements and compare against the previously-calculated solutions.

## Background
### VQE [FIX INSERT CITATIONS]
The Variational Quantum Eigensolver (VQE) is a gate-model quantum algorithm which was designed for the noisy intermediate-scale quantum (NISQ) era of computation. It is a hybrid algorithm which makes use of a classical optimizer to find the ground state of a Hamiltonian $H$. For inputs it takes in the Hamiltonian, written as a sum over the Pauli matrices, and an **ansatz**. An ansatz circuit is a parametric quantum circuit which prepares an ansatz state; i.e. the best guess of your ground state. A good ansatz is defined by being able to get close enough to the ground state by tweaking the input parameters.

In VQE, we first prepare the ansatz state $\ket{\psi(\theta)}$ on a QPU, then we sample the expectation value $\bra{\psi(\theta)}H\ket{\psi(\theta)}$, then we feed the results into a classical optimizer, then we alter $\theta\rightarrow\theta'$ according to the optimizer and repeat until convergence.


### The LMG Model [FIX INSERT CITATIONS]
The Lipkin-Meshkov-Glick (LMG) model was originally designed to model oxygen nuclei but is more known as a testbed for studying quantum phase transitions in general. It is an exactly-solvable dual-model bosonic Gaudin-Richardson model and can be solved with an eigenstate generating operator (EGO). 
