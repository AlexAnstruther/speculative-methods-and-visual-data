ratings_df = pd.read_csv('archive/ratings_export.csv')
movies_df = pd.read_csv('archive/movie_data.csv',lineterminator='\n')
print('All data successfully imported. Your datframes are: \'ratings_df\' and \'movies_df\'')