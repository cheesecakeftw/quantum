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

In number theory, Euler's totient function ($$\varphi$$) counts the the number of positive integers $$k \leq n$$ such that $$\gcd(k,n) = 1$$

#### [The Multiplicative Group $$(\mathbb{Z}/N\mathbb{Z})^{\times}$$](https://en.wikipedia.org/wiki/Multiplicative_group_of_integers_modulo_n)

In modular arithmetic, the integers coprime (relatively prime) to n from the set { $$0 , 1 , \ldots , n − 1 $$} of $$n$$ non-negative integers form a group under multiplication modulo $$n$$, called the multiplicative group of integers modulo $$n$$ or denoted by the ring $$(\mathbb{Z}/N\mathbb{Z})^{\times}$$. 

Note, that the [order](https://en.wikipedia.org/wiki/Order_(group_theory)) of this group is defined by the earlier stated Euler's Totient Function ($$\varphi(n)$$). This means that in any finite order group $$G$$, the order of an element $$g \in G$$ is the smallest integer $$r$$ such that $$g^r=e$$, where $$e$$ denotes the identity element of the group. 

Additionally, for some $$a$$ in the group, the multiplicative inverse of $$a$$ modulo $$n$$ is given by $$x \in Z$$ satisfying $$ax \equiv 1 \pmod{n}$$. It exists precisely when $$\gcd(a,n)=1$$ (a is coprime to n) and by [Bezout's Lemma](https://en.wikipedia.org/wiki/B%C3%A9zout%27s_lemma) which states that there are $$x,y \in Z$$, such that $$ax+ny=0$$, we can easily show x is coprime to n. It follows that the multiplicative inverse belongs to the group.

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

We notice a really cool pattern here! Notice that 1, 2, 4, 8, 7, 5 are repeating. Hence, we can say that the order of 2 modulo 9 is 6. 


This is where the quantum part comes in! We use the quantum subroutine to find $$r$$. Quantum computers speed up this part of the algorithm exponentially making this algorithm much more efficient than classical methods.

We rewrite the definition of multiplicative order to get

$$N \mid a^r-1$$

Factoring we get

$$N \mid (a^{r/2}-1)(a^{r/2}+1)$$

Here, we must note that the algorithm doesn't work for an odd $$r$$ because the power $$\frac{r}{2}$$ must be an integer. This would mean that the algorithm would have to start again using another value of $$a$$.

Hence, based on the previous criteria we assume that $$r$$ is an even integer. Let's claim that $$N \mid (a^{r/2}-1)$$. But then, $$a^{r/2} \equiv 1 \pmod{N}$$, which would imply that there exists a smaller multiplicative order than $$r$$, since $$r/2 <r$$. But, we already know that $$r$$ is the smallest possible multiplicative order for $$a$$. Hence, the claim that $$N \mid (a^{r/2}-1)$$ can't be true.

This leaves us with two cases. Either $$N \mid (a^{r/2}+1)$$ or not. If $$N$$ doesn't divide $$a^{r/2}+1$$ then we compute $$m=\gcd(N,a^{r/2}-1)$$. If $$m=1$$ then $$N\mid a^{r/2}+1$$ was true, in which case we can't find a nontrivial factor of $$N$$ from $$a$$ and we must restart with a new $$a$$. However, if $$m \neq 1$$ then we have found a nontrivial factor of $$N$$, where $$P=m$$ and $$Q=N/m$$. We could have also computed $$\gcd(N, a^{r/2} + 1)$$ since it might produce a nontrivial factor in cases where $$\gcd(N, a^{r/2} - 1)$$ does not, and it will be trivial precisely when $$N \mid a^{r/2} + 1$$.

The probability of finding an $$a$$ that works is atleast $$\frac{1}{2}$$. Hence, we will always be able to find an $$a$$ that works after multiple attempts. But why is the bound $$\frac{1}{2}$$?



Now that we have gone over the general logic of the algorithm let us move on to the quantum computing implementation.

The main goal of the quantum subroutine is to find the order $$r$$ of $$a$$ modulo $$N$$ as described previously. Basically we need to find the smallest $$r$$ such that for $$\gcd(a,N)=1$$ where $$1<a<N$$ we have $$a^r \equiv \pmod{1}$$. 


