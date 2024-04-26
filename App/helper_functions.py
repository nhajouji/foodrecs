import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer
embedder = SentenceTransformer("all-MiniLM-L6-v2")




def get_user_SVDvector(user_id: int = 1533):
    rvs = pd.read_pickle("../Models/UserVectors.pk")
    user_SVDvector = np.array([rvs.loc[user_id, SVD_component_col_name] 
                               for SVD_component_col_name in ["SVD_component0", "SVD_component1"]])
    return user_SVDvector


def get_closest_recipes(query: str, number_of_results: int = 5):
    if not query:
        return []
    
    df = pd.read_pickle("../Models/RecipeVectorsFull.pk")

    names_dict = df.Name.to_dict()
    descriptions_dict = df.Description.to_dict()
    vector_dict = df.SemanticVector.to_dict()
    input_vector = embedder.encode(query)

    closest_indices = sorted(list(df.index), key=lambda index: np.dot(vector_dict[index], input_vector), reverse=True)[:number_of_results]
    results = [{"name": names_dict[index].title(), "description": descriptions_dict[index]} for index in closest_indices]

    return results




def get_closest_recipes_with_user_vector(query: str, user_weight = .25, number_of_results = 5, user_id = 1533)->float:
    """
    Returns the top n search results ranked by 
    """
    if not query:
        return []
    
    user_SVDvector = get_user_SVDvector(user_id)

    df = pd.read_pickle("../Models/RecipeVectorsFull.pk")
    names_dict = df.Name.to_dict()
    descriptions_dict = df.Description.to_dict()
    vector_dict = df.SemanticVector.to_dict()
    svd_vector_dict = df.SVDvec.to_dict()
    input_vector = embedder.encode(query)

    def sort_key(index):
        """
        Takes a weighted average of user proximity with the query proximity
        based on the user_weight parameter put into the parent function. 
        """
        user_dot_product = np.dot(svd_vector_dict[index], user_SVDvector)
        sentiment_dot_product = np.dot(vector_dict[index], input_vector)
        return (user_weight)*user_dot_product + (1-user_weight)*sentiment_dot_product

    closest_indices = sorted(list(df.index), key=lambda index: sort_key(index), reverse=True)[:number_of_results]
    results = [{"name": names_dict[index].strip(";").title(), "description": descriptions_dict[index]} for index in closest_indices]

    return results



def get_top_user_recipes(user_id: int, number_of_results = 5) -> list:
    recipe_SVDvectors_df = pd.read_pickle("../Models/RecipeVectorsFull.pk")
    names_dict = recipe_SVDvectors_df.Name.to_dict()
    recipe_svd_vector_dict = recipe_SVDvectors_df.SVDvec.to_dict()

    regions_df = pd.read_pickle("../data/clean_columns/regiondatav0.pk")
    regions_dict = regions_df.Regions.to_dict()

    user_SVDvector = get_user_SVDvector(user_id)
    
    def sort_key(index):
        return np.dot(recipe_svd_vector_dict[index], user_SVDvector)
    
    closest_indices = sorted([index for index in recipe_SVDvectors_df.index if index in regions_df.index], key=sort_key, reverse=True)[:number_of_results]
    results = [{"name": names_dict[index].strip(";").title(), "regions": ", ".join(regions_dict.get(index, "")).title()} for index in closest_indices]

    return results






def get_closest_recipes_from_partial_list(query, number_of_results=5):
    """
    This function was used for the first version of the app. 
    It is no longer used. 
    """
    if not query:
        return []
    
    df = pd.read_parquet("recipes_with_vectors.parquet")

    names_dict = df.Name.to_dict()
    descriptions_dict = df.Description.to_dict()
    vector_dict = df.Vector.to_dict()
    input_vector = embedder.encode(query)

    closest_indices = sorted(list(df.index), key=lambda index: np.dot(vector_dict[index], input_vector), reverse=True)[:number_of_results]
    results = [{"name": names_dict[index].title(), "description": descriptions_dict[index]} for index in closest_indices]

    return results



