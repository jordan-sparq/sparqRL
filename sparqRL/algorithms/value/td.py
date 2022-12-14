import numpy as np
from sparqRL.utils.table import table
from sparqRL.environment.environment import discrete_environment


class QLearning:
    """
    Q-Learning algorithm.
    "Learning from Delayed Rewards". Watkins C.J.C.H.. 1989.
    """

    def __init__(self, environment: discrete_environment, initial_value: float):
        Q = table(shape=environment.state_space + environment.action_space, initial_value=initial_value)
        self.Q = Q
        
    def _update(self,
                state: tuple,
                action: tuple,
                reward: float,
                next_state: tuple,
                absorbing: bool,
                gamma: float,
                alpha: float,
                ):
        """
        update function for q learning
        """
        state_action = state + action
        #print(self.Q[state_action])
        q_current = self.Q.__getitem__(state_action)

        # get maximum of next state if gamma != 0
        if gamma != 0:
            q_next_dense = self.Q.__getitem__(next_state).todense()
            q_next = np.max(q_next_dense) if not absorbing else 0.

            self.Q[state_action] = q_current + alpha * (
                reward + gamma * q_next - q_current)
            #print(self.Q[state_action])

        else:
            self.Q[state_action] = q_current + alpha * (reward - q_current)
            #print(self.Q[state_action])
