import numpy as np
import pandas as pd
import time

np.random.seed(2)   # reproducible

N_STATES = 6    # the length of the 1 dimensional world
ACTIONS = ["left", "right"]     # available actions
EPSILON = 0.9   # greedy police
ALPHA = 0.1     # learning rate
LAMBDA = 0.9    # discount factor
MAX_EPISODES = 13   # maximum episode
FRESH_TIME = 0.3    # fresh time for one move


def build_q_table(n_states, actions):
    table = pd.DataFrame(
        np.zeros((n_states, len(actions))),     # q_table initial values
        columns=actions,    # actions's name
    )
    return table


def choose_action(state, q_table):
    state_actions = q_table.iloc[state, :]
    if np.random.uniform() > EPSILON or state_actions.all() == 0:
        action_name = np.random.choice(ACTIONS)
    else:
        action_name = state_actions.argmax()
    return action_name


def get_env_feedback(S, A):
    if A == 'right':
        if S == N_STATES - 2:   # terminate
            S_ = 'terminal'
            R = 1
        else:
            S_ = S + 1
            R = 0
    else:
        R = 0
        if S == 0:
            S_ = S      # reach the wall
        else:
            S_ = S - 1
    return S_, R


def update_env(S, episode, step_counter):
    # This is how environment be updated
    env_list = ['=']*(N_STATES-1) + ['T']   # '---------T' our environment
    if S == 'terminal':
        interaction = 'Episode %s: total_steps = %s' % (episode+1, step_counter)
        print('\r{}'.format(interaction), end='')
        time.sleep(2)
        print('\r                                ', end='')
    else:
        env_list[S] = '0'
        interaction = ''.join(env_list)
        print('\r{}'.format(interaction), end='')
        time.sleep(FRESH_TIME)


def rl():
    # main part of RL loop
    q_table = build_q_table(N_STATES, ACTIONS)
    for episode in range(MAX_EPISODES):
        step_counter = 0
        S = 0
        is_terminated = False
        update_env(S, episode, step_counter)
        while not is_terminated:
            A = choose_action(S, q_table)
            S_, R = get_env_feedback(S, A)
            q_predict = q_table.ix[S, A]    # predicted value
            if S_ != 'terminal':
                q_target = R + LAMBDA * q_table.iloc[S_, :].max()   # true value
            else:
                q_target = R
                is_terminated = True

            q_table.ix[S, A] += ALPHA * (q_target - q_predict)      # update
            S = S_

            update_env(S, episode, step_counter)
            step_counter += 1
    return q_table


if __name__ == "__main__":
    q_table = rl()
    print("\r\nQ-table:\n")
    print(q_table)




