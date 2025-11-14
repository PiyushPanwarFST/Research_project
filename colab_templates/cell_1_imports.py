# ==============================================================================
# CELL 1: IMPORTS AND BASIC SETUP
# ==============================================================================

import time
import warnings

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from numpy.linalg import LinAlgError, inv
from scipy.optimize import fsolve, minimize
from scipy.stats import norm

# --- Suppress Warnings ---
warnings.filterwarnings('ignore', 'overflow encountered in exp')
warnings.filterwarnings('ignore', 'invalid value encountered in sqrt')
warnings.filterwarnings('ignore', 'divide by zero encountered in double_scalars')
warnings.filterwarnings('ignore', 'invalid value encountered in power')

print("✅ Cell 1: Imports and setup completed!")
