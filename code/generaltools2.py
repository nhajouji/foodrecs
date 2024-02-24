from typing import Iterable

def flatten_to_list(list_of_lists: Iterable(list))->list:
    return list(set([element for element in list_item for list_item in list_of_lists]))

# A class that lets us easily access things we will repeatedly use
class ratingsdata:
    """
    A class that stores a copy of the dataframe and uses the user_id and item_id column names
    to turn the default ids from the dataframe into custom ids for our purpose, just like an 
    auto-incrementing primary key in a table. 
    get_primary_user_key and get_primary_recipe_key return these new ids, or return None if 
    the original id given is not in the dataframe. 
    """
    def __init__(self, df, user_id_name, recipe_id_name):
        self.df = df
        self.user_ids = list(df[user_id_name].unique())
        self.recipe_ids = list(df[recipe_id_name].unique())
        self.user_id_name = user_id_name
        self.recipe_id_name = recipe_id_name
        # The following two dictionaries create auto-incrementing primary keys for users and recipes
        self.user_id_enumerator = {old_id: i for i, old_id in enumerate(df[user_id_name].unique())}
        self.recipe_id_enumerator = {old_id: i for i, old_id in enumerate(df[recipe_id_name].unique)}
    
    def get_primary_user_key(self, old_id):
        return self.user_id_enumerator.get(old_id, "Not found")
    
    def get_primary_recipe_key(self, old_id):
        return self.recipe_enumerator.get(old_id, "Not found")
    
    def rated_something(self):
        """
        Returns a list of pairs of new id names corresponding to the dataframe's rows. 
        """
        return [
                (
                    self.get_primary_recipe_key(row[self.user_id_name]), 
                    self.get_primary_recipy_key(row[self.recipe_id_name])
                ) 
                for row in self.df.iterrows()
                ]
        




# class ratingsdata:
#     def __init__(self,df,useridname,itemidname):
#         self.df = df
#         self.user_ids = list(set(df[useridname].values))
#         self.recipe_ids = list(set(df[itemidname].values))
#         self.ui_to_n = {list(set(df[useridname].values))[i]:i for i in range(len(list(set(df[useridname].values))))}
#         self.ri_to_n = {list(set(df[itemidname].values))[i]:i for i in range(len(list(set(df[itemidname].values))))}
    
#     def user_to_n(self,user):
#         dic = self.ui_to_n
#         if user in dic:
#             return dic[user]
#         else:
#             return 'Not found'
    
#     def recipe_to_n(self,recipe):
#         dic = self.ri_to_n
#         if recipe in dic:
#             return dic[recipe]
#         else:
#             return 'Not found'
        
#     def rated_ijs(self):
        """
        It looks like this method wants to return a list of tuples of the new ids. 
        Is this meant to make a reverse-dictionary, where you feed the df index 
        into the list and get the pair of new ids? 
        I don't understand the syntax of ij[0] or ij[1] because the variable ij 
        is taking values in the index, which is an iterable for the df's rows.  
        """
#         userdic = self.ui_to_n
#         recdic = self.ri_to_n
#         return [(userdic[ij[0]],recdic[ij[1]]) for ij in self.df.index]


        
        
