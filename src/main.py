import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report

def demonstrate_usage():
    """
    Demonstration of SenescenceCellTracker functionality
    """
    # Create sample dataset
    np.random.seed(42)
    n_samples = 1000
    
    # Generate synthetic senescence data
    data = {
        'aptamer_binding_affinity': np.random.normal(0.7, 0.15, n_samples),
        'senescence_marker_expression': np.random.normal(0.6, 0.2, n_samples),
        'sasp_activity_score': np.random.normal(0.5, 0.25, n_samples),
        'cellular_aging_index': np.random.normal(0.4, 0.3, n_samples)
    }
    
    df = pd.DataFrame(data)
    
    # Create target variable (senescent vs non-senescent)
    # Higher values indicate higher probability of being senescent
    senescence_prob = (
        0.3 * df['aptamer_binding_affinity'] +
        0.4 * df['senescence_marker_expression'] +
        0.2 * df['sasp_activity_score'] +
        0.1 * df['cellular_aging_index']
    )
    
    df['is_senescent'] = (senescence_prob > np.percentile(senescence_prob, 70)).astype(int)
    
    # Split data
    X = df[['aptamer_binding_affinity', 'senescence_marker_expression', 
            'sasp_activity_score', 'cellular_aging_index']]
    y = df['is_senescent']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Train model
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    # Make predictions
    y_pred = model.predict(X_test)
    
    # Print results
    print("Senescence Cell Tracker - Usage Demo")
    print("=" * 40)
    print(f"Accuracy: {accuracy_score(y_test, y_pred):.3f}")
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred))
    
    # Show feature importance
    feature_importance = pd.DataFrame({
        'feature': X.columns,
        'importance': model.feature_importances_
    }).sort_values('importance', ascending=False)
    
    print("\nFeature Importance:")
    print(feature_importance)
    
    # Plot results
    plt.figure(figsize=(10, 6))
    
    # Scatter plot of aptamer binding vs senescence marker
    plt.subplot(1, 2, 1)
    scatter = plt.scatter(df['aptamer_binding_affinity'], df['senescence_marker_expression'], 
                         c=df['is_senescent'], cmap='viridis', alpha=0.6)
    plt.xlabel('Aptamer Binding Affinity')
    plt.ylabel('Senescence Marker Expression')
    plt.title('Senescence Cell Classification')
    plt.colorbar(scatter)
    
    # Feature importance
    plt.subplot(1, 2, 2)
    plt.barh(feature_importance['feature'], feature_importance['importance'])
    plt.xlabel('Importance')
    plt.title('Feature Importance')
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    demonstrate_usage()