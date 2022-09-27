from cmath import sin, cos

import numpy as np

from .basicgate import BasicRotateGate
from qutrunk.circuit import Command
from qutrunk.circuit.qubit import QuBit


class Ryy(BasicRotateGate):
    """RotationYY gate class.

    Args:
        alpha: The angle to rotate.

    Example:
        .. code-block:: python

            Ryy(alpha) * (qr[0], qr[1])
    """

    def __init__(self, alpha):
        super().__init__()
        self.rotation = alpha

    def __str__(self):
        return "Ryy"

    def __or__(self, qubits):
        """Quantum logic gate operation.

        Args:
            qubits: The quantum bits to apply Ryy gate.

        Example:
            .. code-block:: python

                Ryy(alpha) * (qr[0], qr[1])

        Raises:
            NotImplementedError: If the argument is not a Qubit object.
            AttributeError: If the qubits should not be two.
        """
        if not all(isinstance(qubit, QuBit) for qubit in qubits):
            # TODO:need to improve.
            raise NotImplementedError("The argument must be Qubit object.")

        if len(qubits) != 2:
            raise AttributeError()
        targets = [q.index for q in qubits]
        cmd = Command(self, targets, rotation=[self.rotation], inverse=self.is_inverse)
        self.commit(qubits[0].circuit, cmd)
        return cmd

    def __mul__(self, qubits):
        """Overwrite * operator to achieve quantum logic gate operation, reuse __or__ operator implement."""
        return self.__or__(qubits)

    @property
    def matrix(self):
        """Access to the matrix property of this gate."""
        return np.matrix(
            [
                [cos(0.5 * self.rotation), 0, 0, 1j * sin(0.5 * self.rotation)],
                [0, cos(0.5 * self.rotation), -1j * sin(0.5 * self.rotation), 0],
                [0, -1j * sin(0.5 * self.rotation), cos(0.5 * self.rotation), 0],
                [1j * sin(0.5 * self.rotation), 0, 0, cos(0.5 * self.rotation)],
            ]
        )
