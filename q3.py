import numpy as np

PROBABILITY_A = {"yes": 0.8, "no": 0.2}
PROBABILITY_C = {"yes": 0.5, "no": 0.5}
PROBABILITY_GIVEN_A_C = {
    ("yes", "yes"): {"Good": 0.9, "OK": 0.1},
    ("yes", "no"): {"Good": 0.7, "OK": 0.3},
    ("no", "yes"): {"Good": 0.6, "OK": 0.4},
    ("no", "no"): {"Good": 0.3, "OK": 0.7},
}
PROBABILITY_J_GIVEN_G = {"Good": {"yes": 0.8, "no": 0.2}, "OK": {"yes": 0.2, "no": 0.8}}
PROBABILITY_S_GIVEN_G = {"Good": {"yes": 0.7, "no": 0.3}, "OK": {"yes": 0.3, "no": 0.7}}

def sample_probability(prob_table):
    return "yes" if np.random.rand() < prob_table["yes"] else "no"

def sample_g_value(value_a, value_c):
    prob = PROBABILITY_GIVEN_A_C[(value_a, value_c)]
    return "Good" if np.random.rand() < prob["Good"] else "OK"

def monte_carlo_simulation(sample_size=10000):
    samples = []
    for _ in range(sample_size):
        value_a = sample_probability(PROBABILITY_A)
        value_c = sample_probability(PROBABILITY_C)
        value_g = sample_g_value(value_a, value_c)
        value_j = sample_probability(PROBABILITY_J_GIVEN_G[value_g])
        value_s = sample_probability(PROBABILITY_S_GIVEN_G[value_g])
        samples.append((value_a, value_c, value_g, value_j, value_s))
    return samples

def compute_conditional_probability(samples):
    count_j_yes = 0
    count_s_yes_given_j_yes = 0
    for _, _, _, value_j, value_s in samples:
        if value_j == "yes":
            count_j_yes += 1
            if value_s == "yes":
                count_s_yes_given_j_yes += 1
    return count_s_yes_given_j_yes / count_j_yes if count_j_yes > 0 else 0

sample_size = 100000
samples = monte_carlo_simulation(sample_size)
probability_s_given_j = compute_conditional_probability(samples)
print(f"Estimated P(S | J): {probability_s_given_j:.4f}")