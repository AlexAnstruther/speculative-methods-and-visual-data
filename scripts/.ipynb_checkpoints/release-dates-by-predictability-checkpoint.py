#Reshaping data in preparation for ML.
release_dates = movies_df[movies_df['movie_id'].isin(reviewed_by_all.index)].set_index('movie_id')['release_date']
release_date_errors = pd.concat([pd.to_datetime(release_dates),means],axis=1).rename(columns={0: 'errors'})
#Creating dummy variables.
release_date_errors['release_date_dummy'] = release_date_errors['release_date'].apply(lambda x: 1 if x.year < 1960 else 0)
#Fitting logisitc regression.
reg = LogisticRegression()
reg.fit(release_date_errors[['errors']],release_date_errors['release_date_dummy'])
#Calculating descision barrier (sigmoid).
beta_0 = reg.intercept_
beta_1 = reg.coef_[0]
x_range = np.linspace(release_date_errors[['errors']].min() - 7, release_date_errors[['errors']].max() + 7, 300)
sigmoid = expit(beta_0 + beta_1 * x_range)
#Plotting.
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(15, 15))
ax1.scatter(release_date_errors['release_date'], release_date_errors['errors'])
ax1.set_xlabel('Release Year')
ax1.set_ylabel('Unpredictability')
ax2.plot(x_range, sigmoid, linestyle=(0, (1, 2)), color='black', linewidth=3, label='Logistic Regression')
ax2.set_xlabel('Unpredictability')
ax2.set_ylabel('Probability of being a \'Classic\'')
ax2.grid(False)
ax2.scatter(release_date_errors['errors'], release_date_errors['release_date_dummy'], color='red')
ax2.legend()
plt.show()