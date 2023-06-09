#!/usr/bin/env/ python
"""
q_learner.py
An easy-to-follow script to train, test and evaluate a Q-learning agent on the Mountain Car
problem using the OpenAI Gym. |Praveen Palanisamy
# Chapter 5, Hands-on Intelligent Agents with OpenAI Gym, 2018
Source code: https://github.com/PacktPublishing/Hands-On-Intelligent-Agents-with-OpenAI-Gym/blob/master/ch5/Q_learner_MountainCar.py
"""
import gym
import numpy as np
import matplotlib.pyplot as plt

MAX_NUM_EPISODES = 50000
STEPS_PER_EPISODE = 200 #  This is specific to MountainCar. May change with env
EPSILON_MIN = 0.005
max_num_steps = MAX_NUM_EPISODES * STEPS_PER_EPISODE
EPSILON_DECAY = 500 * EPSILON_MIN / max_num_steps
ALPHA = 0.08  # Learning rate
GAMMA = 0.98  # Discount factor
NUM_DISCRETE_BINS = 30  # Number of bins to Discretize each observation dim
rewards = [] # Variable for "true learning" condition and plotting function


class Q_Learner(object):
    def __init__(self, env):
        self.obs_shape = env.observation_space.shape
        self.obs_high = env.observation_space.high
        self.obs_low = env.observation_space.low
        self.obs_bins = NUM_DISCRETE_BINS  # Number of bins to Discretize each observation dim
        self.bin_width = (self.obs_high - self.obs_low) / self.obs_bins
        self.action_shape = env.action_space.n
        # Create a multi-dimensional array (aka. Table) to represent the
        # Q-values
        self.Q = np.zeros((self.obs_bins + 1, self.obs_bins + 1, self.action_shape))  # (51 x 51 x 3)
        self.alpha = ALPHA  # Learning rate
        self.gamma = GAMMA  # Discount factor
        self.epsilon = 1.0

    def discretize(self, obs):
        return tuple(((obs - self.obs_low) / self.bin_width).astype(int))

    def get_action(self, obs):
        discretized_obs = self.discretize(obs)
        # Epsilon-Greedy action selection
        if self.epsilon > EPSILON_MIN:
            self.epsilon -= EPSILON_DECAY

        # Takes exploratory action with probability of epsilon
        # Takes a greedy action with probability of 1 - epsilon
        # Goal: Ensure all action spaces are explored
        if np.random.random() < (1 - self.epsilon):
            return np.argmax(self.Q[discretized_obs])
        else:  # Choose a random action
            return np.random.choice([a for a in range(self.action_shape)])

    def learn(self, obs, action, reward, next_obs, next_action):
        discretized_obs = self.discretize(obs)
        discretized_next_obs = self.discretize(next_obs)

        # Change the nature of Q-Learning which maximizes the possible reward
        # Replace with an on-policy where it will be guided by a policy
        td_target = reward + self.gamma * self.Q[discretized_next_obs][next_action]
        td_error = td_target - self.Q[discretized_obs][action]
        self.Q[discretized_obs][action] += self.alpha * td_error

def train(agent, env):
    best_reward = -float('inf')
    rewards_streak = 0

    for episode in range(MAX_NUM_EPISODES):
        done = False
        obs, _ = env.reset()
        total_reward = 0.0
        while not done:
            action = agent.get_action(obs)
            next_obs, reward, done, info, _ = env.step(action)

            # Implementation of on-policy algorithm
            # Obtain the next suitable action using the next observation rather than taking action with highest reward
            next_action = agent.get_action(next_obs)
            agent.learn(obs, action, reward, next_obs, next_action)
            obs = next_obs
            total_reward += reward
        if total_reward > best_reward:
            best_reward = total_reward
        print("Episode#:{} reward:{} best_reward:{} eps:{}".format(episode,
                                     total_reward, best_reward, agent.epsilon))
   
        # Added " true learning" condition
        # Checks whether the reward is unchanged after n number of iterations
        rewards.append(best_reward)
        previous_episode = episode - 1
        if (episode != 0) and ((rewards[episode]) == (rewards[previous_episode])):
            rewards_streak += 1
            if (rewards_streak == 10000):
                print("Best Reward: {}".format(best_reward))
                break
        elif ((rewards[episode]) != (rewards[previous_episode])):
            rewards_streak = 0

    # Plotting function
    plt.plot(range(episode + 1), rewards)
    plt.xlabel("Number of Episodes")
    plt.ylabel("Rewards")
    plt.show()

    # Return the trained policy
    return np.argmax(agent.Q, axis=2)


if __name__ == "__main__":
    env = gym.make('MountainCar-v0')
    agent = Q_Learner(env)
    learned_policy = train(agent, env)

    env.close()




    
