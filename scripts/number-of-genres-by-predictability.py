genres = movies_df[movies_df['movie_id'].isin(reviewed_by_all.index)].set_index('movie_id')['genres']
genres_errors = pd.concat([genres,means],axis=1).rename(columns={0: 'errors'})
genres_errors['genres'] = genres_errors['genres'].apply(ast.literal_eval)
genres_errors['n_genres'] = genres_errors['genres'].apply(len)
#Plotting.
fig, (ax1) = plt.subplots(1, 1, figsize=(15, 7))
ax1.scatter(genres_errors['n_genres'],genres_errors['errors'],color='orange',label='Errors')
ax1.plot(genres_errors.groupby('n_genres')['errors'].mean(),color='blue',label='Mean')
ax1.set_xlabel('Number of genres')
ax1.set_ylabel('Unpredictability')
ax1.set_xlim(1.9,5.1)
ax1.legend()
plt.show()