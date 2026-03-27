"""
This script demonstrates basic quantum circuit construction and simulation in Qiskit.

The first section builds a 2-qubit circuit, applies an X gate and a Hadamard gate,
and inspects the resulting statevector. It also highlights Qiskit’s convention of
reversing qubit order before analyzing amplitudes. The circuit is then
measured and executed on a simulator to obtain sample measurement outcomes.

The second section generalizes to an n-qubit system (n=4), where Hadamard gates are
applied to all qubits to produce a uniform superposition over all computational basis
states. Measurement results from a high-shot simulation are collected and visualized,
confirming the expected uniform distribution.
"""


from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit
from qiskit_aer import Aer, QasmSimulator
from qiskit.quantum_info import Statevector
from qiskit.visualization import plot_histogram
import matplotlib.pyplot as plt

qr = QuantumRegister(2,'q')
cr = ClassicalRegister(2, 'c')
qc = QuantumCircuit(qr,cr)
print('Initialize the quantum and classical registers:')
print(qc)
print('\n')

from qiskit.quantum_info import Statevector
#state = Statevector(qc)
qc.x(0)
state = Statevector(qc)
print('Apply X gate to the 0th qubit')
print(qc)
print(state.data)
print('\n')

state = Statevector(qc.reverse_bits())
print('Reversing the component ordering:')
print(state.data)
print('\n')

qc.h(1)
state = Statevector(qc.reverse_bits())
print('Apply Hadamard gate to 1st qubit:')
print(state.data)
print(qc)
print('\n')

# Perform a computational basis measurement
qc.measure(0, 0)
qc.measure(1, 1)
print(qc)

# Run the circuit and get a 2-bit ouput
from qiskit.providers.basic_provider import BasicSimulator
backend = BasicSimulator()
result = backend.run(qc.reverse_bits(), shots=100).result()
counts = result.get_counts()

# Initialize 4-qubit quantum register and 4-bit classical register
n = 4
qr = QuantumRegister(n,'q')
cr = ClassicalRegister(n, 'c')

# Build the quantum circuit
qc = QuantumCircuit(qr,cr)
print(qc)
print('\n')

# Apply n-fold Hadamard gate
qc.h(range(n))
print(qc)
print('\n')

# # Perform computational basis measurements
for i in range(n):
    qc.measure(i, i)
print(qc)
print('\n')

# Run the circuit and get a 4-bit ouput
backend = Aer.get_backend('qasm_simulator')
result = backend.run(qc.reverse_bits(), shots=1000000).result()
counts = result.get_counts()
plot_histogram(counts, title = 'Counts vs State for $10^6$ shots')
plt.show()