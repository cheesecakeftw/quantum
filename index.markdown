---
layout: post
title: The Math Behind Quantum Algorithms
---
<script src="https://cdn.mathjax.org/mathjax/latest/MathJax.js?config=TeX-AMS-MML_HTMLorMML" type="text/javascript"></script>

## Introduction:

## Quantum Fourier Transform

The [Quantum Fourier Transform (QFT)](https://en.wikipedia.org/wiki/Quantum_Fourier_transform) transforms between the computational basis and the state in fourier basis. Here, the computational basis represents the Z-basis states $$ \mid 0 \rangle$$ and $$ \mid 1 \rangle$$ and the fourier basis represents the X-basis states $$ \mid + \rangle$$ and $$ \mid - \rangle$$.Now that we have talked about what the Quantum Fourier Transform is basically doing, lets get into the math.

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

Another property worth mentioning is that, when we encode a state $$\mid q \rangle$$ on an $$n$$ number of qubits, the first qubit rotates with a frequency of $$\frac{q}{2^n}$$ around the z-axis. For example, if we encode the state $$\mid \tilde 5 \rangle$$ on 3 qubits, the first qubit rotates $$\frac{5}{8} * 2 \pi$$ radians and then the second qubit rotates  $$\frac{10}{8} * 2 \pi$$ around the z-axis and so on. We can verify this by simulating it. Check out this [link](https://github.com/Qiskit/textbook/blob/main/notebooks/ch-algorithms/quantum-fourier-transform.ipynb) for a really cool simulation.

Now, we implement the circuit for the Quantum Fourier Transform

The Quantum Fourier Transform only requires two gates. 

The first gate is the Hadamard Gate, H where $$ H = \frac{1}{\sqrt{2}} \begin{bmatrix} 1 & 1 \\ 1 & -1 \end{bmatrix} $$. Applying the operator on a single qubit state $$\mid x_k \rangle$$ gives

$$
H \mid x_k \rangle = \frac{1}{\sqrt{2}}( \mid 0 \rangle - x_k\mid 1\rangle )
$$

The second gate is the controlled R gate. This gate can be represented by the matrix  $$ R_k = \begin{bmatrix} 1 & 0 \\ 0 & e^{\frac{2\pi i}{2^k}} \end{bmatrix} $$. Here,

$$
R_k \mid 0\rangle =  \mid 0\rangle 
$$

$$
R_k \mid 1 \rangle = e^{\frac{2\pi i}{2^k}} \mid 1 \rangle
$$

Visually we can represent the circut as:

<img 
  src="{{ "./Screenshot%202025-06-07%20at%2012.01.13 AM.png" | relative_url }}" 
  width="600" 
  class="my-responsive-class"
/>

Let's see how does this circut work now! We start with an n qubit input state $$\mid x_1x_2\ldots x_n \rangle$$.

Firstly, we apply the Hadamard gate to $$ \mid x_1 \rangle$$,

$$
H \mid x_1x_2\ldots x_n \rangle = \frac{1}{\sqrt{2}} (\mid 0 \rangle +e^\frac{2\pi i x_1}{2} \mid 1 \rangle )   \;\otimes\;  \mid x_2x_3\ldots x_n \rangle 
$$

Notice that $$e^\frac{2\pi i}{2}=e^{\pi i}=-1
$$

Then after the $$R_2$$ gate on qubit 1, which is controlled by qubit 2, we get

$$
\frac{1}{\sqrt{2}} (\mid 0 \rangle +e^{\frac{2\pi i x_1}{2}+\frac{2\pi i x_2}{2^2}} \mid 1 \rangle )   \;\otimes\;  \mid x_2x_3\ldots x_n \rangle 
$$

Note that $$x_1$$ and $$x_2$$ are in the exponent because their binary representations control the sign on $$\mid 1 \rangle$$.

Similarly, after the $$R_n$$ gate on qubit 1 controlled by qubit n, the state becomes

$$
\frac{1}{\sqrt{2}} \left( \mid 0 \rangle + e^{\left( \frac{2\pi i}{2^n} x_n + \frac{2\pi i}{2^{n-1}} x_{n-1} + \cdots + \frac{2\pi i}{2^2} x_2 + \frac{2\pi i}{2} x_1 \right)} \mid 1 \rangle \right) \otimes \mid x_2 x_3 \ldots x_n \rangle
$$

Let $$ x = 2^{n-1} x_1 + 2^{n-2} x_2 + \cdots + 2^{1} x_{n-1} + 2^{0} x_n $$.

Then the transform becomes, 

$$
\frac{1}{\sqrt{2}} (\mid 0 \rangle +e^\frac{2\pi i x}{2^n} \mid 1 \rangle )   \;\otimes\;  \mid x_2x_3\ldots x_n \rangle 
$$

After applying a similar sequence of gates on all the qubits we get,

$$
\frac{1}{\sqrt{2}} \left( \mid 0 \rangle + e^{\frac{2\pi i}{2^n} x} \mid 1 \rangle \right)
\otimes \frac{1}{\sqrt{2}} \left( \mid 0 \rangle + e^{\frac{2\pi i}{2^{n-1}} x} \mid 1 \rangle \right)
\otimes \cdots 
\otimes \frac{1}{\sqrt{2}} \left( \mid 0 \rangle + e^{\frac{2\pi i}{2} x} \mid 1 \rangle \right)
$$

which is what we derived earlier for the $$2^n$$ qubits state generalization.

Let us now try applying the Quantum Fourier Transform to a 3 qubit state $$\mid \psi\rangle = \mid q_0q_1q_2\rangle$$. The circiut can be visualized as:

<img 
  src="{{ "./Screenshot 2025-06-07 at 12.53.52 AM.png" | relative_url }}" 
  width="600" 
  class="my-responsive-class"
/>


Firstly, we apply the Hadamard gate to the first qubit,

$$
H \mid q_0 \rangle = \frac{1}{\sqrt{2}}(\mid 0 \rangle + e^{\frac{2\pi i q_0}{2}}\mid 1\rangle)
$$

Then, we apply the controlled $$R_2$$ gate. Since $$q_1$$ is the control we can put the relative phase it adds to the power of $$q_1$$, since if $$q_1$$ is 0, then we don't apply the phase and if $$q_1=1$$ then we apply the phase. Hence, we get

$$
R_2H \mid q_0 \rangle = \frac{1}{\sqrt{2}}(\mid 0 \rangle + e^{\frac{2\pi i q_0}{2}}e^{\frac{2\pi i q_1}{2^2}}\mid 1\rangle) =  \frac{1}{\sqrt{2}}(\mid 0 \rangle + e^{2\pi i(\frac{q_0}{2}+\frac{q_1}{4})}\mid 1\rangle)
$$

Now we apply the $$R_3$$ gate,

$$
R_3R_2H \mid q_0 \rangle = \frac{1}{\sqrt{2}}(\mid 0 \rangle + e^{2\pi i(\frac{q_0}{2}+\frac{q_1}{4})}e^{\frac{2\pi i q_2}{2^3}}\mid 1\rangle) = \frac{1}{\sqrt{2}}(\mid 0 \rangle + e^{2\pi i(\frac{q_0}{2}+\frac{q_1}{4}+\frac{q_2}{8})}\mid 1\rangle)
$$

Now lets talk about the second qubit. Firstly, we apply the Hadamard gate to get

$$
H \mid q_1 \rangle = \frac{1}{\sqrt{2}}(\mid 0 \rangle + e^{\frac{2\pi i q_1}{2}}\mid 1\rangle)
$$

Then, we apply the $$R_2$$ gate and simplify similarly

$$
R_2H \mid q_1 \rangle = \frac{1}{\sqrt{2}}(\mid 0 \rangle + e^{\frac{2\pi i q_1}{2}}e^{\frac{2\pi i q_2}{2^2}}\mid 1\rangle) =  \frac{1}{\sqrt{2}}(\mid 0 \rangle + e^{2\pi i(\frac{q_1}{2}+\frac{q_2}{4})}\mid 1\rangle)
$$

Finally, we apply the Hadamard gate to the last qubit to get the state

$$
H \mid q_2 \rangle = \frac{1}{\sqrt{2}}(\mid 0 \rangle + e^{\frac{2\pi i q_2}{2}}\mid 1\rangle)
$$

Hence, the final state is

$$
\mid \psi \rangle = \frac{1}{\sqrt{2}} \left( \mid 0 \rangle + e^{2\pi i \left( \frac{q_0}{2} + \frac{q_1}{4} + \frac{q_2}{8} \right)} \mid 1 \rangle \right) 
\otimes \frac{1}{\sqrt{2}} \left( \mid 0 \rangle + e^{2\pi i \left( \frac{q_1}{2} + \frac{q_2}{4} \right)} \mid 1 \rangle \right)
\otimes \frac{1}{\sqrt{2}} \left( \mid 0 \rangle + e^{2\pi i \left( \frac{q_2}{2} \right)} \mid 1 \rangle \right)
$$

Notice that this is the exact form that we would have gotten using the formula derived. Also, earlier we talked about encoding $$\mid \tilde 5 \rangle$$ where we got the angles of rotation for each qubit. We found out that the first qubit rotates $$\frac{5}{8} * 2 \pi$$ radians and then the second qubit rotates  $$\frac{10}{8} * 2 \pi$$ radians around the z-axis and the third qubit rotates  $$\frac{15}{8} * 2 \pi$$ radians around the z-axis. The binary representation of 5 is $$\mid 101 \rangle$$. After substituting this into the formula above we get,

$$
\mid \psi \rangle = \frac{1}{\sqrt{2}} \left( \mid 0 \rangle + e^{2\pi i \left( \frac{1}{2} + \frac{0}{4} + \frac{1}{8} \right)} \mid 1 \rangle \right) 
\otimes \frac{1}{\sqrt{2}} \left( \mid 0 \rangle + e^{2\pi i \left( \frac{0}{2} + \frac{1}{4} \right)} \mid 1 \rangle \right)
\otimes \frac{1}{\sqrt{2}} \left( \mid 0 \rangle + e^{2\pi i \left( \frac{1}{2} \right)} \mid 1 \rangle \right)
$$

which is equivalent to,

$$
\mid \psi \rangle = \frac{1}{\sqrt{2}} \left( \mid 0 \rangle + e^{2\pi i \frac{5}{8}} \mid 1 \rangle \right) 
\otimes \frac{1}{\sqrt{2}} \left( \mid 0 \rangle + e^{2\pi i \frac{1}{4}} \mid 1 \rangle \right)
\otimes \frac{1}{\sqrt{2}} \left( \mid 0 \rangle + e^{2\pi i \frac{1}{2}} \mid 1 \rangle \right)
$$

Notice, that taking module $$2 \pi$$ on the angles that we chose earlier gives us the same angles that the formula gives us! Hence, our initial work is confirmed by the formula and can also be confirmed visually.

Hence, we can mathematically represent the  QFT on a basis state $$\mid x_1x_2\ldots x_n \rangle$$ through the identity

$$
QFT \mid x \rangle = \frac{1}{\sqrt{2^n}} \sum_{y=0}^{2^n - 1} e^{\frac{2\pi i x y}{2^n}} \mid y \rangle
$$

## Shor's Algorithm



