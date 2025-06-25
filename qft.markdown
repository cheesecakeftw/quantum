---
layout: post
title: Quantum Fourier Transform
---
<script src="https://cdn.mathjax.org/mathjax/latest/MathJax.js?config=TeX-AMS-MML_HTMLorMML" type="text/javascript"></script>


The [Quantum Fourier Transform (QFT)](https://en.wikipedia.org/wiki/Quantum_Fourier_transform) transforms between the computational basis and the state in fourier basis. Here, the computational basis represents the Z-basis states $$ \lvert 0 \rangle$$ and $$ \lvert 1 \rangle$$ and the fourier basis represents the X-basis states $$ \lvert + \rangle$$ and $$ \lvert - \rangle$$. Now that we have talked about what the Quantum Fourier Transform is basically doing, lets get into the math.

The complex Fourier coefficients of a real valued function $$f$$ are defined on an interval $$[0,2L]$$ as 

$$
c_n = \frac{1}{\sqrt{2L}} \int_0^{2L} f(x) e^{\frac{in\pi x}{A}} , dx
$$

The factor $$1/\sqrt{2L}$$ gives

$$
\sum_{n=0}^{\infty} \lvert c_n \rvert^2 = \int_0^{2L} \lvert f(x) \rvert^2 \, dx
$$

Now suppose that we think of a sequence $$f=f_0,f_1,\ldots,f_{2L-1}$$, where L is an integer, as the set of values at $$x=0,x=1,\ldots,x=2L-1$$ of a function $$f(x)$$. Here we define a new $$c_n$$ replacing the fourier integral with $$2L$$ equal subdivisions of length 1 (essentially taking the Reimann Sum). Basically we turned the continuous transform to a discrete one and the sum only involves the elements of $$f$$ 

$$
c_n = \frac{1}{\sqrt{2L}} \sum_{m=0}^{2L - 1} f_m , e^{\frac{in\pi m}{A}}
$$

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

The quantum Fourier transform can also be represented as a unitary matrix defined by F which is the DFT matrix

$$
F_N = \frac{1}{\sqrt{N}}
\begin{pmatrix}
1 & 1 & 1 & 1 & \cdots & 1 \\
1 & \omega & \omega^2 & \omega^3 & \cdots & \omega^{N-1} \\
1 & \omega^2 & \omega^4 & \omega^6 & \cdots & \omega^{2(N-1)} \\
1 & \omega^3 & \omega^6 & \omega^9 & \cdots & \omega^{3(N-1)} \\
\vdots & \vdots & \vdots & \vdots & \ddots & \vdots \\
1 & \omega^{N-1} & \omega^{2(N-1)} & \omega^{3(N-1)} & \cdots & \omega^{(N-1)(N-1)}
\end{pmatrix}
$$

where $$w=w_n=e^{\frac{2\pi i}{N}}$$ is an N-th root of unity and we define the transform as $$F_{N_{j,k}}=\frac{1}{\sqrt{N}}w_n^{jk}$$.

For example, in the cases of $$N=1$$ to $$N=4$$ and the phase $$w=i$$ we get

$$F_1 = [1],\quad F_2 = \frac1{\sqrt2}\begin{pmatrix}1&1\\1&-1\end{pmatrix},\quad F_3 = \frac1{\sqrt3}\begin{pmatrix}1&1&1\\1&\omega&\omega^2\\1&\omega^2&\omega\end{pmatrix},\quad F_4 = \frac12\begin{pmatrix}1&1&1&1\\1&i&-1&-i\\1&-1&1&-1\\1&-i&-1&i\end{pmatrix}$$

Another important property of the Fourier transform is that it is [unitary](https://en.wikipedia.org/wiki/Unitary_transformation). Before we understand what that is let us introduce the Inverse quantum Fourier Transform. It acts similarly to the Fourier transform but instead undoes the Fourier transform instead of applying the transform. It is represented as

$$
x_j = \frac{1}{\sqrt{N}} \sum_{k=0}^{N-1}  e^{-\frac{2\pi ijk}{N}} y_k, \quad k = 0, 1, 2, \ldots, N-1.
$$

Finally, we prove that the quantum fourier transform is unitary. This is a really important property that is used in various quantum algorithms and makes the transform easier to understand. Note that we represent the inverse of the quantum fourier transform as $$F^{-1}=F^{\dagger}$$.

We define the Quantum Fourier Transform by

$$
F = \frac{1}{\sqrt{N}} \sum_{j,k=0}^{N-1}
      e^{2\pi i\,jk/N}
      \lvert k\rangle\langle j\rvert
$$

Its conjugate matrix is obtained by complex conjugation of the phase

$$
F^{\dagger} = \frac{1}{\sqrt{N}} \sum_{j,k=0}^{N-1}
      e^{-2\pi i\,jk/N}
      \lvert j\rangle\langle k\rvert
$$

To show that its unitary we compute

$$
F^{\dagger}F
= \frac{1}{N} \sum_{j,k=0}^{N-1} \sum_{j'=0}^{N-1}
    e^{-2\pi i\,jk/N}
    e^{2\pi i\,j'k/N}
    \lvert j\rangle\langle j'\rvert
$$

Using the inner product property

$$
\langle k\vert k'\rangle = \delta_{k,k'}
$$

reduces the expression to

$$
F^{\dagger}F
= \frac{1}{N} \sum_{j,j'=0}^{N-1} \sum_{k=0}^{N-1}
    e^{2\pi i\,k(j'-j)/N}
    \lvert j\rangle\langle j'\rvert
$$

For each pair $$j$$ and $$j'$$ the finite geometric sum obeys

$$
\frac{1}{N}\sum_{k=0}^{N-1} e^{2\pi i\,k(j'-j)/N}
= \delta_{j',j}
$$

When $$j' = j$$ every term equals one the average equals one and when $$j' \neq j$$ the terms form a complete set of roots of unity whose sum equals zero.

Substituting this result collapses the sums to

$$
F^{\dagger}F
= \sum_{j,j'=0}^{N-1} \delta_{j',j}
    \lvert j\rangle\langle j'\rvert
= \sum_{j=0}^{N-1}
    \lvert j\rangle\langle j\rvert
= 1
$$

Hence, $$F^\dagger F$$ equals to 1 and $$F$$ is unitary!


Using these definitions of the Fourier Transform lets expand the Quantum Fourier transform for some $$N$$!

Firstly, lets define the state $$\lvert x \rangle = \lvert x_1 x_2 \ldots x_n\rangle$$, for $$N=2^n$$. We use n so that the Hilbert Space is exactly $$2^n$$ dimensional. A Hilbert Space is a vector space over the complex numbers. We use 2 as the base because you only have two complex coordinates, making the Hilbert Space for one qubit $$C^2$$. Then we can define 

$$
QFT\lvert x \rangle = \frac{1}{\sqrt{N}} \sum_{y=0}^{N-1}  e^{\frac{2\pi iyj}{N}} \lvert y \rangle
$$ 

After substituting $$N=2^n$$,

$$
= \frac{1}{\sqrt{2^n}}  \sum_{y=0}^{N-1}  e^{\frac{2\pi iyj}{2^n}}\lvert y \rangle
$$

Rewriting in fractional bit notation,

$$
= \frac{1}{\sqrt{2^n}}  \sum_{y=0}^{N-1}  e^{2\pi i(\sum_{k=0}^{n} \frac{y_k}{2^k})j}  \lvert y_1,y_2 \ldots y_n \rangle 
$$

$$
= \frac{1}{\sqrt{2^n}}  \sum_{y=0}^{N-1} \prod_{k=1}^{n} e^{\frac{2\pi i y_kj}{2^k}}  \lvert y_1,y_2 \ldots y_n \rangle
$$

Because each $$y_k$$ represents a bit,

$$
= \frac{1}{\sqrt{2^n}} \sum_{y_1=0}^1 \sum_{y_2=0}^1 \cdots \sum_{y_n=0}^1 
   \Bigl(\,\prod_{k=1}^{n} e^{\frac{2\pi i\,y_k\,j}{2^k}}\Bigr)\;\lvert y_1,y_2,\ldots,y_n \rangle
$$

$$
= \frac{1}{\sqrt{2^n}} 
   \Bigl(\sum_{y_1=0}^1 e^{\frac{2\pi i\,y_1\,j}{2^1}}\lvert y_1 \rangle\Bigr)\,
   \Bigl(\sum_{y_2=0}^1 e^{\frac{2\pi i\,y_2\,j}{2^2}}\lvert y_2 \rangle\Bigr)\,
   \cdots\,
   \Bigl(\sum_{y_n=0}^1 e^{\frac{2\pi i\,y_n\,j}{2^n}}\lvert y_n \rangle\Bigr)
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
QFT\lvert x \rangle = \Bigl(\frac{\lvert 0 \rangle + e^{\frac{2\pi i\,j}{2^1}}\,\lvert 1 \rangle}{\sqrt{2}}\Bigr)
  \;\otimes\;
  \Bigl(\frac{\lvert 0 \rangle + e^{\frac{2\pi i\,j}{2^2}}\,\lvert 1 \rangle}{\sqrt{2}}\Bigr)
  \;\otimes \cdots \otimes\;
  \Bigl(\frac{\lvert 0 \rangle + e^{\frac{2\pi i\,j}{2^n}}\,\lvert 1 \rangle}{\sqrt{2}}\Bigr).
$$

which can be confirmed by analyzing the Fourier Transform. 

Another property worth mentioning is that, when we encode a state $$\lvert q \rangle$$ on an $$n$$ number of qubits, the first qubit rotates with a frequency of $$\frac{q}{2^n}$$ around the z-axis. For example, if we encode the state $$\lvert \tilde 5 \rangle$$ on 3 qubits, the first qubit rotates $$\frac{5}{8} * 2 \pi$$ radians and then the second qubit rotates  $$\frac{10}{8} * 2 \pi$$ around the z-axis and so on. We can verify this by simulating it. Check out this [link](https://github.com/Qiskit/textbook/blob/main/notebooks/ch-algorithms/quantum-fourier-transform.ipynb) for a really cool simulation.

Now, we implement the circuit for the Quantum Fourier Transform

The Quantum Fourier Transform only requires two gates. 

The first gate is the Hadamard Gate, H where $$ H = \frac{1}{\sqrt{2}} \begin{bmatrix} 1 & 1 \\ 1 & -1 \end{bmatrix} $$. Applying the operator on a single qubit state $$\lvert x_k \rangle$$ gives

$$
H \lvert x_k \rangle = \frac{1}{\sqrt{2}}( \lvert 0 \rangle - x_k\lvert 1\rangle )
$$

The second gate is the controlled R gate. This gate can be represented by the matrix  $$ R_k = \begin{bmatrix} 1 & 0 \\ 0 & e^{\frac{2\pi i}{2^k}} \end{bmatrix} $$. Here,

$$
R_k \lvert 0\rangle =  \lvert 0\rangle 
$$

$$
R_k \lvert 1 \rangle = e^{\frac{2\pi i}{2^k}} \lvert 1 \rangle
$$

Visually we can represent the circuit as:

<img 
  src="{{ "./Screenshot%202025-06-07%20at%2012.01.13 AM.png" | relative_url }}" 
  width="600" 
  class="my-responsive-class"
/>

Let's see how does this circuit work now! We start with an n qubit input state $$\lvert x_1x_2\ldots x_n \rangle$$.

Firstly, we apply the Hadamard gate to $$ \lvert x_1 \rangle$$,

$$
H \lvert x_1x_2\ldots x_n \rangle = \frac{1}{\sqrt{2}} (\lvert 0 \rangle +e^\frac{2\pi i x_1}{2} \lvert 1 \rangle )   \;\otimes\;  \lvert x_2x_3\ldots x_n \rangle 
$$

Notice that $$e^\frac{2\pi i}{2}=e^{\pi i}=-1
$$

Then after the $$R_2$$ gate on qubit 1, which is controlled by qubit 2, we get

$$
\frac{1}{\sqrt{2}} (\lvert 0 \rangle +e^{\frac{2\pi i x_1}{2}+\frac{2\pi i x_2}{2^2}} \lvert 1 \rangle )   \;\otimes\;  \lvert x_2x_3\ldots x_n \rangle 
$$

Note that $$x_1$$ and $$x_2$$ are in the exponent because their binary representations control the sign on $$\lvert 1 \rangle$$.

Similarly, after the $$R_n$$ gate on qubit 1 controlled by qubit n, the state becomes

$$
\frac{1}{\sqrt{2}} \left( \lvert 0 \rangle + e^{\left( \frac{2\pi i}{2^n} x_n + \frac{2\pi i}{2^{n-1}} x_{n-1} + \cdots + \frac{2\pi i}{2^2} x_2 + \frac{2\pi i}{2} x_1 \right)} \lvert 1 \rangle \right) \otimes \lvert x_2 x_3 \ldots x_n \rangle
$$

Let $$ x = 2^{n-1} x_1 + 2^{n-2} x_2 + \cdots + 2^{1} x_{n-1} + 2^{0} x_n $$.

Then the transform becomes, 

$$
\frac{1}{\sqrt{2}} (\lvert 0 \rangle +e^\frac{2\pi i x}{2^n} \lvert 1 \rangle )   \;\otimes\;  \lvert x_2x_3\ldots x_n \rangle 
$$

After applying a similar sequence of gates on all the qubits we get,

$$
\frac{1}{\sqrt{2}} \left( \lvert 0 \rangle + e^{\frac{2\pi i}{2^n} x} \lvert 1 \rangle \right)
\otimes \frac{1}{\sqrt{2}} \left( \lvert 0 \rangle + e^{\frac{2\pi i}{2^{n-1}} x} \lvert 1 \rangle \right)
\otimes \cdots 
\otimes \frac{1}{\sqrt{2}} \left( \lvert 0 \rangle + e^{\frac{2\pi i}{2} x} \lvert 1 \rangle \right)
$$

which is what we derived earlier for the $$2^n$$ qubits state generalization.

Let us now apply the Quantum Fourier Transform to a 3 qubit state $$\lvert \psi\rangle = \lvert q_0q_1q_2\rangle$$. The circuit can be visualized as:

<img 
  src="{{ "./Screenshot 2025-06-07 at 12.53.52 AM.png" | relative_url }}" 
  width="600" 
  class="my-responsive-class"
/>


Firstly, we apply the Hadamard gate to the first qubit,

$$
H \lvert q_0 \rangle = \frac{1}{\sqrt{2}}(\lvert 0 \rangle + e^{\frac{2\pi i q_0}{2}}\lvert 1\rangle)
$$

Then, we apply the controlled $$R_2$$ gate. Since $$q_1$$ is the control we can put the relative phase it adds to the power of $$q_1$$, since if $$q_1$$ is 0, then we don't apply the phase and if $$q_1=1$$ then we apply the phase. Hence, we get

$$
R_2H \lvert q_0 \rangle = \frac{1}{\sqrt{2}}(\lvert 0 \rangle + e^{\frac{2\pi i q_0}{2}}e^{\frac{2\pi i q_1}{2^2}}\lvert 1\rangle) =  \frac{1}{\sqrt{2}}(\lvert 0 \rangle + e^{2\pi i(\frac{q_0}{2}+\frac{q_1}{4})}\lvert 1\rangle)
$$

Now we apply the $$R_3$$ gate,

$$
R_3R_2H \lvert q_0 \rangle = \frac{1}{\sqrt{2}}(\lvert 0 \rangle + e^{2\pi i(\frac{q_0}{2}+\frac{q_1}{4})}e^{\frac{2\pi i q_2}{2^3}}\lvert 1\rangle) = \frac{1}{\sqrt{2}}(\lvert 0 \rangle + e^{2\pi i(\frac{q_0}{2}+\frac{q_1}{4}+\frac{q_2}{8})}\lvert 1\rangle)
$$

Now lets talk about the second qubit. Firstly, we apply the Hadamard gate to get

$$
H \lvert q_1 \rangle = \frac{1}{\sqrt{2}}(\lvert 0 \rangle + e^{\frac{2\pi i q_1}{2}}\lvert 1\rangle)
$$

Then, we apply the $$R_2$$ gate and simplify similarly

$$
R_2H \lvert q_1 \rangle = \frac{1}{\sqrt{2}}(\lvert 0 \rangle + e^{\frac{2\pi i q_1}{2}}e^{\frac{2\pi i q_2}{2^2}}\lvert 1\rangle) =  \frac{1}{\sqrt{2}}(\lvert 0 \rangle + e^{2\pi i(\frac{q_1}{2}+\frac{q_2}{4})}\lvert 1\rangle)
$$

Finally, we apply the Hadamard gate to the last qubit to get the state

$$
H \lvert q_2 \rangle = \frac{1}{\sqrt{2}}(\lvert 0 \rangle + e^{\frac{2\pi i q_2}{2}}\lvert 1\rangle)
$$

Hence, the final state is

$$
\lvert \psi \rangle = \frac{1}{\sqrt{2}} \left( \lvert 0 \rangle + e^{2\pi i \left( \frac{q_0}{2} + \frac{q_1}{4} + \frac{q_2}{8} \right)} \lvert 1 \rangle \right) 
\otimes \frac{1}{\sqrt{2}} \left( \lvert 0 \rangle + e^{2\pi i \left( \frac{q_1}{2} + \frac{q_2}{4} \right)} \lvert 1 \rangle \right)
\otimes \frac{1}{\sqrt{2}} \left( \lvert 0 \rangle + e^{2\pi i \left( \frac{q_2}{2} \right)} \lvert 1 \rangle \right)
$$

Notice that this is the exact form that we would have gotten using the formula derived. Also, earlier we talked about encoding $$\lvert \tilde 5 \rangle$$ where we got the angles of rotation for each qubit. We found out that the first qubit rotates $$\frac{5}{8} * 2 \pi$$ radians and then the second qubit rotates  $$\frac{10}{8} * 2 \pi$$ radians around the z-axis and the third qubit rotates  $$\frac{15}{8} * 2 \pi$$ radians around the z-axis. The binary representation of 5 is $$\lvert 101 \rangle$$. After substituting this into the formula above we get,

$$
\lvert \psi \rangle = \frac{1}{\sqrt{2}} \left( \lvert 0 \rangle + e^{2\pi i \left( \frac{1}{2} + \frac{0}{4} + \frac{1}{8} \right)} \lvert 1 \rangle \right) 
\otimes \frac{1}{\sqrt{2}} \left( \lvert 0 \rangle + e^{2\pi i \left( \frac{0}{2} + \frac{1}{4} \right)} \lvert 1 \rangle \right)
\otimes \frac{1}{\sqrt{2}} \left( \lvert 0 \rangle + e^{2\pi i \left( \frac{1}{2} \right)} \lvert 1 \rangle \right)
$$

which is equivalent to,

$$
\lvert \psi \rangle = \frac{1}{\sqrt{2}} \left( \lvert 0 \rangle + e^{2\pi i \frac{5}{8}} \lvert 1 \rangle \right) 
\otimes \frac{1}{\sqrt{2}} \left( \lvert 0 \rangle + e^{2\pi i \frac{1}{4}} \lvert 1 \rangle \right)
\otimes \frac{1}{\sqrt{2}} \left( \lvert 0 \rangle + e^{2\pi i \frac{1}{2}} \lvert 1 \rangle \right)
$$

Notice, that taking module $$2 \pi$$ on the angles that we chose earlier gives us the same angles that the formula gives us! Hence, our initial work is confirmed by the formula and can also be confirmed visually.

Hence, we can mathematically represent the  QFT on a basis state $$\lvert x_1x_2\ldots x_n \rangle$$ through the identity

$$
QFT \lvert x \rangle = \frac{1}{\sqrt{2^n}} \sum_{y=0}^{2^n - 1} e^{\frac{2\pi i x y}{2^n}} \lvert y \rangle
$$

Lastly, let us consider the time complexity of the Quantum Fourier Transform. In the quantum circuit for the $$n$$ qubit Fourier transform, each qubit $$k$$ (for $$k=1\ldots,n$$) is first acted on by a single Hadamard gate and then by a sequence of controlled phase rotations controlled by that qubit and targeting each of the remaining $$(n−k)$$ qubits. Thus, qubit 1 requires one Hadamard plus $$ (n−1)$$ controlled phase gates, qubit 2 requires one Hadamard plus $$(n−2)$$ controlled phase gates, and so on down to the last qubit, which needs only a Hadamard. Summing these gate we get

$$
[1 + (n - 1)] + [1 + (n - 2)] + \cdots + [1 + 0] = n + (n - 1) + \cdots + 1 = \frac{n(n + 1)}{2} = O(n^2).
$$

This shows that the time complexity is proportional to $$n^2$$ which is a quadratic polynomial of the number of qubits. Since the time complexity of the QFT is in polynomial time it is a smaller time complexity than the classical Fourier transform which is exponential.

Side Note: Using the generalized Fourier transform on [abelian groups](https://en.wikipedia.org/wiki/Abelian_group) (commutative operations groups), which are basically definite, there are two ways to define a quantum Fourier transform on an $$n$$ qubit register. The first one is that you index the qubits by the cyclic ring $$\mathbb{Z} / 2^n \mathbb{Z}$$, which maps 

$$
\lvert x \rangle ;\longmapsto; \frac{1}{\sqrt{2^n}} \sum_{y=0}^{2^n - 1} e^{\frac{2\pi i x y}{2^n}} \lvert y \rangle
$$

In the second one you view the register as the Boolean group $$(\mathbb{Z} / 2\mathbb{Z})^n$$, where the transform reduces to applying a Hadamard gate to each qubit in parallel.

Shor’s algorithm combines both transforms starting with a layer of Hadamard's on $$(\mathbb{Z} / 2\mathbb{Z})^n$$ and then a QFT on $$\mathbb{Z} / 2^n \mathbb{Z}$$ to factor integers efficiently. We define these groups and the algorithm more accurately and properly in the [Shor's Algorithm article](./)!