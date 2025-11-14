# ==============================================================================
# CELL 4: ESTIMATION FUNCTIONS
# ==============================================================================

def neg_log_likelihood(params, observed_failures, R_actual, termination_time, num_observed_failures, remaining_at_termination):
    """Negative Log-Likelihood function."""
    lam = params[0]
    if lam <= 0: return 1e10
    logL = np.sum(np.log(xgamma_E_pdf(observed_failures, lam) + 1e-9))
    logL += np.sum(R_actual * np.log(xgamma_E_sf(observed_failures, lam) + 1e-9))
    if remaining_at_termination > 0:
        logL += remaining_at_termination * np.log(xgamma_E_sf(termination_time, lam) + 1e-9)
    return -logL

def neg_log_mps(params, observed_failures, R_actual, termination_time, num_observed_failures, remaining_at_termination):
    """Negative Log of Product of Spacings."""
    lam = params[0]
    if lam <= 0 or num_observed_failures == 0: return 1e10
    cdf_values = xgamma_E_cdf(observed_failures, lam)
    extended_cdf = np.concatenate(([0], cdf_values, [xgamma_E_cdf(termination_time, lam)]))
    spacings = np.diff(extended_cdf)
    spacings[spacings <= 0] = 1e-10
    return -np.sum(np.log(spacings))

def log_posterior(params, observed_failures, R_actual, termination_time, num_observed_failures, remaining_at_termination, prior_shape, prior_rate):
    """Log-Posterior function for Bayesian analysis."""
    log_likelihood_val = -neg_log_likelihood(params, observed_failures, R_actual, termination_time, num_observed_failures, remaining_at_termination)
    lam = params[0]
    if lam <= 0: return -np.inf
    log_prior = (prior_shape - 1) * np.log(lam) - lam * prior_rate
    return log_likelihood_val + log_prior

def metropolis_sampler(init, observed_failures, R_actual, termination_time, num_observed_failures, remaining_at_termination, n_samples, proposal_sd, prior_shape, prior_rate):
    """Metropolis-Hastings sampler."""
    samples, current = [], init
    current_lp = log_posterior([current], observed_failures, R_actual, termination_time, num_observed_failures, remaining_at_termination, prior_shape, prior_rate)
    for _ in range(n_samples):
        proposal = np.abs(np.random.normal(current, proposal_sd))
        proposal_lp = log_posterior([proposal], observed_failures, R_actual, termination_time, num_observed_failures, remaining_at_termination, prior_shape, prior_rate)
        if np.random.rand() < min(1, np.exp(proposal_lp - current_lp)):
            current, current_lp = proposal, proposal_lp
        samples.append(current)
    return np.array(samples)

print("✅ Cell 4: Estimation functions defined!")
