---
layout: post
title: The Math Behind Quantum Algorithms
---

## Introduction:

<script src="https://cdn.mathjax.org/mathjax/latest/MathJax.js?config=TeX-AMS-MML_HTMLorMML" type="text/javascript"></script>
## Quantum Fourier Transform

The [Quantum Fourier Transform (QFT) ](https://en.wikipedia.org/wiki/Quantum_Fourier_transform) transforms between the computational basis and the state in fourier basis. Here, the computational basis represents the Z-basis states $$ \mid 0 \rangle$$ and $$ \mid 1 \rangle$$ and the fourier basis represents the X-basis states $$ \mid + \rangle$$ and $$ \mid - \rangle$$.Now that we have talked about what the Quantum Fourier Transform is basically doing, lets get into the math.

In general, the classical Fourier transform acts on a vector $$(x_0, x_1, \ldots, x_{N-1}) \in \mathbb{C}^N$$ and maps it to the vector $$(y_0, y_1, \ldots, y_{N-1}) \in \mathbb{C}^N$$ according to the formula

$$
y_k =  \sum_{j=0}^{N-1} e^{2\pi ijk} x_j, \quad k = 0, 1, 2, \ldots, N-1.
$$

This is simply a clever rephrasing of the formula for coefficients in a Fourier Series that we derive using complex analysis, and represents the Riemann sum step. 


From this it isn't too hard to see the Quantum Fourier transform, which acts on the a quantum state

$$
|x\rangle = \sum_{j=0}^{N-1} x_j |j\rangle
$$

and maps it to the quantum state

$$
\sum_{j=0}^{N-1} y_j |j\rangle
$$

according to the formula

$$
y_k = \frac{1}{\sqrt{N}} \sum_{j=0}^{N-1}  e^{\frac{2\pi ijk}{N}} x_j, \quad k = 0, 1, 2, \ldots, N-1.
$$

Note that, the $$\frac{1}{\sqrt{N}}$$ is a normalization constant so that the magnitude of the quantum vectors stays unitary. Also, note that we can connect the fraction $$\frac{2\pi i}{N}$$ to something we commonly know as the N-th [root of unity](https://en.wikipedia.org/wiki/Root_of_unity).


Using this defintion of the Fourier Transform lets try to derive the Quantum Fourier transform for some N!

Firstly, lets define the state $$\mid x \rangle = \mid x_1 x_2 \ldots x_n\rangle$$, for $$N=2^n$$. We use n so that the Hilbert Space is exactly $$2^n$$ dimensional. A Hilbert Space is a vector space over the complex numbers. We use 2 as the base because you only have two complex coordinates, making the Hilbert Space for one qubit $$C^2$$. Then we can define 

$$
QFT\mid x \rangle = \frac{1}{\sqrt{N}} \sum_{y=0}^{N-1}  e^{\frac{2\pi iyj}{N}} \mid y \rangle
$$ 

After substituting $$N=2^n$$,

$$
= \frac{1}{\sqrt{2^n}}  \sum_{y=0}^{N-1}  e^{\frac{2\pi iyj}{2^n}}\mid y \rangle
$$

Rewriting in fractional bit notation,

$$
= \frac{1}{\sqrt{2^n}}  \sum_{y=0}^{N-1}  e^{2\pi i(\sum_{k=0}^{n} \frac{y_k}{2^k})j}  \mid y_1,y_2 \ldots y_n \rangle 
$$

$$
= \frac{1}{\sqrt{2^n}}  \sum_{y=0}^{N-1} \prod_{k=1}^{n} e^{\frac{2\pi i y_kj}{2^k}}  \mid y_1,y_2 \ldots y_n \rangle
$$

Because each $$y_k$$ represents a bit,

$$
= \frac{1}{\sqrt{2^n}} \sum_{y_1=0}^1 \sum_{y_2=0}^1 \cdots \sum_{y_n=0}^1 
   \Bigl(\,\prod_{k=1}^{n} e^{\frac{2\pi i\,y_k\,j}{2^k}}\Bigr)\;\mid y_1,y_2,\ldots,y_n \rangle
$$

$$
= \frac{1}{\sqrt{2^n}} 
   \Bigl(\sum_{y_1=0}^1 e^{\frac{2\pi i\,y_1\,j}{2^1}}\mid y_1 \rangle\Bigr)\,
   \Bigl(\sum_{y_2=0}^1 e^{\frac{2\pi i\,y_2\,j}{2^2}}\mid y_2 \rangle\Bigr)\,
   \cdots\,
   \Bigl(\sum_{y_n=0}^1 e^{\frac{2\pi i\,y_n\,j}{2^n}}\mid y_n \rangle\Bigr)
$$

Because, 

$$
\sum_{y_k=0}^1 e^{\frac{2\pi i\,y_k\,j}{2^k}} \lvert y_k \rangle
\;=\;
\bigl(e^0 \lvert 0 \rangle\bigr)
\;+\;
\bigl(e^{\frac{2\pi i\,j}{2^k}} \lvert 1 \rangle\bigr)
\;=\;
\lvert 0 \rangle \;+\; e^{\frac{2\pi i\,j}{2^k}} \lvert 1 \rangle.
$$

$$
QFT\mid x \rangle = \Bigl(\frac{\mid 0 \rangle + e^{\frac{2\pi i\,j}{2^1}}\,\mid 1 \rangle}{\sqrt{2}}\Bigr)
  \;\otimes\;
  \Bigl(\frac{\mid 0 \rangle + e^{\frac{2\pi i\,j}{2^2}}\,\mid 1 \rangle}{\sqrt{2}}\Bigr)
  \;\otimes \cdots \otimes\;
  \Bigl(\frac{\mid 0 \rangle + e^{\frac{2\pi i\,j}{2^n}}\,\mid 1 \rangle}{\sqrt{2}}\Bigr).
$$

which can be confirmed by analyzing the Fourier Transform. 

Another property worth mentioning is that, when we encode a state $$\mid q \rangle$$ on an $$n$$ number of qubits, the first qubit rotates with a frequency of $$\frac{q}{2^n}$$ around the z-axis. For example, if we encode the state $$\mid \tilde q \rangle$$ on 3 qubits, the first qubit rotates $$\frac{5}{8} * 2 \pi$$ radians and then the second qubit rotates  $$\frac{10}{8} * 2 \pi$$ around the z-axis and so on. We can verify this by simulating it. Check out this [link](https://github.com/Qiskit/textbook/blob/main/notebooks/ch-algorithms/quantum-fourier-transform.ipynb) for a really cool simulation.

Now, lets get into the circuit to implement the Quantum Fourier Transform.







