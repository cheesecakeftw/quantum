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

A qubit can be thought of as a 2-dimensional complex vector, which is called a superposition state vector. Note that it has two fundamental states which are again $$0$$ and $$1$$.

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

We can define a superposition state vector in $$2^n$$ dimensional Hilbert space using probability theory as 

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

Now we define important gates that we use in another articles.







