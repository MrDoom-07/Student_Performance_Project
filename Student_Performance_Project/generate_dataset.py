import pandas as pd
import numpy as np

rows = 1000
np.random.seed(42)

data = {
    "study_hours": np.random.randint(1, 10, rows),
    "previous_score": np.random.randint(30, 100, rows),
    "attendance": np.random.randint(50, 100, rows),
    "extra_classes": np.random.randint(0, 2, rows),
    "assignments_submitted": np.random.randint(3, 10, rows),
    "parental_support": np.random.randint(0, 4, rows),
    "internet_usage": np.random.randint(1, 6, rows),
    "sleep_hours": np.random.randint(4, 10, rows),
    "exam_stress": np.random.randint(1, 10, rows)
}

df = pd.DataFrame(data)

df["final_score"] = (
    df["study_hours"] * 4 +
    df["previous_score"] * 0.4 +
    df["attendance"] * 0.3 +
    df["assignments_submitted"] * 2 +
    df["parental_support"] * 1.5 +
    df["sleep_hours"] * 1 -
    df["internet_usage"] * 1 -
    df["exam_stress"] * 1.5 +
    np.random.randint(-5, 5, rows)
)

df["final_score"] = df["final_score"].clip(0, 100)

df.to_csv("data/student_performance_large.csv", index=False)


print("Dataset generated successfully → data/student_performance_large.csv")
