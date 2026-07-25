"""
EnLang ML Engine — Natural English AI/ML & Data Science Syntax Transpiler
==========================================================================
Converts simplified natural English ML statements into production sklearn/pandas code.

Supported Natural Syntax:
  .enlg (Python target) with ML/DS keywords

DESIGN PRINCIPLE:
  - PURELY ADDITIVE: Zero changes to existing EnLang syntax
  - Native Python passthrough still works
  - EnLang natural syntax (set/define/for/while etc.) still works
  - ML Engine adds a NEW 3rd layer on top
"""

import re


# ─────────────────────────────────────────────────────────────────────────────
# INTERNAL STATE TRACKER
# Tracks context variables (dataset, model, vectorizer) across lines
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
        self.text_column     = "text"
        self.label_column    = "label"
        self.y_pred_var      = "_enlg_y_pred"
        self.scaler_var      = "_enlg_scaler"
        self.encoder_var     = "_enlg_enc"
        self.pipeline_var    = "_enlg_pipeline"

# Single global context instance (per transpile session)
_ctx = MLContext()


def reset_context():
    _ctx.reset()


def _strip(s):
    return s.strip().strip('"').strip("'")


# ─────────────────────────────────────────────────────────────────────────────
# NATURAL ML SYNTAX → PYTHON CODE TRANSPILER
# Returns transpiled Python string or None if not an ML line
# ─────────────────────────────────────────────────────────────────────────────

def translate_ml_line(line: str) -> str | None:
    """
    Attempts to translate a natural EnLang ML line into Python sklearn/pandas code.
    Returns the transpiled Python string, or None if this is not an ML line.
    """
    s = line.strip()

    # ── 1. LOAD DATASET ──────────────────────────────────────────────────────

    # load dataset from "file.csv" into df
    m = re.match(
        r'^load\s+dataset\s+from\s+["\'](.+?)["\']\s+into\s+([a-zA-Z_]\w*)\s*$', s, re.IGNORECASE)
    if m:
        path, var = m.group(1), m.group(2)
        _ctx.dataset_var = var
        return (
            f"import pandas as pd; "
            f"{var} = pd.read_csv('{path}', encoding='utf-8', on_bad_lines='skip')"
        )

    # load dataset from "file.csv" with text column email and label column spam into df
    m = re.match(
        r'^load\s+dataset\s+from\s+["\'](.+?)["\']\s+with\s+text\s+column\s+([a-zA-Z_]\w*)\s+and\s+label\s+column\s+([a-zA-Z_]\w*)(?:\s+into\s+([a-zA-Z_]\w*))?\s*$',
        s, re.IGNORECASE)
    if m:
        path, tcol, lcol, var = m.group(1), m.group(2), m.group(3), m.group(4) or "df"
        _ctx.dataset_var = var
        _ctx.text_column = tcol
        _ctx.label_column = lcol
        _ctx.X_var = "X"
        _ctx.y_var = "y"
        return (
            f"import pandas as pd; "
            f"{var} = pd.read_csv('{path}', encoding='utf-8', on_bad_lines='skip'); "
            f"X = {var}['{tcol}'].fillna('').tolist(); "
            f"y = {var}['{lcol}'].tolist()"
        )

    # load dataset from "file.csv" with labels column spam
    m = re.match(
        r'^load\s+dataset\s+from\s+["\'](.+?)["\']\s+with\s+labels?\s+column\s+([a-zA-Z_]\w*)\s*$',
        s, re.IGNORECASE)
    if m:
        path, lcol = m.group(1), m.group(2)
        _ctx.label_column = lcol
        _ctx.X_var = "X"
        _ctx.y_var = "y"
        return (
            f"import pandas as pd; "
            f"{_ctx.dataset_var} = pd.read_csv('{path}', encoding='utf-8', on_bad_lines='skip'); "
            f"X = {_ctx.dataset_var}.drop(columns=['{lcol}']).values.tolist(); "
            f"y = {_ctx.dataset_var}['{lcol}'].tolist()"
        )

    # load csv "file.csv" into df
    m = re.match(r'^load\s+csv\s+["\'](.+?)["\']\s+into\s+([a-zA-Z_]\w*)\s*$', s, re.IGNORECASE)
    if m:
        path, var = m.group(1), m.group(2)
        _ctx.dataset_var = var
        return f"import pandas as pd; {var} = pd.read_csv('{path}', encoding='utf-8', on_bad_lines='skip')"

    # ── 2. SHOW / EXPLORE DATASET ─────────────────────────────────────────────

    # show dataset info
    m = re.match(r'^show\s+dataset\s+info\s*$', s, re.IGNORECASE)
    if m:
        return (
            f"print('\\n=== Dataset Info ===')\n"
            f"print(f'Shape: {{{_ctx.dataset_var}.shape}}')\n"
            f"print(f'Columns: {{{_ctx.dataset_var}.columns.tolist()}}')\n"
            f"{_ctx.dataset_var}.info()"
        )

    # show dataset statistics
    m = re.match(r'^show\s+dataset\s+statistics?\s*$', s, re.IGNORECASE)
    if m:
        return f"print('\\n=== Dataset Statistics ==='); print({_ctx.dataset_var}.describe())"

    # show first N rows
    m = re.match(r'^show\s+first\s+(\d+)\s+rows?\s*$', s, re.IGNORECASE)
    if m:
        n = m.group(1)
        return f"print('\\n=== First {n} Rows ==='); print({_ctx.dataset_var}.head({n}))"

    # show column distribution of columnname
    m = re.match(r'^show\s+(?:column\s+)?distribution\s+of\s+([a-zA-Z_]\w*)\s*$', s, re.IGNORECASE)
    if m:
        col = m.group(1)
        return f"print('\\n=== {col} Distribution ==='); print({_ctx.dataset_var}['{col}'].value_counts())"

    # show missing values
    m = re.match(r'^show\s+missing\s+values?\s*$', s, re.IGNORECASE)
    if m:
        return f"print('\\n=== Missing Values ==='); print({_ctx.dataset_var}.isnull().sum())"

    # ── 3. DATA CLEANING ─────────────────────────────────────────────────────

    # drop missing values from df
    m = re.match(r'^drop\s+missing\s+values?\s+from\s+([a-zA-Z_]\w*)\s*$', s, re.IGNORECASE)
    if m:
        var = m.group(1)
        return f"{var} = {var}.dropna().reset_index(drop=True)"

    # drop missing values
    m = re.match(r'^drop\s+missing\s+values?\s*$', s, re.IGNORECASE)
    if m:
        return f"{_ctx.dataset_var} = {_ctx.dataset_var}.dropna().reset_index(drop=True)"

    # fill missing values in column age with 0
    m = re.match(r'^fill\s+missing\s+values?\s+in\s+(?:column\s+)?([a-zA-Z_]\w*)\s+with\s+(.+)\s*$', s, re.IGNORECASE)
    if m:
        col, val = m.group(1), m.group(2).strip()
        return f"{_ctx.dataset_var}['{col}'] = {_ctx.dataset_var}['{col}'].fillna({val})"

    # ── 4. SPLIT DATASET ─────────────────────────────────────────────────────

    # split dataset into 80 percent training and 20 percent testing
    m = re.match(
        r'^split\s+(?:dataset\s+)?into\s+(\d+)\s+percent\s+training\s+and\s+(\d+)\s+percent\s+testing(?:\s+with\s+seed\s+(\d+))?\s*$',
        s, re.IGNORECASE)
    if m:
        train_pct, test_pct = int(m.group(1)), int(m.group(2))
        seed = int(m.group(3)) if m.group(3) else 42
        test_size = round(test_pct / 100, 2)
        Xv, yv = _ctx.X_var, _ctx.y_var
        return (
            f"from sklearn.model_selection import train_test_split; "
            f"{_ctx.X_train}, {_ctx.X_test}, {_ctx.y_train}, {_ctx.y_test} = "
            f"train_test_split({Xv}, {yv}, test_size={test_size}, random_state={seed}); "
            f"print(f'Training: {{len({_ctx.X_train})}} samples | Testing: {{len({_ctx.X_test})}} samples')"
        )

    # ── 5. VECTORIZE / FEATURE EXTRACTION ────────────────────────────────────

    # vectorize text using tfidf with max features 5000
    m = re.match(
        r'^vectorize\s+text\s+using\s+tfidf(?:\s+with\s+max\s+features?\s+(\d+))?\s*$',
        s, re.IGNORECASE)
    if m:
        max_feat = int(m.group(1)) if m.group(1) else 10000
        v = _ctx.vectorizer_var
        return (
            f"from sklearn.feature_extraction.text import TfidfVectorizer; "
            f"{v} = TfidfVectorizer(stop_words='english', max_features={max_feat}); "
            f"{_ctx.X_train} = {v}.fit_transform({_ctx.X_train}); "
            f"{_ctx.X_test} = {v}.transform({_ctx.X_test})"
        )

    # vectorize text using bag of words
    m = re.match(r'^vectorize\s+text\s+using\s+(?:bag\s+of\s+words|bow|countvectorizer)(?:\s+with\s+max\s+features?\s+(\d+))?\s*$',
        s, re.IGNORECASE)
    if m:
        max_feat = int(m.group(1)) if m.group(1) else 10000
        v = _ctx.vectorizer_var
        return (
            f"from sklearn.feature_extraction.text import CountVectorizer; "
            f"{v} = CountVectorizer(stop_words='english', max_features={max_feat}); "
            f"{_ctx.X_train} = {v}.fit_transform({_ctx.X_train}); "
            f"{_ctx.X_test} = {v}.transform({_ctx.X_test})"
        )

    # scale features using standard scaler
    m = re.match(r'^scale\s+features?\s+using\s+(?:standard\s+scaler|standardscaler)\s*$', s, re.IGNORECASE)
    if m:
        sc = _ctx.scaler_var
        return (
            f"from sklearn.preprocessing import StandardScaler; "
            f"{sc} = StandardScaler(); "
            f"{_ctx.X_train} = {sc}.fit_transform({_ctx.X_train}); "
            f"{_ctx.X_test} = {sc}.transform({_ctx.X_test})"
        )

    # scale features using minmax scaler
    m = re.match(r'^scale\s+features?\s+using\s+(?:minmax\s+scaler|minmaxscaler)\s*$', s, re.IGNORECASE)
    if m:
        sc = _ctx.scaler_var
        return (
            f"from sklearn.preprocessing import MinMaxScaler; "
            f"{sc} = MinMaxScaler(); "
            f"{_ctx.X_train} = {sc}.fit_transform({_ctx.X_train}); "
            f"{_ctx.X_test} = {sc}.transform({_ctx.X_test})"
        )

    # ── 6. TRAIN CLASSIFIER / REGRESSOR ──────────────────────────────────────

    _CLASSIFIERS = {
        'naive_bayes':          ('sklearn.naive_bayes', 'MultinomialNB', 'MultinomialNB()'),
        'gaussian_naive_bayes': ('sklearn.naive_bayes', 'GaussianNB', 'GaussianNB()'),
        'logistic_regression':  ('sklearn.linear_model', 'LogisticRegression', 'LogisticRegression(max_iter=1000)'),
        'svm':                  ('sklearn.svm', 'SVC', 'SVC(probability=True)'),
        'random_forest':        ('sklearn.ensemble', 'RandomForestClassifier', 'RandomForestClassifier(n_estimators=100, random_state=42)'),
        'decision_tree':        ('sklearn.tree', 'DecisionTreeClassifier', 'DecisionTreeClassifier(random_state=42)'),
        'knn':                  ('sklearn.neighbors', 'KNeighborsClassifier', 'KNeighborsClassifier(n_neighbors=5)'),
        'gradient_boosting':    ('sklearn.ensemble', 'GradientBoostingClassifier', 'GradientBoostingClassifier(random_state=42)'),
        'xgboost':              ('xgboost', 'XGBClassifier', 'XGBClassifier(random_state=42, eval_metric="logloss")'),
    }

    _REGRESSORS = {
        'linear_regression':    ('sklearn.linear_model', 'LinearRegression', 'LinearRegression()'),
        'ridge_regression':     ('sklearn.linear_model', 'Ridge', 'Ridge()'),
        'lasso_regression':     ('sklearn.linear_model', 'Lasso', 'Lasso()'),
        'decision_tree':        ('sklearn.tree', 'DecisionTreeRegressor', 'DecisionTreeRegressor(random_state=42)'),
        'random_forest':        ('sklearn.ensemble', 'RandomForestRegressor', 'RandomForestRegressor(n_estimators=100, random_state=42)'),
        'svr':                  ('sklearn.svm', 'SVR', 'SVR()'),
        'gradient_boosting':    ('sklearn.ensemble', 'GradientBoostingRegressor', 'GradientBoostingRegressor(random_state=42)'),
    }

    # train <algorithm> classifier on training data
    m = re.match(
        r'^train\s+([a-zA-Z_]+(?:\s+[a-zA-Z_]+)?)\s+classifier\s+on\s+training\s+data\s*$',
        s, re.IGNORECASE)
    if m:
        algo = m.group(1).strip().lower().replace(' ', '_')
        if algo in _CLASSIFIERS:
            mod, cls, init = _CLASSIFIERS[algo]
            mv = _ctx.model_var
            return (
                f"from {mod} import {cls}; "
                f"{mv} = {init}; "
                f"{mv}.fit({_ctx.X_train}, {_ctx.y_train}); "
                f"print('[ENLANG ML] {cls} classifier trained successfully!')"
            )

    # train <algorithm> regressor on training data
    m = re.match(
        r'^train\s+([a-zA-Z_]+(?:\s+[a-zA-Z_]+)?)\s+regressor?\s+on\s+training\s+data\s*$',
        s, re.IGNORECASE)
    if m:
        algo = m.group(1).strip().lower().replace(' ', '_')
        if algo in _REGRESSORS:
            mod, cls, init = _REGRESSORS[algo]
            mv = _ctx.model_var
            return (
                f"from {mod} import {cls}; "
                f"{mv} = {init}; "
                f"{mv}.fit({_ctx.X_train}, {_ctx.y_train}); "
                f"print('[ENLANG ML] {cls} regressor trained successfully!')"
            )

    # ── 7. EVALUATE MODEL ────────────────────────────────────────────────────

    # evaluate classifier accuracy and store in acc
    m = re.match(
        r'^evaluate\s+(?:classifier|model|regressor)\s+accuracy\s+and\s+store\s+in\s+([a-zA-Z_]\w*)\s*$',
        s, re.IGNORECASE)
    if m:
        var = m.group(1)
        yp = _ctx.y_pred_var
        mv = _ctx.model_var
        return (
            f"from sklearn.metrics import accuracy_score; "
            f"{yp} = {mv}.predict({_ctx.X_test}); "
            f"{var} = round(accuracy_score({_ctx.y_test}, {yp}) * 100, 2); "
            f"print(f'[ENLANG ML] Test Accuracy: {{{var}}}%')"
        )

    # evaluate regression model and store rmse in err
    m = re.match(
        r'^evaluate\s+regression\s+model\s+and\s+store\s+rmse\s+in\s+([a-zA-Z_]\w*)\s*$',
        s, re.IGNORECASE)
    if m:
        var = m.group(1)
        yp = _ctx.y_pred_var
        mv = _ctx.model_var
        return (
            f"from sklearn.metrics import mean_squared_error; import math; "
            f"{yp} = {mv}.predict({_ctx.X_test}); "
            f"{var} = round(math.sqrt(mean_squared_error({_ctx.y_test}, {yp})), 4); "
            f"print(f'[ENLANG ML] RMSE: {{{var}}}')"
        )

    # show confusion matrix
    m = re.match(r'^show\s+confusion\s+matrix\s*$', s, re.IGNORECASE)
    if m:
        mv = _ctx.model_var
        yp = _ctx.y_pred_var
        return (
            f"from sklearn.metrics import confusion_matrix, classification_report; "
            f"{yp} = {mv}.predict({_ctx.X_test}) if '{yp}' not in dir() else {yp}; "
            f"print('\\n=== Confusion Matrix ==='); "
            f"print(confusion_matrix({_ctx.y_test}, {yp})); "
            f"print('\\n=== Classification Report ==='); "
            f"print(classification_report({_ctx.y_test}, {yp}))"
        )

    # ── 8. PREDICT ───────────────────────────────────────────────────────────

    # predict label for "some text" and store in result
    m = re.match(
        r'^predict\s+label\s+for\s+["\'](.+?)["\']\s+and\s+store\s+in\s+([a-zA-Z_]\w*)\s*$',
        s, re.IGNORECASE)
    if m:
        text, var = m.group(1), m.group(2)
        mv = _ctx.model_var
        vv = _ctx.vectorizer_var
        return (
            f"{var} = {mv}.predict({vv}.transform(['{text}']))[0]"
        )

    # predict spam from "email text"
    m = re.match(r'^predict\s+(?:spam\s+)?from\s+["\'](.+?)["\']\s*$', s, re.IGNORECASE)
    if m:
        text = m.group(1)
        mv = _ctx.model_var
        vv = _ctx.vectorizer_var
        return (
            f"_pred = {mv}.predict({vv}.transform(['{text}']))[0]; "
            f"_proba = {mv}.predict_proba({vv}.transform(['{text}']))[0]; "
            f"print('[SPAM DETECTED] Confidence: ' + str(round(_proba[1]*100,2)) + '%' if _pred == 1 else '[NOT SPAM] Confidence: ' + str(round(_proba[0]*100,2)) + '%')"
        )

    # predict label for variable and store in result
    m = re.match(
        r'^predict\s+label\s+for\s+([a-zA-Z_]\w*)\s+and\s+store\s+in\s+([a-zA-Z_]\w*)\s*$',
        s, re.IGNORECASE)
    if m:
        inp_var, out_var = m.group(1), m.group(2)
        mv = _ctx.model_var
        vv = _ctx.vectorizer_var
        return f"{out_var} = {mv}.predict({vv}.transform([{inp_var}]))[0]"

    # ── 9. SAVE / LOAD MODEL ─────────────────────────────────────────────────

    # save model to "model.pkl"
    m = re.match(r'^save\s+model\s+to\s+["\'](.+?)["\']\s*$', s, re.IGNORECASE)
    if m:
        path = m.group(1)
        mv = _ctx.model_var
        return (
            f"import pickle; "
            f"pickle.dump({mv}, open('{path}', 'wb')); "
            f"print('[ENLANG ML] Model saved to {path}')"
        )

    # load model from "model.pkl"
    m = re.match(r'^load\s+model\s+from\s+["\'](.+?)["\']\s*$', s, re.IGNORECASE)
    if m:
        path = m.group(1)
        mv = _ctx.model_var
        return (
            f"import pickle; "
            f"{mv} = pickle.load(open('{path}', 'rb')); "
            f"print('[ENLANG ML] Model loaded from {path}')"
        )

    # save vectorizer to "vectorizer.pkl"
    m = re.match(r'^save\s+vectorizer\s+to\s+["\'](.+?)["\']\s*$', s, re.IGNORECASE)
    if m:
        path = m.group(1)
        vv = _ctx.vectorizer_var
        return (
            f"import pickle; "
            f"pickle.dump({vv}, open('{path}', 'wb')); "
            f"print('[ENLANG ML] Vectorizer saved to {path}')"
        )

    # load vectorizer from "vectorizer.pkl"
    m = re.match(r'^load\s+vectorizer\s+from\s+["\'](.+?)["\']\s*$', s, re.IGNORECASE)
    if m:
        path = m.group(1)
        vv = _ctx.vectorizer_var
        return (
            f"import pickle; "
            f"{vv} = pickle.load(open('{path}', 'rb')); "
            f"print('[ENLANG ML] Vectorizer loaded from {path}')"
        )

    # ── 10. DATA VISUALIZATION ───────────────────────────────────────────────

    # plot column distribution of spam
    m = re.match(r'^plot\s+(?:column\s+)?distribution\s+of\s+([a-zA-Z_]\w*)\s*$', s, re.IGNORECASE)
    if m:
        col = m.group(1)
        return (
            f"import matplotlib.pyplot as plt; "
            f"{_ctx.dataset_var}['{col}'].value_counts().plot(kind='bar', title='{col} Distribution'); "
            f"plt.tight_layout(); plt.show()"
        )

    # plot correlation heatmap
    m = re.match(r'^plot\s+correlation\s+heatmap\s*$', s, re.IGNORECASE)
    if m:
        return (
            f"import matplotlib.pyplot as plt; import seaborn as sns; "
            f"plt.figure(figsize=(10, 8)); "
            f"sns.heatmap({_ctx.dataset_var}.corr(), annot=True, cmap='coolwarm'); "
            f"plt.title('Correlation Heatmap'); plt.tight_layout(); plt.show()"
        )

    # Not an ML line
    return None
