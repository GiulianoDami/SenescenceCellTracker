import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from .senescence_analyzer import SenescenceAnalyzer
from .data_loader import load_dataset

class BatchProcessor:
    def __init__(self):
        self.analyzer = SenescenceAnalyzer()
        
    def process_dataset(self, dataset_path):
        """Process a single dataset and return results"""
        try:
            # Load dataset
            data = load_dataset(dataset_path)
            
            # Analyze for senescence markers
            results = self.analyzer.analyze_senescence_markers(data)
            
            # Calculate aging scores
            aging_score = self.analyzer.calculate_aging_score(data)
            
            # Identify SASPs
            sasp_data = self.analyzer.identify_sasps(data)
            
            return {
                'dataset_path': dataset_path,
                'senescence_markers': results,
                'aging_score': aging_score,
                'sasp_data': sasp_data,
                'cell_count': len(data)
            }
        except Exception as e:
            print(f"Error processing {dataset_path}: {str(e)}")
            return None
            
    def process_batch(self, dataset_paths):
        """Process multiple datasets in batch"""
        results = []
        for path in dataset_paths:
            result = self.process_dataset(path)
            if result:
                results.append(result)
        return results

def process_dataset_batch(dataset_paths):
    """Convenience function to process a batch of datasets"""
    processor = BatchProcessor()
    return processor.process_batch(dataset_paths)

def save_results(results, filename):
    """Save batch processing results to CSV"""
    if not results:
        return
        
    # Flatten results for CSV export
    flattened_results = []
    for result in results:
        flat_result = {
            'dataset_path': result['dataset_path'],
            'cell_count': result['cell_count'],
            'aging_score': result['aging_score']
        }
        
        # Add senescence marker data
        for marker, value in result['senescence_markers'].items():
            flat_result[f'marker_{marker}'] = value
            
        # Add SASP data
        for i, sasp in enumerate(result['sasp_data']):
            flat_result[f'sasp_{i}'] = sasp
            
        flattened_results.append(flat_result)
    
    df = pd.DataFrame(flattened_results)
    df.to_csv(filename, index=False)