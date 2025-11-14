# ==============================================================================
# CELL 6: SIMULATION CONTROL PANEL
# ==============================================================================

# --- 6.1: Simulation Controls ---
# NOTE: Set to 2 for testing. Change to 2000 for the final run.
n_replications = 2000
mcmc_samples = 12000
mcmc_burn_in = 2000

# --- 6.2: Bayesian Priors Configuration ---
ip_prior_shape, ip_prior_rate = 2.0, 2.0
nip_prior_shape, nip_prior_rate = 0.00001, 0.00001

# --- 6.3: Censoring Setups (Fully Dynamic Generation) ---
n_values = [20, 30, 50, 100]
m_proportions = [0.5, 0.8] # m = 0.5*n and m = 0.8*n
target_R_values = [0.4, 0.5, 0.7]

setups = []

# --- Nested loops to create all combinations ---
for r_val in target_R_values:
    # Find the lambda parameters for the current R value first
    lambda1, lambda2, _ = find_lambda_pair_for_R(r_val)

    for n_val in n_values:
        for m_prop in m_proportions:
            m_val = int(m_prop * n_val)
            k_val = m_val - 1

            # Get the schemes
            schemes = generate_all_schemes(n_val, m_val)

            for scheme_name, r_scheme_val in schemes.items():
                # Calculate T values based on mean/median
                T_mean = xgamma_E_mean(lambda1)
                T_median = xgamma_E_median(lambda1)
                T_values = {"Mean": T_mean, "Median": T_median}

                for t_name, t_val in T_values.items():
                    t_val_str = f"{t_val:.2f}"
                    setup_name = f"R_{r_val}_n{n_val}_m{m_val}_{scheme_name}_T_{t_name}"

                    setup_dict = {
                        "name": setup_name,
                        "target_R": r_val,
                        "n1": n_val, "m1": m_val, "k1": k_val, "T1": t_val,
                        "n2": n_val, "m2": m_val, "k2": k_val, "T2": t_val,
                        "R_scheme": r_scheme_val
                    }
                    setups.append(setup_dict)

# --- 6.4: Setup Validation (Safety Guard) ---
for setup in setups:
    assert setup['m1'] <= setup['n1'], f"Error in {setup['name']}: m1 > n1"
    assert setup['m2'] <= setup['n2'], f"Error in {setup['name']}: m2 > n2"
    assert setup['k1'] < setup['m1'], f"Error in {setup['name']}: k1 >= m1"
    assert setup['k2'] < setup['m2'], f"Error in {setup['name']}: k2 >= m2"

print("✅ Cell 6: Control Panel ready.")
print(f"Total setups to run: {len(setups)}")
print(f"Replications per setup: {n_replications}")
