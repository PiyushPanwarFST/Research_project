# ==============================================================================
# CELL 5: HELPER FUNCTIONS
# ==============================================================================

def xgamma_E_mean(lam):
    """Calculates the theoretical mean of the Xg-E distribution."""
    if lam <= 0: return np.nan
    return 2.0 / lam

def xgamma_E_median(lam):
    """Calculates the theoretical median of the Xg-E distribution numerically."""
    if lam <= 0: return np.nan
    median_func = lambda x: xgamma_E_cdf(x, lam) - 0.5
    initial_guess = xgamma_E_mean(lam)
    try:
        median_val = fsolve(median_func, initial_guess)
        return median_val[0]
    except:
        return np.nan

def generate_all_schemes(n, m):
    """Generates a dictionary of the four standard removal schemes."""
    if m > n:
        raise ValueError("m cannot be greater than n")
    n_minus_m = n - m
    schemes = {
        "S1_End":    [0]*(m - 1) + [n_minus_m] if m > 0 else [],
        "S2_Begin":  [n_minus_m] + [0]*(m - 1) if m > 0 else [],
        "S3_Middle": [0]*(m//2 - 1) + [n_minus_m] + [0]*(m - m//2) if m > 1 else ([n_minus_m] if m == 1 else []),
        "S4_Uniform": [(n_minus_m // m) + (1 if i < n_minus_m % m else 0) for i in range(m)] if m > 0 else []
    }
    return schemes

def calculate_r_variance_delta_method(lambda1_hat, lambda2_hat, cov_matrix, h=1e-6):
    """Delta Method se R ka variance nikalta hai."""
    grad = np.array([(R_xgamma_e(lambda1_hat + h, lambda2_hat) - R_xgamma_e(lambda1_hat - h, lambda2_hat)) / (2 * h),
                     (R_xgamma_e(lambda1_hat, lambda2_hat + h) - R_xgamma_e(lambda1_hat, lambda2_hat - h)) / (2 * h)])
    return grad.T @ cov_matrix @ grad

def calculate_fisher_info(lam, estimator_func, *args):
    """Numerically Fisher Information nikalta hai."""
    h = 1e-6
    f_lam = estimator_func([lam], *args)
    f_plus = estimator_func([lam+h], *args)
    f_minus = estimator_func([lam-h], *args)
    return (f_plus - 2*f_lam + f_minus) / h**2

def hpd_credible_interval(samples, alpha=0.05):
    """Highest Posterior Density (HPD) credible interval nikalta hai."""
    samples = np.sort(samples)
    n = len(samples)
    n_in_interval = int(n * (1 - alpha))
    if n_in_interval < 2: return (np.nan, np.nan)
    intervals = samples[n_in_interval:] - samples[:n-n_in_interval]
    min_interval_index = np.argmin(intervals)
    return (samples[min_interval_index], samples[min_interval_index + n_in_interval])

def R_xgamma_e_from_samples(lambda1_samples, lambda2_samples):
    """MCMC samples se R ke samples nikalta hai."""
    return np.array([R_xgamma_e(l1, l2) for l1, l2 in zip(lambda1_samples, lambda2_samples)])

def calculate_metrics(reps, true_val):
    """Point estimates ke final metrics (Avg, MSE, Bias) nikalta hai."""
    reps = np.array(reps)
    return {"Avg_Estimate": np.nanmean(reps), "MSE": np.nanmean((reps - true_val)**2), "Bias": np.nanmean(reps - true_val)}

def calculate_interval_metrics(lower_reps, upper_reps, true_val):
    """Intervals ke final metrics (Avg_Width, Coverage) nikalta hai."""
    lower_reps, upper_reps = np.array(lower_reps), np.array(upper_reps)
    valid_indices = ~np.isnan(lower_reps) & ~np.isnan(upper_reps)
    if np.sum(valid_indices) == 0: return {"Avg_Width": np.nan, "Coverage": np.nan}
    width = np.nanmean(upper_reps[valid_indices] - lower_reps[valid_indices])
    coverage = np.nanmean((lower_reps[valid_indices] <= true_val) & (true_val <= upper_reps[valid_indices]))
    return {"Avg_Width": width, "Coverage": coverage}

def export_table(df, filename_prefix, caption, label):
    """DataFrame ko alag-alag formats mein export karta hai."""
    df.to_csv(f"{filename_prefix}.csv", index=False)
    with open(f"{filename_prefix}.txt", "w") as f:
        f.write(caption + "\n\n")
        f.write(df.to_string(index=False))
    print(f"Table exported to {filename_prefix}.[csv, txt]")

print("✅ Cell 5: Helper functions defined!")
