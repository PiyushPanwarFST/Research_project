# ==============================================================================
# CELL 8: RESULTS ANALYSIS AND EXPORT
# ==============================================================================

print("Generating and exporting final tables from saved checkpoint file...")

# --- STEP 1: Load the results from the checkpoint file ---
checkpoint_file = 'simulation_checkpoint.csv'

if os.path.exists(checkpoint_file):
    df_final_results = pd.read_csv(checkpoint_file)
    print(f"Successfully loaded {len(df_final_results)} results from '{checkpoint_file}'")

    # --- STEP 2: Generate Tables ---
    base_cols = ['Setup_Name','True_R', 'n1', 'm1', 'k1', 'T1', 'n2', 'm2', 'k2', 'T2']

    # --- Table 1: Classical (MLE & MPS) Results ---
    classical_cols = [
        'Avg_MLE', 'MSE_MLE', 'Bias_MLE', 'Avg_Width_MLE', 'Coverage_MLE',
        'Avg_MPS', 'MSE_MPS', 'Bias_MPS', 'Avg_Width_MPS', 'Coverage_MPS'
    ]
    df_classical = df_final_results[base_cols + classical_cols].copy()
    print("\n" + "="*80)
    print("### TABLE 1: CLASSICAL (MLE & MPS) RESULTS ###")
    print("="*80)
    display(df_classical)
    export_table(df_classical, "classical_results", "Results for Classical Estimation (MLE and MPS).", "tab:classical")

    # --- Table 2: Bayesian (Informative Prior) Results ---
    bayes_ip_cols = ['Avg_Bayes_IP', 'MSE_Bayes_IP', 'Bias_Bayes_IP', 'Avg_Width_Bayes_IP', 'Coverage_Bayes_IP']
    df_bayes_ip = df_final_results[base_cols + bayes_ip_cols].copy()
    df_bayes_ip.rename(columns={"Avg_Bayes_IP": "Avg_Estimate", "MSE_Bayes_IP": "MSE", "Bias_Bayes_IP": "Bias", "Avg_Width_Bayes_IP": "Avg_Width", "Coverage_Bayes_IP": "Coverage"}, inplace=True)
    print("\n" + "="*80)
    print("### TABLE 2: BAYESIAN (INFORMATIVE PRIOR) RESULTS ###")
    print("="*80)
    display(df_bayes_ip)
    export_table(df_bayes_ip, "bayes_ip_results", "Results for Bayesian Estimation with Informative Priors.", "tab:bayes_ip")

    # --- Table 3: Bayesian (Non-Informative Prior) Results ---
    bayes_nip_cols = ['Avg_Bayes_NIP', 'MSE_Bayes_NIP', 'Bias_Bayes_NIP', 'Avg_Width_Bayes_NIP', 'Coverage_Bayes_NIP']
    df_bayes_nip = df_final_results[base_cols + bayes_nip_cols].copy()
    df_bayes_nip.rename(columns={"Avg_Bayes_NIP": "Avg_Estimate", "MSE_Bayes_NIP": "MSE", "Bias_Bayes_NIP": "Bias", "Avg_Width_Bayes_NIP": "Avg_Width", "Coverage_Bayes_NIP": "Coverage"}, inplace=True)
    print("\n" + "="*80)
    print("### TABLE 3: BAYESIAN (NON-INFORMATIVE PRIOR) RESULTS ###")
    print("="*80)
    display(df_bayes_nip)
    export_table(df_bayes_nip, "bayes_nip_results", "Results for Bayesian Estimation with Non-Informative Priors.", "tab:bayes_nip")

else:
    print(f"Error: Checkpoint file '{checkpoint_file}' not found.")
    print("Please run Cell 7 to generate the results file before running this cell.")

print("✅ Cell 8: Results analysis and export completed!")
