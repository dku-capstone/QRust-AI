import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
import joblib

# 1. 데이터 로드
df = pd.read_csv("urldata_features10.csv")

# 2. 사용할 feature
features = [
    'hostname_length', 'count_dir', 'count-www',
    'url_length', 'fd_length', 'count-', 'count.',
    'tld_length', 'count-digits', 'count='
]

X = df[features]
y = df['label']

# 3. 학습-검증 분할
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, stratify=y, random_state=42)

# 4. 모델 학습
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# 5. 성능 평가
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
report = classification_report(y_test, y_pred, target_names=["Benign", "Malicious"])

print("모델 성능 평가 결과:")
print(f"Accuracy: {accuracy:.4f}")
print(report)

# 6. 모델 저장
joblib.dump(model, "url_model_new.pkl")
print("모델 학습 및 저장 완료 (url_model_new.pkl)")