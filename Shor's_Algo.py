from qiskit import QuantumCircuit, transpile
from qiskit.circuit.library import QFTGate
from qiskit_aer import AerSimulator
from fractions import Fraction
import random
import sympy
import math

def exp_gate(a, binary_power, N):
    n_qubits = N.bit_length()
    power = 2 ** binary_power
    base = QuantumCircuit(n_qubits, name=f'{a}^{power} mod {N}')
    for exp in range(power):
        a_exp = pow(a, exp, N)
        for i in range(n_qubits):
            if (a_exp >> i) & 1:
                base.x(i)
            for j in range(i + 1, n_qubits):
                if (a_exp >> j) & 1:
                    base.swap(i, j)
    return base.to_gate().control()

def qpe_circuit(a, N):
    n = N.bit_length()
    qc = QuantumCircuit(2 * n + n, 2 * n)
    qc.h(range(2 * n))  
    qc.x(2 * n)                 
    qc.barrier()
    for j in range(2 * n):
        qc.append(exp_gate(a, j, N), [j] + list(range(2 * n, 2 * n + n)))
    qc.barrier()
    inv_qft = QFTGate(2 * n).inverse()
    qc.append(inv_qft, range(2 * n))
    return qc

def measure(circ, simulator):
    circ.measure(range(circ.num_clbits), range(circ.num_clbits))
    qc_t = transpile(circ, simulator)
    result = simulator.run(qc_t, memory=True).result()
    return result.get_memory()[0]

def check_N(N):
    if N <= 3:
        return True, None
    if N % 2 == 0:
        return True, (2, N // 2)
    if sympy.isprime(N):
        return True, None
    max_exp = int(math.log2(N))
    for k in range(max_exp, 1, -1):
        p = round(N ** (1 / k))
        if p ** k == N:
            return True, (p, k)
    return False, None

def smallest_period(a, N, r_cand):
    divs = set()
    for i in range(1, int(math.isqrt(r_cand)) + 1):
        if r_cand % i == 0:
            divs.add(i)
            divs.add(r_cand // i)
    for d in sorted(divs):
        if pow(a, d, N) == 1:
            return d
    return r_cand

def quantum_period_finding(N, simulator, a):
    n = N.bit_length()
    while True:
        circ = qpe_circuit(a, N)
        state_bin = measure(circ, simulator)
        state_int = int(state_bin, 2)
        phase = state_int / (2 ** (2 * n))

        r_cand = Fraction(phase).limit_denominator(N).denominator
        if pow(a, r_cand, N) != 1:
            continue

        r = smallest_period(a, N, r_cand)
        if 1 < r <= N:
            return r, state_bin, phase

def postprocess(N, a, r):
    if r % 2 != 0:
        return None
    x = pow(a, r // 2, N)
    f1 = math.gcd(x - 1, N)
    f2 = math.gcd(x + 1, N)
    if f1 not in (1, N) and f2 not in (1, N):
        return x, x - 1, x + 1, f1, f2
    return None

def shor_algorithm(N, simulator=None):
    invalid, trivial = check_N(N)
    if invalid:
        return trivial or f"[ERR] {N} is prime or too small"

    sim = simulator or AerSimulator()
    n = N.bit_length()
    candidates = [7]
    random.shuffle(candidates)

    for a in candidates:
        r, state_bin, phase = quantum_period_finding(N, sim, a)
        post = postprocess(N, a, r)
        if post:
            x, xm1, xp1, f1, f2 = post
            state_int = int(state_bin, 2)
            denom = 2 ** (2 * n)

            print(f"[SUCCESS] a = {a}")
            print(f"r: {r}")
            print(f"raw register state: {state_bin}")
            print(f"integer value: {state_int}")
            print(f"phase = integer/2^(2n): {state_int}/{denom}")
            print(f"a^(r/2) mod N: {x}")
            print(f"a^(r/2) - 1: {xm1}")
            print(f"a^(r/2) + 1: {xp1}")
            print(f"[DONE] Factors: {f1}, {f2}")
            return (f1, f2)

    print(f"[FAIL] No non trivial factors found for N = {N}")
    return None

if __name__ == "__main__":
    sim = AerSimulator()
    N = 15
    print(shor_algorithm(N, simulator=sim))
