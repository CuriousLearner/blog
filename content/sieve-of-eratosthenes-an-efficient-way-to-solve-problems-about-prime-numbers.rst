Sieve of Eratosthenes - An efficient way to solve problems about Prime numbers
##############################################################################
:date: 2015-02-27 13:33
:author: Sanyam Khurana
:category: Experience
:slug: sieve-of-eratosthenes-an-efficient-way-to-solve-problems-about-prime-numbers

Long ago, I think 2-3 years ago, I came to know about Project Euler
Problems, I made an account, solved 1 or 2 problems, and then never
tried them.

Now, I decided to give them a try again. I was solving Project Euler 10
Problem which states that:

    The sum of the primes below 10 is 2 + 3 + 5 + 7 = 17.

    Find the sum of all the primes below two million.

Now, I wrote this Python code for the same. I know it's not optimized.
Not at all. Why, you'll come to know shortly.

| ``http://paste.fedoraproject.org/191242/``
|  I tried to run this first for 10 to get an answer 17, I was happy. So, I changed it to 2 million and ran the code. It ran for some time, but no output, so I decided to keep printing the number on which it is executing at each step. I ran it again. After around 2 hours, I noticed it reached around 0.2 million.

I knew that is terrible and it would not solve this way. So, I
researched about the problem and came to know about **Sieve of
Eratosthenes**\ through this question on StackOverflow:

http://stackoverflow.com/questions/9233408/project-euler-10-why-the-first-python-code-runs-much-faster-than-the-second-on

I jumped over to Wikipedia page and understood what this algorithm was
actually all about, and I knew, my algo was taking time because it would
evaluate a number to be prime or not for each and every number from 1 to
2 million which is processor intensive and redundant.

**What does Sieve of Eratosthenes does?**

First it creates a list of numbers on which we want to carry some prime
number operation for which we want to know if they are prime or not. It
takes a number for example 2, calculate if it's prime, and then remove
all the elements which are multiple of 2.

Then it jumps to next number, say 3, which is prime, and then removes
all it's multiples.

 

While I was trying to do the calculation of whether a number is prime or
not for each and every number till 2 million, this algo would calculate
the prime number property for very low amount of numbers. Hence,
efficient.

I have solved 15 problems on Project Euler till now :)

|  
|  |image0|
|   

.. |image0| image:: https://projecteuler.net/profile/CuriousLearner.png
