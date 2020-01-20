Chinese Poker(DouDiZhu)
========================

Introduction
------------------------

In this project, we want to realize a completely auto-intelligent agent, which can
find a valid card type and put reasonable cards in DouDiZhu.
At first period, we just build a complete project structure roughly, and
special scheduler will describe as follows.
if you are interested in the production using `Machine Learning` include 
`DeepLearning`, `Reinforcement Learning`, we hope that you can join us.

Scheduler
------------------------

1. In 2019, we try to build a project structure roughly
2. We did some attempts in version `pre_*` series
3. Under dirctory `Supervised-Model`, we did some attempts by using CNN model according to a paper
4. Under directory `Rule-Based`, we try to realize this game by rule-based strategy
5. In 2020, we refactor these codes based on previous works and tag version `v1.0`

v1.0
-------------------------

1. Catalog
    - defining the card structure and choosing valid card type
    - using Deep Q-learning algorithm to choose the best action from candidate actions