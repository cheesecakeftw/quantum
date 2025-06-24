---
layout: post
title: The Math Behind Shor's Algorithm
---
<script src="https://cdn.mathjax.org/mathjax/latest/MathJax.js?config=TeX-AMS-MML_HTMLorMML" type="text/javascript"></script>


## Introduction:

[Shor's Algorithm](https://en.wikipedia.org/wiki/Shor%27s_algorithm) is an algorithm used to find the prime factors of an integer. But why is this algorithm so famous in quantum computing? This algorithm has compelling applications such as cracking the most used encryption protocol, [RSA](https://en.wikipedia.org/wiki/RSA_cryptosystem), which functions on the assumption that the prime factors of an integer can't be found. This algorithm has evidence of super-polynomial speedup compared to the best known classical algorithms. However, as of right now our quantum computers aren't advanced enough to factor numbers of practical significance because of a lack of qubits. Also, the noise in quantum circuits requires additional qubits for quantum error correction adding to the impracticality of the algorithm right now. 

Before we get into the math behind the algorithm, lets discuss the time complexity of Shor's Algorithm. To factor an integer $$N$$ on a quantum computer, Shor's algorithm runs in polynomial time. To be specific, it takes quantum gates of order $$O((\log N)^2 (\log \log N)(\log \log \log N))$$ using fast multiplication. However, we can achieve  $$O((\log N)^2 (\log \log N))$$ using the asymptomatically fastest multiplication algorithm. These are both significantly faster time complexities than the most efficient classical factoring algorithm, the general number sieve, which works in exponential time $$ O( e^{1.9 (\log N)^{1/3} (\log \log N)^{2/3}})$$.

It is important to note that this algorithm involves both classical and quantum parts. Specifically, the quantum speedup happens from the order-finding problem which we will explain and go into more detail about later.

The goal of the algorithm, in mathematical terms, is to find primes $$P$$ and $$Q$$ for some $$N$$, such that $$N=PQ$$. For this algorithm to work we assume that $$N$$ isn't even, and $$N$$ isn't a prime or a prime power. We can check if $$N$$ is prime or not using various [primality tests](https://en.wikipedia.org/wiki/Primality_test#Complexity), including the infamous Fermat's little theorem.

If $$N$$ is even then we can use the trivial case $$P=2$$, then $$Q=N/2$$ which is straightforward.

If $$N$$ is a [prime power](https://en.wikipedia.org/wiki/Prime_power), we can check for every $$k$$ such that $$2 \leq k \leq \log_3 N$$ if $$N^{\frac{1}{k}}$$ is an integer. If that happens to be the case, then $$P=N^{\frac{1}{k}}$$ and $$Q=N^{\frac{k-1}{k}}$$ which is again a trivial case.

If none of these easy cases produce a nontrivial factor of $$N$$ then we proceed to use Shor's Algorithm. Before we do that let us review some important mathematical concepts that we need to be familiar with.

## Mathematical Prerequisites:

#### [Basic Modular Arithmetic](https://en.wikipedia.org/wiki/Modular_arithmetic)

For some $$a,b,r,N \in Z$$, we write $$a=b \times N +r$$. This can be written as $$a \equiv r \pmod{N}. $$ This can also be written as $$N \mid  (a-r)$$ which reads as "$$N$$ divides $$a-r$$".

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

Firstly lets define a gate $$U_{a,N} \mid x \rangle = \mid x a \mod(N)\rangle $$. This gate is a quantum phase estimation on the unitary operator. Below, you can see clearly how the [eigenstate](https://en.wikipedia.org/wiki/Eigenvalues_and_eigenvectors) of $$U$$ might look like. QPE extracts the eigenvalue phase of a unitary operator.

If we apply this gate multiple times we get $$U^0_{a,N} \mid 1 \rangle = \mid 1 \mod(N)\rangle $$, $$U^1_{a,N} \mid 1 \rangle = \mid a \mod(N)\rangle $$, $$U^2_{a,N} \mid 1\rangle = \mid a^2 \mod(N)\rangle $$, $$U^3_{a,N} \mid 1 \rangle = \mid a^3 \mod(N)\rangle $$ $$\ldots$$ $$U^r_{a,N} \mid 1 \rangle = \mid a^r \mod(N)\rangle $$. Note that at the final stage $$U^r_{a,N} \mid 1 \rangle = \mid a^r \mod(N)\rangle = \mid 1 \mod(N) \rangle$$. For the rest of our discussion we define $$U_{a,N}$$ as $$U$$ for clarity.

Now consider the state

$$
\mid u_k \rangle = \frac{1}{\sqrt{r}} \left(e^{-2\pi i k(0)/r} \mid a^0 \bmod (N) \rangle + e^{-2\pi i k(1)/r} \mid a^1 \bmod (N) \rangle + \ldots + e^{-2\pi i k(r-1)/r} \mid a^{r} \bmod (N) \rangle \right)
$$ 
 
If we apply the $$U$$ gate we get

$$
U \mid u_k \rangle = \frac{1}{\sqrt{r}} \left(e^{-2\pi i k(0)/r} U \mid a^0 \bmod (N) \rangle + e^{-2\pi i k(1)/r} U \mid a^1 \bmod (N) \rangle + \ldots + e^{-2\pi i k(r-1)/r} U \mid a^{r} \bmod (N) \rangle \right)
$$

But, 

$$
\mid a^r \bmod (N) \rangle = \mid a^0 \bmod (N) \rangle = 1 \bmod (N)
$$. So we get

$$
U \mid u_k \rangle = \frac{1}{\sqrt{r}} \left(e^{-2\pi i k(0)/r} U \mid a^0 \bmod (N) \rangle + e^{-2\pi i k(1)/r} U \mid a^1 \bmod (N) \rangle + \ldots + e^{-2\pi i k(r-1)/r} U \mid a^{0} \bmod (N) \rangle \right)
$$

Now we multiply the expression on the RHS by $$e^{2\pi i k/r} e^{-2\pi i k/r}$$

$$
U \mid u_k \rangle = e^{2\pi i k/r} e^{-2\pi i k/r} \frac{1}{\sqrt{r}} \left(e^{-2\pi i k(0)/r} U \mid a^0 \bmod (N) \rangle + e^{-2\pi i k(1)/r} U \mid a^1 \bmod (N) \rangle + \ldots + e^{-2\pi i k(r-1)/r} U \mid a^{0} \bmod (N) \rangle \right)
$$

$$
= e^{2\pi i k/r} \frac{1}{\sqrt{r}} \left(e^{-2\pi i k(1)/r} U \mid a^0 \bmod (N) \rangle + e^{-2\pi i k(2)/r} U \mid a^1 \bmod (N) \rangle + \ldots + e^{-2\pi i k(r)/r} U \mid a^{0} \bmod (N) \rangle \right)
$$

Since, $$e^{-2\pi i k}$$ is a root of unity, 

$$
e^{-2\pi i k (r)/r} = 1
$$

$$
U \mid u_k \rangle = e^{2\pi i k/r} \frac{1}{\sqrt{r}} \left(e^{-2\pi i k(1)/r} U \mid a^0 \bmod (N) \rangle + e^{-2\pi i k(2)/r} U \mid a^1 \bmod (N) \rangle + \ldots + U \mid a^{0} \bmod (N) \rangle \right)
$$

$$
= e^{2\pi i k/r} \mid u_k \rangle
$$


Hence, $$U$$ has eigenstate $$u_k$$ with eigenvalues of the form $$e^{2\pi i k/r}$$, which fits naturally into the phase estimation framework. This means that if we can construct the $$u_k$$ state we can use the quantum phase estimation algorithm to get the value of $$k/r$$. Additionally, it turns out that it is far easier to construct the equal superposition of all the $$u_k$$ states because 

$$
\frac{1}{\sqrt{r}} \sum_{s=0}^{r-1} \mid u_k \rangle = \mid 1 \bmod N \rangle
$$


To prove this we start with the definition of $$\mid u_k \rangle$$:

$$
\mid u_k \rangle = \frac{1}{\sqrt{r}} \sum_{j=0}^{r-1} e^{-\frac{2\pi i k j}{r}} \mid a^j \bmod N \rangle
$$

Summing over all $$k$$ from 0 to $$r-1$$, we get

$$
\frac{1}{\sqrt{r}} \sum_{k=0}^{r-1} \mid u_k \rangle = \frac{1}{\sqrt{r}} \sum_{k=0}^{r-1} \frac{1}{\sqrt{r}} \sum_{j=0}^{r-1} e^{-\frac{2\pi i k j}{r}} \mid a^j \bmod N \rangle = \frac{1}{r} \sum_{j=0}^{r-1} \sum_{k=0}^{r-1} e^{-\frac{2\pi i k j}{r}} \mid a^j \bmod N \rangle
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
\frac{1}{r} \cdot r \mid a^0 \bmod N \rangle = \mid 1 \bmod N \rangle
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
Equivalently, running the continued-fraction algorithm on $$\phi$$
recovers exactly the pair $$(k_{0},\,r_{0})$$.

In other words, the measured fraction $$j/2^{2n}$$ approximates the true ratio $$k/r$$ within $$\frac{1}{2r^2}$$. This error is extremely small – so small that it essentially guarantees $$\frac{k}{r}$$ is the only rational number (with a reasonably bounded denominator) that could fit this approximation. 

**Theorem**: Let $$\phi$$ be a real number, and suppose $$ \frac{s}{r}$$ (in lowest terms) is a rational number satisfying $$ \lvert \frac{s}{r} - \phi\rvert \le \frac{1}{2N^2}$$ for some positive integer $$N$$. Then $$ \frac{s}{r}$$ is the unique rational with denominator less than $$N$$ that lies within $$\frac{1}{2N^2}$$ of $$\phi$$.  In fact, if $$\frac{p}{q}$$ is any other rational satisfying $$ \lvert \frac{p}{q} - \phi\rvert \le \frac{1}{2N^2}$$ with $$q < N$$, it must hold that $$ \frac{p}{q} = \frac{s}{r}$$.

**Proof** :  Let $$\frac{p}{q}$$ be another rational number with $$q < N$$ that also satisfies $$\lvert \frac{p}{q} - \phi\rvert \le \frac{1}{2N^2}$$. By the triangle inequality, the difference between $$p/q$$ and $$s/r$$ is bounded by

$$\lvert \frac{p}{q} - \frac{s}{r}\rvert \;\le\; \lvert \frac{p}{q} - \phi\rvert + \lvert \phi - \frac{s}{r}\rvert \;\le\; \frac{1}{2N^2} + \frac{1}{2N^2} \;=\; \frac{1}{N^2}\,.$$

Now express this difference with a common denominator:

$$\lvert \frac{p}{q} - \frac{s}{r}\rvert \;=\; \frac{\lvert p r - s q\rvert}{q\,r}\,.$$

The above inequality then gives $$\lvert p r - s q\rvert/(q r) \le \frac{1}{N^2}$$.  Since $$r < N$$ and $$q < N$$, we know $$q,r < N^2$$. It follows that

$$ \lvert p r - s q\rvert \;\le\; \frac{q\,r}{N^2} \;\leq \; 1\,.$$

But $$p r - s q$$ is an integer, so the only way it can have an absolute value less than 1 is if $$p r - s q = 0$$.  Hence $$p r = s q$$, which means $$\frac{p}{q} = \frac{s}{r}$$ as rational numbers (even if $$p\neq s$$ or $$q\neq r$$, they represent the same fraction). This proves that $$\frac{s}{r}$$ is the only rational with denominator smaller than $$N$$ satisfying the inequality.  Moreover, by the theory of continued fractions, each successive continued fraction approximation to $$\phi$$ is strictly closer to $$\phi$$ than any approximation with a smaller denominator.  Therefore no fraction with denominator $$<N$$ other than $$s/r$$ can approximate $$\phi$$ this closely.

Now, write $$ \frac{s}{r} = \frac{p_n}{q_n}$$ as a continued fraction approximation of the continued fraction expansion of $$\phi$$, with $$p_n, q_n$$ coprime. (That is, $$p_n/q_n$$ is one of the terms converging to $$\phi$$, so in particular $$q_n = r < N$$.) By the known error bound for converging terms, we have

$$\lvert \phi - \frac{p_n}{q_n}\rvert \;=\; \frac{1}{z_{n+1}q_n^2 + q_n/z_{n+2}}\,,$$

where $$z_{n+1}, z_{n+2},\dots$$ are the partial quotients of $$\phi$$. (This formula comes from the recursive relation $$q_{n+1} = z_{n+1}q_n + q_{n-1}$$ for converging terms.) Our assumption $$\lvert \frac{s}{r} - \phi\rvert \le \frac{1}{2N^2}$$ then implies

$$\frac{1}{z_{n+1}q_n^2 + \frac{q_n}{z_{n+2}}} \;\le\; \frac{1}{2N^2}\,.$$

Rearranging this inequality yields

$$q_n\!\Big(q_{n+1} + \frac{q_n}{\,z_{n+2}\!}\Big) \;=\; q_n\!\Big(z_{n+1}q_n + q_{n-1}\Big) \;\ge\; 2\,N^2.$$

Since $$q_n < N$$, $$q_{n+1} > q_n$$, and every partial quotient $$z_i \ge 1$$, the above can only hold if $$q_{n+1} > N$$.  In other words, the *next* continued fraction approximation after $$p_n/q_n$$ has a denominator exceeding $$N$$. This means $$p_n/q_n = s/r$$ was in fact the last continued fraction approximation whose denominator was below $$N$$. No other distinct rational with denominator $$< N$$ can approximate $$\phi$$ as closely as $$s/r$$ does, for if there were another, it would contradict the fact that converging terms are the best approximations. $$\square$$

Hence, we have shown that if a measured value $$j/2^{2n}$$ is within $$1/(2N^2)$$ of some rational $$s/r$$ (with $$r < N$$), then $$s/r$$ is uniquely determined — no other rational with a smaller denominator could fit that criterion. In the context of the algorithm, this assures us that the fraction $$\frac{k}{r}$$ will be identified correctly by the continued fraction algorithm applied to $$j/2^{2n}$$. In practice, one simply computes the continued fraction expansion of $$j/2^{2n}$$ and finds the continued fraction approximation with denominator $$\le N$$; by the above reasoning, that continued fraction approximation must equal $$k/r$$. Thus, by choosing a first quantum register of size $$2n$$ (ensuring the denominator $$2^{2n} = N^2$$ in the phase estimation output), we guarantee that the classical post processing can reliably recover the period $$r$$ from the measured data. This is the mathematical insight behind the first quantum register’s role in Shor’s algorithm, completing our understanding of how the algorithm succeeds in finding the period. 

## Implementing Shor's Algorithm

We first import all the libraries that we will need to implement the algorithm using [IBM qiskit](https://www.ibm.com/quantum/qiskit).

{% highlight ruby %}
from qiskit import QuantumCircuit, transpile
from qiskit.circuit.library import QFT
from qiskit_aer import AerSimulator
from fractions import Fraction
import random
import sympy
import math
{% endhighlight %}

We start with the controlled modular multiplication class for $$U(x)=a^x \mod N$$.

