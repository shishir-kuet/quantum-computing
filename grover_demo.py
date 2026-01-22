from qiskit import QuantumCircuit, transpile
from qiskit_aer import Aer
from qiskit.visualization import plot_histogram
import matplotlib.pyplot as plt

# -----------------------------
# Parameters
# -----------------------------
n_qubits = 2          # search space size = 2^n = 4
marked_state = "11"   # the solution we want Grover to find

# -----------------------------
# Oracle: marks |11> by phase flip
# -----------------------------
def grover_oracle(n, marked):
    qc = QuantumCircuit(n)
    
    # Flip qubits where marked bit is 0
    for i, bit in enumerate(marked):
        if bit == "0":
            qc.x(i)

    # Multi-controlled Z (for 2 qubits, this is just CZ via H-CX-H)
    qc.h(n-1)
    qc.cx(0, n-1)
    qc.h(n-1)

    # Undo the X gates
    for i, bit in enumerate(marked):
        if bit == "0":
            qc.x(i)

    return qc

# -----------------------------
# Diffuser (inversion about mean)
# -----------------------------
def grover_diffuser(n):
    qc = QuantumCircuit(n)

    qc.h(range(n))
    qc.x(range(n))

    qc.h(n-1)
    qc.cx(0, n-1)
    qc.h(n-1)

    qc.x(range(n))
    qc.h(range(n))

    return qc

# -----------------------------
# Build Grover circuit
# -----------------------------
qc = QuantumCircuit(n_qubits, n_qubits)

# Step 1: Create uniform superposition
qc.h(range(n_qubits))

# Step 2: Apply Grover iteration (only 1 iteration needed for 2 qubits)
oracle = grover_oracle(n_qubits, marked_state)
diffuser = grover_diffuser(n_qubits)

qc.append(oracle, range(n_qubits))
qc.append(diffuser, range(n_qubits))

# Step 3: Measure
qc.measure(range(n_qubits), range(n_qubits))

print("Grover circuit:")
print(qc)

# -----------------------------
# Simulate
# -----------------------------
backend = Aer.get_backend("aer_simulator")
compiled = transpile(qc, backend)
result = backend.run(compiled, shots=1024).result()
counts = result.get_counts()

print("\nMeasurement results (counts):")
print(counts)

# -----------------------------
# Plot results
# -----------------------------
plot_histogram(counts)
plt.show()
