def flatten(l):
    lnew = []
    for l0 in l:
        lnew+=l0
    return list(set(lnew))


# A class that lets us easily access things we will repeatedly use

class ratingsdata:
    def __init__(self,df,useridname,itemidname):
        self.df = df
        self.user_ids = list(set(df[useridname].values))
        self.recipe_ids = list(set(df[itemidname].values))
        self.ui_to_n = {list(set(df[useridname].values))[i]:i for i in range(len(list(set(df[useridname].values))))}
        self.ri_to_n = {list(set(df[itemidname].values))[i]:i for i in range(len(list(set(df[itemidname].values))))}
    
    def user_to_n(self,user):
        dic = self.ui_to_n
        if user in dic:
            return dic[user]
        else:
            return 'Not found'
    
    def recipe_to_n(self,recipe):
        dic = self.ri_to_n
        if recipe in dic:
            return dic[recipe]
        else:
            return 'Not found'


    def rated_ijs(self):
        userdic = self.ui_to_n
        recdic = self.ri_to_n
        return [(userdic[ij[0]],recidc[ij[1]]) for ij in self.df.index]


        
        
