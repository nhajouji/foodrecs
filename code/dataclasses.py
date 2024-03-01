
#This should be useful for user similarity/collaborative filtering

def get_dictionaries(ratingsdf:pd.core.frame.DataFrame,usercol:str,itemcol:str,ratingcol:str):
    users = list(set(ratingsdf[usercol].values))
    items = list(set(ratingsdf[itemcol].values))
    ratings_by_user = {user_id:{} for user_id in users}
    users_by_item = {item_id:[] for item_id in items}
    for review_index in ratingsdf.index:
        user_id = ratingsdf[usercol][review_index]
        item_id = ratingsdf[itemcol][review_index]
        rating = ratingsdf[ratingcol][review_index]
        ratings_by_user[user_id][item_id] = rating
        users_by_item[item_id].append(user_id)
    return ratings_by_user,users_by_item

def convert_ratings(user_rating_dic:dict)->dict:
    user_mean = np.mean(list(user_rating_dic.values()))
    user_max = max(list(user_rating_dic.values()))
    new_ratings = {}
    for item in user_rating_dic:
        if user_rating_dic[item]==user_max:
            new_ratings[item]=1
        elif user_rating_dic[item] >= user_mean:
            new_ratings[item]=0
        else:
            new_ratings[item]=-1
    return new_ratings

class RatingsData:
    def __init__(self,ratingsdataframe:pd.core.frame.DataFrame,usercol:str,itemcol:str,ratingcol:str):
        self.dataframe = ratingsdataframe
        self.usercol = usercol
        self.itemcol = itemcol
        self.userlist = list(set(ratingsdataframe[usercol].values))
        self.itemlist = list(set(ratingsdataframe[itemcol].values))
        self.ratingcol = ratingcol
        self.user_ratings = {}
        self.users_by_item = {}
        self.features = []

    def add_feature(self,feature_df:pd.core.frame.DataFrame,feature_name:'str')->None:
        df0 = self.dataframe
        itemcol = self.itemcol
        newcol = []
        for i in df0.index:
            item = df0[itemcol][i]
            if item in feature_df.index:
                newcol.append(feature_df[feature_name][item])
            else:
                newcol.append(None)
        self.dataframe[feature_name] = newcol
        self.features.append(feature_name)

    def get_dicts(self,insist = False)->None:
        if len(self.user_ratings) == 0 or insist == True:
            user_ratings, users_by_item = get_dictionaries(self.dataframe,
                                                           self.usercol,
                                                           self.itemcol,
                                                           self.ratingcol)
            self.user_ratings = user_ratings
            self.users_by_item = users_by_item
    
    def get_user_lists(self,min_revs=1,min_std=-1,max_mean = 5):
        get_dicts()
        user_ratings = self.user_ratings
        user_list = []
        for user in user_ratings:
            vals = list(user_ratings[user].values())
            if len(vals)>=min_revs and np.mean(vals)<= max_mean and np.std(vals)>min_std:
                user_list.append(user)
        return user_list


    def restr_dataframe(self,user_list:list,item_list:list)->pd.core.frame.DataFrame:
        df = self.dataframe
        usercol = self.usercol
        itemcol = self.itemcol
        df0 = df[df[usercol].isin(user_list)]
        df1 = df0[df0[itemcol].isin(item_list)]
        return df1
    
    def user_related_dataframe(self,user,min_ratingcount_item = 0):
        df = self.dataframe
        usercol = self.usercol
        df0 = df.loc[df[usercol]==user]
        relevant_items = list(df0[self.itemcol].values)
        df1 = df[df[self.itemcol].isin(relevant_items)]
        relevant_users = list(set(df1[usercol].values))
        df1 = self.restr_dataframe(relevant_users,relevant_items)
        if min_ratingcount_item == 0:
            return df1
        else:
            df1 = df1.groupby(self.itemcol).filter(lambda x: len(x) > min_ratingcount_item)
        return df1
        
## Features 
    
def get_user_dataframe(reviewsdf,featuredf,usercol,itemcol,featurecols, user):
    userdf = reviewsdf.loc[reviewsdf[usercol]==user].copy()
    for feature in featurecols:
        userdf[feature]=[featuredf[feature][item]
                         for item in userdf[itemcol].values]
    return userdf

