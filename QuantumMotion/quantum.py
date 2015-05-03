import sys
from numpy import matrix, kron
import numpy as np
from math import sqrt, pow, pi
#import math.e as ex
import cmath
from exceptions import Exception

qnot = matrix([[0, 1], [1, 0]])
hadamard = 1/sqrt(2) * matrix([[1, 1],[1, -1]])
I = matrix([[1., 0],[0, 1.]])
phase = matrix([[1, 0], [0, 1j]])
T = matrix([[cmath.rect(1,0), 0], [0, cmath.rect(1, pi/4)]])

def controlled_gate(gate, c=0):
    if c:
        return gate
    else:
        return I

class QGate:

    op = None
    name = None

    def __init__(self, U, name, controlled=False):
        if U.size > 0 and np.allclose(U*U.transpose(), I):
            self.op = U
            self.name = name
        else:
            print "Matrix must be unitary!"
            return None

    def __str__(self):
        return self.name

    def opr(self, input):
        try:
            return self.op * input
        except Exception, e:  # catch exceptions, e.g. input wrong matrix shape            
            e.args += (self.op, input,)
            print "You goofed! The input data are not aligned! ",
            print "%s" % (sys.exc_info()[0])
            
            raise

class CQGate(QGate): # Controlled gate

    def __init__(self):
        pass

class QCircuit:

    qubits = 0
    gates = []
    tmp_result = None

    def __init__(self, gates, n=1):
        print "number of qubits: %d" % n
        print "gates: %s" % gates
        self.qubits = n
        self.gates = gates

    def calculate(self, input):
        if not self.tmp_result:
            self.tmp_result = input
        if self.gates:
            for g in self.gates:
                #if self.tmp_result:
                #    #if hasattr(g, 'opr'):
                #    #    self.tmp_result = g.opr(self.tmp_result)
                #    #else:
                #    #    self.tmp_result = g * self.tmp_result
                #    self.tmp_result = self._operate(g, self.tmp_result)
                #else:
                #    #self.tmp_result = g * input
                #    self.tmp_result = self._operate(g, input)
                self.tmp_result = self._operate(g, self.tmp_result)
            return self.tmp_result
        else:
            print "No gates found! Oh, no!"
            return None
   
    def _operate(self, gate, input):
        if hasattr(gate, 'opr'):
            result = gate.opr(input)
        else:
            result = gate * input
        return result
            
            

if __name__ == "__main__":
    #foo = kron(I, T)
    #print "Foo:\n%s" % foo
    qi = QGate(I, "IDENTITY")
    #print "gate: %s, %s" % (qg, qg.op)
    qn = QGate(qnot, "NOT")
    qh = QGate(hadamard, "HADAMARD")

    print hadamard*hadamard.transpose()

    qc = QCircuit([qh])
    result = qc.calculate(matrix([[1],[0]]))
    print "QC result: %s" % result