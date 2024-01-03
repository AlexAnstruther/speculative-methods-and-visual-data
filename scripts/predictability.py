#Resctricting exploration to the ten most active Letterboxd users.
top_ten_users = ratings_df['user_id'].value_counts().head(10).index
top_ten_users_df = ratings_df[ratings_df['user_id'].isin(top_ten_users)]
#Resctricting exploration to the films all ten users have reviewed.
n_reviewed_by_all = (top_ten_users_df['movie_id'].value_counts() == 10).sum()
reviewed_by_all = top_ten_users_df['movie_id'].value_counts()[0:n_reviewed_by_all]
reviewed_by_all_df = top_ten_users_df[top_ten_users_df['movie_id'].isin(reviewed_by_all.index)]
#Reshaping the data in preparation for ML.
ml_ready_df = pd.DataFrame()
for user in top_ten_users:
    ml_ready_df[user] = (reviewed_by_all_df[reviewed_by_all_df['user_id'] == user]
                         .set_index('movie_id')
                         ['rating_val'])
ml_ready_df = ml_ready_df.T
#Exploring a how predictable each film's ratings are, based on the user's other film ratings.
n_iters = 1000
results = []
for n in range(n_iters):
    errors = []
    for i in reviewed_by_all.index:
        columns_bool = ml_ready_df.columns == i
        X = ml_ready_df.iloc[:, ~columns_bool]
        y = ml_ready_df.iloc[:, columns_bool]
        x_train, x_test,y_train,y_test = train_test_split(X,y,test_size=0.2)
        model = LinearRegression()
        model.fit(x_train, y_train)
        errors.append((model.predict(x_test).round(0) - y_test).mean().iloc[0])
    results.append(pd.Series(errors, index = reviewed_by_all.index))
results_df = pd.concat(results,axis=1)
means = (results_df.abs().sum(axis=1,skipna=True)/1000).sort_values(ascending=False)
print(f'The least predictably rated film is: {means.index[0]} with an error of: {means.iloc[0]} \nThe most predictably rated film is: {means.index[-1]} with an error of: {means.iloc[-1]}')