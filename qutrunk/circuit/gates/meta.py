"""Definition of some meta operator."""

from typing import Union

from .basicgate import BasicGate
from qutrunk.circuit import QuBit, Qureg


class All(BasicGate):
    """Meta operator, provides unified operation of multiple qubits.

    Args:
        gate: The gate will apply to all qubits.

    Example:
        .. code-block:: python

            All(H) * qureg
            All(Measure) * qureg
    """

    def __init__(self, gate):
        self.gate = gate

    def __or__(self, qureg):
        """Quantum logic gate operation.

        Args:
            qureg: The qureg(represent a set of qubit) to apply gate.

        Example:
            .. code-block:: python

                All(H) * qureg
                All(Measure) * qureg
        """
        for q in qureg:
            self.gate * q

    def __mul__(self, qureg):
        """Overwrite * operator to achieve quantum logic gate operation, \
            reuse __or__ operator implement."""
        self.__or__(qureg)


class Power(BasicGate):
    """Power Gate.

    Args:
        power: The power to raise target gate to.
        gate: The target gate to raise.

    Example:
        .. code-block:: python

            Power(2, gate) * q[0]
    """

    def __init__(self, power, gate):
        self.power = power
        self.gate = gate

    def __or__(self, qubits: Union[QuBit, Qureg, tuple]):
        """Quantum logic gate operation."""
        if self.power < 0:
            raise ValueError("power should >= 0")

        if not isinstance(qubits, (QuBit, Qureg, tuple)):
            raise TypeError("qubits should be type of QuBit, Qureg or tuple.")

        for _ in range(self.power):
            self.gate * qubits

    def __mul__(self, qubits: Union[QuBit, Qureg, tuple]):
        self.__or__(qubits)

class Gate:
    """Used to define custom gate.

    Example:
        .. code-block:: python

            from qutrunk.circuit import QCircuit
            from qutrunk.circuit.gates import H, CNOT, CustomGate, All, Measure, gate

            circuit = QCircuit()
            q = circuit.allocate(2)

            @def_gate
            def my_gate(a, b):
                return Gate() << (H, a) << (CNOT, (a, b))

            my_gate * (q[0], q[1])
            All(Measure) * q
            circuit.print()
            res = circuit.run(shots=100)
            print(res.get_counts()) 
            
    """

    def __init__(self):
        super().__init__()
        self.gate_type = None
        self.gates = []
        self.matrix = None

    def append_gate(self, gate, qubits):
        """Append basic gate to custom gate.
        
        Args:
            gate: Basic gate.
            qubits: The target qubits of quantum gate to apply.
        """
        if self.gate_type is None:
            self.gate_type = "compose"
        self.gates.append({"gate": gate, "qubits": qubits})

    def __lshift__(self, gate_define):
        self.append_gate(gate_define[0], gate_define[1])
        return self

    def define_matrix(self, matrix):
        """Define specific matrix for custom gate.
        
        Args:
            matrix: The matrix defined by user.
        """
        if self.gate_type is None:
            self.gate_type = "matrix"
        self.matrix = matrix

class def_gate(BasicGate):
    """Definition of custom gate.

    Implement by composing some basic logic gates or define specific matrix.

    Example:
        .. code-block:: python

            from qutrunk.circuit import QCircuit
            from qutrunk.circuit.gates import H, CNOT, CustomGate, All, Measure, gate

            circuit = QCircuit()
            q = circuit.allocate(2)

            @def_gate
            def my_gate(a, b):
                return Gate() << (H, a) << (CNOT, (a, b))

            my_gate * (q[0], q[1])
            All(Measure) * q
            circuit.print()
            res = circuit.run(shots=100)
            print(res.get_counts()) 
    """

    def __init__(self, func):
        self.compose_gate = True
        self.callable = func

    def __or__(self, qubits: Union[QuBit, tuple]):
        """Quantum logic gate operation."""
        if not isinstance(qubits, (QuBit, tuple)):
            raise TypeError("qubits should be type of QuBit or tuple")
        if isinstance(qubits, QuBit):
            custom_gate = self.callable(qubits)
        else:
            custom_gate = self.callable(*qubits)
        if custom_gate.gate_type == "compose":
            for c in custom_gate.gates:
                c['gate'] * c['qubits']
        elif custom_gate.gate_type == "matrix":
            # apply custom gate defined by matrix
            pass

    def __mul__(self, qubits: Union[QuBit, tuple]):
        self.__or__(qubits)

    @property
    def matrix(self):
        """Access to the matrix property of this gate."""
        # 根据比特位数将每个量子门张成一个大矩阵，G.matrix @ I @ I（根据量子比特位置关系调整I的顺序）
        # 然后每个门张成的矩阵再做矩阵乘法
        pass

    def inv(self):
        """Apply inverse gate."""
        pass

    def ctrl(self, ctrl_cnt=1):
        """Apply controlled gate.
        
        Args:
            ctrl_cnt: The number of control qubits, default: 1.
        """
        pass


# note: 该方法会导致部分门操作产生状态污染，比如通过对象实例调用的门操作
# 只要设置过状态，那么后续所有该量子门操作都带了这个状态
# def Inv(gate):
#     """Inverse gate.

#     Args:
#         gate: The gate will apply inverse operator.

#     Example:
#         .. code-block:: python

#             Inv(H) * q[0]
#     """
#     if isinstance(gate, BasicGate):
#         gate.is_inverse = not gate.is_inverse

#     return gate
