# ==============================================================================
# CELL 7: MAIN SIMULATION LOOP
# ==============================================================================

import os

# --- 7.1: Checkpointing Setup ---
checkpoint_file = 'simulation_checkpoint.csv'
all_setups_summary = []

if os.path.exists(checkpoint_file):
    print(f"Resuming from checkpoint file: {checkpoint_file}")
    df_checkpoint = pd.read_csv(checkpoint_file)
    completed_setups = list(df_checkpoint['name'])
    all_setups_summary = df_checkpoint.to_dict('records')
    print(f"Found {len(completed_setups)} completed setups. Will skip them.")
else:
    print("Starting a new simulation run. No checkpoint file found.")
    completed_setups = []

start_time = time.time()
print(f"--- Running Monte Carlo Simulation for {len(setups)} setups ---")

# --- 7.2: Outer Loop ---
for setup in setups:
    if setup['name'] in completed_setups:
        print(f"\n⏭ Skipping already completed setup: {setup['name']}")
        continue

    target_R = setup["target_R"]
    try:
        lambda1_true, lambda2_true, achieved_R = find_lambda_pair_for_R(target_R)
    except RuntimeError:
        print(f"Skipping setup {setup['name']} due to lambda optimization failure.")
        continue

    # Temporary lists for this setup
    mle_r_reps, mps_r_reps, bayes_ip_r_reps, bayes_nip_r_reps = [], [], [], []
    mle_lower, mle_upper = [], []
    mps_lower, mps_upper = [], []
    bayes_ip_lower, bayes_ip_upper = [], []
    bayes_nip_lower, bayes_nip_upper = [], []

    print(f"\n Running Setup: {setup['name']} | Target R={target_R:.2f}, True R={achieved_R:.4f}")

    # --- 7.3: Inner Loop (Replications) ---
    for i in range(n_replications):
        X_samples = generate_xgamma_E(setup["n1"], lambda1_true)
        Y_samples = generate_xgamma_E(setup["n2"], lambda2_true)

        gphc_args_X = (X_samples, setup['n1'], setup['m1'], setup['k1'], setup['T1'], setup['R_scheme'])
        gphc_args_Y = (Y_samples, setup['n2'], setup['m2'], setup['k2'], setup['T2'], setup['R_scheme'])

        obs_X, R_X, T_X, D_X, rem_X = apply_gphc_scheme(*gphc_args_X)
        obs_Y, R_Y, T_Y, D_Y, rem_Y = apply_gphc_scheme(*gphc_args_Y)

        solver_args_X = (obs_X, R_X, T_X, D_X, rem_X)
        solver_args_Y = (obs_Y, R_Y, T_Y, D_Y, rem_Y)

        # MLE Estimation
        try:
            res_X_mle = minimize(neg_log_likelihood, x0=[1.0], args=solver_args_X, bounds=[(1e-6, None)])
            res_Y_mle = minimize(neg_log_likelihood, x0=[1.0], args=solver_args_Y, bounds=[(1e-6, None)])
            l1_mle, l2_mle = res_X_mle.x[0], res_Y_mle.x[0]
            mle_r_reps.append(R_xgamma_e(l1_mle, l2_mle))
            fisher_1 = calculate_fisher_info(l1_mle, neg_log_likelihood, *solver_args_X)
            fisher_2 = calculate_fisher_info(l2_mle, neg_log_likelihood, *solver_args_Y)
            cov = inv(np.diag([fisher_1, fisher_2]))
            var_R = calculate_r_variance_delta_method(l1_mle, l2_mle, cov)
            std_err = np.sqrt(var_R) if var_R > 0 else 0
            z = norm.ppf(0.975)
            mle_lower.append(mle_r_reps[-1] - z * std_err); mle_upper.append(mle_r_reps[-1] + z * std_err)
        except (ValueError, LinAlgError):
            mle_r_reps.append(np.nan); mle_lower.append(np.nan); mle_upper.append(np.nan)

        # MPS Estimation
        try:
            res_X_mps = minimize(neg_log_mps, x0=[1.0], args=solver_args_X, bounds=[(1e-6, None)])
            res_Y_mps = minimize(neg_log_mps, x0=[1.0], args=solver_args_Y, bounds=[(1e-6, None)])
            l1_mps, l2_mps = res_X_mps.x[0], res_Y_mps.x[0]
            mps_r_reps.append(R_xgamma_e(l1_mps, l2_mps))
            fisher_mps1 = calculate_fisher_info(l1_mps, neg_log_mps, *solver_args_X)
            fisher_mps2 = calculate_fisher_info(l2_mps, neg_log_mps, *solver_args_Y)
            cov_mps = inv(np.diag([fisher_mps1, fisher_mps2]))
            var_R_mps = calculate_r_variance_delta_method(l1_mps, l2_mps, cov_mps)
            std_err_mps = np.sqrt(var_R_mps) if var_R_mps > 0 else 0
            z = norm.ppf(0.975)
            mps_lower.append(mps_r_reps[-1] - z * std_err_mps); mps_upper.append(mps_r_reps[-1] + z * std_err_mps)
        except (ValueError, LinAlgError):
            mps_r_reps.append(np.nan); mps_lower.append(np.nan); mps_upper.append(np.nan)

        # Bayesian IP
        l1_samp_ip = metropolis_sampler(1.0, obs_X, R_X, T_X, D_X, rem_X, n_samples=mcmc_samples, proposal_sd=0.5, prior_shape=ip_prior_shape, prior_rate=ip_prior_rate)[mcmc_burn_in:]
        l2_samp_ip = metropolis_sampler(1.0, obs_Y, R_Y, T_Y, D_Y, rem_Y, n_samples=mcmc_samples, proposal_sd=0.5, prior_shape=ip_prior_shape, prior_rate=ip_prior_rate)[mcmc_burn_in:]
        r_samp_ip = R_xgamma_e_from_samples(l1_samp_ip, l2_samp_ip)
        bayes_ip_r_reps.append(np.mean(r_samp_ip))
        low, up = hpd_credible_interval(r_samp_ip); bayes_ip_lower.append(low); bayes_ip_upper.append(up)

        # Bayesian NIP
        l1_samp_nip = metropolis_sampler(1.0, obs_X, R_X, T_X, D_X, rem_X, n_samples=mcmc_samples, proposal_sd=0.5, prior_shape=nip_prior_shape, prior_rate=nip_prior_rate)[mcmc_burn_in:]
        l2_samp_nip = metropolis_sampler(1.0, obs_Y, R_Y, T_Y, D_Y, rem_Y, n_samples=mcmc_samples, proposal_sd=0.5, prior_shape=nip_prior_shape, prior_rate=nip_prior_rate)[mcmc_burn_in:]
        r_samp_nip = R_xgamma_e_from_samples(l1_samp_nip, l2_samp_nip)
        bayes_nip_r_reps.append(np.mean(r_samp_nip))
        low, up = hpd_credible_interval(r_samp_nip); bayes_nip_lower.append(low); bayes_nip_upper.append(up)

    # --- 7.4: Aggregation for the current setup ---
    metrics_mle = {**calculate_metrics(mle_r_reps, achieved_R), **calculate_interval_metrics(mle_lower, mle_upper, achieved_R)}
    metrics_mps = {**calculate_metrics(mps_r_reps, achieved_R), **calculate_interval_metrics(mps_lower, mps_upper, achieved_R)}
    metrics_bayes_ip = {**calculate_metrics(bayes_ip_r_reps, achieved_R), **calculate_interval_metrics(bayes_ip_lower, bayes_ip_upper, achieved_R)}
    metrics_bayes_nip = {**calculate_metrics(bayes_nip_r_reps, achieved_R), **calculate_interval_metrics(bayes_nip_lower, bayes_nip_upper, achieved_R)}

    summary_row = {
        "Setup_Name": setup["name"], **setup, "True_R": achieved_R,
        "Avg_MLE": metrics_mle["Avg_Estimate"], "MSE_MLE": metrics_mle["MSE"], "Bias_MLE": metrics_mle["Bias"],
        "Avg_Width_MLE": metrics_mle["Avg_Width"], "Coverage_MLE": metrics_mle["Coverage"],
        "Avg_MPS": metrics_mps["Avg_Estimate"], "MSE_MPS": metrics_mps["MSE"], "Bias_MPS": metrics_mps["Bias"],
        "Avg_Width_MPS": metrics_mps["Avg_Width"], "Coverage_MPS": metrics_mps["Coverage"],
        "Avg_Bayes_IP": metrics_bayes_ip["Avg_Estimate"], "MSE_Bayes_IP": metrics_bayes_ip["MSE"], "Bias_Bayes_IP": metrics_bayes_ip["Bias"],
        "Avg_Width_Bayes_IP": metrics_bayes_ip["Avg_Width"], "Coverage_Bayes_IP": metrics_bayes_ip["Coverage"],
        "Avg_Bayes_NIP": metrics_bayes_nip["Avg_Estimate"], "MSE_Bayes_NIP": metrics_bayes_nip["MSE"], "Bias_Bayes_NIP": metrics_bayes_nip["Bias"],
        "Avg_Width_Bayes_NIP": metrics_bayes_nip["Avg_Width"], "Coverage_Bayes_NIP": metrics_bayes_nip["Coverage"],
    }
    all_setups_summary.append(summary_row)

    # --- 7.5: Checkpointing ---
    pd.DataFrame(all_setups_summary).to_csv(checkpoint_file, index=False)
    print(f"Checkpoint saved for setup: {setup['name']}")

# --- 7.6: Final DataFrame Creation ---
df_final_results = pd.DataFrame(all_setups_summary)
end_time = time.time()
print("\n\n" + "="*80)
print("Simulation Finished!")
print(f"Total execution time: {(end_time - start_time)/60:.2f} minutes")
print("="*80)
