import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt

class SenescenceAnalyzer:
    """
    Core class for senescence detection and analysis
    """
    
    def __init__(self):
        self.marker_genes = ['p16', 'p21', 'p53', 'SA-β-gal', 'IL6', 'IL8', 'TNFα']
        self.scaler = StandardScaler()
        self.pca = PCA(n_components=2)
        
    def identify_senescent_cells(self, df):
        """
        Identify senescent cells based on marker gene expression
        
        Parameters:
        df (pd.DataFrame): DataFrame containing cell data with marker genes
        
        Returns:
        dict: Dictionary containing senescence results
        """
        # Validate input
        if not all(marker in df.columns for marker in self.marker_genes):
            raise ValueError(f"Missing required marker genes. Required: {self.marker_genes}")
        
        # Normalize marker gene expressions
        marker_data = df[self.marker_genes]
        normalized_data = self.scaler.fit_transform(marker_data)
        
        # Apply PCA for dimensionality reduction
        reduced_data = self.pca.fit_transform(normalized_data)
        
        # Cluster cells using K-means
        kmeans = KMeans(n_clusters=2, random_state=42)
        clusters = kmeans.fit_predict(reduced_data)
        
        # Determine which cluster represents senescent cells
        # Assume higher expression of senescence markers indicates senescence
        marker_means = marker_data.mean()
        senescence_score = np.dot(normalized_data, np.array([1]*len(self.marker_genes)))
        
        # Classify cells based on marker expression thresholds
        threshold = np.percentile(senescence_score, 75)
        senescence_status = (senescence_score >= threshold).astype(int)
        
        return {
            'cell_identification': senescence_status,
            'cluster_labels': clusters,
            'senescence_scores': senescence_score,
            'marker_expressions': marker_data
        }
    
    def calculate_aging_scores(self, results):
        """
        Calculate aging scores based on senescence detection results
        
        Parameters:
        results (dict): Results from identify_senescent_cells
        
        Returns:
        pd.Series: Aging scores for each cell
        """
        # Extract senescence scores
        senescence_scores = results['senescence_scores']
        
        # Normalize aging scores between 0 and 1
        min_score = np.min(senescence_scores)
        max_score = np.max(senescence_scores)
        
        if max_score == min_score:
            aging_scores = np.ones_like(senescence_scores)
        else:
            aging_scores = (senescence_scores - min_score) / (max_score - min_score)
            
        return pd.Series(aging_scores, name='aging_score')

def identify_senescent_cells(df):
    """
    Function to identify senescent cells
    
    Parameters:
    df (pd.DataFrame): DataFrame containing cell data
    
    Returns:
    dict: Senescence detection results
    """
    analyzer = SenescenceAnalyzer()
    return analyzer.identify_senescent_cells(df)

def calculate_aging_scores(results):
    """
    Function to calculate aging scores
    
    Parameters:
    results (dict): Results from senescence detection
    
    Returns:
    pd.Series: Aging scores
    """
    analyzer = SenescenceAnalyzer()
    return analyzer.calculate_aging_scores(results)