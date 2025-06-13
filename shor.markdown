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

If none of these easy cases produce a nontrivial factor of $N$ then we proceed to use Shor's Algorithm. Before we do that let us review some important mathematical concepts that we need to be familiar with.

### Mathematical Prerequisites

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

#### [The Multiplicative Group $$(\mathbb{Z}/N\mathbb{Z})$$](https://people.reed.edu/~jerry/361/lectures/lec07.pdf)


