# valueIterationAgents.py
# -----------------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


# valueIterationAgents.py
# -----------------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


import mdp, util

from learningAgents import ValueEstimationAgent
import collections
import operator

class ValueIterationAgent(ValueEstimationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A ValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs value iteration
        for a given number of iterations using the supplied
        discount factor.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 100):
        """
          Your value iteration agent should take an mdp on
          construction, run the indicated number of iterations
          and then act according to the resulting policy.

          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state, action, nextState)
              mdp.isTerminal(state)
        """
        self.mdp = mdp
        self.discount = discount
        self.iterations = iterations
        self.values = util.Counter() # A Counter is a dict with default 0
        self.runValueIteration()

    def runValueIteration(self):
        # Write value iteration code here

        "*** YOUR CODE HERE ***"
        yy = util.Counter()


        for xx in range(self.iterations):
            yy = util.Counter()

            for s in self.mdp.getStates():
                if self.mdp.isTerminal(s):
                    continue
                # p = mdp.getTransitionStatesAndProbs(state, action)
                # c = mdp.getPossibleActions(state)
                ww = self.computeActionFromValues(s)
                qq = self.computeQValueFromValues(s, ww)

                yy[s] = qq

            self.values = yy
            ww = self.computeActionFromValues(s)
            qq = self.computeQValueFromValues(s, ww)


    def getValue(self, state):
        """
          Return the value of the state (computed in __init__).

        """
        return self.values[state]


    def computeQValueFromValues(self, state, action):
        """
          Compute the Q-value of action in state from the
          value function stored in self.values.

        """
        "*** YOUR CODE HERE ***"
        # util.raiseNotDefined()
        trx = 0
        # p = mdp.getTransitionStatesAndProbs(state, action)
        trx = self.mdp.getTransitionStatesAndProbs(state, 
                                                   action)
        xx = 0

        qq = sum(
            # SUM
            aa * (self.mdp.getReward(state, 
                                     action, ii) + 
                  self.discount * self.values[ii])
            # THE LOOP
            for ii, aa in trx
        )

        # Result
        return qq

    def computeActionFromValues(self, state):
        """
          The policy is the best action in the given state
          according to the values currently stored in self.values.

          You may break ties any way you see fit.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return None.

        """
        "*** YOUR CODE HERE ***"
        # util.raiseNotDefined()
        PPA = 0
        # a = mdp.isTerminal(state)
        if self.mdp.isTerminal(state):
            return None

        PPA = self.mdp.getPossibleActions(state)

        aQ = [(i, self.computeQValueFromValues(state, 
                                               i)) 
              for i in PPA]


        RES = max(aQ, key =
                  lambda x: x[1])[0]

        # Result
        return RES

    def getPolicy(self, state):
        return self.computeActionFromValues(state)

    def getAction(self, state):
        "Returns the policy at the state (no exploration)."
        return self.computeActionFromValues(state)

    def getQValue(self, state, action):
        return self.computeQValueFromValues(state, action)

class AsynchronousValueIterationAgent(ValueIterationAgent):
    """
        * Please read learningAgents.py before reading this.*

        An AsynchronousValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs cyclic value iteration
        for a given number of iterations using the supplied
        discount factor.

    """
    def __init__(self, mdp, discount = 0.9, iterations = 1000):
        """
          Your cyclic value iteration agent should take an mdp on
          construction, run the indicated number of iterations,
          and then act according to the resulting policy. Each iteration
          updates the value of only one state, which cycles through
          the states list. If the chosen state is terminal, nothing
          happens in that iteration.

          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state)
              mdp.isTerminal(state)

        """
        ValueIterationAgent.__init__(self, mdp, discount, iterations)

    def runValueIteration(self):
        "*** YOUR CODE HERE ***"
        # util.raiseNotDefined()

        #s = mdp.getStates()
        #c = mdp.getPossibleActions(state)
        #p = mdp.getTransitionStatesAndProbs(state, action)
        #b = mdp.getReward(state)
        #a = mdp.isTerminal(state)
        xx = 0
        s = self.mdp.getStates()
        mm = float('-inf')

        xx = len(s)

        for i in s:
            self.values[i] = 0.00

        for i in range(self.iterations):
            xx = len(s)

            i = s[i % xx]

            if self.mdp.isTerminal(i):
                continue

            mm = float('-inf')
            for j in self.mdp.getPossibleActions(i):
                s = self.mdp.getStates()

                final = self.computeQValueFromValues(i, j)
                mm = max(mm, final)

            # Res
            final = 0
            j = 0

            self.values[i] = mm


class PrioritizedSweepingValueIterationAgent(AsynchronousValueIterationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A PrioritizedSweepingValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs prioritized sweeping value iteration
        for a given number of iterations using the supplied parameters.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 100, theta = 1e-5):
        """
          Your prioritized sweeping value iteration agent should take an mdp on
          construction, run the indicated number of iterations,
          and then act according to the resulting policy.
        """
        self.theta = theta
        ValueIterationAgent.__init__(self, mdp, discount, iterations)

    def runValueIteration(self):
        "*** YOUR CODE HERE ***"

