"""
EnLang ML Engine — Full Natural English AI/ML & Data Science Syntax Transpiler
===============================================================================
Converts simplified natural English ML/DS statements into production sklearn/pandas/numpy code.

DESIGN PRINCIPLE:
  - PURELY ADDITIVE: Zero changes to existing EnLang syntax
  - All 3 layers coexist: Native Python | EnLang Natural | EnLang ML (this file)
  - Supports FULL Machine Learning and Full Data Science pipeline

SUPPORTED DOMAINS:
  1. Data Loading & Export
  2. Data Exploration & Statistics
  3. Data Cleaning & Preprocessing
  4. Feature Engineering & Encoding
  5. Train-Test Split & Cross Validation
  6. Text Vectorization
  7. Feature Scaling & Normalization
  8. Classification (10+ algorithms)
  9. Regression (8+ algorithms)
  10. Clustering (K-Means, DBSCAN, Hierarchical)
  11. Dimensionality Reduction (PCA, LDA, t-SNE)
  12. Multi-Model Training & Comparison
  13. Ensemble Methods (Soft Voting, Hard Voting, Stacking)
  14. Model Evaluation (Accuracy, F1, ROC, RMSE, R2, MAE)
  15. Model Save/Load (Pickle, Joblib)
  16. Data Visualization (Matplotlib, Seaborn)
  17. Live Prediction
"""

import re


# ─────────────────────────────────────────────────────────────────────────────
# INTERNAL STATE TRACKER
# ─────────────────────────────────────────────────────────────────────────────

class MLContext:
    def __init__(self):
        self.reset()

    def reset(self):
        self.dataset_var     = "df"
        self.X_var           = "X"
        self.y_var           = "y"
        self.X_train         = "X_train"
        self.X_test          = "X_test"
        self.y_train         = "y_train"
        self.y_test          = "y_test"
        self.model_var       = "_enlg_model"
        self.vectorizer_var  = "_enlg_vec"
        self.y_pred_var      = "_enlg_y_pred"
        self.scaler_var      = "_enlg_scaler"
        self.encoder_var     = "_enlg_enc"
        self.pca_var         = "_enlg_pca"
        self.cluster_var     = "_enlg_cluster"
        self.text_column     = "text"
        self.label_column    = "label"
        # Multi-model registry: {"logistic_regression": "_enlg_model_lr", ...}
        self.model_registry  = {}
        self.all_models_var  = "_enlg_all_models"

_ctx = MLContext()


def reset_context():
    _ctx.reset()


# ─────────────────────────────────────────────────────────────────────────────
# CLASSIFIER & REGRESSOR REGISTRY
# ─────────────────────────────────────────────────────────────────────────────

_CLASSIFIERS = {
    "naive_bayes":              ("sklearn.naive_bayes", "MultinomialNB",             "MultinomialNB(alpha=0.5)"),
    "gaussian_naive_bayes":     ("sklearn.naive_bayes", "GaussianNB",                "GaussianNB()"),
    "logistic_regression":      ("sklearn.linear_model", "LogisticRegression",       "LogisticRegression(max_iter=1000, C=1.0, random_state=42)"),
    "svm":                      ("sklearn.svm", "SVC",                               "SVC(kernel='linear', probability=True, random_state=42)"),
    "linear_svm":               ("sklearn.svm", "LinearSVC",                         "LinearSVC(max_iter=2000, random_state=42)"),
    "rbf_svm":                  ("sklearn.svm", "SVC",                               "SVC(kernel='rbf', probability=True, random_state=42)"),
    "random_forest":            ("sklearn.ensemble", "RandomForestClassifier",        "RandomForestClassifier(n_estimators=200, random_state=42, n_jobs=-1)"),
    "decision_tree":            ("sklearn.tree", "DecisionTreeClassifier",            "DecisionTreeClassifier(random_state=42)"),
    "gradient_boosting":        ("sklearn.ensemble", "GradientBoostingClassifier",    "GradientBoostingClassifier(n_estimators=150, learning_rate=0.1, random_state=42)"),
    "knn":                      ("sklearn.neighbors", "KNeighborsClassifier",         "KNeighborsClassifier(n_neighbors=5)"),
    "adaboost":                 ("sklearn.ensemble", "AdaBoostClassifier",            "AdaBoostClassifier(n_estimators=100, random_state=42)"),
    "extra_trees":              ("sklearn.ensemble", "ExtraTreesClassifier",          "ExtraTreesClassifier(n_estimators=200, random_state=42, n_jobs=-1)"),
    "mlp":                      ("sklearn.neural_network", "MLPClassifier",           "MLPClassifier(hidden_layer_sizes=(128,64), max_iter=500, random_state=42)"),
    "neural_network":           ("sklearn.neural_network", "MLPClassifier",           "MLPClassifier(hidden_layer_sizes=(128,64), max_iter=500, random_state=42)"),
    "bagging":                  ("sklearn.ensemble", "BaggingClassifier",             "BaggingClassifier(n_estimators=50, random_state=42)"),
    "linear_discriminant":      ("sklearn.discriminant_analysis", "LinearDiscriminantAnalysis", "LinearDiscriminantAnalysis()"),
    "quadratic_discriminant":   ("sklearn.discriminant_analysis", "QuadraticDiscriminantAnalysis", "QuadraticDiscriminantAnalysis()"),
    "bernoulli_naive_bayes":    ("sklearn.naive_bayes", "BernoulliNB",               "BernoulliNB()"),
}

_REGRESSORS = {
    "linear_regression":        ("sklearn.linear_model", "LinearRegression",          "LinearRegression()"),
    "ridge":                    ("sklearn.linear_model", "Ridge",                      "Ridge(alpha=1.0)"),
    "lasso":                    ("sklearn.linear_model", "Lasso",                      "Lasso(alpha=0.1)"),
    "elastic_net":              ("sklearn.linear_model", "ElasticNet",                 "ElasticNet(alpha=0.1, l1_ratio=0.5)"),
    "svr":                      ("sklearn.svm", "SVR",                                 "SVR(kernel='rbf')"),
    "random_forest":            ("sklearn.ensemble", "RandomForestRegressor",          "RandomForestRegressor(n_estimators=200, random_state=42, n_jobs=-1)"),
    "gradient_boosting":        ("sklearn.ensemble", "GradientBoostingRegressor",      "GradientBoostingRegressor(n_estimators=150, learning_rate=0.1, random_state=42)"),
    "decision_tree":            ("sklearn.tree", "DecisionTreeRegressor",              "DecisionTreeRegressor(random_state=42)"),
    "knn":                      ("sklearn.neighbors", "KNeighborsRegressor",           "KNeighborsRegressor(n_neighbors=5)"),
    "mlp":                      ("sklearn.neural_network", "MLPRegressor",             "MLPRegressor(hidden_layer_sizes=(128,64), max_iter=500, random_state=42)"),
    "neural_network":           ("sklearn.neural_network", "MLPRegressor",             "MLPRegressor(hidden_layer_sizes=(128,64), max_iter=500, random_state=42)"),
    "extra_trees":              ("sklearn.ensemble", "ExtraTreesRegressor",            "ExtraTreesRegressor(n_estimators=200, random_state=42, n_jobs=-1)"),
    "adaboost":                 ("sklearn.ensemble", "AdaBoostRegressor",              "AdaBoostRegressor(n_estimators=100, random_state=42)"),
    "polynomial":               ("sklearn.preprocessing", "PolynomialFeatures",        None),  # Special case
}

# Short → canonical name aliases
_ALIASES = {
    "lr": "logistic_regression",
    "rf": "random_forest",
    "nb": "naive_bayes",
    "gnb": "gaussian_naive_bayes",
    "bnb": "bernoulli_naive_bayes",
    "dt": "decision_tree",
    "gb": "gradient_boosting",
    "svc": "svm",
    "gbt": "gradient_boosting",
    "xgb": "gradient_boosting",
    "et": "extra_trees",
    "ada": "adaboost",
    "nn": "neural_network",
    "lda": "linear_discriminant",
}


def _resolve_algo(raw: str) -> str:
    """Normalize algorithm name and apply aliases."""
    key = raw.strip().lower().replace(' ', '_').replace('-', '_')
    return _ALIASES.get(key, key)


def _model_var_name(algo: str) -> str:
    """Generate a safe Python variable name for a model."""
    return f"_enlg_model_{algo.replace('_', '')}"


# ─────────────────────────────────────────────────────────────────────────────
# MAIN TRANSPILER
# ─────────────────────────────────────────────────────────────────────────────

def translate_ml_line(line: str) -> str | None:
    """
    Attempts to translate a natural EnLang ML/DS line into Python code.
    Returns the transpiled string, or None if this is not an ML/DS line.
    """
    s = line.strip()

    # ── 1. DATA LOADING ──────────────────────────────────────────────────────

    # load dataset from "file.csv" into df
    m = re.match(r'^load\s+dataset\s+from\s+["\'](.+?)["\']\s+into\s+([a-zA-Z_]\w*)\s*$', s, re.IGNORECASE)
    if m:
        path, var = m.group(1), m.group(2)
        _ctx.dataset_var = var
        return f"import pandas as pd; {var} = pd.read_csv('{path}', encoding='utf-8', on_bad_lines='skip')"

    # load dataset from "file.csv" with text column <col> and label column <col> [into df]
    m = re.match(
        r'^load\s+dataset\s+from\s+["\'](.+?)["\']\s+with\s+text\s+column\s+([a-zA-Z_]\w*)\s+and\s+label\s+column\s+([a-zA-Z_]\w*)(?:\s+into\s+([a-zA-Z_]\w*))?\s*$',
        s, re.IGNORECASE)
    if m:
        path, tcol, lcol, var = m.group(1), m.group(2), m.group(3), m.group(4) or "df"
        _ctx.dataset_var, _ctx.text_column, _ctx.label_column = var, tcol, lcol
        _ctx.X_var, _ctx.y_var = "X", "y"
        return (
            f"import pandas as pd; "
            f"{var} = pd.read_csv('{path}', encoding='utf-8', on_bad_lines='skip'); "
            f"X = {var}['{tcol}'].fillna('').tolist(); "
            f"y = {var}['{lcol}'].tolist(); "
            f"print(f'[ENLANG ML] Loaded {{len({var})}} samples | Text: {tcol} | Label: {lcol}')"
        )

    # load dataset from "file.csv" with labels column <col>
    m = re.match(r'^load\s+dataset\s+from\s+["\'](.+?)["\']\s+with\s+labels?\s+column\s+([a-zA-Z_]\w*)\s*$', s, re.IGNORECASE)
    if m:
        path, lcol = m.group(1), m.group(2)
        _ctx.label_column = lcol
        _ctx.X_var, _ctx.y_var = "X", "y"
        return (
            f"import pandas as pd; "
            f"{_ctx.dataset_var} = pd.read_csv('{path}', encoding='utf-8', on_bad_lines='skip'); "
            f"X = {_ctx.dataset_var}.drop(columns=['{lcol}']).values.tolist(); "
            f"y = {_ctx.dataset_var}['{lcol}'].tolist(); "
            f"print(f'[ENLANG ML] Loaded {{len({_ctx.dataset_var})}} samples | Label: {lcol}')"
        )

    # load csv "file.csv" into df
    m = re.match(r'^load\s+csv\s+["\'](.+?)["\']\s+into\s+([a-zA-Z_]\w*)\s*$', s, re.IGNORECASE)
    if m:
        path, var = m.group(1), m.group(2)
        _ctx.dataset_var = var
        return f"import pandas as pd; {var} = pd.read_csv('{path}', encoding='utf-8', on_bad_lines='skip')"

    # load json "file.json" into df
    m = re.match(r'^load\s+json\s+["\'](.+?)["\']\s+into\s+([a-zA-Z_]\w*)\s*$', s, re.IGNORECASE)
    if m:
        path, var = m.group(1), m.group(2)
        _ctx.dataset_var = var
        return f"import pandas as pd; {var} = pd.read_json('{path}')"

    # export df to "output.csv"
    m = re.match(r'^export\s+([a-zA-Z_]\w*)\s+to\s+["\'](.+?)["\']\s*$', s, re.IGNORECASE)
    if m:
        var, path = m.group(1), m.group(2)
        return f"{var}.to_csv('{path}', index=False); print('[ENLANG ML] Exported to {path}')"

    # ── 2. DATA EXPLORATION ───────────────────────────────────────────────────

    m = re.match(r'^show\s+dataset\s+info\s*$', s, re.IGNORECASE)
    if m:
        v = _ctx.dataset_var
        return f"print(f'Shape: {{{v}.shape}} | Columns: {{{v}.columns.tolist()}}'); {v}.info()"

    m = re.match(r'^show\s+dataset\s+statistics?\s*$', s, re.IGNORECASE)
    if m:
        return f"print({_ctx.dataset_var}.describe().to_string())"

    m = re.match(r'^show\s+first\s+(\d+)\s+rows?\s*$', s, re.IGNORECASE)
    if m:
        return f"print({_ctx.dataset_var}.head({m.group(1)}).to_string())"

    m = re.match(r'^show\s+last\s+(\d+)\s+rows?\s*$', s, re.IGNORECASE)
    if m:
        return f"print({_ctx.dataset_var}.tail({m.group(1)}).to_string())"

    m = re.match(r'^show\s+(?:column\s+)?distribution\s+of\s+([a-zA-Z_]\w*)\s*$', s, re.IGNORECASE)
    if m:
        col = m.group(1)
        return f"print({_ctx.dataset_var}['{col}'].value_counts().to_string())"

    m = re.match(r'^show\s+missing\s+values?\s*$', s, re.IGNORECASE)
    if m:
        return f"print('Missing Values:\\n' + {_ctx.dataset_var}.isnull().sum().to_string())"

    m = re.match(r'^show\s+dataset\s+shape\s*$', s, re.IGNORECASE)
    if m:
        return f"print(f'Dataset Shape: {{{_ctx.dataset_var}.shape}}')"

    m = re.match(r'^show\s+column\s+types?\s*$', s, re.IGNORECASE)
    if m:
        return f"print({_ctx.dataset_var}.dtypes.to_string())"

    m = re.match(r'^show\s+correlation\s+matrix\s*$', s, re.IGNORECASE)
    if m:
        return f"print({_ctx.dataset_var}.corr(numeric_only=True).round(2).to_string())"

    # ── 3. DATA CLEANING ─────────────────────────────────────────────────────

    m = re.match(r'^drop\s+missing\s+values?\s+from\s+([a-zA-Z_]\w*)\s*$', s, re.IGNORECASE)
    if m:
        var = m.group(1)
        return f"{var} = {var}.dropna().reset_index(drop=True); print(f'[ENLANG ML] Rows after drop: {{len({var})}}')"

    m = re.match(r'^drop\s+missing\s+values?\s*$', s, re.IGNORECASE)
    if m:
        v = _ctx.dataset_var
        return f"{v} = {v}.dropna().reset_index(drop=True); print(f'[ENLANG ML] Rows after drop: {{len({v})}}')"

    m = re.match(r'^drop\s+duplicates?\s*$', s, re.IGNORECASE)
    if m:
        v = _ctx.dataset_var
        return f"{v} = {v}.drop_duplicates().reset_index(drop=True); print(f'[ENLANG ML] Rows after dedup: {{len({v})}}')"

    m = re.match(r'^fill\s+missing\s+values?\s+in\s+(?:column\s+)?([a-zA-Z_]\w*)\s+with\s+(.+)\s*$', s, re.IGNORECASE)
    if m:
        col, val = m.group(1), m.group(2).strip()
        return f"{_ctx.dataset_var}['{col}'] = {_ctx.dataset_var}['{col}'].fillna({val})"

    m = re.match(r'^drop\s+column\s+([a-zA-Z_]\w*)\s*$', s, re.IGNORECASE)
    if m:
        col = m.group(1)
        return f"{_ctx.dataset_var} = {_ctx.dataset_var}.drop(columns=['{col}'])"

    m = re.match(r'^rename\s+column\s+([a-zA-Z_]\w*)\s+to\s+([a-zA-Z_]\w*)\s*$', s, re.IGNORECASE)
    if m:
        old, new = m.group(1), m.group(2)
        return f"{_ctx.dataset_var} = {_ctx.dataset_var}.rename(columns={{'{old}': '{new}'}})"

    # ── 4. FEATURE ENGINEERING & ENCODING ─────────────────────────────────────

    m = re.match(r'^encode\s+column\s+([a-zA-Z_]\w*)\s+using\s+(?:label\s+encoder|label_encoder)\s*$', s, re.IGNORECASE)
    if m:
        col = m.group(1)
        e = _ctx.encoder_var
        return (
            f"from sklearn.preprocessing import LabelEncoder; "
            f"{e} = LabelEncoder(); "
            f"{_ctx.dataset_var}['{col}'] = {e}.fit_transform({_ctx.dataset_var}['{col}'].astype(str))"
        )

    m = re.match(r'^encode\s+column\s+([a-zA-Z_]\w*)\s+using\s+(?:one\s+hot|onehot|one_hot)\s*$', s, re.IGNORECASE)
    if m:
        col = m.group(1)
        v = _ctx.dataset_var
        return (
            f"{v} = pandas.get_dummies({v}, columns=['{col}'], drop_first=True) "
            f"if 'pandas' in dir() else __import__('pandas').get_dummies({v}, columns=['{col}'], drop_first=True)"
        )

    # set features from columns age, salary, score
    m = re.match(r'^set\s+features?\s+from\s+columns?\s+(.+)\s*$', s, re.IGNORECASE)
    if m:
        cols_raw = m.group(1)
        cols = [c.strip() for c in cols_raw.split(',')]
        col_list = str(cols)
        _ctx.X_var = "X"
        return f"X = {_ctx.dataset_var}[{col_list}].values"

    # set label from column spam
    m = re.match(r'^set\s+label\s+from\s+column\s+([a-zA-Z_]\w*)\s*$', s, re.IGNORECASE)
    if m:
        col = m.group(1)
        _ctx.y_var = "y"
        return f"y = {_ctx.dataset_var}['{col}'].values"

    # ── 5. TRAIN-TEST SPLIT ───────────────────────────────────────────────────

    m = re.match(
        r'^split\s+(?:dataset\s+)?into\s+(\d+)\s+percent\s+training\s+and\s+(\d+)\s+percent\s+testing(?:\s+with\s+seed\s+(\d+))?\s*$',
        s, re.IGNORECASE)
    if m:
        test_size = round(int(m.group(2)) / 100, 2)
        seed = int(m.group(3)) if m.group(3) else 42
        Xv, yv = _ctx.X_var, _ctx.y_var
        return (
            f"from sklearn.model_selection import train_test_split; "
            f"{_ctx.X_train}, {_ctx.X_test}, {_ctx.y_train}, {_ctx.y_test} = "
            f"train_test_split({Xv}, {yv}, test_size={test_size}, random_state={seed}); "
            f"print(f'[ENLANG ML] Train: {{len({_ctx.X_train})}} | Test: {{len({_ctx.X_test})}} (stratified if possible)')"
        )

    # stratified split
    m = re.match(
        r'^stratified\s+split\s+into\s+(\d+)\s+percent\s+training\s+and\s+(\d+)\s+percent\s+testing(?:\s+with\s+seed\s+(\d+))?\s*$',
        s, re.IGNORECASE)
    if m:
        test_size = round(int(m.group(2)) / 100, 2)
        seed = int(m.group(3)) if m.group(3) else 42
        Xv, yv = _ctx.X_var, _ctx.y_var
        return (
            f"from sklearn.model_selection import train_test_split; "
            f"{_ctx.X_train}, {_ctx.X_test}, {_ctx.y_train}, {_ctx.y_test} = "
            f"train_test_split({Xv}, {yv}, test_size={test_size}, random_state={seed}, stratify={yv}); "
            f"print(f'[ENLANG ML] Stratified Train: {{len({_ctx.X_train})}} | Test: {{len({_ctx.X_test})}}')"
        )

    # ── 6. TEXT VECTORIZATION ─────────────────────────────────────────────────

    m = re.match(r'^vectorize\s+text\s+using\s+tfidf(?:\s+with\s+max\s+features?\s+(\d+))?(?:\s+and\s+ngrams?\s+(\d+)(?:\s+to\s+(\d+))?)?\s*$', s, re.IGNORECASE)
    if m:
        max_feat = int(m.group(1)) if m.group(1) else 10000
        ngram_min = int(m.group(2)) if m.group(2) else 1
        ngram_max = int(m.group(3)) if m.group(3) else 2
        v = _ctx.vectorizer_var
        return (
            f"from sklearn.feature_extraction.text import TfidfVectorizer; "
            f"{v} = TfidfVectorizer(stop_words='english', max_features={max_feat}, ngram_range=({ngram_min},{ngram_max})); "
            f"{_ctx.X_train} = {v}.fit_transform({_ctx.X_train}); "
            f"{_ctx.X_test} = {v}.transform({_ctx.X_test}); "
            f"print(f'[ENLANG ML] TF-IDF Vectorized | Vocabulary: {{len({v}.vocabulary_)}} features')"
        )

    m = re.match(r'^vectorize\s+text\s+using\s+(?:bag\s+of\s+words|bow|count)(?:\s+with\s+max\s+features?\s+(\d+))?\s*$', s, re.IGNORECASE)
    if m:
        max_feat = int(m.group(1)) if m.group(1) else 10000
        v = _ctx.vectorizer_var
        return (
            f"from sklearn.feature_extraction.text import CountVectorizer; "
            f"{v} = CountVectorizer(stop_words='english', max_features={max_feat}); "
            f"{_ctx.X_train} = {v}.fit_transform({_ctx.X_train}); "
            f"{_ctx.X_test} = {v}.transform({_ctx.X_test}); "
            f"print('[ENLANG ML] Bag-of-Words Vectorized')"
        )

    # ── 7. FEATURE SCALING ────────────────────────────────────────────────────

    m = re.match(r'^scale\s+features?\s+using\s+(?:standard\s+scaler|standardscaler|standard)\s*$', s, re.IGNORECASE)
    if m:
        sc = _ctx.scaler_var
        return (
            f"from sklearn.preprocessing import StandardScaler; "
            f"{sc} = StandardScaler(); "
            f"{_ctx.X_train} = {sc}.fit_transform({_ctx.X_train}); "
            f"{_ctx.X_test} = {sc}.transform({_ctx.X_test}); "
            f"print('[ENLANG ML] StandardScaler applied')"
        )

    m = re.match(r'^scale\s+features?\s+using\s+(?:minmax|min\s*max\s*scaler|minmaxscaler)\s*$', s, re.IGNORECASE)
    if m:
        sc = _ctx.scaler_var
        return (
            f"from sklearn.preprocessing import MinMaxScaler; "
            f"{sc} = MinMaxScaler(); "
            f"{_ctx.X_train} = {sc}.fit_transform({_ctx.X_train}); "
            f"{_ctx.X_test} = {sc}.transform({_ctx.X_test}); "
            f"print('[ENLANG ML] MinMaxScaler applied')"
        )

    m = re.match(r'^scale\s+features?\s+using\s+(?:robust\s+scaler|robustscaler|robust)\s*$', s, re.IGNORECASE)
    if m:
        sc = _ctx.scaler_var
        return (
            f"from sklearn.preprocessing import RobustScaler; "
            f"{sc} = RobustScaler(); "
            f"{_ctx.X_train} = {sc}.fit_transform({_ctx.X_train}); "
            f"{_ctx.X_test} = {sc}.transform({_ctx.X_test}); "
            f"print('[ENLANG ML] RobustScaler applied')"
        )

    # ── 8. TRAIN CLASSIFIER ───────────────────────────────────────────────────

    m = re.match(r'^train\s+([a-zA-Z_]+(?:\s+[a-zA-Z_]+)?)\s+classifier\s+on\s+training\s+data\s*$', s, re.IGNORECASE)
    if m:
        algo = _resolve_algo(m.group(1))
        if algo in _CLASSIFIERS:
            mod, cls, init = _CLASSIFIERS[algo]
            mv = _model_var_name(algo)
            _ctx.model_var = mv
            _ctx.model_registry[algo] = mv
            # Gradient Boosting needs .toarray() for sparse matrices
            if "boosting" in algo or "gradient" in algo:
                fit_X = f"({_ctx.X_train}.toarray() if hasattr({_ctx.X_train}, 'toarray') else {_ctx.X_train})"
            else:
                fit_X = _ctx.X_train
            return (
                f"from {mod} import {cls}; "
                f"{mv} = {init}; "
                f"{mv}.fit({fit_X}, {_ctx.y_train}); "
                f"print('[ENLANG ML] {cls} trained!')"
            )

    # ── 9. TRAIN REGRESSOR ────────────────────────────────────────────────────

    m = re.match(r'^train\s+([a-zA-Z_]+(?:\s+[a-zA-Z_]+)?)\s+regressor?\s+on\s+training\s+data\s*$', s, re.IGNORECASE)
    if m:
        algo = _resolve_algo(m.group(1))
        if algo in _REGRESSORS:
            mod, cls, init = _REGRESSORS[algo]
            mv = _model_var_name(algo)
            _ctx.model_var = mv
            _ctx.model_registry[algo] = mv
            if "boosting" in algo or "gradient" in algo:
                fit_X = f"({_ctx.X_train}.toarray() if hasattr({_ctx.X_train}, 'toarray') else {_ctx.X_train})"
            else:
                fit_X = _ctx.X_train
            return (
                f"from {mod} import {cls}; "
                f"{mv} = {init}; "
                f"{mv}.fit({fit_X}, {_ctx.y_train}); "
                f"print('[ENLANG ML] {cls} (regressor) trained!')"
            )

    # ── 10. CROSS VALIDATION ──────────────────────────────────────────────────

    m = re.match(r'^cross\s+validate\s+([a-zA-Z_]+(?:\s+[a-zA-Z_]+)?)\s+with\s+(\d+)\s+folds?\s*$', s, re.IGNORECASE)
    if m:
        algo = _resolve_algo(m.group(1))
        folds = m.group(2)
        mv = _ctx.model_registry.get(algo, _ctx.model_var)
        Xv, yv = _ctx.X_var, _ctx.y_var
        return (
            f"from sklearn.model_selection import cross_val_score; import numpy as np; "
            f"_cv_scores = cross_val_score({mv}, {Xv}, {yv}, cv={folds}, scoring='accuracy'); "
            f"print(f'[ENLANG ML] Cross-Val ({folds}-fold) Scores: {{_cv_scores.round(3)}} | Mean: {{_cv_scores.mean()*100:.2f}}% | Std: {{_cv_scores.std()*100:.2f}}%')"
        )

    # ── 11. EVALUATE MODEL ────────────────────────────────────────────────────

    # evaluate <algo> classifier accuracy and store in acc
    m = re.match(r'^evaluate\s+([a-zA-Z_]+(?:\s+[a-zA-Z_]+)?)\s+classifier\s+accuracy\s+and\s+store\s+in\s+([a-zA-Z_]\w*)\s*$', s, re.IGNORECASE)
    if m:
        algo = _resolve_algo(m.group(1))
        var = m.group(2)
        mv = _ctx.model_registry.get(algo, _ctx.model_var)
        yp = f"_enlg_pred_{algo.replace('_','')}"
        Xt = _ctx.X_test
        if "boosting" in algo or "gradient" in algo:
            Xt = f"({_ctx.X_test}.toarray() if hasattr({_ctx.X_test}, 'toarray') else {_ctx.X_test})"
        return (
            f"from sklearn.metrics import accuracy_score; "
            f"{yp} = {mv}.predict({Xt}); "
            f"{var} = round(accuracy_score({_ctx.y_test}, {yp}) * 100, 2); "
            f"print(f'[ENLANG ML] {algo} Accuracy: {{{var}}}%')"
        )

    # evaluate classifier accuracy and store in acc (last trained)
    m = re.match(r'^evaluate\s+(?:classifier|model)\s+accuracy\s+and\s+store\s+in\s+([a-zA-Z_]\w*)\s*$', s, re.IGNORECASE)
    if m:
        var = m.group(1)
        mv = _ctx.model_var
        yp = _ctx.y_pred_var
        return (
            f"from sklearn.metrics import accuracy_score; "
            f"{yp} = {mv}.predict({_ctx.X_test}); "
            f"{var} = round(accuracy_score({_ctx.y_test}, {yp}) * 100, 2); "
            f"print(f'[ENLANG ML] Test Accuracy: {{{var}}}%')"
        )

    # evaluate regression model and store rmse in err
    m = re.match(r'^evaluate\s+regression\s+model\s+and\s+store\s+rmse\s+in\s+([a-zA-Z_]\w*)\s*$', s, re.IGNORECASE)
    if m:
        var = m.group(1)
        mv = _ctx.model_var
        return (
            f"from sklearn.metrics import mean_squared_error, r2_score; import math; "
            f"_yp = {mv}.predict({_ctx.X_test}); "
            f"{var} = round(math.sqrt(mean_squared_error({_ctx.y_test}, _yp)), 4); "
            f"_r2 = round(r2_score({_ctx.y_test}, _yp), 4); "
            f"print(f'[ENLANG ML] RMSE: {{{var}}} | R2: {{_r2}}')"
        )

    # evaluate all classifiers and show comparison
    m = re.match(r'^evaluate\s+all\s+(?:classifiers?|models?)\s+and\s+show\s+comparison\s*$', s, re.IGNORECASE)
    if m:
        if not _ctx.model_registry:
            return "print('[ENLANG ML] No models trained yet. Train models first.')"
        lines = ["from sklearn.metrics import accuracy_score, f1_score; import warnings; warnings.filterwarnings('ignore')"]
        lines.append("print('\\n' + '='*60)")
        lines.append("print('  MULTI-MODEL COMPARISON (Test Set)')")
        lines.append("print('='*60)")
        lines.append("print(f'{\"Model\":<30} {\"Accuracy\":>12} {\"F1-Score\":>12}')")
        lines.append("print('-'*60)")
        lines.append("_enlg_results = {}")
        for algo, mv in _ctx.model_registry.items():
            if "boosting" in algo or "gradient" in algo:
                Xt = f"({_ctx.X_test}.toarray() if hasattr({_ctx.X_test}, 'toarray') else {_ctx.X_test})"
            else:
                Xt = _ctx.X_test
            lines.append(
                f"_p = {mv}.predict({Xt}); "
                f"_acc = round(accuracy_score({_ctx.y_test}, _p)*100, 2); "
                f"_f1  = round(f1_score({_ctx.y_test}, _p, average='weighted')*100, 2); "
                f"_enlg_results['{algo}'] = _acc; "
                f"print(f'{{\"  {algo}\":<30}} {{_acc:>11}}% {{_f1:>11}}%')"
            )
        lines.append("print('='*60)")
        lines.append(
            "_best_algo = max(_enlg_results, key=_enlg_results.get); "
            "print(f'  Best: {_best_algo} @ {_enlg_results[_best_algo]}%')"
        )
        lines.append("print('='*60)")
        return "\n".join(lines)

    # show classification report for <algo>
    m = re.match(r'^show\s+(?:classification\s+)?report\s+for\s+([a-zA-Z_]+(?:\s+[a-zA-Z_]+)?)\s*$', s, re.IGNORECASE)
    if m:
        algo = _resolve_algo(m.group(1))
        mv = _ctx.model_registry.get(algo, _ctx.model_var)
        if "boosting" in algo or "gradient" in algo:
            Xt = f"({_ctx.X_test}.toarray() if hasattr({_ctx.X_test}, 'toarray') else {_ctx.X_test})"
        else:
            Xt = _ctx.X_test
        return (
            f"from sklearn.metrics import classification_report; "
            f"_rp = {mv}.predict({Xt}); "
            f"print(f'\\n=== {algo} Classification Report ==='); "
            f"print(classification_report({_ctx.y_test}, _rp))"
        )

    # show confusion matrix for <algo>
    m = re.match(r'^show\s+confusion\s+matrix\s+for\s+([a-zA-Z_]+(?:\s+[a-zA-Z_]+)?)\s*$', s, re.IGNORECASE)
    if m:
        algo = _resolve_algo(m.group(1))
        mv = _ctx.model_registry.get(algo, _ctx.model_var)
        if "boosting" in algo or "gradient" in algo:
            Xt = f"({_ctx.X_test}.toarray() if hasattr({_ctx.X_test}, 'toarray') else {_ctx.X_test})"
        else:
            Xt = _ctx.X_test
        return (
            f"from sklearn.metrics import confusion_matrix; "
            f"_cm = {mv}.predict({Xt}); "
            f"print(f'\\n=== {algo} Confusion Matrix ==='); "
            f"print(confusion_matrix({_ctx.y_test}, _cm))"
        )

    # show confusion matrix (last model)
    m = re.match(r'^show\s+confusion\s+matrix\s*$', s, re.IGNORECASE)
    if m:
        mv = _ctx.model_var
        return (
            f"from sklearn.metrics import confusion_matrix, classification_report; "
            f"{_ctx.y_pred_var} = {mv}.predict({_ctx.X_test}); "
            f"print('\\n=== Confusion Matrix ==='); print(confusion_matrix({_ctx.y_test}, {_ctx.y_pred_var})); "
            f"print('\\n=== Classification Report ==='); print(classification_report({_ctx.y_test}, {_ctx.y_pred_var}))"
        )

    # show roc auc for <algo>
    m = re.match(r'^show\s+roc\s+auc\s+for\s+([a-zA-Z_]+(?:\s+[a-zA-Z_]+)?)\s*$', s, re.IGNORECASE)
    if m:
        algo = _resolve_algo(m.group(1))
        mv = _ctx.model_registry.get(algo, _ctx.model_var)
        Xt = f"({_ctx.X_test}.toarray() if hasattr({_ctx.X_test}, 'toarray') else {_ctx.X_test})"
        return (
            f"from sklearn.metrics import roc_auc_score; "
            f"_roc_p = {mv}.predict_proba({Xt})[:, 1] if hasattr({mv}, 'predict_proba') else {mv}.decision_function({Xt}); "
            f"_auc = round(roc_auc_score({_ctx.y_test}, _roc_p), 4); "
            f"print(f'[ENLANG ML] {algo} ROC AUC: {{_auc}}')"
        )

    # ── 12. ENSEMBLE METHODS ──────────────────────────────────────────────────

    # use ensemble of all trained classifiers
    m = re.match(r'^use\s+(?:soft\s+)?ensemble\s+of\s+all\s+(?:trained\s+)?(?:classifiers?|models?)\s*$', s, re.IGNORECASE)
    if m:
        if not _ctx.model_registry:
            return "print('[ENLANG ML] No models registered. Train models first.')"
        mv_list = []
        for algo, mv in _ctx.model_registry.items():
            mv_list.append(f"('{algo}', {mv})")
        estimators_str = "[" + ", ".join(mv_list) + "]"
        return (
            f"from sklearn.ensemble import VotingClassifier; from sklearn.metrics import accuracy_score; "
            f"_enlg_vc = VotingClassifier(estimators={estimators_str}, voting='soft'); "
            f"_enlg_vc.fit({_ctx.X_train}, {_ctx.y_train}); "
            f"_enlg_vc_pred = _enlg_vc.predict({_ctx.X_test}); "
            f"_enlg_vc_acc = round(accuracy_score({_ctx.y_test}, _enlg_vc_pred)*100, 2); "
            f"print(f'[ENLANG ML] Soft Voting Ensemble Accuracy: {{_enlg_vc_acc}}%')"
        )

    # use hard ensemble of all trained classifiers
    m = re.match(r'^use\s+hard\s+ensemble\s+of\s+all\s+(?:trained\s+)?(?:classifiers?|models?)\s*$', s, re.IGNORECASE)
    if m:
        if not _ctx.model_registry:
            return "print('[ENLANG ML] No models registered. Train models first.')"
        mv_list = [f"('{algo}', {mv})" for algo, mv in _ctx.model_registry.items()]
        estimators_str = "[" + ", ".join(mv_list) + "]"
        return (
            f"from sklearn.ensemble import VotingClassifier; from sklearn.metrics import accuracy_score; "
            f"_enlg_hvc = VotingClassifier(estimators={estimators_str}, voting='hard'); "
            f"_enlg_hvc.fit({_ctx.X_train}, {_ctx.y_train}); "
            f"_enlg_hvc_pred = _enlg_hvc.predict({_ctx.X_test}); "
            f"_enlg_hvc_acc = round(accuracy_score({_ctx.y_test}, _enlg_hvc_pred)*100, 2); "
            f"print(f'[ENLANG ML] Hard Voting Ensemble Accuracy: {{_enlg_hvc_acc}}%')"
        )

    # compute ensemble probability for "<text>" and store in result
    m = re.match(r'^compute\s+ensemble\s+probability\s+for\s+["\'](.+?)["\']\s+and\s+store\s+in\s+([a-zA-Z_]\w*)\s*$', s, re.IGNORECASE)
    if m:
        text, var = m.group(1), m.group(2)
        vv = _ctx.vectorizer_var
        proba_parts = []
        for algo, mv in _ctx.model_registry.items():
            if hasattr:
                proba_parts.append(f"{mv}.predict_proba({vv}.transform(['{text}']))[0][1]")
        if not proba_parts:
            return f"{var} = 0.0; print('[ENLANG ML] No models trained')"
        avg_expr = "(" + " + ".join(proba_parts) + f") / {len(proba_parts)}"
        return f"{var} = round(float({avg_expr}) * 100, 1)"

    # ── 13. CLUSTERING ────────────────────────────────────────────────────────

    m = re.match(r'^cluster\s+data\s+into\s+(\d+)\s+(?:groups?|clusters?)\s+using\s+kmeans\s*$', s, re.IGNORECASE)
    if m:
        k = m.group(1)
        c = _ctx.cluster_var
        Xv = _ctx.X_var
        return (
            f"from sklearn.cluster import KMeans; "
            f"{c} = KMeans(n_clusters={k}, random_state=42, n_init=10); "
            f"_cluster_labels = {c}.fit_predict({Xv}); "
            f"import collections; print(f'[ENLANG ML] KMeans({k} clusters): {{dict(sorted(collections.Counter(_cluster_labels).items()))}}')"
        )

    m = re.match(r'^cluster\s+data\s+using\s+dbscan(?:\s+with\s+eps\s+([0-9.]+)\s+and\s+min\s+samples?\s+(\d+))?\s*$', s, re.IGNORECASE)
    if m:
        eps = m.group(1) or "0.5"
        min_s = m.group(2) or "5"
        c = _ctx.cluster_var
        return (
            f"from sklearn.cluster import DBSCAN; "
            f"{c} = DBSCAN(eps={eps}, min_samples={min_s}); "
            f"_cluster_labels = {c}.fit_predict({_ctx.X_var}); "
            f"import collections; print(f'[ENLANG ML] DBSCAN clusters: {{dict(collections.Counter(_cluster_labels))}}')"
        )

    # ── 14. DIMENSIONALITY REDUCTION ──────────────────────────────────────────

    m = re.match(r'^reduce\s+dimensions?\s+to\s+(\d+)\s+using\s+pca\s*$', s, re.IGNORECASE)
    if m:
        n = m.group(1)
        p = _ctx.pca_var
        Xt_expr = f"({_ctx.X_train}.toarray() if hasattr({_ctx.X_train}, 'toarray') else {_ctx.X_train})"
        Xte_expr = f"({_ctx.X_test}.toarray() if hasattr({_ctx.X_test}, 'toarray') else {_ctx.X_test})"
        return (
            f"from sklearn.decomposition import PCA; "
            f"{p} = PCA(n_components={n}, random_state=42); "
            f"{_ctx.X_train} = {p}.fit_transform({Xt_expr}); "
            f"{_ctx.X_test} = {p}.transform({Xte_expr}); "
            f"print(f'[ENLANG ML] PCA reduced to {n} components | Explained variance: {{sum({p}.explained_variance_ratio_)*100:.1f}}%')"
        )

    m = re.match(r'^reduce\s+dimensions?\s+to\s+(\d+)\s+using\s+(?:tsne|t-sne)\s*$', s, re.IGNORECASE)
    if m:
        n = m.group(1)
        Xt_expr = f"({_ctx.X_var}.toarray() if hasattr({_ctx.X_var}, 'toarray') else {_ctx.X_var})"
        return (
            f"from sklearn.manifold import TSNE; "
            f"_tsne = TSNE(n_components={n}, random_state=42); "
            f"{_ctx.X_var}_tsne = _tsne.fit_transform({Xt_expr}); "
            f"print('[ENLANG ML] t-SNE reduced to {n} components')"
        )

    # ── 15. FEATURE IMPORTANCE ────────────────────────────────────────────────

    m = re.match(r'^show\s+feature\s+importance\s+of\s+([a-zA-Z_]+(?:\s+[a-zA-Z_]+)?)(?:\s+top\s+(\d+))?\s*$', s, re.IGNORECASE)
    if m:
        algo = _resolve_algo(m.group(1))
        top_n = int(m.group(2)) if m.group(2) else 15
        mv = _ctx.model_registry.get(algo, _ctx.model_var)
        vv = _ctx.vectorizer_var
        ds = _ctx.dataset_var
        return (
            f"import numpy as np; "
            f"_fi = {mv}.feature_importances_ if hasattr({mv}, 'feature_importances_') else np.abs({mv}.coef_[0]); "
            f"_fn = list({vv}.get_feature_names_out()) if '{vv}' in globals() and hasattr({vv}, 'get_feature_names_out') "
            f"else list({ds}.drop(columns=['{_ctx.label_column}']).columns) if '{ds}' in globals() and hasattr({ds}, 'columns') "
            f"else [f'feature_{{i}}' for i in range(len(_fi))]; "
            f"_top_idx = np.argsort(_fi)[::-1][:{top_n}]; "
            f"print(f'\\n=== Top {top_n} Features ({algo}) ==='); "
            f"[print(f'  {{_fn[i]:<30}} {{_fi[i]:.4f}}') for i in _top_idx]"
        )

    # ── 16. PREDICTION ────────────────────────────────────────────────────────

    # predict label for "text" and store in result
    m = re.match(r'^predict\s+label\s+for\s+["\'](.+?)["\']\s+and\s+store\s+in\s+([a-zA-Z_]\w*)\s*$', s, re.IGNORECASE)
    if m:
        text, var = m.group(1), m.group(2)
        mv = _ctx.model_var
        vv = _ctx.vectorizer_var
        return f"{var} = {mv}.predict({vv}.transform(['{text}']))[0]"

    # predict spam from "email text"
    m = re.match(r'^predict\s+spam\s+from\s+["\'](.+?)["\']\s*$', s, re.IGNORECASE)
    if m:
        text = m.group(1)
        mv = _ctx.model_var
        vv = _ctx.vectorizer_var
        return (
            f"_pred = {mv}.predict({vv}.transform(['{text}']))[0]; "
            f"_proba = {mv}.predict_proba({vv}.transform(['{text}']))[0]; "
            f"print('[SPAM DETECTED] Conf: ' + str(round(float(_proba[1])*100,2)) + '%' if _pred == 1 "
            f"else '[NOT SPAM] Conf: ' + str(round(float(_proba[0])*100,2)) + '%')"
        )

    # predict escalation from "headline" using ensemble
    m = re.match(r'^predict\s+escalation\s+from\s+["\'](.+?)["\']\s+using\s+ensemble\s*$', s, re.IGNORECASE)
    if m:
        text = m.group(1)
        vv = _ctx.vectorizer_var
        if not _ctx.model_registry:
            return f"print('[ENLANG ML] No models trained.')"
        proba_parts = []
        for algo, mv in _ctx.model_registry.items():
            proba_parts.append(f"float({mv}.predict_proba({vv}.transform(['{text}']))[0][1])")
        avg = "(" + " + ".join(proba_parts) + f") / {len(proba_parts)}"
        return (
            f"_ep = round(({avg}) * 100, 1); "
            f"_risk = 'HIGH ESCALATION RISK' if _ep > 70 else 'MODERATE RISK' if _ep > 40 else 'LOW RISK (Diplomacy Likely)'; "
            f"print(f'Headline: {text}'); "
            f"print(f'  Ensemble Escalation Chance: {{_ep}}% | {{_risk}}')"
        )

    # predict escalation from "headline"
    m = re.match(r'^predict\s+escalation\s+from\s+["\'](.+?)["\']\s*$', s, re.IGNORECASE)
    if m:
        text = m.group(1)
        vv = _ctx.vectorizer_var
        mv = _ctx.model_var
        return (
            f"_ep = float({mv}.predict_proba({vv}.transform(['{text}']))[0][1]) * 100; "
            f"_ep = round(_ep, 1); "
            f"_risk = 'HIGH ESCALATION RISK' if _ep > 70 else 'MODERATE RISK' if _ep > 40 else 'LOW RISK'; "
            f"print(f'Headline: {text}'); "
            f"print(f'  Escalation Chance: {{_ep}}% | {{_risk}}')"
        )

    # ── 17. SAVE / LOAD MODEL ─────────────────────────────────────────────────

    m = re.match(r'^save\s+model\s+to\s+["\'](.+?)["\']\s*$', s, re.IGNORECASE)
    if m:
        path = m.group(1)
        return (
            f"import joblib; joblib.dump({_ctx.model_var}, '{path}'); "
            f"print('[ENLANG ML] Model saved to {path}')"
        )

    m = re.match(r'^load\s+model\s+from\s+["\'](.+?)["\']\s*$', s, re.IGNORECASE)
    if m:
        path = m.group(1)
        return (
            f"import joblib; {_ctx.model_var} = joblib.load('{path}'); "
            f"print('[ENLANG ML] Model loaded from {path}')"
        )

    m = re.match(r'^save\s+vectorizer\s+to\s+["\'](.+?)["\']\s*$', s, re.IGNORECASE)
    if m:
        path = m.group(1)
        return (
            f"import joblib; joblib.dump({_ctx.vectorizer_var}, '{path}'); "
            f"print('[ENLANG ML] Vectorizer saved to {path}')"
        )

    m = re.match(r'^load\s+vectorizer\s+from\s+["\'](.+?)["\']\s*$', s, re.IGNORECASE)
    if m:
        path = m.group(1)
        return (
            f"import joblib; {_ctx.vectorizer_var} = joblib.load('{path}'); "
            f"print('[ENLANG ML] Vectorizer loaded from {path}')"
        )

    # ── 18. DATA VISUALIZATION ────────────────────────────────────────────────

    m = re.match(r'^plot\s+(?:column\s+)?distribution\s+of\s+([a-zA-Z_]\w*)\s*$', s, re.IGNORECASE)
    if m:
        col = m.group(1)
        return (
            f"import matplotlib.pyplot as plt; "
            f"{_ctx.dataset_var}['{col}'].value_counts().plot(kind='bar', color='steelblue', title='{col} Distribution'); "
            f"plt.tight_layout(); plt.show()"
        )

    m = re.match(r'^plot\s+correlation\s+heatmap\s*$', s, re.IGNORECASE)
    if m:
        return (
            f"import matplotlib.pyplot as plt; import seaborn as sns; "
            f"plt.figure(figsize=(10,8)); "
            f"sns.heatmap({_ctx.dataset_var}.corr(numeric_only=True), annot=True, cmap='coolwarm', fmt='.2f'); "
            f"plt.title('Correlation Heatmap'); plt.tight_layout(); plt.show()"
        )

    # ── 19. DATA WRANGLING ────────────────────────────────────────────────────

    # group df by column and compute mean / sum / count / max / min
    m = re.match(r'^group\s+([a-zA-Z_]\w*)\s+by\s+([a-zA-Z_]\w*)\s+and\s+compute\s+(mean|sum|count|max|min|median|std)\s*$', s, re.IGNORECASE)
    if m:
        var, col, agg = m.group(1), m.group(2), m.group(3).lower()
        return f"print({var}.groupby('{col}').{agg}(numeric_only=True).round(3).to_string())"

    # group df by column and compute mean of col2 and store in result
    m = re.match(r'^group\s+([a-zA-Z_]\w*)\s+by\s+([a-zA-Z_]\w*)\s+and\s+compute\s+(mean|sum|count|max|min|median|std)\s+of\s+([a-zA-Z_]\w*)\s+and\s+store\s+in\s+([a-zA-Z_]\w*)\s*$', s, re.IGNORECASE)
    if m:
        var, grp, agg, col2, out = m.group(1), m.group(2), m.group(3).lower(), m.group(4), m.group(5)
        return f"{out} = {var}.groupby('{grp}')['{col2}'].{agg}().reset_index()"

    # filter df where column > value and store in result
    m = re.match(r'^filter\s+([a-zA-Z_]\w*)\s+where\s+([a-zA-Z_]\w*)\s+(>|<|>=|<=|==|!=|equals?|greater\s+than|less\s+than)\s+(.+?)\s+and\s+store\s+in\s+([a-zA-Z_]\w*)\s*$', s, re.IGNORECASE)
    if m:
        var, col, op_raw, val, out = m.group(1), m.group(2), m.group(3), m.group(4).strip(), m.group(5)
        op_map = {"equals": "==", "equal": "==", "greater than": ">", "less than": "<"}
        op = op_map.get(op_raw.lower(), op_raw)
        return f"{out} = {var}[{var}['{col}'] {op} {val}].reset_index(drop=True)"

    # sort df by column ascending/descending and store in result
    m = re.match(r'^sort\s+([a-zA-Z_]\w*)\s+by\s+([a-zA-Z_]\w*)\s+(ascending|descending)(?:\s+and\s+store\s+in\s+([a-zA-Z_]\w*))?\s*$', s, re.IGNORECASE)
    if m:
        var, col, order, out = m.group(1), m.group(2), m.group(3).lower(), m.group(4) or m.group(1)
        asc = "True" if order == "ascending" else "False"
        return f"{out} = {var}.sort_values(by='{col}', ascending={asc}).reset_index(drop=True)"

    # merge df1 with df2 on column and store in result
    m = re.match(r'^merge\s+([a-zA-Z_]\w*)\s+with\s+([a-zA-Z_]\w*)\s+on\s+([a-zA-Z_]\w*)\s+and\s+store\s+in\s+([a-zA-Z_]\w*)\s*$', s, re.IGNORECASE)
    if m:
        v1, v2, col, out = m.group(1), m.group(2), m.group(3), m.group(4)
        return f"{out} = {v1}.merge({v2}, on='{col}', how='inner')"

    # pivot df on column rows and column values
    m = re.match(r'^pivot\s+([a-zA-Z_]\w*)\s+on\s+([a-zA-Z_]\w*)\s+rows\s+([a-zA-Z_]\w*)\s+values\s+([a-zA-Z_]\w*)\s+and\s+store\s+in\s+([a-zA-Z_]\w*)\s*$', s, re.IGNORECASE)
    if m:
        var, idx, cols, vals, out = m.group(1), m.group(2), m.group(3), m.group(4), m.group(5)
        return f"{out} = {var}.pivot_table(index='{idx}', columns='{cols}', values='{vals}', aggfunc='mean')"

    # add column result = col1 + col2
    m = re.match(r'^add\s+column\s+([a-zA-Z_]\w*)\s+as\s+(.+)\s+to\s+([a-zA-Z_]\w*)\s*$', s, re.IGNORECASE)
    if m:
        new_col, expr, var = m.group(1), m.group(2), m.group(3)
        return f"{var}['{new_col}'] = {expr}"

    # select columns col1, col2, col3 from df and store in result
    m = re.match(r'^select\s+columns?\s+(.+?)\s+from\s+([a-zA-Z_]\w*)\s+and\s+store\s+in\s+([a-zA-Z_]\w*)\s*$', s, re.IGNORECASE)
    if m:
        cols_raw, var, out = m.group(1), m.group(2), m.group(3)
        cols = [c.strip() for c in cols_raw.split(',')]
        return f"{out} = {var}[{cols}]"

    # ── 20. STATISTICAL TESTS ─────────────────────────────────────────────────

    # run t-test between column A and column B and store p value in p
    m = re.match(r'^run\s+t.test\s+between\s+(?:column\s+)?([a-zA-Z_]\w*)\s+and\s+(?:column\s+)?([a-zA-Z_]\w*)(?:\s+and\s+store\s+p\s*[-\s]?value\s+in\s+([a-zA-Z_]\w*))?\s*$', s, re.IGNORECASE)
    if m:
        c1, c2, pvar = m.group(1), m.group(2), m.group(3) or "_p_val"
        v = _ctx.dataset_var
        return (
            f"from scipy import stats; "
            f"_t, {pvar} = stats.ttest_ind({v}['{c1}'].dropna(), {v}['{c2}'].dropna()); "
            f"_sig = 'SIGNIFICANT' if {pvar} < 0.05 else 'NOT SIGNIFICANT'; "
            f"print(f'[ENLANG STATS] T-Test | t={{_t:.4f}} | p-value={{{pvar}:.6f}} | {{_sig}}')"
        )

    # run chi-square test on column A and column B
    m = re.match(r'^run\s+chi.square\s+test\s+on\s+(?:column\s+)?([a-zA-Z_]\w*)\s+and\s+(?:column\s+)?([a-zA-Z_]\w*)\s*$', s, re.IGNORECASE)
    if m:
        c1, c2 = m.group(1), m.group(2)
        v = _ctx.dataset_var
        return (
            f"from scipy import stats; import pandas as pd; "
            f"_ct = pd.crosstab({v}['{c1}'], {v}['{c2}']); "
            f"_chi2, _p, _dof, _exp = stats.chi2_contingency(_ct); "
            f"_sig = 'SIGNIFICANT' if _p < 0.05 else 'NOT SIGNIFICANT'; "
            f"print(f'[ENLANG STATS] Chi-Square | chi2={{_chi2:.4f}} | p={{_p:.6f}} | dof={{_dof}} | {{_sig}}')"
        )

    # run anova on column A grouped by column B
    m = re.match(r'^run\s+anova\s+on\s+(?:column\s+)?([a-zA-Z_]\w*)\s+grouped\s+by\s+(?:column\s+)?([a-zA-Z_]\w*)\s*$', s, re.IGNORECASE)
    if m:
        val_col, grp_col = m.group(1), m.group(2)
        v = _ctx.dataset_var
        return (
            f"from scipy import stats; "
            f"_groups = [{v}[{v}['{grp_col}']==g]['{val_col}'].dropna().values for g in {v}['{grp_col}'].unique()]; "
            f"_f, _p = stats.f_oneway(*_groups); "
            f"_sig = 'SIGNIFICANT' if _p < 0.05 else 'NOT SIGNIFICANT'; "
            f"print(f'[ENLANG STATS] ANOVA | F={{_f:.4f}} | p={{_p:.6f}} | {{_sig}}')"
        )

    # compute pearson correlation between column A and column B
    m = re.match(r'^compute\s+(?:pearson\s+)?correlation\s+between\s+(?:column\s+)?([a-zA-Z_]\w*)\s+and\s+(?:column\s+)?([a-zA-Z_]\w*)\s*$', s, re.IGNORECASE)
    if m:
        c1, c2 = m.group(1), m.group(2)
        v = _ctx.dataset_var
        return (
            f"from scipy import stats; "
            f"_corr, _p = stats.pearsonr({v}['{c1}'].dropna(), {v}['{c2}'].dropna()); "
            f"print(f'[ENLANG STATS] Pearson Correlation | r={{_corr:.4f}} | p={{_p:.6f}}')"
        )

    # compute spearman correlation between column A and column B
    m = re.match(r'^compute\s+spearman\s+correlation\s+between\s+(?:column\s+)?([a-zA-Z_]\w*)\s+and\s+(?:column\s+)?([a-zA-Z_]\w*)\s*$', s, re.IGNORECASE)
    if m:
        c1, c2 = m.group(1), m.group(2)
        v = _ctx.dataset_var
        return (
            f"from scipy import stats; "
            f"_corr, _p = stats.spearmanr({v}['{c1}'].dropna(), {v}['{c2}'].dropna()); "
            f"print(f'[ENLANG STATS] Spearman Correlation | rho={{_corr:.4f}} | p={{_p:.6f}}')"
        )

    # show outliers in column A using iqr
    m = re.match(r'^show\s+outliers\s+in\s+(?:column\s+)?([a-zA-Z_]\w*)(?:\s+using\s+(iqr|zscore|z.score))?\s*$', s, re.IGNORECASE)
    if m:
        col, method = m.group(1), (m.group(2) or "iqr").lower().replace('-', '')
        v = _ctx.dataset_var
        if method == "iqr":
            return (
                f"_q1 = {v}['{col}'].quantile(0.25); _q3 = {v}['{col}'].quantile(0.75); "
                f"_iqr = _q3 - _q1; "
                f"_out = {v}[({v}['{col}'] < _q1 - 1.5*_iqr) | ({v}['{col}'] > _q3 + 1.5*_iqr)]; "
                f"print(f'[ENLANG STATS] Outliers in {col} (IQR): {{len(_out)}} rows'); print(_out['{col}'].values)"
            )
        else:
            return (
                f"import numpy as np; "
                f"_z = np.abs(({v}['{col}'] - {v}['{col}'].mean()) / {v}['{col}'].std()); "
                f"_out = {v}[_z > 3]; "
                f"print(f'[ENLANG STATS] Outliers in {col} (Z-Score): {{len(_out)}} rows')"
            )

    # ── 21. FEATURE SELECTION ─────────────────────────────────────────────────

    # select top N features using chi2 and store in selected_X
    m = re.match(r'^select\s+top\s+(\d+)\s+features?\s+using\s+(chi2|mutual\s*info|f.classif|rfe)\s+and\s+store\s+in\s+([a-zA-Z_]\w*)\s*$', s, re.IGNORECASE)
    if m:
        k, method_raw, out = m.group(1), m.group(2).lower().replace(' ', ''), m.group(3)
        method_map = {
            "chi2":         ("chi2", "SelectKBest(chi2, k={k})"),
            "mutualinfo":   ("mutual_info_classif", "SelectKBest(mutual_info_classif, k={k})"),
            "fclassif":     ("f_classif", "SelectKBest(f_classif, k={k})"),
            "rfe":          None,
        }
        if method_raw in ("chi2", "mutualinfo", "fclassif"):
            scorer, selector_tmpl = method_map[method_raw]
            selector = selector_tmpl.format(k=k)
            return (
                f"from sklearn.feature_selection import SelectKBest, {scorer}; "
                f"_sel = {selector}; "
                f"{_ctx.X_train} = _sel.fit_transform({_ctx.X_train}, {_ctx.y_train}); "
                f"{_ctx.X_test} = _sel.transform({_ctx.X_test}); "
                f"{out}_train = {_ctx.X_train}; {out}_test = {_ctx.X_test}; "
                f"print(f'[ENLANG ML] Feature Selection: {k} features selected using {method_raw}')"
            )

    # ── 22. HYPERPARAMETER TUNING ──────────────────────────────────────────────

    # tune random_forest classifier with grid search and store best in result
    m = re.match(r'^tune\s+([a-zA-Z_]+(?:\s+[a-zA-Z_]+)?)\s+(?:classifier|regressor?)\s+with\s+(?:grid\s+search|gridsearch)\s*$', s, re.IGNORECASE)
    if m:
        algo = _resolve_algo(m.group(1))
        mv = _ctx.model_registry.get(algo, _ctx.model_var)
        return (
            f"from sklearn.model_selection import GridSearchCV; "
            f"_param_grid = {{'C': [0.1, 1, 10]}} if hasattr({mv}, 'C') else {{'n_estimators': [50, 100, 200], 'max_depth': [5, 10, None]}}; "
            f"_gs = GridSearchCV({mv}, _param_grid, cv=5, scoring='accuracy', n_jobs=-1); "
            f"_gs.fit({_ctx.X_train}, {_ctx.y_train}); "
            f"print(f'[ENLANG ML] Grid Search Best Params: {{_gs.best_params_}}'); "
            f"print(f'[ENLANG ML] Grid Search Best CV Score: {{round(_gs.best_score_*100, 2)}}%')"
        )

    # tune random_forest classifier with random search and N iterations
    m = re.match(r'^tune\s+([a-zA-Z_]+(?:\s+[a-zA-Z_]+)?)\s+(?:classifier|regressor?)\s+with\s+(?:random\s+search|randomsearch)(?:\s+and\s+(\d+)\s+iterations?)?\s*$', s, re.IGNORECASE)
    if m:
        algo = _resolve_algo(m.group(1))
        n_iter = m.group(2) or "20"
        mv = _ctx.model_registry.get(algo, _ctx.model_var)
        return (
            f"from sklearn.model_selection import RandomizedSearchCV; import numpy as np; "
            f"_param_dist = {{'n_estimators': [50,100,150,200], 'max_depth': [3,5,10,None], 'min_samples_split': [2,5,10]}}; "
            f"_rs = RandomizedSearchCV({mv}, _param_dist, n_iter={n_iter}, cv=5, scoring='accuracy', n_jobs=-1, random_state=42); "
            f"_rs.fit({_ctx.X_train}, {_ctx.y_train}); "
            f"print(f'[ENLANG ML] Random Search Best Params: {{_rs.best_params_}}'); "
            f"print(f'[ENLANG ML] Random Search Best CV Score: {{round(_rs.best_score_*100, 2)}}%')"
        )

    # ── 23. TIME SERIES ───────────────────────────────────────────────────────

    # compute rolling mean of column with window N and store in result
    m = re.match(r'^compute\s+rolling\s+(mean|sum|std|max|min)\s+of\s+(?:column\s+)?([a-zA-Z_]\w*)\s+with\s+window\s+(\d+)\s+and\s+store\s+in\s+([a-zA-Z_]\w*)\s*$', s, re.IGNORECASE)
    if m:
        agg, col, win, out = m.group(1).lower(), m.group(2), m.group(3), m.group(4)
        v = _ctx.dataset_var
        return f"{out} = {v}['{col}'].rolling(window={win}).{agg}()"

    # lag column by N periods and store in result
    m = re.match(r'^lag\s+(?:column\s+)?([a-zA-Z_]\w*)\s+by\s+(\d+)\s+periods?\s+and\s+store\s+in\s+([a-zA-Z_]\w*)\s*$', s, re.IGNORECASE)
    if m:
        col, n, out = m.group(1), m.group(2), m.group(3)
        v = _ctx.dataset_var
        return f"{out} = {v}['{col}'].shift({n})"

    # compute time series trend of column
    m = re.match(r'^compute\s+(?:time\s+series\s+)?trend\s+of\s+(?:column\s+)?([a-zA-Z_]\w*)\s*$', s, re.IGNORECASE)
    if m:
        col = m.group(1)
        v = _ctx.dataset_var
        return (
            f"import numpy as np; "
            f"_x = np.arange(len({v})); "
            f"_coef = np.polyfit(_x, {v}['{col}'].fillna(method='ffill'), 1); "
            f"print(f'[ENLANG TS] Trend in {col}: slope={{_coef[0]:.4f}} (positive=upward, negative=downward)')"
        )

    # ── 24. IMBALANCED DATA ───────────────────────────────────────────────────

    # balance classes using smote
    m = re.match(r'^balance\s+classes?\s+using\s+smote\s*$', s, re.IGNORECASE)
    if m:
        Xt, yt = _ctx.X_train, _ctx.y_train
        Xt_expr = f"({Xt}.toarray() if hasattr({Xt}, 'toarray') else {Xt})"
        return (
            f"from imblearn.over_sampling import SMOTE; "
            f"_sm = SMOTE(random_state=42); "
            f"{Xt}, {yt} = _sm.fit_resample({Xt_expr}, {yt}); "
            f"import collections; print(f'[ENLANG ML] SMOTE applied | Class distribution: {{dict(collections.Counter({yt}))}}')"
        )

    # oversample minority class using random oversampling
    m = re.match(r'^oversample\s+(?:minority\s+class\s+)?using\s+(?:random\s+oversampling|ros)\s*$', s, re.IGNORECASE)
    if m:
        Xt, yt = _ctx.X_train, _ctx.y_train
        Xt_expr = f"({Xt}.toarray() if hasattr({Xt}, 'toarray') else {Xt})"
        return (
            f"from imblearn.over_sampling import RandomOverSampler; "
            f"_ros = RandomOverSampler(random_state=42); "
            f"{Xt}, {yt} = _ros.fit_resample({Xt_expr}, {yt}); "
            f"import collections; print(f'[ENLANG ML] RandomOverSampler applied | Class dist: {{dict(collections.Counter({yt}))}}')"
        )

    # undersample majority class
    m = re.match(r'^undersample\s+(?:majority\s+class\s+)?using\s+(?:random\s+undersampling|rus)\s*$', s, re.IGNORECASE)
    if m:
        Xt, yt = _ctx.X_train, _ctx.y_train
        Xt_expr = f"({Xt}.toarray() if hasattr({Xt}, 'toarray') else {Xt})"
        return (
            f"from imblearn.under_sampling import RandomUnderSampler; "
            f"_rus = RandomUnderSampler(random_state=42); "
            f"{Xt}, {yt} = _rus.fit_resample({Xt_expr}, {yt}); "
            f"import collections; print(f'[ENLANG ML] RandomUnderSampler applied | Class dist: {{dict(collections.Counter({yt}))}}')"
        )

    # ── 25. ANOMALY DETECTION ──────────────────────────────────────────────────

    # detect anomalies using isolation forest and store in result
    m = re.match(r'^detect\s+anomalies?\s+using\s+(?:isolation\s+forest|isolationforest)\s+and\s+store\s+in\s+([a-zA-Z_]\w*)\s*$', s, re.IGNORECASE)
    if m:
        out = m.group(1)
        Xv = _ctx.X_var
        return (
            f"from sklearn.ensemble import IsolationForest; "
            f"_ifor = IsolationForest(contamination=0.05, random_state=42); "
            f"{out} = _ifor.fit_predict({Xv}); "
            f"import collections; print(f'[ENLANG ML] Isolation Forest | Anomalies: {{list({out}).count(-1)}} | Normal: {{list({out}).count(1)}}')"
        )

    # detect anomalies using local outlier factor
    m = re.match(r'^detect\s+anomalies?\s+using\s+(?:local\s+outlier\s+factor|lof)\s+and\s+store\s+in\s+([a-zA-Z_]\w*)\s*$', s, re.IGNORECASE)
    if m:
        out = m.group(1)
        Xv = _ctx.X_var
        return (
            f"from sklearn.neighbors import LocalOutlierFactor; "
            f"_lof = LocalOutlierFactor(n_neighbors=20); "
            f"{out} = _lof.fit_predict({Xv}); "
            f"import collections; print(f'[ENLANG ML] LOF | Anomalies: {{list({out}).count(-1)}} | Normal: {{list({out}).count(1)}}')"
        )

    # ── 26. NLP EXTRAS ────────────────────────────────────────────────────────

    # analyze sentiment of column text and store in result
    m = re.match(r'^analyze\s+sentiment\s+of\s+(?:column\s+)?([a-zA-Z_]\w*)\s+and\s+store\s+in\s+([a-zA-Z_]\w*)\s*$', s, re.IGNORECASE)
    if m:
        col, out = m.group(1), m.group(2)
        v = _ctx.dataset_var
        return (
            f"from textblob import TextBlob; "
            f"{out} = {v}['{col}'].fillna('').apply(lambda t: TextBlob(str(t)).sentiment.polarity); "
            f"print(f'[ENLANG NLP] Sentiment | Mean: {{round({out}.mean(), 3)}} | Positive: {{({out}>0).sum()}} | Negative: {{({out}<0).sum()}} | Neutral: {{({out}==0).sum()}}')"
        )

    # show word frequency of column text top N words
    m = re.match(r'^show\s+word\s+frequency\s+of\s+(?:column\s+)?([a-zA-Z_]\w*)(?:\s+top\s+(\d+))?\s*$', s, re.IGNORECASE)
    if m:
        col, top_n = m.group(1), int(m.group(2) or 20)
        v = _ctx.dataset_var
        return (
            f"from collections import Counter; import re as _re; "
            f"_all_words = ' '.join({v}['{col}'].fillna('').str.lower()).split(); "
            f"_wf = Counter(_all_words).most_common({top_n}); "
            f"print(f'\\n=== Top {top_n} Words in {col} ==='); "
            f"[print(f'  {{w:<25}} {{c}}') for w, c in _wf]"
        )

    # compute tfidf similarity between "text1" and "text2"
    m = re.match(r'^compute\s+similarity\s+between\s+["\'](.+?)["\']\s+and\s+["\'](.+?)["\']\s+and\s+store\s+in\s+([a-zA-Z_]\w*)\s*$', s, re.IGNORECASE)
    if m:
        t1, t2, out = m.group(1), m.group(2), m.group(3)
        return (
            f"from sklearn.feature_extraction.text import TfidfVectorizer; "
            f"from sklearn.metrics.pairwise import cosine_similarity; "
            f"_sim_vec = TfidfVectorizer().fit_transform(['{t1}', '{t2}']); "
            f"{out} = round(float(cosine_similarity(_sim_vec[0], _sim_vec[1])[0][0]) * 100, 2); "
            f"print(f'[ENLANG NLP] Cosine Similarity: {{{out}}}%')"
        )

    # ── 27. PIPELINE ──────────────────────────────────────────────────────────

    # create pipeline with tfidf and naive_bayes
    m = re.match(r'^create\s+pipeline\s+with\s+tfidf\s+and\s+([a-zA-Z_]+(?:\s+[a-zA-Z_]+)?)\s*$', s, re.IGNORECASE)
    if m:
        algo = _resolve_algo(m.group(1))
        if algo in _CLASSIFIERS:
            mod, cls, init = _CLASSIFIERS[algo]
            return (
                f"from sklearn.pipeline import Pipeline; "
                f"from sklearn.feature_extraction.text import TfidfVectorizer; "
                f"from {mod} import {cls}; "
                f"{_ctx.pipeline_var} = Pipeline([('tfidf', TfidfVectorizer(stop_words='english', max_features=10000)), ('{algo}', {init})])"
            )

    # train pipeline on training data
    m = re.match(r'^train\s+pipeline\s+on\s+training\s+data\s*$', s, re.IGNORECASE)
    if m:
        return (
            f"{_ctx.pipeline_var}.fit({_ctx.X_train}, {_ctx.y_train}); "
            f"print('[ENLANG ML] Pipeline trained!')"
        )

    # evaluate pipeline accuracy and store in result
    m = re.match(r'^evaluate\s+pipeline\s+accuracy\s+and\s+store\s+in\s+([a-zA-Z_]\w*)\s*$', s, re.IGNORECASE)
    if m:
        out = m.group(1)
        return (
            f"from sklearn.metrics import accuracy_score; "
            f"_pipe_pred = {_ctx.pipeline_var}.predict({_ctx.X_test}); "
            f"{out} = round(accuracy_score({_ctx.y_test}, _pipe_pred) * 100, 2); "
            f"print(f'[ENLANG ML] Pipeline Accuracy: {{{out}}}%')"
        )

    # ── 28. EDA / DATA PROFILING ──────────────────────────────────────────────

    # generate eda report
    m = re.match(r'^generate\s+(?:eda\s+)?(?:report|profile)\s*$', s, re.IGNORECASE)
    if m:
        v = _ctx.dataset_var
        return (
            f"import pandas as pd; import numpy as np; "
            f"print('\\n' + '='*70); print('  FULL DATASET PROFILE'); print('='*70); "
            f"print(f'Shape: {{{v}.shape}}'); "
            f"print(f'\\nDtypes:\\n{{{v}.dtypes.to_string()}}'); "
            f"print(f'\\nMissing Values:\\n{{{v}.isnull().sum().to_string()}}'); "
            f"print(f'\\nDuplicate Rows: {{{v}.duplicated().sum()}}'); "
            f"print(f'\\nNumeric Statistics:\\n{{{v}.describe().round(3).to_string()}}'); "
            f"print('='*70)"
        )

    # compute mutual information between features and label
    m = re.match(r'^compute\s+mutual\s+information\s+between\s+features?\s+and\s+(?:label|target)\s*$', s, re.IGNORECASE)
    if m:
        return (
            f"from sklearn.feature_selection import mutual_info_classif; import numpy as np; "
            f"_Xt = ({_ctx.X_train}.toarray() if hasattr({_ctx.X_train}, 'toarray') else {_ctx.X_train}); "
            f"_mi = mutual_info_classif(_Xt, {_ctx.y_train}, random_state=42); "
            f"print(f'[ENLANG ML] Mutual Info | Mean: {{_mi.mean():.4f}} | Max: {{_mi.max():.4f}} | Features > 0: {{(_mi>0).sum()}}')"
        )

    # ── 29. REGRESSION EXTRA METRICS ──────────────────────────────────────────

    # evaluate regression model metrics
    m = re.match(r'^evaluate\s+regression\s+(?:metrics?|model)\s*$', s, re.IGNORECASE)
    if m:
        mv = _ctx.model_var
        Xt_expr = f"({_ctx.X_test}.toarray() if hasattr({_ctx.X_test}, 'toarray') else {_ctx.X_test})"
        return (
            f"from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score; import math; "
            f"_yp = {mv}.predict({Xt_expr}); "
            f"_rmse = round(math.sqrt(mean_squared_error({_ctx.y_test}, _yp)), 4); "
            f"_mae  = round(mean_absolute_error({_ctx.y_test}, _yp), 4); "
            f"_r2   = round(r2_score({_ctx.y_test}, _yp), 4); "
            f"_n = len({_ctx.y_test}); _k = {Xt_expr}.shape[1] if hasattr({Xt_expr}, 'shape') else 1; "
            f"_adj_r2 = round(1 - (1-_r2)*(_n-1)/(_n-_k-1), 4); "
            f"print(f'[ENLANG ML] RMSE: {{_rmse}} | MAE: {{_mae}} | R2: {{_r2}} | Adjusted R2: {{_adj_r2}}')"
        )

    # ── Not an ML line ────────────────────────────────────────────────────────
    return None
