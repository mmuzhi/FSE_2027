"""RQ3.1 task-identification probe with action-trace features."""
import numpy as np
from pathlib import Path
from collections import Counter
import json

from data_infrastructure import COTSample, CATEGORIES, load_all_tasks

KEY_TRANSITIONS = [
    ("PU", "VV"),
    ("PU", "SD"),
    ("VV", "AUX"),
    ("VV", "SD"),
    ("VV", "CC"),
    ("SD", "VV"),
    ("SD", "IP"),
    ("IP", "VV"),
    ("VV", "IP"),
    ("IP", "MR"),
    ("MR", "VV"),
    ("VV", "MR"),
]

def extract_features_v2(sample: COTSample) -> tuple[np.ndarray, list[str]]:
    features = []
    names = []
    raw = sample.raw_sequence
    compressed = sample.compressed_sequence
    dist = sample.category_distribution

    def add(name: str, value: float) -> None:
        names.append(name)
        features.append(value)

    for cat in CATEGORIES:
        add(f"dist_{cat}", dist.get(cat, 0))

    add("len_raw", len(raw))
    add("compress_ratio", len(compressed) / max(len(raw), 1))

    transitions = Counter(zip(raw[:-1], raw[1:])) if len(raw) > 1 else Counter()
    total_trans = sum(transitions.values()) or 1
    for from_cat, to_cat in KEY_TRANSITIONS:
        add(f"trans_{from_cat}->{to_cat}", transitions.get((from_cat, to_cat), 0) / total_trans)

    self_loops = sum(1 for i in range(len(raw) - 1) if raw[i] == raw[i + 1])
    vv_loops = sum(1 for i in range(len(raw) - 2)
                   if raw[i] == "VV" and raw[i + 2] == "VV")
    sd_loops = sum(1 for i in range(len(raw) - 2)
                   if raw[i] == "SD" and raw[i + 2] == "SD")
    add("self_loop_ratio", self_loops / max(len(raw) - 1, 1))
    add("vv_iteration_ratio", vv_loops / max(len(raw) - 2, 1))
    add("sd_iteration_ratio", sd_loops / max(len(raw) - 2, 1))

    n = len(raw)
    first_end = max(1, int(n * 0.25))
    mid_start = first_end
    mid_end = max(mid_start + 1, int(n * 0.75))
    last_start = mid_end
    for prefix, segment in (
        ("first25pct", raw[:first_end]),
        ("mid50pct", raw[mid_start:mid_end]),
        ("last25pct", raw[last_start:] if last_start < n else raw[-1:]),
    ):
        counter = Counter(segment)
        total = len(segment) or 1
        for cat in CATEGORIES:
            add(f"{prefix}_{cat}", counter.get(cat, 0) / total)

    effort_dict = {}
    for cat, cnt in zip(compressed, sample.effort_counts):
        effort_dict.setdefault(cat, []).append(cnt)

    for cat in ["PU", "VV", "SD", "AUX"]:
        values = effort_dict.get(cat, [])
        add(f"effort_{cat}", np.mean(values) if values else 0)

    add("vv_density", dist.get("VV", 0) * len(compressed))
    add("design_ratio", dist.get("SD", 0) + dist.get("IP", 0))
    add("reflection_ratio", dist.get("MR", 0))
    add("code_output_ratio", dist.get("CC", 0))

    return np.array(features, dtype=float), names

def build_dataset(all_samples: dict[str, list[COTSample]]) -> tuple[np.ndarray, np.ndarray, list[str]]:
    X_list = []
    y_list = []
    feature_names = None
    for task_type, samples in all_samples.items():
        for s in samples:
            feats, names = extract_features_v2(s)
            X_list.append(feats)
            y_list.append(task_type)
            if feature_names is None:
                feature_names = names
    return np.array(X_list), np.array(y_list), feature_names

def analyze_feature_importance(X, y, feature_names):
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.feature_selection import mutual_info_classif
    from sklearn.preprocessing import LabelEncoder

    le = LabelEncoder()
    y_encoded = le.fit_transform(y)

    mi_scores = mutual_info_classif(X, y_encoded, random_state=42)
    mi_ranking = sorted(zip(feature_names, mi_scores), key=lambda x: -x[1])

    rf = RandomForestClassifier(n_estimators=100, max_depth=10, random_state=42)
    rf.fit(X, y_encoded)
    rf_ranking = sorted(zip(feature_names, rf.feature_importances_), key=lambda x: -x[1])

    return mi_ranking, rf_ranking

def train_and_evaluate(all_samples: dict[str, list[COTSample]], output_dir: Path):
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.linear_model import LogisticRegression
    from sklearn.metrics import confusion_matrix
    from sklearn.model_selection import StratifiedKFold, cross_val_score
    from sklearn.preprocessing import LabelEncoder, StandardScaler

    output_dir.mkdir(parents=True, exist_ok=True)

    X, y, feature_names = build_dataset(all_samples)
    le = LabelEncoder()
    y_encoded = le.fit_transform(y)

    print(f"Dataset: {X.shape[0]} samples, {X.shape[1]} features")
    print(f"Classes: {list(le.classes_)}")
    print(f"Class distribution: {dict(Counter(y))}\n")
    print(f"Features: {feature_names}\n")

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    cv = StratifiedKFold(5, shuffle=True, random_state=42)

    lr = LogisticRegression(penalty="l2", max_iter=2000, C=1.0)
    lr_scores = cross_val_score(lr, X_scaled, y_encoded, cv=cv)
    print(f"Logistic Regression: {lr_scores.mean():.3f} (+/- {lr_scores.std():.3f})")

    rf = RandomForestClassifier(n_estimators=100, max_depth=8, random_state=42, min_samples_leaf=5)
    rf_scores = cross_val_score(rf, X, y_encoded, cv=cv)
    print(f"Random Forest: {rf_scores.mean():.3f} (+/- {rf_scores.std():.3f})")

    mi_ranking, rf_ranking = analyze_feature_importance(X, y, feature_names)

    print("\n=== Feature Importance (Mutual Information) ===")
    for name, score in mi_ranking[:15]:
        print(f"  {name}: {score:.4f}")

    print("\n=== Feature Importance (Random Forest) ===")
    for name, score in rf_ranking[:15]:
        print(f"  {name}: {score:.4f}")

    rf.fit(X, y_encoded)
    y_pred = rf.predict(X)
    cm = confusion_matrix(y_encoded, y_pred)

    print("\n=== Confusion Matrix ===")
    print(f"Labels: {list(le.classes_)}")
    print(cm)

    print("\n=== Per-Class Metrics ===")
    for i, cls in enumerate(le.classes_):
        tp = cm[i, i]
        fp = cm[:, i].sum() - tp
        fn = cm[i, :].sum() - tp
        precision = tp / (tp + fp) if (tp + fp) > 0 else 0
        recall = tp / (tp + fn) if (tp + fn) > 0 else 0
        f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0
        print(f"  {cls}: P={precision:.3f}, R={recall:.3f}, F1={f1:.3f}")

    results = {
        "num_features": len(feature_names),
        "feature_names": feature_names,
        "logistic_regression_accuracy": round(lr_scores.mean(), 4),
        "logistic_regression_std": round(lr_scores.std(), 4),
        "random_forest_accuracy": round(rf_scores.mean(), 4),
        "random_forest_std": round(rf_scores.std(), 4),
        "feature_importance_mi": {name: round(score, 4) for name, score in mi_ranking},
        "feature_importance_rf": {name: round(score, 4) for name, score in rf_ranking},
        "confusion_matrix": cm.tolist(),
        "labels": list(le.classes_)
    }
    (output_dir / "classifier_results.json").write_text(json.dumps(results, indent=2), encoding="utf-8")
    print(f"\nSaved: {output_dir / 'classifier_results.json'}")

if __name__ == "__main__":
    root = Path(__file__).resolve().parents[2]
    base_dir = root / "data" / "derived_cot" / "rq1_segmented"
    output_dir = root / "data" / "derived_cot" / "rq3_task_identification" / "default" / "classifier_analysis"
    all_samples = load_all_tasks(base_dir)
    train_and_evaluate(all_samples, output_dir)
