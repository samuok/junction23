import celery
from celery import Celery
import os
import group as gp
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from celery import Celery


@celery.task
def ML():
    filename1_in = "\data\Indoor\Participant_1\AFE_000_CONFIDENTIAL.json"
    filename2_in = "\data\Indoor\Participant_1\AFE_001_CONFIDENTIAL.json"
    filename3_in = "\data\Indoor\Participant_1\AFE_002_CONFIDENTIAL.json"
    filename4_in = "\data\Indoor\Participant_1\AFE_003_CONFIDENTIAL.json"

    filename1_dr = "\data\Driving\Participant_1\AFE_000_CONFIDENTIAL.json"
    filename2_dr = "\data\Driving\Participant_1\AFE_001_CONFIDENTIAL.json"
    filename3_dr = "\data\Driving\Participant_1\AFE_002_CONFIDENTIAL.json"
    filename4_dr = "\data\Driving\Participant_1\AFE_003_CONFIDENTIAL.json"

    filename1_wa = "\data\Walking\Participant_1\AFE_000_CONFIDENTIAL.json"
    filename2_wa = "\data\Walking\Participant_1\AFE_001_CONFIDENTIAL.json"

    filenames_1 = [filename1_in, filename2_in, filename3_in, filename4_in]
    filenames_2 = [filename1_dr, filename2_dr, filename3_dr, filename4_dr]
    filenames_3 = [filename1_wa, filename2_wa]

    df_indoors = gp.process_and_combine_files(filenames_1, 0)

    df_drive = gp.process_and_combine_files(filenames_2, 1)

    df_walking = gp.process_and_combine_files(filenames_3, 2)

    df = gp.combine_dataframes(df_drive, df_indoors)
    df = gp.combine_dataframes(df, df_walking)

    df = df.sample(5)

    print(df.columns)

    left = df['left'].apply(pd.Series)
    right = df['left'].apply(pd.Series)

    # Drop the last two columns
    left = left.iloc[:, :6]
    right = right.iloc[:, :6]
    # Rename these new columns (optional)
    left.columns = ['Col1_l', 'Col2_l', 'Col3_l', 'Col4_l', 'Col5_l', 'Col6_l']
    right.columns = ['Col1_r', 'Col2_r', 'Col3_r', 'Col4_r', 'Col5_r', 'Col6_r']
    # Concatenate the new columns to the original DataFrame (if needed)
    df = pd.concat([df.drop('left', axis=1), left], axis=1)
    df = pd.concat([df.drop('right', axis=1), right], axis=1)

    X = df[["left_erratic", "right_erratic", "blink_count", 'Col1_l', 'Col2_l', 'Col3_l', 'Col4_l', 'Col5_l', 'Col6_l',
            'Col1_r', 'Col2_r', 'Col3_r', 'Col4_r', 'Col5_r', 'Col6_r']]  # Features

    y = df['type']

    # scaler = sklearn.StandardScaler()
    # X = scaler.fit_transform(X)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = RandomForestClassifier()
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)

    accuracy = accuracy_score(y_test, y_pred)
    print(f"Accuracy: {accuracy}")
