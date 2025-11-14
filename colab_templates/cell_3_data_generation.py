# ==============================================================================
# CELL 3: DATA GENERATION FUNCTIONS
# ==============================================================================

def generate_xgamma_E(n, lam):
    """IMPROVEMENT: Xg-E distribution se samples (Mixture Method se - zyada accurate)."""
    choices = np.random.rand(n)
    n_exp = np.sum(choices < 0.5)
    n_gamma = n - n_exp
    samples_exp = np.random.exponential(scale=1/lam, size=n_exp)
    samples_gamma = np.random.gamma(shape=3, scale=1/lam, size=n_gamma)
    return np.sort(np.concatenate((samples_exp, samples_gamma)))

def apply_gphc_scheme(samples, n, m, k, T, R_scheme_input):
    """GPHC scheme ko data par apply karta hai."""
    sorted_samples = np.sort(samples)
    temp_failures, temp_R_actual, current_sample = [], [], list(sorted_samples)
    for i in range(m):
        if not current_sample: break
        t_fail = current_sample.pop(0)
        temp_failures.append(t_fail)
        r_j = R_scheme_input[i] if i < len(R_scheme_input) else 0
        temp_R_actual.append(r_j)
        if len(current_sample) > 0:
            for _ in range(r_j):
                if current_sample: current_sample.pop(0) # Remove from start
                else: break
    X_k_mn = temp_failures[k-1] if k <= len(temp_failures) else np.inf
    X_m_mn = temp_failures[m-1] if m <= len(temp_failures) else np.inf
    termination_time = min(X_m_mn, T) if k > len(temp_failures) else max(X_k_mn, min(X_m_mn, T))
    observed_failures, R_actual = [], []
    for i, t_fail in enumerate(temp_failures):
        if t_fail <= termination_time:
            observed_failures.append(t_fail)
            R_actual.append(temp_R_actual[i])
        else:
            break
    num_observed_failures = len(observed_failures)
    remaining_at_termination = max(0, n - np.sum(R_actual) - num_observed_failures)
    return (np.array(observed_failures), np.array(R_actual), termination_time, num_observed_failures, remaining_at_termination)

print("✅ Cell 3: Data generation functions defined!")
