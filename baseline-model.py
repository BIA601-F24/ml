import pandas as pd
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score


"""
A baseline model using Logistic Regression on the breast cancer dataset.
This is a testing file to ensure the environment is set up correctly.
"""
def main():
    # 1. Load Data
    cancer = load_breast_cancer()
    X = pd.DataFrame(cancer.data, columns=cancer.feature_names)
    y = pd.Series(cancer.target)

    print("Dataset loaded.")
    print(f"Number of features: {X.shape[1]}")
    print("Feature names:")
    print(list(X.columns))
    print("-" * 30)

    # 2. For now, let's manually select the FIRST 10 features as an example
    # This is what a 'chromosome' will do automatically later
    selected_features = X.columns[:10]
    X_subset = X[selected_features]
    
    print(f"Using a subset of {len(selected_features)} features.")

    # 3. Split data for training and testing
    X_train, X_test, y_train, y_test = train_test_split(
        X_subset, y, test_size=0.3, random_state=42
    )
    
    # 4. Train a simple model
    model = LogisticRegression(max_iter=10000) # max_iter to ensure convergence
    model.fit(X_train, y_train)
    print("Model trained.")
    
    # 5. Evaluate the model
    predictions = model.predict(X_test)
    accuracy = accuracy_score(y_test, predictions)

    print(f"Model accuracy with the first {len(selected_features)} features: {accuracy:.4f}")

if __name__ == "__main__":
    main()