---
layout: home
---
<script src="https://cdn.mathjax.org/mathjax/latest/MathJax.js?config=TeX-AMS-MML_HTMLorMML" type="text/javascript"></script>

# The Math Behind Shor's Algorithm and Implementation in Qiskit
## Introduction

[Shor's Algorithm](https://en.wikipedia.org/wiki/Shor%27s_algorithm) is an algorithm used to find the prime factors of an integer. But why is this algorithm so famous in quantum computing? This algorithm has compelling applications such as cracking the most used encryption protocol, [RSA](https://en.wikipedia.org/wiki/RSA_cryptosystem), which functions on the assumption that the prime factors of an integer can't be found. This algorithm has evidence of super-polynomial speedup compared to the best known classical algorithms. However, as of right now our quantum computers aren't advanced enough to factor numbers of practical significance because of a lack of qubits. Also, the noise in quantum circuits requires additional qubits for quantum error correction adding to the impracticality of the algorithm right now. 

Before we get into the math behind the algorithm, lets discuss the time complexity of Shor's Algorithm. To factor an integer $$N$$ on a quantum computer, Shor's algorithm runs in polynomial time. To be specific, it takes quantum gates of order $$O((\log N)^2 (\log \log N)(\log \log \log N))$$ using fast multiplication. However, we can achieve $$O((\log N)^2 (\log \log N))$$ using the asymptomatically fastest multiplication algorithm. These are both significantly faster time complexities than the most efficient classical factoring algorithm, the general number sieve, which works in exponential time $$ O( e^{1.9 (\log N)^{1/3} (\log \log N)^{2/3}})$$.

It is important to note that this algorithm involves both classical and quantum parts. Specifically, the quantum speedup happens from the order-finding problem which we will explain and go into more detail about later.

The goal of the algorithm, in mathematical terms, is to find primes $$P$$ and $$Q$$ for some $$N$$, such that $$N=PQ$$. For this algorithm to work we assume that $$N$$ isn't even, and $$N$$ isn't a prime or a prime power. We can check if $$N$$ is prime or not using various [primality tests](https://en.wikipedia.org/wiki/Primality_test#Complexity), including the infamous Fermat's little theorem.

If $$N$$ is even then we can use the trivial case $$P=2$$, then $$Q=N/2$$ which is straightforward.

If $$N$$ is a [prime power](https://en.wikipedia.org/wiki/Prime_power), we can check for every $$k$$ such that $$2 \leq k \leq \log_3 N$$ if $$N^{\frac{1}{k}}$$ is an integer. If that happens to be the case, then $$P=N^{\frac{1}{k}}$$ and $$Q=N^{\frac{k-1}{k}}$$ which is again a trivial case.

If none of these easy cases produce a nontrivial factor of $$N$$ then we proceed to use Shor's Algorithm. Before we do that let us review some important mathematical concepts that we need to be familiar with.

## Mathematical Prerequisites:

#### [Basic Modular Arithmetic](https://en.wikipedia.org/wiki/Modular_arithmetic)

For some $$a,b,r,N \in Z$$, we write $$a=b \times N +r$$. This can be written as $$a \equiv r \pmod{N}. $$ This can also be written as $$N \mid (a-r)$$ which reads as "$$N$$ divides $$a-r$$".

#### [Euclidean Algorithm](https://en.wikipedia.org/wiki/Euclidean_algorithm)

The Euclidean Algorithm is one of the most efficient algorithms to find the $$GCD$$ of two numbers $$a,b$$. While, we won't use the Euclidean algorithm in the quantum part, it will be used consistently in the classical part. Let $$a,b \in N$$, $$b \neq 0$$, $$a \geq b$$. Then for $$r_{k+1}<r_k<r_{k-1}$$ the Euclidean algorithm is then defined as  

$$
a = b \cdot q_1 + r_1 \\
b = r_1 \cdot q_2 + r_2 \\
r_1 = r_2 \cdot q_3 + r_3 \\
\vdots \\
r_{n-1} = r_n \cdot q_{n+1} + 0 \\
$$

where $$r_n$$ is $$GCD(a,b)$$.

This can also be represented as the continued fraction

$$\frac{a}{b} = q_1 + \cfrac{1}{q_2 + \cfrac{1}{\cdots + \cfrac{1}{q_n}}}$$

Note that the Euclidean Algorithm finds $$GCD(a,b)$$ in at most $$\log(a)$$ divisions.

#### [Euler's Totient Function](https://en.wikipedia.org/wiki/Euler%27s_totient_function)

In number theory, Euler's totient function ($$\varphi$$) counts the number of positive integers $$k \leq n$$ such that $$\gcd(k,n) = 1$$

#### [The Multiplicative Group $$(\mathbb{Z}/N\mathbb{Z})^{\times}$$](https://en.wikipedia.org/wiki/Multiplicative_group_of_integers_modulo_n)

In modular arithmetic, the integers coprime (relatively prime) to n from the set { $$0 , 1 , \ldots , n − 1 $$} of $$n$$ non-negative integers form a group under multiplication modulo $$n$$, called the multiplicative group of integers modulo $$n$$ or denoted by the ring $$(\mathbb{Z}/N\mathbb{Z})^{\times}$$. 

Note, that the [order](https://en.wikipedia.org/wiki/Order_(group_theory)) of this group is defined by the earlier stated Euler's Totient Function ($$\varphi(n)$$). This means that in any finite order group $$G$$, the order of an element $$g \in G$$ is the smallest integer $$r$$ such that $$g^r=e$$, where $$e$$ denotes the identity element of the group. 

Additionally, for some $$a$$ in the group, the multiplicative inverse of $$a$$ modulo $$n$$ is given by $$x \in Z$$ satisfying $$ax \equiv 1 \pmod{n}$$. It exists precisely when $$\gcd(a,n)=1$$ (a is coprime to n) and by [Bezout's Lemma](https://en.wikipedia.org/wiki/B%C3%A9zout%27s_lemma) which states that there are $$x,y \in Z$$, such that $$ax+ny=gcd(a,n)$$, we can easily show x is coprime to n. It follows that the multiplicative inverse belongs to the group.

## The Algorithm and the Quantum Circuit

Let us begin with some $$N$$ that isn't a prime power, prime number or even as previously defined. Firstly, we pick some integer $$1 < a <N$$. Then we check the trivial case where $$\gcd(a,N)$$ could be a nontrivial divisor of $$N$$. If this produces a divisor then obviously $$P=gcd(a,N)$$ and $$Q=\frac{N}{\gcd(a,N)}$$. If this case isn't satisfied then we move on with the algorithm.

We know that if this case wasn't satisfied $$\gcd(a,N)=1$$ and so $$a$$ is contained in the multiplicative group of integers modulo $$N$$ defined by the ring $$(\mathbb{Z}/N\mathbb{Z})^{\times}$$. This means that $$a$$ has a multiplicative inverse modulo $$N$$. Thus, $$a$$ has a multiplicative order $$r$$ modulo $$N$$.

Consider the infinite sequence of powers in a group $$G=(\mathbb{Z}/N\mathbb{Z})^{\times}$$:

$$a,a^2,a^3 \ldots $$

Since $$G$$, only has $$\lvert G \rvert$$ elements, by the pigeonhole principle we know that two of these powers must coincide to give

$$a^i = a^j \quad (i<j)$$

Multiplying on the left by the inverse of $$a^i$$ gives

$$a^{j-i}=1$$

So, there exists some positive integer $$r=j-i$$ with

$$ a^r \equiv 1\pmod{N}$$

The smallest such $$r$$ is known as the multiplicative order of a in the group $$G$$. Hence, a has a multiplicative order $$r$$ modulo $$N$$ in the group where $$ a^r \equiv 1\pmod{N}$$.

Let's try out an example here. Consider $$a=2$$ and $$N=9$$,

$$
\begin{aligned}
2^0 \equiv 1 \pmod{9} \qquad & 2^7 \equiv 2 \pmod{9} \qquad \\
2^1 \equiv 2 \pmod{9} \qquad & 2^8 \equiv 4 \pmod{9} \qquad \\
2^2 \equiv 4 \pmod{9} \qquad & 2^9 \equiv 8 \pmod{9} \qquad \\
2^3 \equiv 8 \pmod{9} \qquad & 2^{10} \equiv 7 \pmod{9} \qquad \\
2^4 \equiv 7 \pmod{9} \qquad & 2^{11} \equiv 5 \pmod{9} \qquad \\
2^5 \equiv 5 \pmod{9} \qquad & 2^{12} \equiv 1 \pmod{9} \qquad \\
2^6 \equiv 1 \pmod{9} \qquad & \ldots
\end{aligned}
$$

We notice a really cool pattern here! Notice that the residues 1, 2, 4, 8, 7, 5 are repeating. Hence, we can say that the order of 2 modulo 9 is 6. 


This is where the quantum part comes in! We use the quantum subroutine to find $$r$$. Quantum computers speed up this part of the algorithm exponentially making this algorithm much more efficient than classical methods.

We rewrite the definition of multiplicative order to get

$$N \mid a^r-1$$

Factoring we get

$$N \mid (a^{r/2}-1)(a^{r/2}+1)$$

Here, we must note that the algorithm doesn't work for an odd $$r$$ because the power $$\frac{r}{2}$$ must be an integer. This would mean that the algorithm would have to start again using another value of $$a$$.

Hence, based on the previous criteria we assume that $$r$$ is an even integer. Let's claim that $$N \mid (a^{r/2}-1)$$. But then, $$a^{r/2} \equiv 1 \pmod{N}$$, which would imply that there exists a smaller multiplicative order than $$r$$, since $$r/2 <r$$. But, we already know that $$r$$ is the smallest possible multiplicative order for $$a$$. Hence, the claim that $$N \mid (a^{r/2}-1)$$ can't be true.

This leaves us with two cases. Either $$N \mid (a^{r/2}+1)$$ or not. If $$N$$ doesn't divide $$a^{r/2}+1$$ then we compute $$m=\gcd(N,a^{r/2}-1)$$. If $$m=1$$ then $$N\mid a^{r/2}+1$$ was true, in which case we can't find a nontrivial factor of $$N$$ from $$a$$ and we must restart with a new $$a$$. However, if $$m \neq 1$$ then we have found a nontrivial factor of $$N$$, where $$P=m$$ and $$Q=N/m$$. We could have also computed $$\gcd(N, a^{r/2} + 1)$$ since it might produce a nontrivial factor in cases where $$\gcd(N, a^{r/2} - 1)$$ does not, and it will be trivial precisely when $$N \mid a^{r/2} + 1$$.

Now that we have gone over the logic of the algorithm let us move on to the quantum computing implementation.

The main goal of the quantum subroutine is to find the order $$r$$ of $$a$$ modulo $$N$$ as described previously. Basically we need to find the smallest $$r$$ such that for $$\gcd(a,N)=1$$ where $$1<a<N$$ we have $$a^r \equiv 1\pmod{N}$$. 

The quantum subroutine of this algorithm uses a quantum circuit with two registers. The second register uses $$n$$ qubits, where $$n$$ is the smallest integer such that $$N<2^n$$. The size of the first register determines how accurate the approximation of the circuit produces. We will show later that $$2n$$ qubits are enough to find $$r$$.

The first register therefore has $$m=2n$$ qubits, giving it $$2^{m}=2^{2n}$$ computational basis states.

Firstly lets define a gate $$U_{a,N} \lvert x \rangle = \lvert x a \pmod{N}\rangle $$. This gate is a quantum phase estimation on the unitary operator. Below, you can see clearly how the [eigenstate](https://en.wikipedia.org/wiki/Eigenvalues_and_eigenvectors) of $$U$$ might look like. QPE extracts the eigenvalue phase of a unitary operator.

If we apply this gate multiple times we get $$U^0_{a,N} \lvert 1 \rangle = \lvert 1 \mod(N)\rangle $$, $$U^1_{a,N} \lvert 1 \rangle = \lvert a \mod(N)\rangle $$, $$U^2_{a,N} \lvert 1\rangle = \lvert a^2 \mod(N)\rangle $$, $$U^3_{a,N} \lvert 1 \rangle = \lvert a^3 \mod(N)\rangle $$ $$\ldots$$ $$U^r_{a,N} \lvert 1 \rangle = \lvert a^r \mod(N)\rangle $$. Note that at the final stage $$U^r_{a,N} \lvert 1 \rangle = \lvert a^r \mod(N)\rangle = \lvert 1 \mod(N) \rangle$$. For the rest of our discussion we define $$U_{a,N}$$ as $$U$$ for clarity.

Now consider the state

$$
\lvert u_k \rangle = \frac{1}{\sqrt{r}} \left(e^{-2\pi i k(0)/r} \lvert a^0 \bmod (N) \rangle + e^{-2\pi i k(1)/r} \lvert a^1 \bmod (N) \rangle + \ldots + e^{-2\pi i k(r-1)/r} \lvert a^{r} \bmod (N) \rangle \right)
$$ 
 
If we apply the $$U$$ gate we get

$$
U \lvert u_k \rangle = \frac{1}{\sqrt{r}} \left(e^{-2\pi i k(0)/r} U \lvert a^0 \bmod (N) \rangle + e^{-2\pi i k(1)/r} U \lvert a^1 \bmod (N) \rangle + \ldots + e^{-2\pi i k(r-1)/r} U \lvert a^{r} \bmod (N) \rangle \right)
$$

But, 

$$
\lvert a^r \bmod (N) \rangle = \lvert a^0 \bmod (N) \rangle = 1 \bmod (N)
$$. So we get

$$
U \lvert u_k \rangle = \frac{1}{\sqrt{r}} \left(e^{-2\pi i k(0)/r} U \lvert a^0 \bmod (N) \rangle + e^{-2\pi i k(1)/r} U \lvert a^1 \bmod (N) \rangle + \ldots + e^{-2\pi i k(r-1)/r} U \lvert a^{0} \bmod (N) \rangle \right)
$$

Now we multiply the expression on the RHS by $$e^{2\pi i k/r} e^{-2\pi i k/r}$$

$$
U \lvert u_k \rangle = e^{2\pi i k/r} e^{-2\pi i k/r} \frac{1}{\sqrt{r}} \left(e^{-2\pi i k(0)/r} U \lvert a^0 \bmod (N) \rangle + e^{-2\pi i k(1)/r} U \lvert a^1 \bmod (N) \rangle + \ldots + e^{-2\pi i k(r-1)/r} U \lvert a^{0} \bmod (N) \rangle \right)
$$

$$
= e^{2\pi i k/r} \frac{1}{\sqrt{r}} \left(e^{-2\pi i k(1)/r} U \lvert a^0 \bmod (N) \rangle + e^{-2\pi i k(2)/r} U \lvert a^1 \bmod (N) \rangle + \ldots + e^{-2\pi i k(r)/r} U \lvert a^{0} \bmod (N) \rangle \right)
$$

Since, $$e^{-2\pi i k}$$ is a root of unity, 

$$
e^{-2\pi i k (r)/r} = 1
$$

$$
U \lvert u_k \rangle = e^{2\pi i k/r} \frac{1}{\sqrt{r}} \left(e^{-2\pi i k(1)/r} U \lvert a^0 \bmod (N) \rangle + e^{-2\pi i k(2)/r} U \lvert a^1 \bmod (N) \rangle + \ldots + U \lvert a^{0} \bmod (N) \rangle \right)
$$

$$
= e^{2\pi i k/r} \lvert u_k \rangle
$$


Hence, $$U$$ has eigenstate $$u_k$$ with eigenvalues of the form $$e^{2\pi i k/r}$$, which fits naturally into the phase estimation framework. This means that if we can construct the $$u_k$$ state we can use the quantum phase estimation algorithm to get the value of $$k/r$$. Additionally, it turns out that it is far easier to construct the equal superposition of all the $$u_k$$ states because 

$$
\frac{1}{\sqrt{r}} \sum_{s=0}^{r-1} \lvert u_k \rangle = \lvert 1 \bmod N \rangle
$$


To prove this we start with the definition of $$\lvert u_k \rangle$$:

$$
\lvert u_k \rangle = \frac{1}{\sqrt{r}} \sum_{j=0}^{r-1} e^{-\frac{2\pi i k j}{r}} \lvert a^j \bmod N \rangle
$$

Summing over all $$k$$ from 0 to $$r-1$$, we get

$$
\frac{1}{\sqrt{r}} \sum_{k=0}^{r-1} \lvert u_k \rangle = \frac{1}{\sqrt{r}} \sum_{k=0}^{r-1} \frac{1}{\sqrt{r}} \sum_{j=0}^{r-1} e^{-\frac{2\pi i k j}{r}} \lvert a^j \bmod N \rangle = \frac{1}{r} \sum_{j=0}^{r-1} \sum_{k=0}^{r-1} e^{-\frac{2\pi i k j}{r}} \lvert a^j \bmod N \rangle
$$

Now consider the inner sum:

$$
\sum_{k=0}^{r-1} e^{-\frac{2\pi i k j}{r}}
$$

- When $$j=0$$, the sum becomes

$$
\sum_{k=0}^{r-1} 1 = r
$$

- When $$j \neq 0$$, define $$\omega = e^{-\frac{2\pi i j}{r}}$$, then this sum is a geometric series:

$$
\sum_{k=0}^{r-1} \omega^k = \frac{1 - \omega^r}{1 - \omega} = \frac{1 - 1}{1 - \omega} = 0
$$

because $$\omega^r = e^{-2\pi i j} = 1$$.

Thus only the $$j=0$$ term survives, giving

$$
\frac{1}{r} \cdot r \lvert a^0 \bmod N \rangle = \lvert 1 \bmod N \rangle
$$

which is the exact result we wanted to prove!

Now let's specifically get into the quantum subroutine which can be visually represented as

<img 
  src="{{ "./Shor's_algorithm.png" | relative_url }}" 
  class="my-responsive-class"
  style="border: 2px solid black;"
/>

This is the circuit which we use to estimate the eigenvalue $$e^{2\pi i k/r}$$ for $$0\leq k < r$$

Since, $$
\frac{1}{\sqrt{r}} \sum_{s=0}^{r-1} \mid u_k \rangle = \mid 1 \rangle$$ we are calculating the [eigenvector](https://en.wikipedia.org/wiki/Eigenvalues_and_eigenvectors) for all of the $$\mid u_k \rangle$$ states. When measuring we only get the eigenvalue for one $$\mid u_k \rangle$$. We repeat the circuit until we get a nonzero eigenvalue.

From the quantum circuit we get the value $$j \approx 2^{2n} k/r$$ is divided by $$2^{2n}$$ to get a decimal value. Phase estimation returns an integer $$j$$ satisfying
$$
\Bigl\lvert \tfrac{k}{r} - \tfrac{j}{2^{2n}}\Bigr\rvert \;\le\;\tfrac1{2^{2n+1}}\,;
$$
hence we divide by $$2^{2n}$$ to obtain the phase estimate
$$
\frac{j}{2^{2n}}\,.
$$

Note that the $$2^{2n}$$ comes from fact that a register of $$2n$$ qubits spans exactly $$2^{2n}$$ orthogonal basis states, so after the inverse QFT the measured value naturally lies in the range $$0\ldots2^{2n}–1$$ and must be divided by $$2^{2n}$$ to produce the phase estimate.Then using the decimal value we apply the [continued fraction algorithm](https://en.wikipedia.org/wiki/Continued_fraction) to find integers $$b,c$$ where $$b/c$$ gives the best approximation for $$k/r$$ where $$b,c < N$$. If the $$c$$ value that we approximate is odd or $$\gcd(b,c)>1$$, repeat the quantum subroutine. To recover the full order we could run the quantum subroutine an arbitrary amount of times to produce a list of fraction approximations

 $$
\frac{b_1}{c_1},\;\frac{b_2}{c_2},\;\dots,\;\frac{b_m}{c_m},
$$ 

where $$m$$ represents the number of times we ran the subroutine. Each $$c_k$$ will have different contributions because the circuit will most likely measure different possible values of $$j$$. Finally to get the order take 

$$
\mathrm{lcm}(c_1,c_2,\ldots, c_n)
$$

which will be the order of the original $$a$$ with a high probability. However, in practice a single run will most likely be enough.


## The Math Behind the First register

After performing the quantum phase estimation with a first register of 2n qubits (for an $$n$$-bit number $$N$$), we obtain an outcome that approximates the unknown phase $$\frac{k}{r}$$ to high precision. In particular, the measurement yields an integer $$j$$ (with $$0 \le j < 2^{2n}$$) such that $$j/2^{2n}$$ is extremely close to $$k/r$$. The reason we choose 2n qubits for the first register (hence working with $$2^{2n}$$ states) is to achieve this level of precision. In fact, with high probability the following bound holds for the difference between the true value $$k/r$$ and its estimate $$j/2^{2n}$$ after the quantum Fourier transform is measured:

$$\lvert \frac{k}{r} - \frac{j}{2^{2n}} \rvert \;\le\; \frac{1}{2^{2n+1}}\,.$$

This inequality is the mathematical expression of why $$2^{2n}$$ appears in phase estimation: the denominator $$2^{2n}$$ (the size of the Fourier space) determines the accuracy of the approximation. We can rewrite the bound by noting that the phase estimation is accurate to $$k/r$$ within $$2n$$ bits. Note that $$2^{2n} = (2^n)^2 = N^2$$ where $$n = \lceil \log_2 N \rceil$$. Thus,

$$\lvert \frac{k}{r} - \frac{j}{2^{2n}} \rvert \;\le\; \frac{1}{2^{2n+1}} \;=\; \frac{1}{2\,N^2}\,.$$

Moreover, since the unknown denominator (the period) $$r$$ is at most on the order of $$N$$ (indeed we can assume $$r < N$$ for the hardest case), we have $$N^2 \ge r^2$$. This means $$\frac{1}{2N^2} \le \frac{1}{2r^2}$$, so the above implies

$$\lvert \frac{k}{r} - \frac{j}{2^{2n}} \rvert \;\le\; \frac{1}{2\,r^2}\,.$$

Let $$k$$ and $$r$$ be positive $$n$$-bit integers and let $$\phi$$ satisfy  

$$
\left\lvert \phi - \frac{k}{r} \right\rvert \;\le\; \frac{1}{2\,r^{2}} .
$$

where $$\phi$$ specifically represents the phase estimate $$j/2^{2n}$$.

Write $$d = \gcd(k,r)$$ and set  

$$
\frac{k_{0}}{r_{0}}
  \;=\;
\frac{\,k/d\,}{\,r/d\,}.
$$

Then the reduced fraction $$k_{0}/r_{0}$$ appears as a continued fraction approximation in the
continued fraction expansion of $$\phi$$.
Hence, the continued fractions algorithm will recover $$k $$ and $$r$$ (or with their greatest common divisor taken out). 

In other words, the measured fraction $$j/2^{2n}$$ approximates the true ratio $$k/r$$ within $$\frac{1}{2r^2}$$. This error is extremely small: so small that it essentially guarantees $$\frac{k}{r}$$ is the only rational number (with a reasonably bounded denominator) that could fit this approximation. 

**Theorem**: Let $$\phi$$ be a real number, and suppose $$ \frac{s}{r}$$ (in lowest terms) is a rational number satisfying $$ \lvert \frac{s}{r} - \phi\rvert \le \frac{1}{2N^2}$$ for some positive integer $$N$$. Then $$ \frac{s}{r}$$ is the unique rational with denominator less than $$N$$ that lies within $$\frac{1}{2N^2}$$ of $$\phi$$.  In fact, if $$\frac{p}{q}$$ is any other rational satisfying $$ \lvert \frac{p}{q} - \phi\rvert \le \frac{1}{2N^2}$$ with $$q < N$$, it must hold that $$ \frac{p}{q} = \frac{s}{r}$$.

**Proof** : Let $$\frac{p}{q}$$ be another rational number with $$q < N$$ that also satisfies $$\lvert \frac{p}{q} - \phi\rvert \le \frac{1}{2N^2}$$. By the triangle inequality, the difference between $$p/q$$ and $$s/r$$ is bounded by

$$\lvert \frac{p}{q} - \frac{s}{r}\rvert \;\le\; \lvert \frac{p}{q} - \phi\rvert + \lvert \phi - \frac{s}{r}\rvert \;\le\; \frac{1}{2N^2} + \frac{1}{2N^2} \;=\; \frac{1}{N^2}\,.$$

Now express this difference with a common denominator:

$$\lvert \frac{p}{q} - \frac{s}{r}\rvert \;=\; \frac{\lvert p r - s q\rvert}{q\,r}\,.$$

The above inequality then gives $$\lvert p r - s q\rvert/(q r) \le \frac{1}{N^2}$$. Since $$r < N$$ and $$q < N$$, we know $$q,r < N^2$$. It follows that

$$ \lvert p r - s q\rvert \;\le\; \frac{q\,r}{N^2} \;\leq \; 1\,.$$

But $$p r - s q$$ is an integer, so the only way it can have an absolute value less than 1 is if $$p r - s q = 0$$. Hence $$p r = s q$$, which means $$\frac{p}{q} = \frac{s}{r}$$ as rational numbers (even if $$p\neq s$$ or $$q\neq r$$, they represent the same fraction). This proves that $$\frac{s}{r}$$ is the only rational with denominator smaller than $$N$$ satisfying the inequality. Additionally, by the theory of continued fractions each successive continued fraction approximation to $$\phi$$ is strictly closer to $$\phi$$ than any approximation with a smaller denominator. Therefore no fraction with denominator $$<N$$ other than $$s/r$$ can approximate $$\phi$$ this closely.

Now, write $$ \frac{s}{r} = \frac{p_n}{q_n}$$ as a continued fraction approximation of the continued fraction expansion of $$\phi$$, with $$p_n, q_n$$ coprime. (That is, $$p_n/q_n$$ is one of the terms converging to $$\phi$$, so in particular $$q_n = r < N$$.) By the known [error bound](https://en.wikipedia.org/wiki/Approximation_error) for converging terms, we have

$$\lvert \phi - \frac{p_n}{q_n}\rvert \;=\; \frac{1}{z_{n+1}q_n^2 + q_n/z_{n+2}}\,,$$

where $$z_{n+1}, z_{n+2},\dots$$ are the partial quotients of $$\phi$$. (This formula comes from the recursive relation $$q_{n+1} = z_{n+1}q_n + q_{n-1}$$ for converging terms.) Our assumption $$\lvert \frac{s}{r} - \phi\rvert \le \frac{1}{2N^2}$$ then implies

$$\frac{1}{z_{n+1}q_n^2 + \frac{q_n}{z_{n+2}}} \;\le\; \frac{1}{2N^2}\,.$$

Rearranging this inequality yields

$$q_n\!\Big(q_{n+1} + \frac{q_n}{\,z_{n+2}\!}\Big) \;=\; q_n\!\Big(z_{n+1}q_n + q_{n-1}\Big) \;\ge\; 2\,N^2.$$

Since $$q_n < N$$, $$q_{n+1} > q_n$$, and every partial quotient $$z_i \ge 1$$, the above can only hold if $$q_{n+1} > N$$.  In other words, the *next* continued fraction approximation after $$p_n/q_n$$ has a denominator exceeding $$N$$. This means $$p_n/q_n = s/r$$ was in fact the last continued fraction approximation whose denominator was below $$N$$. No other distinct rational with denominator $$< N$$ can approximate $$\phi$$ as closely as $$s/r$$ does, for if there were another, it would contradict the fact that converging terms are the best approximations. $$\square$$

Hence, we have shown that if a measured value $$j/2^{2n}$$ is within $$1/(2N^2)$$ of some rational $$s/r$$ (with $$r < N$$), then $$s/r$$ is uniquely determined — no other rational with a smaller denominator could fit that criterion. In the context of the algorithm, this assures us that the fraction $$\frac{k}{r}$$ will be identified correctly by the [continued fraction algorithm](https://en.wikipedia.org/wiki/Continued_fraction) applied to $$j/2^{2n}$$. 

In practice, one simply computes the continued fraction expansion of $$j/2^{2n}$$ and finds the continued fraction approximation with denominator $$\le N$$; by the above reasoning, that continued fraction approximation must equal $$k/r$$. Thus, by choosing a first quantum register of size $$2n$$ (ensuring the denominator $$2^{2n} = N^2$$ in the phase estimation output), we guarantee that the classical post processing can recover the period $$r$$ from the measured data. 

## Implementing Shor's Algorithm

<img 
  src="{{ "/code_screenshots/code1.png" | relative_url }}" 
  class="my-responsive-class"
/>

We start by importing all the libraries that we will need to implement the algorithm using [IBM qiskit](https://www.ibm.com/quantum/qiskit).

<img 
  src="{{ "/code_screenshots/code2.png" | relative_url }}" 
  class="my-responsive-class"
/>

We start with the controlled modular multiplication gate for
$$U : \lvert x \rangle \mapsto \lvert a x \bmod N \rangle.$$
Here, we build an $$n$$-qubit circuit (where $$n = \lceil \log_2 N \rceil$$) that carries out the map
$$\lvert x \rangle \mapsto \lvert a^{2^j} x \bmod N \rangle$$
for a particular exponent $$2^j$$. Basically the routine computes the binary pattern of each integer $$a^k \bmod N$$ (for $$0 \le k < 2^j$$) and applies the [Pauli X-gates](https://en.wikipedia.org/wiki/Quantum_logic_gate) to flip exactly those target register bits that are 1. 

Then it uses SWAP gates to permute them into the correct positions: ensuring reversibility because the gate is unitary. Finally, we wrap the entire $$n$$-qubit block with .control() to make the multiplication execute only when its phase-estimation qubit is $$\lvert 1 \rangle$$, hence entangling the control register with the eigenphase of $$U$$.

<img 
  src="{{ "/code_screenshots/code3.png" | relative_url }}" 
  class="my-responsive-class"
/>

Now we move on to the qpe_circuit(a, N) function. This function constructs the entire Quantum Phase Estimation circuit for the unitary $$U_{a,N}$$. First, it allocates a control register of $$2n$$ qubits (where $$n = \lceil \log_2 N \rceil$$) and a target register of $$n$$ qubits. Then it applies the Hadamard gates to the control register to create an equal superposition. Additionally, it applies a Pauli X-gate to the least significant qubit of the target register to initialize it to $$\lvert 1 \rangle$$. We start with $$\lvert 1 \rangle$$ to get the sequence $$
\lvert 1 \rangle, \lvert a \bmod N \rangle, \dots
$$ which is the periodic behavior we want to see.

Then we insert a barrier for clarity of code. Then the function iterates over each control-register qubit index $$j$$ and appends the controlled-$$U_{a,N}^{2^j}$$ gate with control on qubit $$j$$ and target on the entire target register. Lastly, it places another barrier.

Finally, it applies the inverse Quantum Fourier Transform. We does this on the control register so that, upon measurement, the resulting bitstring $$j$$ has an estimate of the eigenphase $$2\pi k / r$$ as the fraction $$j / 2^{2n}$$. This is what we later post process to recover the period $$r$$.

<img 
  src="{{ "/code_screenshots/code4.png" | relative_url }}" 
  class="my-responsive-class"
/>

Now we look at the def measure(circ, simulator) function. The measure(circ, simulator) function first adds measurement operations on every qubit so their values are recorded in classical bits. Then we calls Qiskit’s transpiler to convert the circuit into the backend’s supported gate set and qubit layout. 

After running the transpiled circuit, it returns the resulting bitstring (i.e. "01101"), which you can convert into an integer or individual bits. We later use that integer for the continued-fraction and postprocessing steps.

<img 
  src="{{ "/code_screenshots/code5.png" | relative_url }}" 
  class="my-responsive-class"
/>

After all of that quantum computing lets go over perhaps the easiest function: check_N(N). This function finds the values of $$N$$ for which Shor's algorithm isn't needed or simply wont work. We have already discussed these conditions try to recollect them!

First, if $$N \le 3$$, it flags it as “invalid” because its too small to factor. If this case is true it returns (True, None). The second case is if $$N$$ is even, it immediately returns $$(\text{True}, (2, N // 2)),$$ since 2 is a trivial factor. The third case is when $$N$$ is prime in which it uses SymPy’s primality test to see if $$N$$ is prime. If it is it again returns (True, None) because there’s nothing to factor. Finally, it checks for prime power cases by trying exponents $$k$$ from $$\lfloor \log_2 N \rfloor$$ down to 2: if $$N = p^k$$ for some integer $$p$$. If the case is valid it returns $$(\text{True}, (p, k)),$$ giving the trivial factorization. 

If none of these special cases apply, it returns (False, None). This is when we proceed with the full quantum subroutine.

<img 
  src="{{ "/code_screenshots/code6.png" | relative_url }}" 
  class="my-responsive-class"
/>

Now we address the most important function that is the backbone of the quantum subroutine of the algorithm: quantum_period_finding(N, simulator, a). This function uses quantum phase estimation to extract the candidate period $$r$$ for the multiplication-by-$$a$$ modulo $$N$$. 

First, it computes $$n = \lceil \log_2 N \rceil,$$ as usual. Then it enters a loop where it builds the phase estimation circuit for $$U_{a,N}$$. After that it measures the control register to get a binary string, and converts that to an integer. Dividing by $$2^{2n}$$ yields an estimated phase $$\phi = \frac{\text{state_int}}{2^{2n}}.$$

We then call Fraction($$\phi$$).limit_denominator(N) to find the fraction $$\frac{k}{r}$$ whose denominator $$r$$ is at most $$N$$. We showed how we find $$r$$ using the continued fraction algorithm

$$
\frac{k}{r} = a_0 + \cfrac{1}{a_1 + \cfrac{1}{a_2 + \cfrac{1}{\ddots + \cfrac{1}{a_n}}}}
$$

We also proved that we would find the fraction $$k/r$$ using the continued fraction algorithm and that a convergent $$p_m/q_m$$ with $$q_m\leq N$$ would give us the value of $$r$$ with a really high probability.

If this $$r$$ is nontrivial and valid ($$1 < r \le N$$) the function returns the triple $$(r, \text{state_bin}, \phi)$$.
However, if the value of $$r$$ isn't valid then it repeats, ignoring noisy or invalid estimates until a valid period emerges.

<img 
  src="{{ "/code_screenshots/code7.png" | relative_url }}" 
  class="my-responsive-class"
/>

Before we get to the main algorithm's function we discuss the *classical function* we use after we run the quantum subroutine:  postprocess(N, a, r). This function takes the calculated $$r$$ found by phase estimation and tries to turn that into nontrivial factors of $$N$$. 

First, it checks if $$r$$ is odd. If it is odd then there is no integer $$r/2$$ and hence, the function returns None. If it is even then the function calculates $$x = a^{r/2} \bmod N$$
and then calculates the two greatest common divisors:
$$\gcd(x - 1, N)$$ and $$\gcd(x + 1,, N).$$


If both of these GCDs are trivial (i.e. 1 or $$N$$ itself), which means that none of the GCDs were factors, we return None. We do this to signal that we must pick a different base $$a$$ and repeat the period finding subroutine. If one of the factors produced are nontrivial (which means they are a factor) they are returned through the tuple $$(x, x - 1, x + 1)$$ which we use in the main function.

<img 
  src="{{ "/code_screenshots/code8.png" | relative_url }}" 
  class="my-responsive-class"
/>

Finally, we get to the most important function in this implementation, the function that ties it all together: shor_algorithm(N, simulator=None). We begin by checking if $$N$$ is nontrivial: it isn't prime, small, even or a prime power. If any of those cases arise we return an error message because Shor's algorithm isn't optimal for any of those cases.

If $$N$$ is nontrivial we proceed with Shor's Algorithm. Next we set up an AerSimulator and compute $$n = \lceil \log_2 N \rceil$$ to get the necessary number of bits for later definitions. Then we build up a list of integers $$a \in [2,N)$$ which are candidates for the base of the modular exponentiation. They must also satisfy the criteria that $$\gcd(a,N)=1$$. Then we shuffle the list at random. This allows us to iterate through the list and try out random $$a$$'s as bases.

For each $$a$$ we call the quantum_period_finding function, which calls on the quantum phase estimation subroutine from within it. Through this function we get a tentative $$r$$ and then call the postprocess function to turn the period into actual factors. If $$r$$ is odd and none of the GCDs are nontrivial we skip this iteration and keep iterating until we get a nontrivial factor.

Finally, when the algorithm see's a valid result we print out all the relevant data that might help us better understand how the algorithm works. However, in the case that no $$a$$ succeeds we print a failure message and return None.

<img 
  src="{{ "/code_screenshots/code9.png" | relative_url }}" 
  class="my-responsive-class"
/>

This is the last block of code which is the script's entry and starts an AerSimulator. Here, we choose the number we desire to find the nontrivial factors of. 

Finally, let us go over a quick example. Consider $$n=15$$ and $$a=13$$. Before we work the example by hand, we look at what the code outputs:

<img 
  src="{{ "/code_screenshots/output.png" | relative_url }}" 
  class="my-responsive-class"
/>

There is a chance that the code could have given $$r=12$$ due to the nature of the simplified quantum subroutine which is also fine because $$12$$ is a multiple of $$4$$. It is quite easy to classically find the smallest $$r$$ once we have a candidate that works since it's a multiple of the smallest $$r$$.

Now let us see how the algorithm works for $$N=15$$ and $$a=13$$. Note that $$\gcd(a,N)=1$$ so $$a=13$$ is a valid choice. Then we use the quantum subroutine to estimate $$r$$ such that $$13^r \equiv 1 \pmod{15}$$. Using the algorithm we find that $$r=4$$. Then we calculate $$\gcd(13^{4/2}+1,15)$$ and $$\gcd(13^{4/2}-1,15)$$ which are $$\gcd(170,15)$$ and $$\gcd(168,15)$$ respectively. Evaluating the GCDs we get $$\gcd(170,15)=5$$ and $$\gcd(168,15)=3$$ Hence, the factors are $$5$$ and $$3$$ where $$15=5\times 3$$. Hence, we found the factors using Shor's Algorithm!

To view the entire code with the reduced period function refer to [this link](https://github.com/cheesecakeftw/quantum/blob/main/Shor's_Algo.py)

## Limitations of the Algorithm

Although the algorithm runs in polynomial time, which is quite impressive, the degree of the polynomial is really high and for very large $$n$$'s the time complexity scales up really fast. The quantum subroutine in particular for the period finding and the modular exponentiation raise the time complexity harshly. Additionally, the algorithm requires an order of $$O(n^3 \log n)$$ elementary gates and a large number of gates which rise dramatically as $$n$$ increases.

However, the main problem is the current quantum hardware. Quantum noise and [error correction](https://en.wikipedia.org/wiki/Quantum_error_correction) are significant challenges in implementing Shor's Algorithm. Because of the noisy nature of quantum computers they are prone to errors. Additionally, the algorithm itself requires a large number of bits to factorize large numbers which have 100's of bits. Currently most of the best quantum computers have limited qubits and lack the power. Maintaining control over qubits is also another barrier that we must overcome. To implement Shor's Algorithm we must maintain control over qubits to avoid errors.




