import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

def plot_senescence_distribution(scores):
    """
    Plot the distribution of senescence scores from analysis results.
    
    Parameters:
    scores (array-like): Array or list of senescence scores to visualize
    
    Returns:
    None: Displays the plot
    """
    # Convert to numpy array for consistency
    scores = np.array(scores)
    
    # Create the histogram
    plt.figure(figsize=(10, 6))
    n, bins, patches = plt.hist(scores, bins=30, color='skyblue', edgecolor='black', alpha=0.7)
    
    # Add labels and title
    plt.xlabel('Senescence Score')
    plt.ylabel('Frequency')
    plt.title('Distribution of Senescence Scores')
    plt.grid(True, alpha=0.3)
    
    # Add statistics text
    mean_score = np.mean(scores)
    std_score = np.std(scores)
    plt.axvline(mean_score, color='red', linestyle='--', linewidth=2, 
               label=f'Mean: {mean_score:.2f}')
    plt.axvline(mean_score + std_score, color='orange', linestyle=':', 
               label=f'+1 Std: {mean_score + std_score:.2f}')
    plt.axvline(mean_score - std_score, color='orange', linestyle=':', 
               label=f'-1 Std: {mean_score - std_score:.2f}')
    plt.legend()
    
    # Show the plot
    plt.tight_layout()
    plt.show()