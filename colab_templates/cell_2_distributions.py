# ==============================================================================
# CELL 2: CORE DISTRIBUTION FUNCTIONS
# ==============================================================================

# --- 2.1: Core Distribution Functions ---
def xgamma_E_pdf(x, lam):
    """Xgamma-Exponential (Xg-E) PDF, handles arrays correctly."""
    x = np.asarray(x)
    if lam <= 0: return np.zeros_like(x, dtype=float)
    result = np.zeros_like(x, dtype=float)
    valid_mask = x >= 0
    x_valid = x[valid_mask]
    term1 = 0.5 * lam * np.exp(-lam * x_valid)
    term2 = 1 + 0.5 * (lam * x_valid)**2
    result[valid_mask] = term1 * term2
    return result

def xgamma_E_cdf(x, lam):
    """Xgamma-Exponential (Xg-E) CDF, handles arrays correctly."""
    x = np.asarray(x)
    if lam <= 0: return np.zeros_like(x, dtype=float)
    result = np.zeros_like(x, dtype=float)
    valid_mask = x >= 0
    x_valid = x[valid_mask]
    term1 = 0.5 * np.exp(-lam * x_valid)
    term2 = 2 + (lam * x_valid) + 0.5 * (lam * x_valid)**2
    result[valid_mask] = 1 - (term1 * term2)
    return result

def xgamma_E_sf(x, lam):
    """Xgamma-Exponential (Xg-E) Survival Function."""
    return 1 - xgamma_E_cdf(x, lam)

def R_xgamma_e(lambda1, lambda2):
    """Stress-Strength Reliability R = P(Y < X) ka formula."""
    sum_lambda = lambda1 + lambda2
    if sum_lambda <= 1e-9: return np.nan
    term_A = 1
    term_B = lambda2 / (2 * sum_lambda)
    term_C = (2 * lambda1**2 + lambda2**2) / (2 * sum_lambda**2)
    term_D = (3 * lambda1**2 * lambda2) / (2 * sum_lambda**3)
    term_E = (3 * lambda1**2 * lambda2**2) / (sum_lambda**4)
    bracket = term_A + term_B + term_C + term_D + term_E
    R = 1 - (lambda1 / (2 * sum_lambda)) * bracket
    return R

def find_lambda_pair_for_R(target_R, l1_guess=1.0, l2_guess=1.0):
    """Target R ke liye lambda pair dhoondhta hai."""
    def objective(params):
        lambda1, lambda2 = params
        if lambda1 <= 0 or lambda2 <= 0: return 1e6
        return (R_xgamma_e(lambda1, lambda2) - target_R)**2
    result = minimize(objective, [l1_guess, l2_guess], bounds=[(0.1, 10), (0.1, 10)], method='L-BFGS-B')
    if result.success:
        return result.x[0], result.x[1], R_xgamma_e(result.x[0], result.x[1])
    else:
        return 1.0, 1.0, 0.5 # Fallback

print("✅ Cell 2: Core distribution functions defined!")
