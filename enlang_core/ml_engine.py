"""
EnLang ML Engine v2 — Full Natural English AI/ML & Data Science Syntax Transpiler
==================================================================================
Mixed Grammar: Option A (Natural Action) + Option B (Fluent Sentence) + Option C (Verb-Driven)

Grammar Principles:
  - Subject → Action → Object  (natural English sentence structure)
  - Named variables via: "as <var>", "into <var>", "store in <var>"
  - Short punchy verbs: read, create, train, test, compute, show, detect, reduce, combine
  - Natural prepositions: into, using, from, as, on, with, against, by
  - BACKWARD COMPATIBLE: All v1 patterns still work alongside v2

DOMAIN COVERAGE:
  1.  Data Loading & Export
  2.  Data Exploration & EDA Profiling
  3.  Data Cleaning & Wrangling
  4.  Feature Engineering & Encoding
  5.  Train-Test Split & Cross Validation
  6.  Text Vectorization
  7.  Feature Scaling & Normalization
  8.  Model Creation (Classification, Regression)
  9.  Model Training
  10. Model Prediction
  11. Classification Evaluation (Accuracy, F1, ROC, Confusion Matrix)
  12. Regression Evaluation (RMSE, MAE, R2, Adjusted R2)
  13. Multi-Model Comparison
  14. Ensemble Methods (Soft Voting, Hard Voting)
  15. Feature Importance & Feature Selection
  16. Hyperparameter Tuning (GridSearch, RandomSearch)
  17. Clustering (K-Means, DBSCAN, Hierarchical)
  18. Dimensionality Reduction (PCA, t-SNE, LDA)
  19. Anomaly Detection (Isolation Forest, LOF)
  20. Imbalanced Data (SMOTE, Over/Under Sampling)
  21. Statistical Tests (T-Test, Chi-Square, ANOVA, Correlation)
  22. Time Series Analysis
  23. NLP (Sentiment, Word Frequency, Similarity)
  24. Pipeline Creation & Training
  25. Model Save & Load
  26. Data Visualization
"""

import re

# ─────────────────────────────────────────────────────────────────────────────
# INTERNAL STATE TRACKER (Backward Compatible)
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
        self.pca_var         = "_enlg_pca"
        self.cluster_var     = "_enlg_cluster"
        self.pipeline_var    = "_enlg_pipeline"
        self.text_column     = "text"
        self.label_column    = "label"
        self.model_registry  = {}   # algo_name → python_var_name
        self.named_models    = {}   # user_alias → python_var_name
        self.named_scalers   = {}   # user_alias → python_var_name
        self.named_vecs      = {}   # user_alias → python_var_name

_ctx = MLContext()

def reset_context():
    _ctx.reset()

# ─────────────────────────────────────────────────────────────────────────────
# ALGORITHM REGISTRIES
# ─────────────────────────────────────────────────────────────────────────────

_CLASSIFIERS = {
    "naive_bayes":             ("sklearn.naive_bayes",              "MultinomialNB",                  "MultinomialNB(alpha=0.5)"),
    "gaussian_naive_bayes":    ("sklearn.naive_bayes",              "GaussianNB",                     "GaussianNB()"),
    "bernoulli_naive_bayes":   ("sklearn.naive_bayes",              "BernoulliNB",                    "BernoulliNB()"),
    "logistic_regression":     ("sklearn.linear_model",             "LogisticRegression",             "LogisticRegression(max_iter=1000, random_state=42)"),
    "svm":                     ("sklearn.svm",                      "SVC",                            "SVC(kernel='linear', probability=True, random_state=42)"),
    "linear_svm":              ("sklearn.svm",                      "LinearSVC",                      "LinearSVC(max_iter=2000, random_state=42)"),
    "rbf_svm":                 ("sklearn.svm",                      "SVC",                            "SVC(kernel='rbf', probability=True, random_state=42)"),
    "random_forest":           ("sklearn.ensemble",                 "RandomForestClassifier",         "RandomForestClassifier(n_estimators={trees}, random_state=42, n_jobs=-1)"),
    "decision_tree":           ("sklearn.tree",                     "DecisionTreeClassifier",         "DecisionTreeClassifier(random_state=42)"),
    "gradient_boosting":       ("sklearn.ensemble",                 "GradientBoostingClassifier",     "GradientBoostingClassifier(n_estimators={trees}, learning_rate=0.1, random_state=42)"),
    "knn":                     ("sklearn.neighbors",                "KNeighborsClassifier",           "KNeighborsClassifier(n_neighbors={neighbors})"),
    "adaboost":                ("sklearn.ensemble",                 "AdaBoostClassifier",             "AdaBoostClassifier(n_estimators=100, random_state=42)"),
    "extra_trees":             ("sklearn.ensemble",                 "ExtraTreesClassifier",           "ExtraTreesClassifier(n_estimators=200, random_state=42, n_jobs=-1)"),
    "neural_network":          ("sklearn.neural_network",           "MLPClassifier",                  "MLPClassifier(hidden_layer_sizes={layers}, max_iter=500, random_state=42)"),
    "mlp":                     ("sklearn.neural_network",           "MLPClassifier",                  "MLPClassifier(hidden_layer_sizes=(128,64), max_iter=500, random_state=42)"),
    "bagging":                 ("sklearn.ensemble",                 "BaggingClassifier",              "BaggingClassifier(n_estimators=50, random_state=42)"),
    "linear_discriminant":     ("sklearn.discriminant_analysis",    "LinearDiscriminantAnalysis",     "LinearDiscriminantAnalysis()"),
}

_REGRESSORS = {
    "linear_regression":       ("sklearn.linear_model",             "LinearRegression",               "LinearRegression()"),
    "ridge":                   ("sklearn.linear_model",             "Ridge",                          "Ridge(alpha=1.0)"),
    "ridge_regression":        ("sklearn.linear_model",             "Ridge",                          "Ridge(alpha=1.0)"),
    "lasso":                   ("sklearn.linear_model",             "Lasso",                          "Lasso(alpha=0.1)"),
    "lasso_regression":        ("sklearn.linear_model",             "Lasso",                          "Lasso(alpha=0.1)"),
    "elastic_net":             ("sklearn.linear_model",             "ElasticNet",                     "ElasticNet(alpha=0.1)"),
    "svr":                     ("sklearn.svm",                      "SVR",                            "SVR(kernel='rbf')"),
    "random_forest":           ("sklearn.ensemble",                 "RandomForestRegressor",          "RandomForestRegressor(n_estimators={trees}, random_state=42, n_jobs=-1)"),
    "decision_tree":           ("sklearn.tree",                     "DecisionTreeRegressor",          "DecisionTreeRegressor(random_state=42)"),
    "gradient_boosting":       ("sklearn.ensemble",                 "GradientBoostingRegressor",      "GradientBoostingRegressor(n_estimators={trees}, learning_rate=0.1, random_state=42)"),
    "knn":                     ("sklearn.neighbors",                "KNeighborsRegressor",            "KNeighborsRegressor(n_neighbors={neighbors})"),
    "extra_trees":             ("sklearn.ensemble",                 "ExtraTreesRegressor",            "ExtraTreesRegressor(n_estimators=200, random_state=42, n_jobs=-1)"),
    "neural_network":          ("sklearn.neural_network",           "MLPRegressor",                   "MLPRegressor(hidden_layer_sizes=(128,64), max_iter=500, random_state=42)"),
}

_ALIASES = {
    "lr":  "logistic_regression", "rf": "random_forest", "nb": "naive_bayes",
    "dt":  "decision_tree",       "gb": "gradient_boosting", "svc": "svm",
    "knn": "knn",                 "nn": "neural_network", "et": "extra_trees",
    "ada": "adaboost",            "mlp": "neural_network",
}

def _resolve_algo(raw: str) -> str:
    key = raw.strip().lower().replace(' ', '_').replace('-', '_')
    return _ALIASES.get(key, key)

def _safe_var(name: str) -> str:
    """Convert user alias to safe Python variable name."""
    return re.sub(r'[^a-zA-Z0-9_]', '_', name.strip())

def _build_classifier(algo: str, trees: int = 100, neighbors: int = 5, layers: str = "(128,64)") -> tuple:
    if algo not in _CLASSIFIERS:
        return None, None, None
    mod, cls, init_tmpl = _CLASSIFIERS[algo]
    init = init_tmpl.format(trees=trees, neighbors=neighbors, layers=layers)
    return mod, cls, init

def _build_regressor(algo: str, trees: int = 100, neighbors: int = 5) -> tuple:
    if algo not in _REGRESSORS:
        return None, None, None
    mod, cls, init_tmpl = _REGRESSORS[algo]
    init = init_tmpl.format(trees=trees, neighbors=neighbors)
    return mod, cls, init

def _sparse_safe(var: str) -> str:
    return f"({var}.toarray() if hasattr({var}, 'toarray') else {var})"


# ─────────────────────────────────────────────────────────────────────────────
# MAIN TRANSPILER
# ─────────────────────────────────────────────────────────────────────────────

def translate_ml_line(line: str) -> str | None:
    s = line.strip()

    # ══════════════════════════════════════════════════════════════════════════
    # 1. DATA LOADING
    # ══════════════════════════════════════════════════════════════════════════

    # read "file.csv" as df
    m = re.match(r'^read\s+["\'](.+?)["\']\s+as\s+([a-zA-Z_]\w*)\s*$', s, re.IGNORECASE)
    if m:
        path, var = m.group(1), m.group(2)
        _ctx.dataset_var = var
        return f"import pandas as pd; {var} = pd.read_csv('{path}', encoding='utf-8', on_bad_lines='skip'); print(f'[ENLANG] Loaded {{len({var})}} rows from {path}')"

    # load "file.csv" as df  OR  load dataset from "file.csv" as df  OR  load dataset from "file.csv" into df
    m = re.match(r'^load\s+(?:dataset\s+from\s+|csv\s+|json\s+)?["\'](.+?)["\']\s+(?:as|into)\s+([a-zA-Z_]\w*)\s*$', s, re.IGNORECASE)
    if m:
        path, var = m.group(1), m.group(2)
        _ctx.dataset_var = var
        ext = path.rsplit('.', 1)[-1].lower()
        reader = "read_json" if ext == "json" else "read_csv"
        args = f"'{path}', encoding='utf-8', on_bad_lines='skip'" if ext == "csv" else f"'{path}'"
        return f"import pandas as pd; {var} = pd.{reader}({args}); print(f'[ENLANG] Loaded {{len({var})}} rows from {path}')"

    # load dataset from "file.csv" with text column T and label column L
    m = re.match(
        r'^load\s+dataset\s+from\s+["\'](.+?)["\']\s+with\s+text\s+column\s+([a-zA-Z_]\w*)\s+and\s+label\s+column\s+([a-zA-Z_]\w*)(?:\s+(?:as|into)\s+([a-zA-Z_]\w*))?\s*$',
        s, re.IGNORECASE)
    if m:
        path, tcol, lcol, var = m.group(1), m.group(2), m.group(3), m.group(4) or "df"
        _ctx.dataset_var = var; _ctx.text_column = tcol; _ctx.label_column = lcol
        _ctx.X_var = "X"; _ctx.y_var = "y"
        return (
            f"import pandas as pd; {var} = pd.read_csv('{path}', encoding='utf-8', on_bad_lines='skip'); "
            f"X = {var}['{tcol}'].fillna('').tolist(); y = {var}['{lcol}'].tolist(); "
            f"print(f'[ENLANG] Loaded {{len({var})}} samples | Text: {tcol} | Label: {lcol}')"
        )

    # export df to "output.csv"
    m = re.match(r'^export\s+([a-zA-Z_]\w*)\s+(?:to|as)\s+["\'](.+?)["\']\s*$', s, re.IGNORECASE)
    if m:
        var, path = m.group(1), m.group(2)
        return f"{var}.to_csv('{path}', index=False); print('[ENLANG] Exported to {path}')"

    # ══════════════════════════════════════════════════════════════════════════
    # 2. DATA EXPLORATION & EDA
    # ══════════════════════════════════════════════════════════════════════════

    # profile df  /  generate eda report  /  profile dataset df
    m = re.match(r'^(?:profile|generate\s+(?:eda\s+)?(?:report|profile))(?:\s+(?:of\s+|dataset\s+)?([a-zA-Z_]\w*))?\s*$', s, re.IGNORECASE)
    if m:
        v = m.group(1) or _ctx.dataset_var
        return (
            f"print('\\n' + '='*70); print('  DATASET PROFILE: {v}'); print('='*70); "
            f"print(f'Shape: {{{v}.shape}}'); "
            f"print(f'\\nData Types:\\n{{{v}.dtypes.to_string()}}'); "
            f"print(f'\\nMissing Values:\\n{{{v}.isnull().sum().to_string()}}'); "
            f"print(f'\\nDuplicate Rows: {{{v}.duplicated().sum()}}'); "
            f"print(f'\\nStatistics:\\n{{{v}.describe().round(3).to_string()}}'); print('='*70)"
        )

    # show info of df  /  show dataset info
    m = re.match(r'^show\s+(?:info|details)\s+(?:of\s+)?(?:dataset\s+)?([a-zA-Z_]\w*)?\s*$', s, re.IGNORECASE)
    if m:
        v = m.group(1) or _ctx.dataset_var
        return f"print(f'Shape: {{{v}.shape}} | Columns: {{{v}.columns.tolist()}}'); {v}.info()"

    # show statistics of df  /  show dataset statistics
    m = re.match(r'^show\s+statistics?\s+(?:of\s+)?(?:dataset\s+)?([a-zA-Z_]\w*)?\s*$', s, re.IGNORECASE)
    if m:
        v = m.group(1) or _ctx.dataset_var
        return f"print({v}.describe().round(3).to_string())"

    # show first N rows of df  /  show first N rows
    m = re.match(r'^show\s+first\s+(\d+)\s+rows?\s*(?:of\s+([a-zA-Z_]\w*))?\s*$', s, re.IGNORECASE)
    if m:
        n, v = m.group(1), m.group(2) or _ctx.dataset_var
        return f"print({v}.head({n}).to_string())"

    # show distribution of column "crop" in df  /  show distribution of crop
    m = re.match(r'^show\s+distribution\s+of\s+(?:column\s+)?["\']?([a-zA-Z_]\w*)["\']?(?:\s+in\s+([a-zA-Z_]\w*))?\s*$', s, re.IGNORECASE)
    if m:
        col, v = m.group(1), m.group(2) or _ctx.dataset_var
        return f"print(f'\\n=== Distribution of {col} ===\\n' + {v}['{col}'].value_counts().to_string())"

    # show missing values in df  /  show missing values
    m = re.match(r'^show\s+missing\s+values?\s*(?:in\s+([a-zA-Z_]\w*))?\s*$', s, re.IGNORECASE)
    if m:
        v = m.group(1) or _ctx.dataset_var
        return f"print('Missing Values:\\n' + {v}.isnull().sum().to_string())"

    # show shape of df
    m = re.match(r'^show\s+shape\s+(?:of\s+)?([a-zA-Z_]\w*)?\s*$', s, re.IGNORECASE)
    if m:
        v = m.group(1) or _ctx.dataset_var
        return f"print(f'Shape of {v}: {{{v}.shape}}')"

    # show correlation matrix  /  show correlation matrix of df
    m = re.match(r'^show\s+correlation\s+(?:matrix\s+)?(?:of\s+)?([a-zA-Z_]\w*)?\s*$', s, re.IGNORECASE)
    if m:
        v = m.group(1) or _ctx.dataset_var
        return f"print({v}.corr(numeric_only=True).round(3).to_string())"

    # ══════════════════════════════════════════════════════════════════════════
    # 3. DATA CLEANING
    # ══════════════════════════════════════════════════════════════════════════

    # drop missing values from df
    m = re.match(r'^drop\s+missing\s+values?\s+from\s+([a-zA-Z_]\w*)\s*$', s, re.IGNORECASE)
    if m:
        v = m.group(1)
        return f"{v} = {v}.dropna().reset_index(drop=True); print(f'[ENLANG] Rows after drop: {{len({v})}}')"

    # drop missing values  (uses current dataset_var)
    m = re.match(r'^drop\s+missing\s+values?\s*$', s, re.IGNORECASE)
    if m:
        v = _ctx.dataset_var
        return f"{v} = {v}.dropna().reset_index(drop=True); print(f'[ENLANG] Rows after drop: {{len({v})}}')"

    # remove duplicates from df
    m = re.match(r'^remove\s+duplicates?\s+from\s+([a-zA-Z_]\w*)\s*$', s, re.IGNORECASE)
    if m:
        v = m.group(1)
        return f"{v} = {v}.drop_duplicates().reset_index(drop=True); print(f'[ENLANG] Rows after dedup: {{len({v})}}')"

    # drop column "name" from df
    m = re.match(r'^drop\s+column\s+["\']?([a-zA-Z_]\w*)["\']?\s+from\s+([a-zA-Z_]\w*)\s*$', s, re.IGNORECASE)
    if m:
        col, v = m.group(1), m.group(2)
        return f"{v} = {v}.drop(columns=['{col}'])"

    # fill missing values in column "age" of df with 0
    m = re.match(r'^fill\s+missing\s+values?\s+in\s+(?:column\s+)?["\']?([a-zA-Z_]\w*)["\']?\s+(?:of\s+([a-zA-Z_]\w*)\s+)?with\s+(.+)\s*$', s, re.IGNORECASE)
    if m:
        col, v, val = m.group(1), m.group(2) or _ctx.dataset_var, m.group(3).strip()
        return f"{v}['{col}'] = {v}['{col}'].fillna({val})"

    # rename column "old" to "new" in df
    m = re.match(r'^rename\s+column\s+["\']?([a-zA-Z_]\w*)["\']?\s+to\s+["\']?([a-zA-Z_]\w*)["\']?(?:\s+in\s+([a-zA-Z_]\w*))?\s*$', s, re.IGNORECASE)
    if m:
        old, new, v = m.group(1), m.group(2), m.group(3) or _ctx.dataset_var
        return f"{v} = {v}.rename(columns={{'{old}': '{new}'}})"

    # ══════════════════════════════════════════════════════════════════════════
    # 4. FEATURE ENGINEERING
    # ══════════════════════════════════════════════════════════════════════════

    # separate df into features X and target y with target "crop"
    m = re.match(
        r'^separate\s+([a-zA-Z_]\w*)\s+into\s+features\s+([a-zA-Z_]\w*)\s+and\s+target\s+([a-zA-Z_]\w*)\s+with\s+target\s+["\']?([a-zA-Z_]\w*)["\']?\s*$',
        s, re.IGNORECASE)
    if m:
        df_v, X_v, y_v, col = m.group(1), m.group(2), m.group(3), m.group(4)
        _ctx.X_var = X_v; _ctx.y_var = y_v; _ctx.label_column = col
        return (
            f"{X_v} = {df_v}.drop(columns=['{col}']).values; "
            f"{y_v} = {df_v}['{col}'].values; "
            f"print(f'[ENLANG] Features: {X_v} shape {{{X_v}.shape}} | Target: {y_v}')"
        )

    # extract features into X from df excluding "crop"
    m = re.match(
        r'^extract\s+features\s+into\s+([a-zA-Z_]\w*)\s+from\s+([a-zA-Z_]\w*)\s+excluding\s+["\']?([a-zA-Z_]\w*)["\']?\s*$',
        s, re.IGNORECASE)
    if m:
        X_v, df_v, col = m.group(1), m.group(2), m.group(3)
        _ctx.X_var = X_v; _ctx.label_column = col
        return f"{X_v} = {df_v}.drop(columns=['{col}']).values"

    # extract target into y from df using "crop"
    m = re.match(
        r'^extract\s+target\s+into\s+([a-zA-Z_]\w*)\s+from\s+([a-zA-Z_]\w*)\s+using\s+["\']?([a-zA-Z_]\w*)["\']?\s*$',
        s, re.IGNORECASE)
    if m:
        y_v, df_v, col = m.group(1), m.group(2), m.group(3)
        _ctx.y_var = y_v; _ctx.label_column = col
        return f"{y_v} = {df_v}['{col}'].values"

    # select columns "A", "B", "C" from df as X
    m = re.match(r'^select\s+columns?\s+(.+?)\s+from\s+([a-zA-Z_]\w*)\s+as\s+([a-zA-Z_]\w*)\s*$', s, re.IGNORECASE)
    if m:
        cols_raw, df_v, out = m.group(1), m.group(2), m.group(3)
        cols = [c.strip().strip('"').strip("'") for c in cols_raw.split(',')]
        return f"{out} = {df_v}[{cols}].values"

    # encode column "gender" in df using label encoding
    m = re.match(r'^encode\s+(?:column\s+)?["\']?([a-zA-Z_]\w*)["\']?\s+(?:in\s+([a-zA-Z_]\w*)\s+)?using\s+(?:label\s+encod(?:ing|er)|label_encod(?:ing|er))\s*$', s, re.IGNORECASE)
    if m:
        col, v = m.group(1), m.group(2) or _ctx.dataset_var
        return (
            f"from sklearn.preprocessing import LabelEncoder; "
            f"_le_{col} = LabelEncoder(); "
            f"{v}['{col}'] = _le_{col}.fit_transform({v}['{col}'].astype(str))"
        )

    # encode column "color" in df using one hot encoding
    m = re.match(r'^encode\s+(?:column\s+)?["\']?([a-zA-Z_]\w*)["\']?\s+(?:in\s+([a-zA-Z_]\w*)\s+)?using\s+(?:one\s*hot\s*encod(?:ing|er)|onehot)\s*$', s, re.IGNORECASE)
    if m:
        col, v = m.group(1), m.group(2) or _ctx.dataset_var
        return f"import pandas as pd; {v} = pd.get_dummies({v}, columns=['{col}'], drop_first=True)"

    # ══════════════════════════════════════════════════════════════════════════
    # 5. TRAIN-TEST SPLIT
    # ══════════════════════════════════════════════════════════════════════════

    # split X and y into 80 percent train and 20 percent test [with seed 42] [stratified]
    m = re.match(
        r'^(?:split|partition)\s+([a-zA-Z_]\w*)\s+and\s+([a-zA-Z_]\w*)\s+into\s+(\d+)\s+percent\s+train(?:ing)?\s+and\s+(\d+)\s+percent\s+test(?:ing)?(?:\s+with\s+seed\s+(\d+))?(\s+stratified)?\s*$',
        s, re.IGNORECASE)
    if m:
        X_v, y_v = m.group(1), m.group(2)
        test_sz = round(int(m.group(4)) / 100, 2)
        seed = int(m.group(5)) if m.group(5) else 42
        strat = f", stratify={y_v}" if m.group(6) else ""
        _ctx.X_var = X_v; _ctx.y_var = y_v
        return (
            f"from sklearn.model_selection import train_test_split; "
            f"{_ctx.X_train}, {_ctx.X_test}, {_ctx.y_train}, {_ctx.y_test} = "
            f"train_test_split({X_v}, {y_v}, test_size={test_sz}, random_state={seed}{strat}); "
            f"print(f'[ENLANG] Train: {{len({_ctx.X_train})}} | Test: {{len({_ctx.X_test})}}')"
        )

    # stratified split into 80 percent training and 20 percent testing [with seed N] (uses ctx X, y)
    m = re.match(
        r'^stratified\s+split\s+into\s+(\d+)\s+percent\s+train(?:ing)?\s+and\s+(\d+)\s+percent\s+test(?:ing)?(?:\s+with\s+seed\s+(\d+))?\s*$',
        s, re.IGNORECASE)
    if m:
        test_sz = round(int(m.group(2)) / 100, 2)
        seed = int(m.group(3)) if m.group(3) else 42
        Xv, yv = _ctx.X_var, _ctx.y_var
        return (
            f"from sklearn.model_selection import train_test_split; "
            f"{_ctx.X_train}, {_ctx.X_test}, {_ctx.y_train}, {_ctx.y_test} = "
            f"train_test_split({Xv}, {yv}, test_size={test_sz}, random_state={seed}, stratify={yv}); "
            f"print(f'[ENLANG] Stratified Train: {{len({_ctx.X_train})}} | Test: {{len({_ctx.X_test})}}')"
        )

    # split dataset into 80 percent training and 20 percent testing (uses ctx X, y)
    m = re.match(
        r'^split\s+(?:dataset\s+)?into\s+(\d+)\s+percent\s+train(?:ing)?\s+and\s+(\d+)\s+percent\s+test(?:ing)?(?:\s+with\s+seed\s+(\d+))?\s*$',
        s, re.IGNORECASE)
    if m:
        test_sz = round(int(m.group(2)) / 100, 2)
        seed = int(m.group(3)) if m.group(3) else 42
        Xv, yv = _ctx.X_var, _ctx.y_var
        return (
            f"from sklearn.model_selection import train_test_split; "
            f"{_ctx.X_train}, {_ctx.X_test}, {_ctx.y_train}, {_ctx.y_test} = "
            f"train_test_split({Xv}, {yv}, test_size={test_sz}, random_state={seed}); "
            f"print(f'[ENLANG] Train: {{len({_ctx.X_train})}} | Test: {{len({_ctx.X_test})}}')"
        )

    # ══════════════════════════════════════════════════════════════════════════
    # 6. TEXT VECTORIZATION
    # ══════════════════════════════════════════════════════════════════════════

    # vectorize X_train and X_test using tfidf with 5000 features as vectorizer
    m = re.match(
        r'^vectorize\s+([a-zA-Z_]\w*)\s+and\s+([a-zA-Z_]\w*)\s+using\s+tfidf(?:\s+with\s+(\d+)\s+features?)?(?:\s+as\s+([a-zA-Z_]\w*))?\s*$',
        s, re.IGNORECASE)
    if m:
        Xt, Xte, max_f, vec_alias = m.group(1), m.group(2), int(m.group(3) or 10000), m.group(4) or "vectorizer"
        vv = _safe_var(vec_alias); _ctx.vectorizer_var = vv; _ctx.named_vecs[vec_alias] = vv
        return (
            f"from sklearn.feature_extraction.text import TfidfVectorizer; "
            f"{vv} = TfidfVectorizer(stop_words='english', max_features={max_f}, ngram_range=(1,2)); "
            f"{Xt} = {vv}.fit_transform({Xt}); {Xte} = {vv}.transform({Xte}); "
            f"print(f'[ENLANG] TF-IDF vectorized | Vocab: {{len({vv}.vocabulary_)}} features')"
        )

    # vectorize X_train and X_test using bag of words [with N features] [as vec]
    m = re.match(
        r'^vectorize\s+([a-zA-Z_]\w*)\s+and\s+([a-zA-Z_]\w*)\s+using\s+(?:bag\s+of\s+words|bow|count)(?:\s+with\s+(\d+)\s+features?)?(?:\s+as\s+([a-zA-Z_]\w*))?\s*$',
        s, re.IGNORECASE)
    if m:
        Xt, Xte, max_f, vec_alias = m.group(1), m.group(2), int(m.group(3) or 10000), m.group(4) or "vectorizer"
        vv = _safe_var(vec_alias); _ctx.vectorizer_var = vv
        return (
            f"from sklearn.feature_extraction.text import CountVectorizer; "
            f"{vv} = CountVectorizer(stop_words='english', max_features={max_f}); "
            f"{Xt} = {vv}.fit_transform({Xt}); {Xte} = {vv}.transform({Xte}); "
            f"print('[ENLANG] Bag-of-Words vectorized')"
        )

    # vectorize text using tfidf [with N features] [and ngrams N to M] (backward compat)
    m = re.match(r'^vectorize\s+text\s+using\s+tfidf(?:\s+with\s+max\s+features?\s+(\d+))?(?:\s+and\s+ngrams?\s+(\d+)\s+to\s+(\d+))?\s*$', s, re.IGNORECASE)
    if m:
        max_f = int(m.group(1) or 10000)
        ng_min = int(m.group(2) or 1); ng_max = int(m.group(3) or 2)
        vv = _ctx.vectorizer_var
        return (
            f"from sklearn.feature_extraction.text import TfidfVectorizer; "
            f"{vv} = TfidfVectorizer(stop_words='english', max_features={max_f}, ngram_range=({ng_min},{ng_max})); "
            f"{_ctx.X_train} = {vv}.fit_transform({_ctx.X_train}); "
            f"{_ctx.X_test} = {vv}.transform({_ctx.X_test}); "
            f"print(f'[ENLANG] TF-IDF | Vocab: {{len({vv}.vocabulary_)}} features')"
        )

    # ══════════════════════════════════════════════════════════════════════════
    # 7. FEATURE SCALING & NORMALIZATION
    # ══════════════════════════════════════════════════════════════════════════

    _SCALERS = {
        "standard scaler": ("StandardScaler", "StandardScaler()"),
        "standard":        ("StandardScaler", "StandardScaler()"),
        "minmax scaler":   ("MinMaxScaler",   "MinMaxScaler()"),
        "minmax":          ("MinMaxScaler",   "MinMaxScaler()"),
        "robust scaler":   ("RobustScaler",   "RobustScaler()"),
        "robust":          ("RobustScaler",   "RobustScaler()"),
    }

    # normalize X_train and X_test using standard scaler [as scaler]
    m = re.match(
        r'^normalize\s+([a-zA-Z_]\w*)\s+and\s+([a-zA-Z_]\w*)\s+using\s+(standard\s+scaler?|minmax\s+scaler?|robust\s+scaler?)(?:\s+as\s+([a-zA-Z_]\w*))?\s*$',
        s, re.IGNORECASE)
    if m:
        Xt, Xte, stype, alias = m.group(1), m.group(2), m.group(3).lower(), m.group(4) or "scaler"
        sv = _safe_var(alias); _ctx.scaler_var = sv; _ctx.named_scalers[alias] = sv
        sc_key = stype.replace(' scaler', '').strip()
        cls, init = _SCALERS.get(sc_key + " scaler", ("StandardScaler", "StandardScaler()"))[0], _SCALERS.get(sc_key + " scaler", ("StandardScaler", "StandardScaler()"))[1]
        return (
            f"from sklearn.preprocessing import {cls}; "
            f"{sv} = {init}; "
            f"{Xt} = {sv}.fit_transform({Xt}); {Xte} = {sv}.transform({Xte}); "
            f"print('[ENLANG] {cls} applied')"
        )

    # scale features using standard scaler [as scaler_name] (backward compat, applies to ctx train/test)
    m = re.match(r'^scale\s+features?\s+using\s+(standard|minmax|robust)(?:\s+scaler?)?(?:\s+as\s+([a-zA-Z_]\w*))?\s*$', s, re.IGNORECASE)
    if m:
        stype, alias = m.group(1).lower(), m.group(2) or "scaler"
        sv = _safe_var(alias); _ctx.scaler_var = sv
        cls_map = {"standard": ("StandardScaler", "StandardScaler()"), "minmax": ("MinMaxScaler", "MinMaxScaler()"), "robust": ("RobustScaler", "RobustScaler()")}
        cls, init = cls_map.get(stype, ("StandardScaler", "StandardScaler()"))
        return (
            f"from sklearn.preprocessing import {cls}; "
            f"{sv} = {init}; "
            f"{_ctx.X_train} = {sv}.fit_transform({_ctx.X_train}); "
            f"{_ctx.X_test} = {sv}.transform({_ctx.X_test}); "
            f"print('[ENLANG] {cls} applied')"
        )

    # ══════════════════════════════════════════════════════════════════════════
    # 8. MODEL CREATION (v2 Natural Grammar)
    # ══════════════════════════════════════════════════════════════════════════

    # create <algo> classifier as <alias> [with N trees] [with N neighbors] [with layers N N]
    m = re.match(
        r'^(?:create|initialize|define\s+model\s+as)\s+([a-zA-Z_]+(?:\s+[a-zA-Z_]+)?)\s+classifier\s+as\s+([a-zA-Z_]\w*)(?:\s+with\s+(\d+)\s+trees?)?(?:\s+with\s+(\d+)\s+neighbors?)?(?:\s+with\s+layers?\s+([\d\s]+))?\s*$',
        s, re.IGNORECASE)
    if m:
        algo = _resolve_algo(m.group(1))
        alias = m.group(2)
        trees = int(m.group(3)) if m.group(3) else 100
        neighbors = int(m.group(4)) if m.group(4) else 5
        layers_raw = m.group(5)
        layers = f"({','.join(layers_raw.split())})" if layers_raw else "(128,64)"
        mod, cls, init = _build_classifier(algo, trees, neighbors, layers)
        if mod:
            mv = _safe_var(alias)
            _ctx.model_var = mv; _ctx.named_models[alias] = mv; _ctx.model_registry[algo] = mv
            return (
                f"from {mod} import {cls}; "
                f"{mv} = {init}; "
                f"print('[ENLANG] {cls} created as {alias}')"
            )

    # create <algo> regressor as <alias> [with N trees] [with N neighbors]
    m = re.match(
        r'^(?:create|initialize|define\s+model\s+as)\s+([a-zA-Z_]+(?:\s+[a-zA-Z_]+)?)\s+regressor\s+as\s+([a-zA-Z_]\w*)(?:\s+with\s+(\d+)\s+trees?)?(?:\s+with\s+(\d+)\s+neighbors?)?\s*$',
        s, re.IGNORECASE)
    if m:
        algo = _resolve_algo(m.group(1))
        alias = m.group(2)
        trees = int(m.group(3)) if m.group(3) else 100
        neighbors = int(m.group(4)) if m.group(4) else 5
        mod, cls, init = _build_regressor(algo, trees, neighbors)
        if mod:
            mv = _safe_var(alias)
            _ctx.model_var = mv; _ctx.named_models[alias] = mv; _ctx.model_registry[algo] = mv
            return (
                f"from {mod} import {cls}; "
                f"{mv} = {init}; "
                f"print('[ENLANG] {cls} (regressor) created as {alias}')"
            )

    # backward compat: train <algo> classifier on training data (creates + fits implicit model)
    m = re.match(r'^train\s+([a-zA-Z_]+(?:\s+[a-zA-Z_]+)?)\s+classifier\s+on\s+training\s+data\s*$', s, re.IGNORECASE)
    if m:
        algo = _resolve_algo(m.group(1))
        mod, cls, init = _build_classifier(algo)
        if mod:
            mv = f"_enlg_model_{algo.replace('_','')}"
            _ctx.model_var = mv; _ctx.model_registry[algo] = mv
            fit_X = _sparse_safe(_ctx.X_train) if "boosting" in algo else _ctx.X_train
            return (
                f"from {mod} import {cls}; {mv} = {init}; {mv}.fit({fit_X}, {_ctx.y_train}); "
                f"print('[ENLANG] {cls} trained!')"
            )

    # backward compat: train <algo> regressor on training data
    m = re.match(r'^train\s+([a-zA-Z_]+(?:\s+[a-zA-Z_]+)?)\s+regressor?\s+on\s+training\s+data\s*$', s, re.IGNORECASE)
    if m:
        algo = _resolve_algo(m.group(1))
        mod, cls, init = _build_regressor(algo)
        if mod:
            mv = f"_enlg_model_{algo.replace('_','')}"
            _ctx.model_var = mv; _ctx.model_registry[algo] = mv
            fit_X = _sparse_safe(_ctx.X_train) if "boosting" in algo else _ctx.X_train
            return (
                f"from {mod} import {cls}; {mv} = {init}; {mv}.fit({fit_X}, {_ctx.y_train}); "
                f"print('[ENLANG] {cls} regressor trained!')"
            )

    # ══════════════════════════════════════════════════════════════════════════
    # 9. MODEL TRAINING (v2 Named Model)
    # ══════════════════════════════════════════════════════════════════════════

    # train <model_alias> on train data  /  train <model_alias> using train data
    m = re.match(r'^train\s+([a-zA-Z_]\w*)\s+(?:on|using)\s+train(?:ing)?\s+data\s*$', s, re.IGNORECASE)
    if m:
        alias = m.group(1)
        mv = _ctx.named_models.get(alias) or _ctx.model_registry.get(_resolve_algo(alias)) or alias
        Xt = _ctx.X_train; yt = _ctx.y_train
        fit_X = _sparse_safe(Xt) if "gb" in alias.lower() or "boosting" in alias.lower() else Xt
        return f"{mv}.fit({fit_X}, {yt}); print('[ENLANG] {alias} trained!')"

    # train <model_alias> on X_train and y_train
    m = re.match(r'^train\s+([a-zA-Z_]\w*)\s+on\s+([a-zA-Z_]\w*)\s+and\s+([a-zA-Z_]\w*)\s*$', s, re.IGNORECASE)
    if m:
        alias, Xt, yt = m.group(1), m.group(2), m.group(3)
        mv = _ctx.named_models.get(alias) or alias
        return f"{mv}.fit({Xt}, {yt}); print('[ENLANG] {alias} trained!')"

    # ══════════════════════════════════════════════════════════════════════════
    # 10. MODEL PREDICTION (v2 Named Model)
    # ══════════════════════════════════════════════════════════════════════════

    # predict using <model> on test data and store in predictions
    # test <model> on test data and store in predictions
    # predict labels for X_test using <model> and store in predictions
    m = re.match(
        r'^(?:predict\s+(?:using|labels?\s+for\s+[a-zA-Z_]\w*\s+using)|test)\s+([a-zA-Z_]\w*)\s+(?:on|using)?\s*(?:test\s+data|[a-zA-Z_]\w*)?\s+and\s+store\s+in\s+([a-zA-Z_]\w*)\s*$',
        s, re.IGNORECASE)
    if m:
        alias, out = m.group(1), m.group(2)
        mv = _ctx.named_models.get(alias) or _ctx.model_registry.get(_resolve_algo(alias)) or alias
        Xt = _ctx.X_test
        fit_X = _sparse_safe(Xt) if "gb" in alias.lower() or "boosting" in alias.lower() else Xt
        return f"{out} = {mv}.predict({fit_X})"

    # predict using model on X_test and store in result
    m = re.match(r'^predict\s+using\s+([a-zA-Z_]\w*)\s+on\s+([a-zA-Z_]\w*)\s+and\s+store\s+in\s+([a-zA-Z_]\w*)\s*$', s, re.IGNORECASE)
    if m:
        alias, Xt, out = m.group(1), m.group(2), m.group(3)
        mv = _ctx.named_models.get(alias) or alias
        return f"{out} = {mv}.predict({Xt})"

    # ══════════════════════════════════════════════════════════════════════════
    # 11. CLASSIFICATION EVALUATION (v2 Named Variables)
    # ══════════════════════════════════════════════════════════════════════════

    # calculate accuracy for predictions against y_test and store in acc
    # compute accuracy of model on test data and store in acc
    m = re.match(
        r'^(?:calculate|compute)\s+accuracy\s+(?:for\s+([a-zA-Z_]\w*)\s+against\s+([a-zA-Z_]\w*)|of\s+[a-zA-Z_]\w*\s+on\s+test\s+data)\s+and\s+store\s+in\s+([a-zA-Z_]\w*)\s*$',
        s, re.IGNORECASE)
    if m:
        preds = m.group(1) or _ctx.y_pred_var
        actual = m.group(2) or _ctx.y_test
        out = m.group(3)
        return (
            f"from sklearn.metrics import accuracy_score; "
            f"{out} = round(accuracy_score({actual}, {preds}) * 100, 2); "
            f"print(f'[ENLANG] Accuracy: {{{out}}}%')"
        )

    # compute f1 score for predictions against y_test and store in f1
    m = re.match(r'^compute\s+f1\s+(?:score\s+)?for\s+([a-zA-Z_]\w*)\s+against\s+([a-zA-Z_]\w*)\s+and\s+store\s+in\s+([a-zA-Z_]\w*)\s*$', s, re.IGNORECASE)
    if m:
        preds, actual, out = m.group(1), m.group(2), m.group(3)
        return (
            f"from sklearn.metrics import f1_score; "
            f"{out} = round(f1_score({actual}, {preds}, average='weighted') * 100, 2); "
            f"print(f'[ENLANG] F1 Score: {{{out}}}%')"
        )

    # compute roc auc for model on X_test against y_test and store in auc
    m = re.match(r'^compute\s+roc\s+auc\s+for\s+([a-zA-Z_]\w*)\s+on\s+([a-zA-Z_]\w*)\s+against\s+([a-zA-Z_]\w*)\s+and\s+store\s+in\s+([a-zA-Z_]\w*)\s*$', s, re.IGNORECASE)
    if m:
        alias, Xt, yt, out = m.group(1), m.group(2), m.group(3), m.group(4)
        mv = _ctx.named_models.get(alias) or alias
        return (
            f"from sklearn.metrics import roc_auc_score; "
            f"_rp = {mv}.predict_proba({Xt})[:, 1] if hasattr({mv}, 'predict_proba') else {mv}.decision_function({Xt}); "
            f"{out} = round(roc_auc_score({yt}, _rp), 4); "
            f"print(f'[ENLANG] ROC AUC: {{{out}}}')"
        )

    # show report for predictions against y_test
    m = re.match(r'^show\s+(?:classification\s+)?report\s+for\s+([a-zA-Z_]\w*)\s+against\s+([a-zA-Z_]\w*)\s*$', s, re.IGNORECASE)
    if m:
        preds, actual = m.group(1), m.group(2)
        return (
            f"from sklearn.metrics import classification_report; "
            f"print('\\n=== Classification Report ==='); "
            f"print(classification_report({actual}, {preds}))"
        )

    # show report for <model>  (backward compat — uses registry)
    m = re.match(r'^show\s+(?:classification\s+)?report\s+for\s+([a-zA-Z_]\w*)\s*$', s, re.IGNORECASE)
    if m:
        alias = m.group(1)
        mv = _ctx.model_registry.get(_resolve_algo(alias)) or _ctx.named_models.get(alias) or alias
        Xt = _ctx.X_test; yt = _ctx.y_test
        fit_X = _sparse_safe(Xt) if "gb" in alias.lower() or "boosting" in alias.lower() else Xt
        return (
            f"from sklearn.metrics import classification_report; "
            f"_rp = {mv}.predict({fit_X}); "
            f"print(f'\\n=== {alias} Classification Report ==='); "
            f"print(classification_report({yt}, _rp))"
        )

    # show confusion matrix for predictions against y_test
    m = re.match(r'^show\s+confusion\s+matrix\s+for\s+([a-zA-Z_]\w*)\s+against\s+([a-zA-Z_]\w*)\s*$', s, re.IGNORECASE)
    if m:
        preds, actual = m.group(1), m.group(2)
        return (
            f"from sklearn.metrics import confusion_matrix; "
            f"print('\\n=== Confusion Matrix ==='); print(confusion_matrix({actual}, {preds}))"
        )

    # backward compat: evaluate all classifiers and show comparison
    m = re.match(r'^evaluate\s+all\s+(?:classifiers?|models?)\s+and\s+show\s+comparison\s*$', s, re.IGNORECASE)
    if m:
        if not _ctx.model_registry and not _ctx.named_models:
            return "print('[ENLANG] No models trained yet.')"
        all_models = {**_ctx.model_registry, **{k: v for k, v in _ctx.named_models.items()}}
        lines = [
            "from sklearn.metrics import accuracy_score, f1_score; import warnings; warnings.filterwarnings('ignore')",
            "print('\\n' + '='*60)", "print('  MULTI-MODEL COMPARISON (Test Set)')", "print('='*60)",
            "print(f'{\"Model\":<30} {\"Accuracy\":>12} {\"F1-Score\":>12}')", "print('-'*60)",
            "_enlg_results = {}"
        ]
        for alias, mv in all_models.items():
            Xt = _sparse_safe(_ctx.X_test) if "gb" in alias.lower() or "boosting" in alias.lower() else _ctx.X_test
            lines.append(
                f"_p = {mv}.predict({Xt}); "
                f"_acc = round(accuracy_score({_ctx.y_test}, _p)*100, 2); "
                f"_f1  = round(f1_score({_ctx.y_test}, _p, average='weighted')*100, 2); "
                f"_enlg_results['{alias}'] = _acc; "
                f"print(f'{{\"  {alias}\":<30}} {{_acc:>11}}% {{_f1:>11}}%')"
            )
        lines += [
            "print('='*60)",
            "_best = max(_enlg_results, key=_enlg_results.get); print(f'  Best: {{_best}} @ {{_enlg_results[_best]}}%')",
            "print('='*60)"
        ]
        return "\n".join(lines)

    # compare <model1> and <model2> [and <model3>] on test data
    m = re.match(r'^compare\s+(.+?)\s+on\s+test\s+data\s*$', s, re.IGNORECASE)
    if m:
        raw = m.group(1)
        aliases = [a.strip() for a in re.split(r'\s+and\s+', raw, flags=re.IGNORECASE)]
        lines = [
            "from sklearn.metrics import accuracy_score, f1_score; import warnings; warnings.filterwarnings('ignore')",
            "print('\\n' + '='*60)", "print('  MODEL COMPARISON (Test Set)')", "print('='*60)",
            "print(f'{\"Model\":<30} {\"Accuracy\":>12} {\"F1-Score\":>12}')", "print('-'*60)"
        ]
        for alias in aliases:
            mv = _ctx.named_models.get(alias) or _ctx.model_registry.get(_resolve_algo(alias)) or alias
            Xt = _sparse_safe(_ctx.X_test) if "gb" in alias.lower() else _ctx.X_test
            lines.append(
                f"try:\n"
                f"    _p_{alias} = {mv}.predict({Xt}); "
                f"    _a = round(accuracy_score({_ctx.y_test}, _p_{alias})*100,2); "
                f"    _f = round(f1_score({_ctx.y_test}, _p_{alias}, average='weighted')*100,2); "
                f"    print(f'  {alias:<28} {{_a:>11}}% {{_f:>11}}%')\nexcept: pass"
            )
        lines.append("print('='*60)")
        return "\n".join(lines)

    # ══════════════════════════════════════════════════════════════════════════
    # 12. REGRESSION EVALUATION
    # ══════════════════════════════════════════════════════════════════════════

    # calculate rmse for predictions against y_test and store in err
    m = re.match(r'^(?:calculate|compute)\s+rmse\s+for\s+([a-zA-Z_]\w*)\s+against\s+([a-zA-Z_]\w*)\s+and\s+store\s+in\s+([a-zA-Z_]\w*)\s*$', s, re.IGNORECASE)
    if m:
        preds, actual, out = m.group(1), m.group(2), m.group(3)
        return (
            f"from sklearn.metrics import mean_squared_error; import math; "
            f"{out} = round(math.sqrt(mean_squared_error({actual}, {preds})), 4); "
            f"print(f'[ENLANG] RMSE: {{{out}}}')"
        )

    # compute r2 score for predictions against y_test and store in r2
    m = re.match(r'^compute\s+r2\s+(?:score\s+)?for\s+([a-zA-Z_]\w*)\s+against\s+([a-zA-Z_]\w*)\s+and\s+store\s+in\s+([a-zA-Z_]\w*)\s*$', s, re.IGNORECASE)
    if m:
        preds, actual, out = m.group(1), m.group(2), m.group(3)
        return (
            f"from sklearn.metrics import r2_score; "
            f"{out} = round(r2_score({actual}, {preds}), 4); "
            f"print(f'[ENLANG] R2 Score: {{{out}}}')"
        )

    # evaluate regression predictions against y_test and store rmse in err and r2 in r2
    m = re.match(
        r'^evaluate\s+regression\s+(?:predictions?\s+)?(?:([a-zA-Z_]\w*)\s+)?against\s+([a-zA-Z_]\w*)\s+and\s+store\s+rmse\s+in\s+([a-zA-Z_]\w*)\s+and\s+r2\s+in\s+([a-zA-Z_]\w*)\s*$',
        s, re.IGNORECASE)
    if m:
        preds = m.group(1) or _ctx.y_pred_var
        actual, rmse_v, r2_v = m.group(2), m.group(3), m.group(4)
        return (
            f"from sklearn.metrics import mean_squared_error, r2_score; import math; "
            f"{rmse_v} = round(math.sqrt(mean_squared_error({actual}, {preds})), 4); "
            f"{r2_v} = round(r2_score({actual}, {preds}), 4); "
            f"print(f'[ENLANG] RMSE: {{{rmse_v}}} | R2: {{{r2_v}}}')"
        )

    # backward compat: evaluate classifier accuracy and store in acc
    m = re.match(r'^evaluate\s+(?:classifier|model)\s+accuracy\s+and\s+store\s+in\s+([a-zA-Z_]\w*)\s*$', s, re.IGNORECASE)
    if m:
        out = m.group(1)
        mv = _ctx.model_var; yp = _ctx.y_pred_var
        return (
            f"from sklearn.metrics import accuracy_score; "
            f"{yp} = {mv}.predict({_ctx.X_test}); "
            f"{out} = round(accuracy_score({_ctx.y_test}, {yp}) * 100, 2); "
            f"print(f'[ENLANG] Accuracy: {{{out}}}%')"
        )

    # ══════════════════════════════════════════════════════════════════════════
    # 13. ENSEMBLE METHODS
    # ══════════════════════════════════════════════════════════════════════════

    # combine <model1> and <model2> [and <model3>] using soft voting as ensemble
    m = re.match(r'^combine\s+(.+?)\s+using\s+(soft|hard)\s+voting\s+as\s+([a-zA-Z_]\w*)\s*$', s, re.IGNORECASE)
    if m:
        raw, voting, alias = m.group(1), m.group(2).lower(), m.group(3)
        aliases = [a.strip() for a in re.split(r'\s+and\s+', raw, flags=re.IGNORECASE)]
        ev_list = "[" + ", ".join(f"('{a}', {_ctx.named_models.get(a) or a})" for a in aliases) + "]"
        ev_v = _safe_var(alias)
        _ctx.model_var = ev_v; _ctx.named_models[alias] = ev_v
        return (
            f"from sklearn.ensemble import VotingClassifier; from sklearn.metrics import accuracy_score; "
            f"{ev_v} = VotingClassifier(estimators={ev_list}, voting='{voting}'); "
            f"{ev_v}.fit({_ctx.X_train}, {_ctx.y_train}); "
            f"_ev_acc = round(accuracy_score({_ctx.y_test}, {ev_v}.predict({_ctx.X_test}))*100,2); "
            f"print(f'[ENLANG] {alias} ({voting} voting) Accuracy: {{_ev_acc}}%')"
        )

    # combine all models using soft voting as ensemble
    m = re.match(r'^combine\s+all\s+(?:models?|classifiers?)\s+using\s+(soft|hard)\s+voting\s+as\s+([a-zA-Z_]\w*)\s*$', s, re.IGNORECASE)
    if m:
        voting, alias = m.group(1).lower(), m.group(2)
        all_models = {**_ctx.model_registry, **_ctx.named_models}
        if not all_models:
            return "print('[ENLANG] No models to combine.')"
        ev_list = "[" + ", ".join(f"('{a}', {mv})" for a, mv in all_models.items()) + "]"
        ev_v = _safe_var(alias)
        _ctx.model_var = ev_v
        return (
            f"from sklearn.ensemble import VotingClassifier; from sklearn.metrics import accuracy_score; "
            f"{ev_v} = VotingClassifier(estimators={ev_list}, voting='{voting}'); "
            f"{ev_v}.fit({_ctx.X_train}, {_ctx.y_train}); "
            f"_ev_acc = round(accuracy_score({_ctx.y_test}, {ev_v}.predict({_ctx.X_test}))*100,2); "
            f"print(f'[ENLANG] {alias} ({voting} voting) Accuracy: {{_ev_acc}}%')"
        )

    # backward compat: use soft/hard ensemble of all trained classifiers
    m = re.match(r'^use\s+(soft|hard)\s+ensemble\s+of\s+all\s+(?:trained\s+)?(?:classifiers?|models?)\s*$', s, re.IGNORECASE)
    if m:
        voting = m.group(1).lower()
        all_models = {**_ctx.model_registry, **_ctx.named_models}
        if not all_models:
            return "print('[ENLANG] No models registered.')"
        ev_list = "[" + ", ".join(f"('{a}', {mv})" for a, mv in all_models.items()) + "]"
        return (
            f"from sklearn.ensemble import VotingClassifier; from sklearn.metrics import accuracy_score; "
            f"_enlg_vc = VotingClassifier(estimators={ev_list}, voting='{voting}'); "
            f"_enlg_vc.fit({_ctx.X_train}, {_ctx.y_train}); "
            f"_ev_acc = round(accuracy_score({_ctx.y_test}, _enlg_vc.predict({_ctx.X_test}))*100,2); "
            f"print(f'[ENLANG] {voting.title()} Voting Ensemble Accuracy: {{_ev_acc}}%')"
        )

    # backward compat: use soft ensemble of all trained classifiers
    m = re.match(r'^use\s+(?:soft\s+)?ensemble\s+of\s+all\s+(?:trained\s+)?(?:classifiers?|models?)\s*$', s, re.IGNORECASE)
    if m:
        all_models = {**_ctx.model_registry, **_ctx.named_models}
        if not all_models:
            return "print('[ENLANG] No models registered.')"
        ev_list = "[" + ", ".join(f"('{a}', {mv})" for a, mv in all_models.items()) + "]"
        return (
            f"from sklearn.ensemble import VotingClassifier; from sklearn.metrics import accuracy_score; "
            f"_enlg_vc = VotingClassifier(estimators={ev_list}, voting='soft'); "
            f"_enlg_vc.fit({_ctx.X_train}, {_ctx.y_train}); "
            f"_ev_acc = round(accuracy_score({_ctx.y_test}, _enlg_vc.predict({_ctx.X_test}))*100,2); "
            f"print(f'[ENLANG] Soft Voting Ensemble Accuracy: {{_ev_acc}}%')"
        )

    # ══════════════════════════════════════════════════════════════════════════
    # 14. FEATURE IMPORTANCE
    # ══════════════════════════════════════════════════════════════════════════

    # show feature importance of rf_model top 10  /  show feature importance of random_forest top 7
    m = re.match(r'^show\s+feature\s+importance\s+of\s+([a-zA-Z_]\w*)(?:\s+top\s+(\d+))?\s*$', s, re.IGNORECASE)
    if m:
        alias, top_n = m.group(1), int(m.group(2) or 15)
        mv = _ctx.named_models.get(alias) or _ctx.model_registry.get(_resolve_algo(alias)) or alias
        ds = _ctx.dataset_var; lc = _ctx.label_column; vv = _ctx.vectorizer_var
        return (
            f"import numpy as np; "
            f"_fi = {mv}.feature_importances_ if hasattr({mv}, 'feature_importances_') else np.abs({mv}.coef_[0]); "
            f"_fn = list({vv}.get_feature_names_out()) if '{vv}' in dir() and hasattr({vv}, 'get_feature_names_out') "
            f"else list({ds}.drop(columns=['{lc}']).columns) if '{ds}' in dir() and hasattr({ds}, 'columns') "
            f"else [f'feature_{{i}}' for i in range(len(_fi))]; "
            f"_top = np.argsort(_fi)[::-1][:{top_n}]; "
            f"print(f'\\n=== Top {top_n} Features ({alias}) ==='); "
            f"[print(f'  {{_fn[i]:<30}} {{_fi[i]:.4f}}') for i in _top]"
        )

    # ══════════════════════════════════════════════════════════════════════════
    # 15. CROSS VALIDATION
    # ══════════════════════════════════════════════════════════════════════════

    # cross validate model on X and y with 5 folds and store in cv_scores
    m = re.match(
        r'^cross\s+validate\s+([a-zA-Z_]\w*)\s+on\s+([a-zA-Z_]\w*)\s+and\s+([a-zA-Z_]\w*)\s+with\s+(\d+)\s+folds?(?:\s+and\s+store\s+in\s+([a-zA-Z_]\w*))?\s*$',
        s, re.IGNORECASE)
    if m:
        alias, Xv, yv, folds, out = m.group(1), m.group(2), m.group(3), m.group(4), m.group(5) or "_cv"
        mv = _ctx.named_models.get(alias) or alias
        return (
            f"from sklearn.model_selection import cross_val_score; import numpy as np; "
            f"{out} = cross_val_score({mv}, {Xv}, {yv}, cv={folds}, scoring='accuracy'); "
            f"print(f'[ENLANG] Cross-Val ({folds}-fold) | Scores: {{{out}.round(3)}} | Mean: {{{out}.mean()*100:.2f}}% | Std: {{{out}.std()*100:.2f}}%')"
        )

    # backward compat: cross validate <algo> with N folds
    m = re.match(r'^cross\s+validate\s+([a-zA-Z_]+(?:\s+[a-zA-Z_]+)?)\s+with\s+(\d+)\s+folds?\s*$', s, re.IGNORECASE)
    if m:
        algo, folds = _resolve_algo(m.group(1)), m.group(2)
        mv = _ctx.model_registry.get(algo, _ctx.model_var)
        return (
            f"from sklearn.model_selection import cross_val_score; import numpy as np; "
            f"_cv = cross_val_score({mv}, {_ctx.X_var}, {_ctx.y_var}, cv={folds}, scoring='accuracy'); "
            f"print(f'[ENLANG] Cross-Val ({folds}-fold) | Mean: {{_cv.mean()*100:.2f}}%')"
        )

    # ══════════════════════════════════════════════════════════════════════════
    # 16. HYPERPARAMETER TUNING
    # ══════════════════════════════════════════════════════════════════════════

    # tune <model> using grid search on X_train and y_train
    m = re.match(r'^tune\s+([a-zA-Z_]\w*)\s+using\s+(?:grid\s+search|gridsearch)(?:\s+on\s+([a-zA-Z_]\w*)\s+and\s+([a-zA-Z_]\w*))?\s*$', s, re.IGNORECASE)
    if m:
        alias, Xt, yt = m.group(1), m.group(2) or _ctx.X_train, m.group(3) or _ctx.y_train
        mv = _ctx.named_models.get(alias) or alias
        return (
            f"from sklearn.model_selection import GridSearchCV; "
            f"_pg = {{'C': [0.1,1,10]}} if hasattr({mv},'C') else {{'n_estimators':[50,100,200],'max_depth':[5,10,None]}}; "
            f"_gs = GridSearchCV({mv}, _pg, cv=5, scoring='accuracy', n_jobs=-1); "
            f"_gs.fit({Xt}, {yt}); "
            f"print(f'[ENLANG] Grid Search Best: {{_gs.best_params_}} | CV Score: {{round(_gs.best_score_*100,2)}}%')"
        )

    # tune <model> using random search with N iterations on X_train and y_train
    m = re.match(
        r'^tune\s+([a-zA-Z_]\w*)\s+using\s+(?:random\s+search|randomsearch)(?:\s+with\s+(\d+)\s+iterations?)?(?:\s+on\s+([a-zA-Z_]\w*)\s+and\s+([a-zA-Z_]\w*))?\s*$',
        s, re.IGNORECASE)
    if m:
        alias, n_iter, Xt, yt = m.group(1), m.group(2) or "20", m.group(3) or _ctx.X_train, m.group(4) or _ctx.y_train
        mv = _ctx.named_models.get(alias) or alias
        return (
            f"from sklearn.model_selection import RandomizedSearchCV; "
            f"_pd = {{'n_estimators':[50,100,150,200],'max_depth':[3,5,10,None],'min_samples_split':[2,5,10]}}; "
            f"_rs = RandomizedSearchCV({mv}, _pd, n_iter={n_iter}, cv=5, scoring='accuracy', n_jobs=-1, random_state=42); "
            f"_rs.fit({Xt}, {yt}); "
            f"print(f'[ENLANG] Random Search Best: {{_rs.best_params_}} | CV Score: {{round(_rs.best_score_*100,2)}}%')"
        )

    # ══════════════════════════════════════════════════════════════════════════
    # 17. CLUSTERING
    # ══════════════════════════════════════════════════════════════════════════

    # cluster X into 3 groups using kmeans as labels
    m = re.match(r'^cluster\s+([a-zA-Z_]\w*)\s+into\s+(\d+)\s+(?:groups?|clusters?)\s+using\s+kmeans\s+as\s+([a-zA-Z_]\w*)\s*$', s, re.IGNORECASE)
    if m:
        Xv, k, out = m.group(1), m.group(2), m.group(3)
        return (
            f"from sklearn.cluster import KMeans; import collections; "
            f"{_ctx.cluster_var} = KMeans(n_clusters={k}, random_state=42, n_init=10); "
            f"{out} = {_ctx.cluster_var}.fit_predict({Xv}); "
            f"print(f'[ENLANG] KMeans({k}) | Cluster sizes: {{dict(sorted(collections.Counter({out}).items()))}}')"
        )

    # cluster X using dbscan with eps 0.5 and min samples 5 as labels
    m = re.match(r'^cluster\s+([a-zA-Z_]\w*)\s+using\s+dbscan(?:\s+with\s+eps\s+([0-9.]+)\s+and\s+min\s+samples?\s+(\d+))?\s+as\s+([a-zA-Z_]\w*)\s*$', s, re.IGNORECASE)
    if m:
        Xv, eps, min_s, out = m.group(1), m.group(2) or "0.5", m.group(3) or "5", m.group(4)
        return (
            f"from sklearn.cluster import DBSCAN; import collections; "
            f"_dbs = DBSCAN(eps={eps}, min_samples={min_s}); "
            f"{out} = _dbs.fit_predict({Xv}); "
            f"print(f'[ENLANG] DBSCAN | Clusters: {{dict(collections.Counter({out}))}}')"
        )

    # backward compat: cluster data into N groups using kmeans
    m = re.match(r'^cluster\s+(?:data\s+)?into\s+(\d+)\s+(?:groups?|clusters?)\s+using\s+kmeans\s*$', s, re.IGNORECASE)
    if m:
        k = m.group(1)
        return (
            f"from sklearn.cluster import KMeans; import collections; "
            f"{_ctx.cluster_var} = KMeans(n_clusters={k}, random_state=42, n_init=10); "
            f"_cl = {_ctx.cluster_var}.fit_predict({_ctx.X_var}); "
            f"print(f'[ENLANG] KMeans({k}): {{dict(sorted(collections.Counter(_cl).items()))}}')"
        )

    # ══════════════════════════════════════════════════════════════════════════
    # 18. DIMENSIONALITY REDUCTION
    # ══════════════════════════════════════════════════════════════════════════

    # reduce X_train and X_test to 50 dimensions using pca
    m = re.match(r'^reduce\s+([a-zA-Z_]\w*)\s+and\s+([a-zA-Z_]\w*)\s+to\s+(\d+)\s+dimensions?\s+using\s+pca\s*$', s, re.IGNORECASE)
    if m:
        Xt, Xte, n = m.group(1), m.group(2), m.group(3)
        p = _ctx.pca_var
        return (
            f"from sklearn.decomposition import PCA; "
            f"{p} = PCA(n_components={n}, random_state=42); "
            f"{Xt} = {p}.fit_transform({_sparse_safe(Xt)}); "
            f"{Xte} = {p}.transform({_sparse_safe(Xte)}); "
            f"print(f'[ENLANG] PCA → {n} dims | Explained variance: {{sum({p}.explained_variance_ratio_)*100:.1f}}%')"
        )

    # reduce X to 2 dimensions using tsne as X_reduced
    m = re.match(r'^reduce\s+([a-zA-Z_]\w*)\s+to\s+(\d+)\s+dimensions?\s+using\s+(?:tsne|t-sne)\s+as\s+([a-zA-Z_]\w*)\s*$', s, re.IGNORECASE)
    if m:
        Xv, n, out = m.group(1), m.group(2), m.group(3)
        return (
            f"from sklearn.manifold import TSNE; "
            f"_tsne = TSNE(n_components={n}, random_state=42); "
            f"{out} = _tsne.fit_transform({_sparse_safe(Xv)}); "
            f"print('[ENLANG] t-SNE reduced to {n} dimensions')"
        )

    # backward compat: reduce dimensions to N using pca
    m = re.match(r'^reduce\s+dimensions?\s+to\s+(\d+)\s+using\s+pca\s*$', s, re.IGNORECASE)
    if m:
        n = m.group(1); p = _ctx.pca_var
        return (
            f"from sklearn.decomposition import PCA; "
            f"{p} = PCA(n_components={n}, random_state=42); "
            f"{_ctx.X_train} = {p}.fit_transform({_sparse_safe(_ctx.X_train)}); "
            f"{_ctx.X_test} = {p}.transform({_sparse_safe(_ctx.X_test)}); "
            f"print(f'[ENLANG] PCA → {n} dims | Variance: {{sum({p}.explained_variance_ratio_)*100:.1f}}%')"
        )

    # ══════════════════════════════════════════════════════════════════════════
    # 19. FEATURE SELECTION
    # ══════════════════════════════════════════════════════════════════════════

    # select top N features from X_train and X_test using chi2 / mutual info
    m = re.match(
        r'^select\s+top\s+(\d+)\s+features?\s+from\s+([a-zA-Z_]\w*)\s+and\s+([a-zA-Z_]\w*)\s+using\s+(chi2|mutual\s*info|f.classif)\s*$',
        s, re.IGNORECASE)
    if m:
        k, Xt, Xte, method = m.group(1), m.group(2), m.group(3), m.group(4).lower().replace(' ', '')
        scorer_map = {"chi2": "chi2", "mutualinfo": "mutual_info_classif", "fclassif": "f_classif"}
        scorer = scorer_map.get(method, "f_classif")
        return (
            f"from sklearn.feature_selection import SelectKBest, {scorer}; "
            f"_sel = SelectKBest({scorer}, k={k}); "
            f"{Xt} = _sel.fit_transform({Xt}, {_ctx.y_train}); "
            f"{Xte} = _sel.transform({Xte}); "
            f"print('[ENLANG] Feature Selection: {k} features selected using {method}')"
        )

    # select top N features from X_train using mutual info against y_train
    m = re.match(
        r'^select\s+top\s+(\d+)\s+features?\s+from\s+([a-zA-Z_]\w*)\s+using\s+mutual\s+info\s+against\s+([a-zA-Z_]\w*)\s*$',
        s, re.IGNORECASE)
    if m:
        k, Xt, yt = m.group(1), m.group(2), m.group(3)
        return (
            f"from sklearn.feature_selection import SelectKBest, mutual_info_classif; "
            f"_sel = SelectKBest(mutual_info_classif, k={k}); "
            f"{Xt} = _sel.fit_transform({Xt}, {yt}); "
            f"print('[ENLANG] Feature Selection: {k} features selected using mutual info')"
        )

    # ══════════════════════════════════════════════════════════════════════════
    # 20. ANOMALY DETECTION
    # ══════════════════════════════════════════════════════════════════════════

    # detect anomalies in X using isolation forest as anomaly_labels
    m = re.match(r'^detect\s+anomalies?\s+in\s+([a-zA-Z_]\w*)\s+using\s+(?:isolation\s+forest|isolationforest)\s+as\s+([a-zA-Z_]\w*)\s*$', s, re.IGNORECASE)
    if m:
        Xv, out = m.group(1), m.group(2)
        return (
            f"from sklearn.ensemble import IsolationForest; "
            f"_ifor = IsolationForest(contamination=0.05, random_state=42); "
            f"{out} = _ifor.fit_predict({Xv}); "
            f"import collections; print(f'[ENLANG] Isolation Forest | Anomalies: {{list({out}).count(-1)}} | Normal: {{list({out}).count(1)}}')"
        )

    # detect anomalies in X using local outlier factor as labels
    m = re.match(r'^detect\s+anomalies?\s+in\s+([a-zA-Z_]\w*)\s+using\s+(?:local\s+outlier\s+factor|lof)\s+as\s+([a-zA-Z_]\w*)\s*$', s, re.IGNORECASE)
    if m:
        Xv, out = m.group(1), m.group(2)
        return (
            f"from sklearn.neighbors import LocalOutlierFactor; "
            f"_lof = LocalOutlierFactor(n_neighbors=20); "
            f"{out} = _lof.fit_predict({Xv}); "
            f"import collections; print(f'[ENLANG] LOF | Anomalies: {{list({out}).count(-1)}} | Normal: {{list({out}).count(1)}}')"
        )

    # backward compat: detect anomalies using isolation forest and store in X
    m = re.match(r'^detect\s+anomalies?\s+using\s+(?:isolation\s+forest|isolationforest)\s+and\s+store\s+in\s+([a-zA-Z_]\w*)\s*$', s, re.IGNORECASE)
    if m:
        out = m.group(1)
        return (
            f"from sklearn.ensemble import IsolationForest; "
            f"_ifor = IsolationForest(contamination=0.05, random_state=42); "
            f"{out} = _ifor.fit_predict({_ctx.X_var}); "
            f"import collections; print(f'[ENLANG] Isolation Forest | Anomalies: {{list({out}).count(-1)}} | Normal: {{list({out}).count(1)}}')"
        )

    # ══════════════════════════════════════════════════════════════════════════
    # 21. IMBALANCED DATA
    # ══════════════════════════════════════════════════════════════════════════

    # balance train data using smote
    m = re.match(r'^balance\s+(?:train\s+)?(?:data\s+|classes?\s+)?using\s+smote\s*$', s, re.IGNORECASE)
    if m:
        Xt, yt = _ctx.X_train, _ctx.y_train
        return (
            f"from imblearn.over_sampling import SMOTE; "
            f"_sm = SMOTE(random_state=42); "
            f"{Xt}, {yt} = _sm.fit_resample({_sparse_safe(Xt)}, {yt}); "
            f"import collections; print(f'[ENLANG] SMOTE | Class dist: {{dict(collections.Counter({yt}))}}')"
        )

    # oversample train data using random oversampling
    m = re.match(r'^oversample\s+(?:train\s+)?(?:data\s+|minority\s+class\s+)?using\s+(?:random\s+oversampling|ros)\s*$', s, re.IGNORECASE)
    if m:
        Xt, yt = _ctx.X_train, _ctx.y_train
        return (
            f"from imblearn.over_sampling import RandomOverSampler; "
            f"_ros = RandomOverSampler(random_state=42); "
            f"{Xt}, {yt} = _ros.fit_resample({_sparse_safe(Xt)}, {yt}); "
            f"import collections; print(f'[ENLANG] RandomOverSampler | Class dist: {{dict(collections.Counter({yt}))}}')"
        )

    # undersample train data using random undersampling
    m = re.match(r'^undersample\s+(?:train\s+)?(?:data\s+|majority\s+class\s+)?using\s+(?:random\s+undersampling|rus)\s*$', s, re.IGNORECASE)
    if m:
        Xt, yt = _ctx.X_train, _ctx.y_train
        return (
            f"from imblearn.under_sampling import RandomUnderSampler; "
            f"_rus = RandomUnderSampler(random_state=42); "
            f"{Xt}, {yt} = _rus.fit_resample({_sparse_safe(Xt)}, {yt}); "
            f"import collections; print(f'[ENLANG] RandomUnderSampler | Class dist: {{dict(collections.Counter({yt}))}}')"
        )

    # ══════════════════════════════════════════════════════════════════════════
    # 22. STATISTICAL TESTS
    # ══════════════════════════════════════════════════════════════════════════

    # run t-test on column "A" and column "B" in df  /  run t-test between A and B
    m = re.match(
        r'^run\s+t.test\s+(?:on|between)\s+(?:column\s+)?["\']?([a-zA-Z_]\w*)["\']?\s+and\s+(?:column\s+)?["\']?([a-zA-Z_]\w*)["\']?(?:\s+in\s+([a-zA-Z_]\w*))?\s*$',
        s, re.IGNORECASE)
    if m:
        c1, c2, v = m.group(1), m.group(2), m.group(3) or _ctx.dataset_var
        return (
            f"from scipy import stats; "
            f"_t, _p = stats.ttest_ind({v}['{c1}'].dropna(), {v}['{c2}'].dropna()); "
            f"_sig = 'SIGNIFICANT' if _p < 0.05 else 'NOT SIGNIFICANT'; "
            f"print(f'[ENLANG STATS] T-Test | t={{_t:.4f}} | p={{_p:.6f}} | {{_sig}}')"
        )

    # run chi-square test on column "A" and column "B" in df
    m = re.match(
        r'^run\s+chi.square\s+test\s+on\s+(?:column\s+)?["\']?([a-zA-Z_]\w*)["\']?\s+and\s+(?:column\s+)?["\']?([a-zA-Z_]\w*)["\']?(?:\s+in\s+([a-zA-Z_]\w*))?\s*$',
        s, re.IGNORECASE)
    if m:
        c1, c2, v = m.group(1), m.group(2), m.group(3) or _ctx.dataset_var
        return (
            f"from scipy import stats; import pandas as pd; "
            f"_ct = pd.crosstab({v}['{c1}'], {v}['{c2}']); "
            f"_chi2, _p, _dof, _ = stats.chi2_contingency(_ct); "
            f"_sig = 'SIGNIFICANT' if _p < 0.05 else 'NOT SIGNIFICANT'; "
            f"print(f'[ENLANG STATS] Chi-Square | chi2={{_chi2:.4f}} | p={{_p:.6f}} | {{_sig}}')"
        )

    # run anova on column "price" grouped by column "category" in df
    m = re.match(
        r'^run\s+anova\s+on\s+(?:column\s+)?["\']?([a-zA-Z_]\w*)["\']?\s+grouped\s+by\s+(?:column\s+)?["\']?([a-zA-Z_]\w*)["\']?(?:\s+in\s+([a-zA-Z_]\w*))?\s*$',
        s, re.IGNORECASE)
    if m:
        val_col, grp_col, v = m.group(1), m.group(2), m.group(3) or _ctx.dataset_var
        return (
            f"from scipy import stats; "
            f"_groups = [{v}[{v}['{grp_col}']==g]['{val_col}'].dropna().values for g in {v}['{grp_col}'].unique()]; "
            f"_f, _p = stats.f_oneway(*_groups); "
            f"_sig = 'SIGNIFICANT' if _p < 0.05 else 'NOT SIGNIFICANT'; "
            f"print(f'[ENLANG STATS] ANOVA | F={{_f:.4f}} | p={{_p:.6f}} | {{_sig}}')"
        )

    # compute correlation between column "A" and column "B" in df
    m = re.match(
        r'^compute\s+(?:pearson\s+)?correlation\s+between\s+(?:column\s+)?["\']?([a-zA-Z_]\w*)["\']?\s+and\s+(?:column\s+)?["\']?([a-zA-Z_]\w*)["\']?(?:\s+in\s+([a-zA-Z_]\w*))?\s*$',
        s, re.IGNORECASE)
    if m:
        c1, c2, v = m.group(1), m.group(2), m.group(3) or _ctx.dataset_var
        return (
            f"from scipy import stats; "
            f"_r, _p = stats.pearsonr({v}['{c1}'].dropna(), {v}['{c2}'].dropna()); "
            f"print(f'[ENLANG STATS] Pearson r={{_r:.4f}} | p={{_p:.6f}}')"
        )

    # compute spearman correlation between A and B in df
    m = re.match(
        r'^compute\s+spearman\s+correlation\s+between\s+(?:column\s+)?["\']?([a-zA-Z_]\w*)["\']?\s+and\s+(?:column\s+)?["\']?([a-zA-Z_]\w*)["\']?(?:\s+in\s+([a-zA-Z_]\w*))?\s*$',
        s, re.IGNORECASE)
    if m:
        c1, c2, v = m.group(1), m.group(2), m.group(3) or _ctx.dataset_var
        return (
            f"from scipy import stats; "
            f"_r, _p = stats.spearmanr({v}['{c1}'].dropna(), {v}['{c2}'].dropna()); "
            f"print(f'[ENLANG STATS] Spearman rho={{_r:.4f}} | p={{_p:.6f}}')"
        )

    # show outliers in column "price" in df using iqr
    m = re.match(
        r'^show\s+outliers\s+in\s+(?:column\s+)?["\']?([a-zA-Z_]\w*)["\']?(?:\s+in\s+([a-zA-Z_]\w*))?(?:\s+using\s+(iqr|zscore|z.score))?\s*$',
        s, re.IGNORECASE)
    if m:
        col, v, method = m.group(1), m.group(2) or _ctx.dataset_var, (m.group(3) or "iqr").lower().replace('-','')
        if method == "iqr":
            return (
                f"_q1 = {v}['{col}'].quantile(0.25); _q3 = {v}['{col}'].quantile(0.75); _iqr = _q3 - _q1; "
                f"_out = {v}[({v}['{col}'] < _q1-1.5*_iqr) | ({v}['{col}'] > _q3+1.5*_iqr)]; "
                f"print(f'[ENLANG STATS] Outliers in {col} (IQR): {{len(_out)}} rows')"
            )
        else:
            return (
                f"import numpy as np; _z = np.abs(({v}['{col}']-{v}['{col}'].mean())/{v}['{col}'].std()); "
                f"_out = {v}[_z > 3]; print(f'[ENLANG STATS] Outliers in {col} (Z-Score): {{len(_out)}} rows')"
            )

    # ══════════════════════════════════════════════════════════════════════════
    # 23. DATA WRANGLING
    # ══════════════════════════════════════════════════════════════════════════

    # group df by column "category" and compute mean of column "sales" as result
    m = re.match(
        r'^group\s+([a-zA-Z_]\w*)\s+by\s+(?:column\s+)?["\']?([a-zA-Z_]\w*)["\']?\s+and\s+compute\s+(mean|sum|count|max|min|median|std)(?:\s+of\s+(?:column\s+)?["\']?([a-zA-Z_]\w*)["\']?)?\s+as\s+([a-zA-Z_]\w*)\s*$',
        s, re.IGNORECASE)
    if m:
        v, grp, agg, col2, out = m.group(1), m.group(2), m.group(3).lower(), m.group(4), m.group(5)
        if col2:
            return f"{out} = {v}.groupby('{grp}')['{col2}'].{agg}().reset_index()"
        else:
            return f"{out} = {v}.groupby('{grp}').{agg}(numeric_only=True).reset_index()"

    # group df by column and compute mean (print, no store)
    m = re.match(r'^group\s+([a-zA-Z_]\w*)\s+by\s+(?:column\s+)?["\']?([a-zA-Z_]\w*)["\']?\s+and\s+compute\s+(mean|sum|count|max|min|median|std)\s*$', s, re.IGNORECASE)
    if m:
        v, grp, agg = m.group(1), m.group(2), m.group(3).lower()
        return f"print({v}.groupby('{grp}').{agg}(numeric_only=True).round(3).to_string())"

    # filter df where column "age" > 25 as young_df  /  filter df where column age > 25 and store in young_df
    m = re.match(
        r'^filter\s+([a-zA-Z_]\w*)\s+where\s+(?:column\s+)?["\']?([a-zA-Z_]\w*)["\']?\s+(>|<|>=|<=|==|!=|equals?|greater\s+than|less\s+than)\s+(.+?)\s+as\s+([a-zA-Z_]\w*)\s*$',
        s, re.IGNORECASE)
    if m:
        v, col, op_r, val, out = m.group(1), m.group(2), m.group(3), m.group(4).strip(), m.group(5)
        op_map = {"equals": "==", "equal": "==", "greater than": ">", "less than": "<"}
        op = op_map.get(op_r.lower(), op_r)
        return f"{out} = {v}[{v}['{col}'] {op} {val}].reset_index(drop=True)"

    # sort df by column "score" descending as sorted_df
    m = re.match(r'^sort\s+([a-zA-Z_]\w*)\s+by\s+(?:column\s+)?["\']?([a-zA-Z_]\w*)["\']?\s+(ascending|descending)\s+as\s+([a-zA-Z_]\w*)\s*$', s, re.IGNORECASE)
    if m:
        v, col, order, out = m.group(1), m.group(2), m.group(3).lower(), m.group(4)
        asc = "True" if order == "ascending" else "False"
        return f"{out} = {v}.sort_values(by='{col}', ascending={asc}).reset_index(drop=True)"

    # merge df1 and df2 on column "id" as merged_df
    m = re.match(r'^merge\s+([a-zA-Z_]\w*)\s+and\s+([a-zA-Z_]\w*)\s+on\s+(?:column\s+)?["\']?([a-zA-Z_]\w*)["\']?\s+as\s+([a-zA-Z_]\w*)\s*$', s, re.IGNORECASE)
    if m:
        v1, v2, col, out = m.group(1), m.group(2), m.group(3), m.group(4)
        return f"{out} = {v1}.merge({v2}, on='{col}', how='inner')"

    # add column "total" as salary + bonus to df
    m = re.match(r'^add\s+(?:column\s+)?["\']?([a-zA-Z_]\w*)["\']?\s+as\s+(.+?)\s+to\s+([a-zA-Z_]\w*)\s*$', s, re.IGNORECASE)
    if m:
        new_col, expr, v = m.group(1), m.group(2), m.group(3)
        return f"{v}['{new_col}'] = {expr}"

    # ══════════════════════════════════════════════════════════════════════════
    # 24. TIME SERIES
    # ══════════════════════════════════════════════════════════════════════════

    # compute rolling mean of column "sales" in df with window 7 and store in rolling_mean
    m = re.match(
        r'^compute\s+rolling\s+(mean|sum|std|max|min)\s+of\s+(?:column\s+)?["\']?([a-zA-Z_]\w*)["\']?(?:\s+in\s+([a-zA-Z_]\w*))?\s+with\s+window\s+(\d+)\s+and\s+store\s+in\s+([a-zA-Z_]\w*)\s*$',
        s, re.IGNORECASE)
    if m:
        agg, col, v, win, out = m.group(1).lower(), m.group(2), m.group(3) or _ctx.dataset_var, m.group(4), m.group(5)
        return f"{out} = {v}['{col}'].rolling(window={win}).{agg}()"

    # lag column "price" in df by 3 periods and store in price_lagged
    m = re.match(
        r'^lag\s+(?:column\s+)?["\']?([a-zA-Z_]\w*)["\']?(?:\s+in\s+([a-zA-Z_]\w*))?\s+by\s+(\d+)\s+periods?\s+and\s+store\s+in\s+([a-zA-Z_]\w*)\s*$',
        s, re.IGNORECASE)
    if m:
        col, v, n, out = m.group(1), m.group(2) or _ctx.dataset_var, m.group(3), m.group(4)
        return f"{out} = {v}['{col}'].shift({n})"

    # ══════════════════════════════════════════════════════════════════════════
    # 25. NLP
    # ══════════════════════════════════════════════════════════════════════════

    # analyze sentiment of column "text" in df and store in sentiment_scores
    m = re.match(
        r'^analyze\s+sentiment\s+of\s+(?:column\s+)?["\']?([a-zA-Z_]\w*)["\']?(?:\s+in\s+([a-zA-Z_]\w*))?\s+and\s+store\s+in\s+([a-zA-Z_]\w*)\s*$',
        s, re.IGNORECASE)
    if m:
        col, v, out = m.group(1), m.group(2) or _ctx.dataset_var, m.group(3)
        return (
            f"from textblob import TextBlob; "
            f"{out} = {v}['{col}'].fillna('').apply(lambda t: TextBlob(str(t)).sentiment.polarity); "
            f"print(f'[ENLANG NLP] Sentiment | Mean: {{round({out}.mean(),3)}} | Pos: {{({out}>0).sum()}} | Neg: {{({out}<0).sum()}}')"
        )

    # show word frequency of column "text" in df with top 20 words
    m = re.match(
        r'^show\s+word\s+frequency\s+of\s+(?:column\s+)?["\']?([a-zA-Z_]\w*)["\']?(?:\s+in\s+([a-zA-Z_]\w*))?\s+(?:with\s+top\s+|top\s+)?(\d+)?\s*(?:words?)?\s*$',
        s, re.IGNORECASE)
    if m:
        col, v, top_n = m.group(1), m.group(2) or _ctx.dataset_var, int(m.group(3) or 20)
        return (
            f"from collections import Counter; "
            f"_wf = Counter(' '.join({v}['{col}'].fillna('').str.lower()).split()).most_common({top_n}); "
            f"print(f'\\n=== Top {top_n} Words in {col} ==='); [print(f'  {{w:<25}} {{c}}') for w, c in _wf]"
        )

    # compute similarity between "text1" and "text2" and store in sim
    m = re.match(r'^compute\s+similarity\s+between\s+["\'](.+?)["\']\s+and\s+["\'](.+?)["\']\s+and\s+store\s+in\s+([a-zA-Z_]\w*)\s*$', s, re.IGNORECASE)
    if m:
        t1, t2, out = m.group(1), m.group(2), m.group(3)
        return (
            f"from sklearn.feature_extraction.text import TfidfVectorizer; "
            f"from sklearn.metrics.pairwise import cosine_similarity; "
            f"_sv = TfidfVectorizer().fit_transform(['{t1}', '{t2}']); "
            f"{out} = round(float(cosine_similarity(_sv[0], _sv[1])[0][0])*100, 2); "
            f"print(f'[ENLANG NLP] Cosine Similarity: {{{out}}}%')"
        )

    # ══════════════════════════════════════════════════════════════════════════
    # 26. PIPELINE
    # ══════════════════════════════════════════════════════════════════════════

    # create pipeline with tfidf and naive bayes as my_pipeline
    m = re.match(r'^create\s+pipeline\s+with\s+(?:tfidf|tf.idf)\s+and\s+([a-zA-Z_]+(?:\s+[a-zA-Z_]+)?)\s+as\s+([a-zA-Z_]\w*)\s*$', s, re.IGNORECASE)
    if m:
        algo, alias = _resolve_algo(m.group(1)), m.group(2)
        pv = _safe_var(alias); _ctx.pipeline_var = pv
        if algo in _CLASSIFIERS:
            mod, cls, init = _build_classifier(algo)
            return (
                f"from sklearn.pipeline import Pipeline; from sklearn.feature_extraction.text import TfidfVectorizer; from {mod} import {cls}; "
                f"{pv} = Pipeline([('tfidf', TfidfVectorizer(stop_words='english', max_features=10000)), ('{algo}', {init})]); "
                f"print('[ENLANG] Pipeline created: tfidf + {cls}')"
            )

    # train pipeline on X_train and y_train  /  train pipeline on train data
    m = re.match(r'^train\s+([a-zA-Z_]\w*)\s+pipeline\s+on\s+(?:([a-zA-Z_]\w*)\s+and\s+([a-zA-Z_]\w*)|train(?:ing)?\s+data)\s*$', s, re.IGNORECASE)
    if m:
        alias, Xt, yt = m.group(1), m.group(2) or _ctx.X_train, m.group(3) or _ctx.y_train
        pv = _ctx.named_models.get(alias) or alias
        return f"{pv}.fit({Xt}, {yt}); print('[ENLANG] {alias} pipeline trained!')"

    # backward compat: create pipeline with tfidf and ...
    m = re.match(r'^create\s+pipeline\s+with\s+(?:tfidf|tf.idf)\s+and\s+([a-zA-Z_]+(?:\s+[a-zA-Z_]+)?)\s*$', s, re.IGNORECASE)
    if m:
        algo = _resolve_algo(m.group(1))
        pv = _ctx.pipeline_var
        if algo in _CLASSIFIERS:
            mod, cls, init = _build_classifier(algo)
            return (
                f"from sklearn.pipeline import Pipeline; from sklearn.feature_extraction.text import TfidfVectorizer; from {mod} import {cls}; "
                f"{pv} = Pipeline([('tfidf', TfidfVectorizer(stop_words='english', max_features=10000)), ('{algo}', {init})])"
            )

    # ══════════════════════════════════════════════════════════════════════════
    # 27. SAVE / LOAD MODEL & VECTORIZER
    # ══════════════════════════════════════════════════════════════════════════

    # save <model_alias> to "model.pkl"  /  save model to "file"
    m = re.match(r'^save\s+([a-zA-Z_]\w*)\s+to\s+["\'](.+?)["\']\s*$', s, re.IGNORECASE)
    if m:
        alias, path = m.group(1), m.group(2)
        mv = _ctx.named_models.get(alias) or _ctx.named_vecs.get(alias) or _ctx.named_scalers.get(alias) or alias
        return (
            f"import joblib; joblib.dump({mv}, '{path}'); "
            f"print('[ENLANG] {alias} saved to {path}')"
        )

    # load model from "model.pkl" as my_model
    m = re.match(r'^load\s+(?:model|vectorizer|scaler)\s+from\s+["\'](.+?)["\']\s+as\s+([a-zA-Z_]\w*)\s*$', s, re.IGNORECASE)
    if m:
        path, alias = m.group(1), m.group(2)
        mv = _safe_var(alias); _ctx.model_var = mv; _ctx.named_models[alias] = mv
        return (
            f"import joblib; {mv} = joblib.load('{path}'); "
            f"print('[ENLANG] {alias} loaded from {path}')"
        )

    # backward compat: save model to / load model from
    m = re.match(r'^save\s+model\s+to\s+["\'](.+?)["\']\s*$', s, re.IGNORECASE)
    if m:
        return f"import joblib; joblib.dump({_ctx.model_var}, '{m.group(1)}'); print('[ENLANG] Model saved to {m.group(1)}')"
    m = re.match(r'^save\s+vectorizer\s+to\s+["\'](.+?)["\']\s*$', s, re.IGNORECASE)
    if m:
        return f"import joblib; joblib.dump({_ctx.vectorizer_var}, '{m.group(1)}'); print('[ENLANG] Vectorizer saved')"

    # ══════════════════════════════════════════════════════════════════════════
    # 28. LIVE PREDICTION (v2 named)
    # ══════════════════════════════════════════════════════════════════════════

    # classify "this is spam" using model and vectorizer and store in result
    m = re.match(
        r'^classify\s+["\'](.+?)["\']\s+using\s+([a-zA-Z_]\w*)\s+and\s+([a-zA-Z_]\w*)\s+and\s+store\s+in\s+([a-zA-Z_]\w*)\s*$',
        s, re.IGNORECASE)
    if m:
        text, m_alias, v_alias, out = m.group(1), m.group(2), m.group(3), m.group(4)
        mv = _ctx.named_models.get(m_alias) or m_alias
        vv = _ctx.named_vecs.get(v_alias) or v_alias
        return f"{out} = {mv}.predict({vv}.transform(['{text}']))[0]"

    # predict escalation from "text" using ensemble (backward compat)
    m = re.match(r'^predict\s+escalation\s+from\s+["\'](.+?)["\']\s+using\s+ensemble\s*$', s, re.IGNORECASE)
    if m:
        text = m.group(1)
        vv = _ctx.vectorizer_var
        all_models = {**_ctx.model_registry, **_ctx.named_models}
        if not all_models:
            return f"print('[ENLANG] No models trained.')"
        proba_parts = [f"float({mv}.predict_proba({vv}.transform(['{text}']))[0][1])" for mv in all_models.values()]
        avg = "(" + " + ".join(proba_parts) + f") / {len(proba_parts)}"
        return (
            f"_ep = round(({avg}) * 100, 1); "
            f"_risk = 'HIGH ESCALATION RISK' if _ep > 70 else 'MODERATE RISK' if _ep > 40 else 'LOW RISK'; "
            f"print(f'Headline: {text}\\n  Escalation Chance: {{_ep}}% | {{_risk}}')"
        )

    # predict escalation from "text" (single model)
    m = re.match(r'^predict\s+escalation\s+from\s+["\'](.+?)["\']\s*$', s, re.IGNORECASE)
    if m:
        text = m.group(1); mv = _ctx.model_var; vv = _ctx.vectorizer_var
        return (
            f"_ep = round(float({mv}.predict_proba({vv}.transform(['{text}']))[0][1])*100, 1); "
            f"_risk = 'HIGH ESCALATION RISK' if _ep > 70 else 'MODERATE RISK' if _ep > 40 else 'LOW RISK'; "
            f"print(f'Headline: {text}\\n  Escalation Chance: {{_ep}}% | {{_risk}}')"
        )

    # predict spam from "text"
    m = re.match(r'^predict\s+spam\s+from\s+["\'](.+?)["\']\s*$', s, re.IGNORECASE)
    if m:
        text = m.group(1); mv = _ctx.model_var; vv = _ctx.vectorizer_var
        return (
            f"_pred = {mv}.predict({vv}.transform(['{text}']))[0]; "
            f"_pr = {mv}.predict_proba({vv}.transform(['{text}']))[0]; "
            f"print('[SPAM] Conf: '+str(round(float(_pr[1])*100,2))+'%' if _pred==1 "
            f"else '[NOT SPAM] Conf: '+str(round(float(_pr[0])*100,2))+'%')"
        )

    # predict label for "text" and store in result
    m = re.match(r'^predict\s+label\s+for\s+["\'](.+?)["\']\s+and\s+store\s+in\s+([a-zA-Z_]\w*)\s*$', s, re.IGNORECASE)
    if m:
        text, out = m.group(1), m.group(2)
        return f"{out} = {_ctx.model_var}.predict({_ctx.vectorizer_var}.transform(['{text}']))[0]"

    # ══════════════════════════════════════════════════════════════════════════
    # 29. VISUALIZATION
    # ══════════════════════════════════════════════════════════════════════════

    m = re.match(r'^plot\s+(?:column\s+)?distribution\s+of\s+["\']?([a-zA-Z_]\w*)["\']?(?:\s+in\s+([a-zA-Z_]\w*))?\s*$', s, re.IGNORECASE)
    if m:
        col, v = m.group(1), m.group(2) or _ctx.dataset_var
        return (
            f"import matplotlib.pyplot as plt; "
            f"{v}['{col}'].value_counts().plot(kind='bar', color='steelblue', title='{col} Distribution'); "
            f"plt.tight_layout(); plt.show()"
        )

    m = re.match(r'^plot\s+correlation\s+heatmap(?:\s+of\s+([a-zA-Z_]\w*))?\s*$', s, re.IGNORECASE)
    if m:
        v = m.group(1) or _ctx.dataset_var
        return (
            f"import matplotlib.pyplot as plt; import seaborn as sns; "
            f"plt.figure(figsize=(10,8)); sns.heatmap({v}.corr(numeric_only=True), annot=True, cmap='coolwarm', fmt='.2f'); "
            f"plt.title('Correlation Heatmap'); plt.tight_layout(); plt.show()"
        )

    # ── Not an ML line ─────────────────────────────────────────────────────────
    return None
