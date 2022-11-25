"""Bell state example."""

from qutrunk.circuit import QCircuit
from qutrunk.circuit.gates import H, CNOT, Measure


def run_bell_pair(backend=None):
    # Create quantum circuit
    qc = QCircuit(backend=backend)

    # Allocate quantum qubits
    qr = qc.allocate(2)

    # Apply quantum gates
    H * qr[0]
    CNOT * (qr[0], qr[1])
    Measure * qr[0]
    Measure * qr[1]

    # Print quantum circuit
    qc.print()
    # qc.dump(file="bell_pair.qasm", format="openqasm")

    # Run quantum circuit with 100 times
    res = qc.run(shots=100)

    # Print result like:
    meas = res.get_measures()
    if meas.size > 0:
        print(meas[-1, :])

    print(res.get_counts())

    bits = res.get_bitstrs()
    if bits:
        print(bits[-1])

    # Print quantum circuit excution information
    print(res.excute_info())

    return qc


if __name__ == "__main__":
    # Run locally
    circuit = run_bell_pair()

    # Draw quantum circuit
    circuit.draw()
