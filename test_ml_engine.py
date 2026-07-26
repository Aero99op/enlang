from enlang_core.ml_engine import translate_ml_line, reset_context
print("Import OK")

tests = [
    ('read "data.csv" as df',                                              True),
    ('separate df into features X and target y with target crop',           True),
    ('split X and y into 80 percent train and 20 percent test',            True),
    ('stratified split into 80 percent training and 20 percent testing',   True),
    ('create random forest classifier as rf with 100 trees',               True),
    ('create naive bayes classifier as nb',                                True),
    ('train rf on train data',                                             True),
    ('train nb on train data',                                             True),
    ('predict using rf on test data and store in preds',                   True),
    ('calculate accuracy for preds against y_test and store in acc',       True),
    ('show report for preds against y_test',                               True),
    ('show feature importance of rf top 5',                                True),
    ('combine rf and nb using soft voting as ens',                         True),
    ('combine all models using hard voting as ens2',                       True),
    ('compare rf and nb on test data',                                     True),
    ('run anova on rainfall grouped by crop in df',                        True),
    ('run t-test on col1 and col2',                                        True),
    ('compute correlation between A and B',                                True),
    ('detect anomalies in X using isolation forest as outliers',           True),
    ('cluster X into 3 groups using kmeans as labels',                     True),
    ('reduce X_train and X_test to 50 dimensions using pca',               True),
    ('balance train data using smote',                                     True),
    ('group df by category and compute mean as grouped',                   True),
    ('filter df where age > 25 as young',                                  True),
    ('sort df by score descending as sorted_df',                           True),
    ('merge df1 and df2 on id as merged',                                  True),
    ('analyze sentiment of text in df and store in sentiment',             True),
    ('compute rolling mean of sales in df with window 7 and store in rm', True),
    ('lag price in df by 3 periods and store in lagged',                   True),
    ('tune rf using grid search on X_train and y_train',                   True),
    ('profile df',                                                         True),
    ('show distribution of crop in df',                                    True),
    ('show missing values in df',                                          True),
    ('drop missing values from df',                                        True),
    ('encode column gender in df using label encoding',                    True),
    ('save rf to "model.pkl"',                                             True),
    # backward compat tests
    ('train random_forest classifier on training data',                    True),
    ('evaluate all classifiers and show comparison',                       True),
    ('use soft ensemble of all trained classifiers',                       True),
    ('vectorize text using tfidf with max features 5000',                  True),
]

passed = 0
failed = 0
for stmt, should_match in tests:
    reset_context()
    # pre-populate model registry for some tests
    from enlang_core.ml_engine import _ctx, _CLASSIFIERS
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.naive_bayes import MultinomialNB
    _ctx.named_models['rf'] = '_rf'
    _ctx.named_models['nb'] = '_nb'
    _ctx.model_registry['random_forest'] = '_enlg_model_randomforest'
    _ctx.model_registry['naive_bayes'] = '_enlg_model_naivebayes'

    result = translate_ml_line(stmt)
    matched = result is not None
    ok = matched == should_match
    status = "PASS" if ok else "FAIL"
    if ok:
        passed += 1
    else:
        failed += 1
        print(f"  [{status}] {stmt[:60]}")

print(f"\n{'='*50}")
print(f"Results: {passed}/{len(tests)} PASSED | {failed} FAILED")
print('='*50)
