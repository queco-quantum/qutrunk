import numpy as np

from qutrunk.circuit.gates import X, CX
from qutrunk.circuit import QCircuit
from qutrunk.circuit.gates.meta import Matrix
from qutrunk.backends import BackendQuSprout

def test_cx_gate():
    """Test CX matrix."""
    # cx gate
    circuit = QCircuit(backend=BackendQuSprout())
    qr = circuit.allocate(2)
    X * qr[0]
    CX * (qr[0], qr[1])
    result = circuit.get_statevector()
    result_cx = np.array(result).reshape(-1, 1)

    # matrix gate
    _circuit = QCircuit(backend=BackendQuSprout())
    _qr = _circuit.allocate(2)
    Matrix(X.matrix.tolist()) * _qr[0]
    Matrix(CX.matrix.tolist(), 1) * (_qr[0], _qr[1])
    result = _circuit.get_statevector()
    result_matrix = np.array(result).reshape(-1, 1)

    assert np.allclose(result_cx, result_matrix)


def test_cx_inverse_gate():
    """Test CX matrix inverse."""
    # cy gate
    circuit = QCircuit(backend=BackendQuSprout())
    qr = circuit.allocate(2)
    X * qr[0]
    CX.inv() * (qr[0], qr[1])
    result = circuit.get_statevector()
    result_cx = np.array(result).reshape(-1, 1)

    # matrix gate
    _circuit = QCircuit(backend=BackendQuSprout())
    _qr = _circuit.allocate(2)
    Matrix(X.matrix.tolist()) * _qr[0]
    Matrix(CX.matrix.tolist(), 1).inv() * (_qr[0], _qr[1])
    result = _circuit.get_statevector()
    result_matrix = np.array(result).reshape(-1, 1)

    assert np.allclose(result_cx, result_matrix)
