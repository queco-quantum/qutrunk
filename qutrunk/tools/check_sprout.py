"""Run the quantum circuit using QuSprout as the backend."""


def run_check_sprout():
    from qutrunk.circuit import QCircuit
    from qutrunk.backends import BackendQuSprout
    from qutrunk.circuit.gates import H, CNOT, Measure

    # allocate
    qc = QCircuit(backend=BackendQuSprout())
    qr = qc.allocate(2)

    # apply gate
    H * qr[0]
    CNOT * (qr[0], qr[1])
    Measure * qr[0]
    Measure * qr[1]

    print("============QuSL instruction:===========")
    qc.print()
    print("===============Draw circuit=============")
    qc.draw()
    res = qc.run(shots=100)
    print("==========circuit running result=========")
    print(res.get_counts())
    print("===========circuit running info==========")
    print(res.excute_info())
    print("QuTrunk is installed successfully! You can use QuTrunk now.")


if __name__ == "__main__":
    run_check_sprout()
