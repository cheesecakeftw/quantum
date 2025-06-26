---
layout: post
title: Quantum Foundations
---
<script src="https://cdn.mathjax.org/mathjax/latest/MathJax.js?config=TeX-AMS-MML_HTMLorMML" type="text/javascript"></script>

We start by defining what a [classical bit](https://en.wikipedia.org/wiki/Bit) is and how it is different from a [quantum bit](https://en.wikipedia.org/wiki/Qubit). A classical bit is in the ring $$\mathbb{Z} / 2\mathbb{Z}$$ and has the states $$0$$ and $$1$$. Note that classical bits can only be in 1 state at a time. 

A quantum bit, also called a qubit, is the group algebra over a field of complex numbers of the group with two elements such that:

$$
\mathbb{C}[\mathbb{Z}/2\mathbb{Z}] \cong \mathbb{C}^2 \cong {\alpha 0 + \beta 1 : \alpha, \beta \in \mathbb{C} }
$$ 

A qubit can be thought of as a 2-dimensional complex vector, which is called a superposition state vector. A qubit basically lives in the two-dimensional complex Hilbert space $$\mathbb{C}^2$$, Note that it has two fundamental states which are again $$0$$ and $$1$$.

But here is where qubits are different from bits. A state of a qubit is a unit vector in $$\mathbb{C}^2$$ for the standard [inner product](https://en.wikipedia.org/wiki/Inner_product_space) in $$\mathbb{C}^2$$ which makes $$0$$ and $$1$$ an [orthonormal](https://en.wikipedia.org/wiki/Orthonormality) basis. Two vectors in an inner space are called orthonormal if they are orthogonal unit vectors in linear algebra. A unit vector is a vector which has length 1 and orthogonal means that the vectors are perpendicular to each other.

Now here is where it get's interesting. We define any state $$x$$ of the qubit as the complex superposition

$$x = \alpha 0 + \beta 1$$
 
with the condition $$\lvert \alpha \rvert^2 + \lvert \beta \rvert^2 = 1$$. Here $$\alpha$$ and $$\beta$$ are probability amplitudes and are both complex numbers. 

A qubit is denoted using Dirac notation: $$\lvert 0 \rangle $$ and $$\lvert 1\rangle$$. These two orthonormal basis states are in the [Hilbert Space](https://en.wikipedia.org/wiki/Hilbert_space) of a qubit. Using this notation we define the qubit $$\psi$$ as the linear combination 

$$
\lvert \psi \rangle = \alpha \lvert 0\rangle + \beta \lvert 1\rangle$$

Like we previously defined, according to [Born's rule](https://en.wikipedia.org/wiki/Born_rule), the probability of outcome $$\lvert 0\rangle$$ for the qubit is $$\lvert \alpha \rvert^2$$ and outcome $$\lvert 1\rangle$$ for the qubit is $$\lvert \beta \rvert^2$$. To build upon what we stated earlier the condition $$\lvert \alpha \rvert^2 + \lvert \beta \rvert^2 = 1$$ comes from the second axiom of probability of theory and is backed up by the orthonormal nature of the vector.

Additionally using Dirac's bra-ket notation we define the classical states $$0$$ and $$1$$ as a vector

$$
\lvert 0 \rangle = \begin{bmatrix} 1 \\ 0 \end{bmatrix}, \quad
\lvert 1 \rangle = \begin{bmatrix} 0 \\ 1 \end{bmatrix}.
$$

Two qubits live in the tensor product space $$\mathbb{C}^2 \otimes \mathbb{C}^2 \cong \mathbb{C}^4$$, whose standard basis is $$\lvert 00 \rangle, \lvert 01 \rangle, \lvert 10 \rangle, \lvert 11 \rangle$$. In general, $$n$$ qubits form the $$2^n$$-dimensional space $$\mathbb{C}^2 \otimes \cdots \otimes \mathbb{C}^2 \cong \mathbb{C}^{2^n}$$ with basis $$\lvert j \rangle$$ for $$j = 0, \dots, 2^n - 1$$. Hence, We can define a superposition state vector in $$2^n$$ dimensional Hilbert space using probability theory as 

$$
\lvert Y \rangle = \sum_{j=0}^{2^n - 1} x_j \lvert j \rangle
$$

Here, we know that $$
\sum_{j=0}^{2^n - 1} \lvert x_j \rvert^2 = 1.
$$ because the vectors are orthonormal.

When we measure a qubit they can only show the values $$0$$ and $$1$$. When we measure a classical bit we don't disturb its state, but when we measure a qubit we destroy its coherence and disturb the superposition state, which results in only one bit being encoded in one qubit. 

When we measure a qubit we are really projecting the full state $$\lvert x \rangle$$ onto the basis state $$\lvert k \rangle$$. Mathematically, that projection is written:

$$
x_k = \sum_{j=0}^{2^n - 1} x_j \delta_{kj}
$$

where $$\delta_{kj}$$ is the kronecker delta: its $$1$$ if $$k = j$$ and $$0$$ otherwise, so this just picks out the $$k$$th component from the whole state vector. Additionally, note that using the kronecker delta is essentially vector multiplication in the orthonormal state in linear algebra. The kronecker delta is essential in proofs that we use later!

Now we define important gates that we use in other articles. The Pauli gates are three matrices that we apply on a single qubit. The goal of each of these gates ($$X,Y,Z$$) is to rotate around the x,y and z axes of the [Bloch sphere](https://en.wikipedia.org/wiki/Bloch_sphere) by $$\pi$$ radians. Here, the sphere just refers to a geometric representation of the pure state space of a qubit. The north and south poles respectively correspond to the standard basis vectors $$\lvert 1 \rangle$$ and  $$\lvert 0 \rangle$$.

The $$X$$ gate is the quantum equivalent of the $$NOT$$ gate for classical computers. It can be seen as a bit flip as it maps $$\lvert 1 \rangle$$ to  $$\lvert 0 \rangle$$ and $$\lvert 0 \rangle$$ to $$\lvert 1 \rangle$$. The gate is represented by the matrix 

$$
X = 
\begin{bmatrix}
0 & 1 \\
1 & 0
\end{bmatrix}
$$

We can show that the gate maps $$\lvert 1 \rangle\to\lvert 0 \rangle$$ and $$\lvert 0 \rangle\to\lvert 1 \rangle$$ by applying the matrix on a qubit defined as $$\alpha\lvert0\rangle + \beta\lvert1\rangle$$

$$
X(\alpha\lvert0\rangle + \beta\lvert1\rangle)
= \alpha X\lvert0\rangle + \beta X\lvert1\rangle \\
= \alpha\begin{pmatrix}0\\1\end{pmatrix} + \beta\begin{pmatrix}1\\0\end{pmatrix} \\
= \alpha\begin{pmatrix}0\\1\end{pmatrix} + \beta\begin{pmatrix}1\\0\end{pmatrix} \\
= \beta\lvert0\rangle + \alpha\lvert1\rangle
$$

Similar, to the $$X$$ gate the $$Y$$ gate maps $$ \lvert 0 \rangle$$ to $$ i\lvert 1 \rangle $$ and $$\lvert 1 \rangle $$ to $$-i\lvert 0 \rangle $$. It is represented by the matrix 

$$
Y = 
\begin{bmatrix}
0 & -i \\
i & 0
\end{bmatrix}
$$

We can show that the gate maps $$ \lvert 0 \rangle \to i\lvert 1 \rangle $$ and $$\lvert 1 \rangle \to -i\lvert 0 \rangle $$ by applying the matrix on a qubit

$$
Y(\alpha\lvert0\rangle + \beta\lvert1\rangle)
= \alpha Y\lvert0\rangle + \beta Y\lvert1\rangle \\
= \alpha\begin{pmatrix}0\\i\end{pmatrix} + \beta\begin{pmatrix}-i\\0\end{pmatrix} \\
= \alpha\begin{pmatrix}0\\i\end{pmatrix} + \beta(-i)\begin{pmatrix}1\\0\end{pmatrix} \\
= -i\beta\lvert0\rangle + i\alpha\lvert1\rangle
$$

Finally, the $$Z$$ gate leaves the basis state ($$\lvert 0 \rangle $$) unchanged and maps $$\lvert 1 \rangle $$ to $$-\lvert 1 \rangle $$. This gate is also called the phase flip gate sometimes. It is represented by the matrix

$$
Z = 
\begin{bmatrix}
1 & 0 \\
0 & -1
\end{bmatrix}.
$$

We can show that the gate maps  $$\lvert 1 \rangle \to-\lvert 1 \rangle $$ by applying the matrix on a qubit

$$
Z(\alpha\lvert0\rangle + \beta\lvert1\rangle)
= \alpha Z\lvert0\rangle + \beta Z\lvert1\rangle \\
= \alpha\begin{pmatrix}1\\0\end{pmatrix} + \beta\begin{pmatrix}0\\-1\end{pmatrix} \\
= \alpha\begin{pmatrix}1\\0\end{pmatrix} + \beta(-1)\begin{pmatrix}0\\1\end{pmatrix} \\
= \alpha\lvert0\rangle - \beta\lvert1\rangle
$$



While, not specifically relevant to the other articles it is worth noting that the square of any Pauli matrix is the [identity matrix](https://en.wikipedia.org/wiki/Identity_matrix). Hence, we say that the Pauli matrices are [involutory](https://en.wikipedia.org/wiki/Involutory_matrix).

We note that each Pauli matrix squared yields the identity matrix:

$$
X^2 = 
\begin{bmatrix}
0 & 1 \\
1 & 0
\end{bmatrix}^2
=
\begin{bmatrix}
0 & 1 \\
1 & 0
\end{bmatrix}
\begin{bmatrix}
0 & 1 \\
1 & 0
\end{bmatrix}
=
\begin{bmatrix}
1 & 0 \\
0 & 1
\end{bmatrix} = I
$$

$$
Y^2 = 
\begin{bmatrix}
0 & -i \\
i & 0
\end{bmatrix}^2
=
\begin{bmatrix}
0 & -i \\
i & 0
\end{bmatrix}
\begin{bmatrix}
0 & -i \\
i & 0
\end{bmatrix}
=
\begin{bmatrix}
1 & 0 \\
0 & 1
\end{bmatrix} = I
$$

$$
Z^2 = 
\begin{bmatrix}
1 & 0 \\
0 & -1
\end{bmatrix}^2
=
\begin{bmatrix}
1 & 0 \\
0 & -1
\end{bmatrix}
\begin{bmatrix}
1 & 0 \\
0 & -1
\end{bmatrix}
=
\begin{bmatrix}
1 & 0 \\
0 & 1
\end{bmatrix} = I
$$

Now we go over perhaps one of the most important gates in quantum computing: the Hadamard gate. This gate creates an equal superposition state if given a computational basis state. It maps the states $$
\lvert 0 \rangle \mapsto \frac{\lvert 0 \rangle + \lvert 1 \rangle}{\sqrt{2}} \quad \text{and} \quad \lvert 1 \rangle \mapsto \frac{\lvert 0 \rangle - \lvert 1 \rangle}{\sqrt{2}}
$$. Two two states $$(\lvert 0 \rangle + \lvert 1 \rangle)/\sqrt{2}$$ and $$(\lvert 0 \rangle - \lvert 1 \rangle)/\sqrt{2}$$ are written as $$\lvert +\rangle$$ and $$\lvert -\rangle$$ respectively. We represent the Hadamard gate through the Hadamard matrix:

$$
H = \frac{1}{\sqrt{2}} \begin{bmatrix} 1 & 1 \\ 1 & -1 \end{bmatrix}.
$$

Another important term that is crucial to understanding the quantum circuit behind Shor's Algorithm is controlled gates. These are gates which act on 2 qubits or more, where one qubit acts as a control for some operation. For example, the $$CNOT$$ (Controlled NOT) gate acts on 2 qubits, and performs the $$NOT$$ operation on the second qubit iff the first qubit is $$\lvert 1\rangle$$, and otherwise doesn't do anything. Similarly we can define $$CZ,CX$$ and the $$CY$$ gate too!








