from definitions import ROOT_DIR
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
import pickle

class Endpoint(object):
    """
    Recommender System for Space Embeddings
    """

    def __init__(self):
        self.places = pd.read_csv(ROOT_DIR + "/serialized/places_final.csv")
        self.embeddings = pd.read_pickle(ROOT_DIR + "/serialized/continuous_embeddings.pkl")

    def recommend(self, IDs, Ratings):
        # Define user df
        user = pd.DataFrame({'IDs':IDs, 'Rating':Ratings})
        # Save df of visited establishments
        visited = self.places.loc[self.places.gPlusPlaceId.isin(IDs)][['gPlusPlaceId','city','Grid']]
        # Add grid cell, city to user
        user = user.merge(visited, left_on='IDs', right_on='gPlusPlaceId')
        # Save location user is from
        city = user.city.unique()[0]

        # Calculate average rating for user based on average rating user have given for each grid 
        avg_grid_rating = pd.DataFrame(user.groupby('Grid').Rating.mean())
        avg_user_rating = self.embeddings.loc[avg_grid_rating.index].values.T @ avg_grid_rating.values

        # Calculate the cosine similiary
        recommendation = pd.DataFrame(index = [i for i in self.embeddings.index if city[0] not in i])
        for grid in recommendation.index:
            recommendation.loc[grid, 'cosine_similarity'] = cosine_similarity(avg_user_rating.reshape(1,-1),self.embeddings.loc[grid].values.reshape(1,-1))

        if city == "London":
            recommendation['clean_index'] = [int(i[2:]) for i in recommendation.index] 

        else:
            recommendation['clean_index'] = [int(i[1:]) for i in recommendation.index] 
        
        # Return df similiarity to other grids
        return recommendation.sort_values(by="cosine_similarity").tail(5).index.to_list()


if __name__ == "__main__":
    IDs = ['101742583391038750118','100574642292837870712']
    Ratings = [4,2]
    endpoint = Endpoint()
    print(endpoint.recommend(IDs, Ratings))