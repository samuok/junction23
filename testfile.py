import group as gp
import pandas as pd
import pickle
import numpy as np

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
        for activity_idx, activity in enumerate(activities):
                filename = f"/data/Indoor/{participant}/AFE_00{activity_idx}_CONFIDENTIAL.json"
                df = gp.process_and_combine_files([filename], activity_idx)
                df.loc[activity_starts[activity_idx]:activity_ends[activity_idx], "type"] = activity_idx
                atest = df.loc[activity_starts[activity_idx]:activity_ends[activity_idx]]
                dfs.append(atest)

for participant in participants:
        for idx, file_type in enumerate(file_types):
                filename = f"/data/{file_type}/{participant}/AFE_00{idx}_CONFIDENTIAL.json"
                df = gp.process_and_combine_files([filename], idx + 3)
                dfs.append(df)




for data in dfs:
        df = gp.combine_dataframes(df, data)

print(df)
df = df.sample(2400)




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


#scaler = sklearn.StandardScaler()F
#X = scaler.fit_transform(X)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = RandomForestClassifier()
model.fit(X_train, y_train)

y_pred = model.predict(X_test)
pickle.dump(model, open('model.pkl', 'wb'))

X_Sample = X.sample(1)
np.savetxt('file.txt', X_Sample)
y_pred2 = model.predict(X_Sample)
print(y_pred2)



accuracy = accuracy_score(y_test, y_pred)
print(f"Accuracy: {accuracy}")