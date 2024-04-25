from sklearn.metrics import classification_report, accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
import pandas as pd
import numpy as np
import pickle

df = pd.read_csv('core/web_fifa.csv')

# Define features and target variable
features = ['pace', 'shooting', 'passing', 'dribbling', 'defending', 'physicality',
            'player_skill', 'player_attacking', 'player_movement', 'player_power',
            'player_mentality', 'player_defending', 'player_goalkeeper']
target = 'player_positions'

# Split data into features and target variable
X = df[features]
y = df[target]

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Initialize and train the logistic regression classifier
clf = LogisticRegression(max_iter=1000)
clf.fit(X_train, y_train)

pickle.dump(clf, open("model.sav", "wb"))


# # Make predictions on the test set
# y_pred = clf.predict(X_test)

# # Evaluate the model
# accuracy = accuracy_score(y_test, y_pred)
# print("Accuracy:", accuracy)

# # Classification report
# print("Classification Report:")
# print(classification_report(y_test, y_pred))