import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from typing import Dict, List, Tuple, Union

class AptamerSimulator:
    """
    A class to simulate aptamer binding to senescent cells.
    """
    
    def __init__(self):
        # Predefined binding constants for different cell types
        self.binding_constants = {
            'senescent': 1.5e-6,
            'normal': 5e-9,
            'activated': 8e-7
        }
        
        # Aptamer sequences and their known affinities
        self.aptamer_database = {
            'aptamer_A': {'sequence': 'GCATCGATCGATCG', 'affinity': 1.2e-7},
            'aptamer_B': {'sequence': 'TGCATCGATCGATC', 'affinity': 2.1e-8},
            'aptamer_C': {'sequence': 'CGATCGATCGATCG', 'affinity': 3.5e-7}
        }
    
    def simulate_binding(self, cell_type: str, aptamer_sequence: str, 
                        concentration: float = 1e-6) -> Dict[str, float]:
        """
        Simulate aptamer binding to cells of specified type.
        
        Args:
            cell_type (str): Type of cell ('senescent', 'normal', 'activated')
            aptamer_sequence (str): DNA/RNA sequence of aptamer
            concentration (float): Concentration of aptamer in M
            
        Returns:
            Dict containing binding probability and saturation level
        """
        if cell_type not in self.binding_constants:
            raise ValueError(f"Unknown cell type: {cell_type}")
            
        # Calculate binding probability using Langmuir isotherm
        k_d = self.binding_constants[cell_type]
        binding_probability = concentration / (concentration + k_d)
        
        # Calculate saturation level (0-1)
        saturation = min(1.0, concentration / (k_d * 10))
        
        return {
            'binding_probability': binding_probability,
            'saturation_level': saturation,
            'cell_type': cell_type
        }
    
    def predict_binding_profile(self, cell_types: List[str], 
                              aptamer_sequences: List[str]) -> pd.DataFrame:
        """
        Predict binding profiles for multiple cell types and aptamers.
        
        Args:
            cell_types (List[str]): List of cell types
            aptamer_sequences (List[str]): List of aptamer sequences
            
        Returns:
            DataFrame with binding predictions
        """
        results = []
        
        for cell_type in cell_types:
            for aptamer_seq in aptamer_sequences:
                pred = self.simulate_binding(cell_type, aptamer_seq)
                pred['aptamer_sequence'] = aptamer_seq
                results.append(pred)
                
        return pd.DataFrame(results)

def calculate_binding_affinity(cell_type: str, aptamer_sequence: str) -> float:
    """
    Calculate binding affinity between aptamer and specific cell type.
    
    Args:
        cell_type (str): Type of cell ('senescent', 'normal', 'activated')
        aptamer_sequence (str): DNA/RNA sequence of aptamer
        
    Returns:
        Binding affinity constant (Kd) in M
    """
    # Simple heuristic model - in practice this would be more complex
    base_affinities = {
        'senescent': 1.5e-6,
        'normal': 5e-9,
        'activated': 8e-7
    }
    
    if cell_type not in base_affinities:
        raise ValueError(f"Unknown cell type: {cell_type}")
    
    # Adjust based on sequence complementarity (simplified)
    # In reality, this would involve thermodynamic calculations
    sequence_length = len(aptamer_sequence)
    affinity_modifier = 1.0 + (sequence_length - 12) * 0.05  # Simplified
    
    return base_affinities[cell_type] * affinity_modifier