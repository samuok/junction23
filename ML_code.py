

import joblib
from sklearn.metrics import f1_score
import group as gp
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix,  ConfusionMatrixDisplay
from sklearn.model_selection import GridSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score


dfs = []


participants = ["Participant_1", "Participant_3", "Participant_3"]
file_types = ["Driving", "Walking"]
file_types_others = []
activities = ["Reading", "Chatting", "Doom", "Writing"]

activity_starts = [150, 420, 540, 870]
activity_ends = [390, 510, 840, 960]


for participant in participants:
        folder = []
        for i in range(0, 4):
                filename = f"/data/Indoor/{participant}/AFE_00{i}_CONFIDENTIAL.json"
                folder.append(filename)
        df = gp.process_and_combine_files(folder, 1000)
        for activity_idx, activity in enumerate(activities):
                df.loc[activity_starts[activity_idx]:activity_ends[activity_idx], "type"] = activity_idx
                atest = df.loc[activity_starts[activity_idx]:activity_ends[activity_idx]]
                dfs.append(atest)

for participant in participants:
        for idx, file_type in enumerate(file_types):
                filename = f"/data/{file_type}/{participant}/AFE_00{idx}_CONFIDENTIAL.json"
                df = gp.process_and_combine_files([filename], idx + 4)
                dfs.append(df)

for data in dfs:
        df = gp.combine_dataframes(df, data)

df = df.sample(4150)

left = df['left'].apply(pd.Series)
right = df['right'].apply(pd.Series)


# Drop the last two columns
left = left.iloc[:, :6]
right = right.iloc[:, :6]
# Rename these new columns (optional)
left.columns = ['Col1_l', 'Col2_l', 'Col3_l', 'Col4_l', 'Col5_l', 'Col6_l']
right.columns = ['Col1_r', 'Col2_r', 'Col3_r', 'Col4_r', 'Col5_r', 'Col6_r']
# Concatenate the new columns to the original DataFrame (if needed)
df = pd.concat([df.drop('left', axis=1), left], axis=1)
df = pd.concat([df.drop('right', axis=1), right], axis=1)

X = df[["left_erratic", "right_erratic", "blink_count", "distance", 'Col1_l', 'Col2_l', 'Col3_l', 'Col4_l', 'Col5_l', 'Col6_l',
        'Col1_r', 'Col2_r', 'Col3_r', 'Col4_r', 'Col5_r', 'Col6_r']]  # Features

y = df['type']

# Split the data into training, validation, and test sets
X_train, X_temp, y_train, y_temp = train_test_split(X, y, test_size=0.4, random_state=42)
X_val, X_test, y_val, y_test = train_test_split(X_temp, y_temp, test_size=0.5, random_state=42)

# Hyperparameter Tuning (example, you can adjust parameters accordingly)
param_grid = {
    'n_estimators': [50, 100, 200],
    'max_depth': [None, 10, 20],
    'min_samples_split': [2, 5, 10],
    'min_samples_leaf': [1, 2, 4]
}

grid_search = GridSearchCV(RandomForestClassifier(), param_grid, cv=5)
grid_search.fit(X_train, y_train)

best_model = grid_search.best_estimator_

# Save the best model
joblib.dump(best_model, 'best_model.joblib')

# Validation set predictions
y_val_pred = best_model.predict(X_val)

# Test set predictions
y_test_pred = best_model.predict(X_test)

# Evaluate on validation set
val_accuracy = accuracy_score(y_val, y_val_pred)
val_f1 = f1_score(y_val, y_val_pred, average='weighted')
val_conf_matrix = confusion_matrix(y_val, y_val_pred)

# Display and save validation confusion matrix plot for the test set
cm_display = ConfusionMatrixDisplay(confusion_matrix=val_conf_matrix)
cm_display.plot(cmap='viridis', values_format='d')  # You can customize colormap and values format
plt.title('Confusion Matrix - Validation Set\nAccuracy: {:.2f}, F1 Score: {:.2f}'.format(val_accuracy, val_f1))
plt.xlabel('Predicted', fontsize=10)
plt.ylabel('Actual', fontsize=10)

# Save the figure as an image file (e.g., PNG)
fig = plt.gcf()
fig.savefig('confusion_matrix_validation.png')

# Show the Matplotlib plot
plt.show()

print(f"Validation Accuracy: {val_accuracy}")
print(f"Validation F1 Score: {val_f1}")
print("Validation Confusion Matrix:\n", val_conf_matrix)

# Evaluate on test set
test_accuracy = accuracy_score(y_test, y_test_pred)
test_f1 = f1_score(y_test, y_test_pred, average='weighted')
test_conf_matrix = confusion_matrix(y_test, y_test_pred)



# Display and save test confusion matrix plot for the test set
cm_display = ConfusionMatrixDisplay(confusion_matrix=test_conf_matrix)
cm_display.plot(cmap='viridis', values_format='d')
plt.title('Confusion Matrix - Test Set\nAccuracy: {:.2f}, F1 Score: {:.2f}'.format(test_accuracy, test_f1))
plt.xlabel('Predicted')
plt.ylabel('Actual')
fig = plt.gcf()
fig.savefig('confusion_matrix_test.png')

print(f"Test Accuracy: {test_accuracy}")
print(f"Test F1 Score: {test_f1}")
print("Test Confusion Matrix:\n", test_conf_matrix)
