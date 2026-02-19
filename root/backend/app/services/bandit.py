import numpy as np


class ThompsonBandit:
    """Beta-Bernoulli Thompson Sampling for discrete GA hyperparameter arms."""

    def __init__(self, num_arms: int):
        if num_arms <= 0:
            raise ValueError("num_arms must be positive")

        self.num_arms = num_arms
        self.alpha = np.ones(num_arms, dtype=float)
        self.beta = np.ones(num_arms, dtype=float)

    def choose_arm(self) -> int:
        samples = np.random.beta(self.alpha, self.beta)
        return int(np.argmax(samples))

    def update(self, arm_index: int, reward: float) -> None:
        if arm_index < 0 or arm_index >= self.num_arms:
            raise ValueError("arm_index out of range")

        clipped = float(np.clip(reward, 0.0, 1.0))
        self.alpha[arm_index] += clipped
        self.beta[arm_index] += 1.0 - clipped


# Shared scheduler bandit instance used by API routes.
scheduler_bandit = ThompsonBandit(num_arms=3)
