from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit import BasicAer, execute
from qiskit.tools.visualization import plot_histogram, plot_state_city, plot_bloch_multivector
from random import getrandbits
from math import pi

def alice(c_in_bit, q_ent, c_ent_meas, q_circ):
    if (c_in_bit == 1):
        q_circ.ry(pi/2,q_ent)
    q_circ.measure(q_ent, c_ent_meas)

def bob(c_in_bit, q_ent, c_ent_meas, q_circ):
    if (c_in_bit == 0):
        q_circ.ry(pi/4, q_ent)
    else:
        q_circ.ry(-pi/4, q_ent)
    q_circ.measure(q_ent, c_ent_meas)

def entangle(qc):
    en = QuantumRegister(2)
    qc.add_register(en)
    qc.h(en[0])
    qc.cx(en[0], en[1])
    return en

def play():
    overall_count = 0
    trials = 4096
    for i in range(trials):
        en_c = ClassicalRegister(2)
        qc = QuantumCircuit(en_c)
        en = entangle(qc)
        a_r = getrandbits(1)
        b_r = getrandbits(1)
        alice(a_r, en[0], en_c[0], qc)
        bob(b_r, en[1], en_c[1], qc)
        backend = BasicAer.get_backend('qasm_simulator')
        job = execute(qc, backend, shots=1)
        result = job.result()
        counts = result.get_counts()
        # print(counts)
        a = next(iter(counts))
        if (int(a[0]) ^ int(a[1]) == a_r * b_r):
            overall_count += 1
    print("")
    print(overall_count)
    print(overall_count/trials)


def main():
    play()

if __name__ == '__main__':
    main()
