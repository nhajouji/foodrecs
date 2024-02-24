#This takes a list of lists,
# and returns the concatenation of the sublists.
# e.g. [[1,2],[2,3,4]] becomes [1,2,2,3,4]

def flatten(l:list):
    lnew = []
    for l0 in l:
        lnew+=l0
    return lnew

# To compute similarity between two ratings dictionaries,
# we use the following variation on pearson correlation.

def similarity(ratings1,ratings2):
    user1mean = np.mean(list(ratings1.values()))
    user2mean = np.mean(list(ratings2.values()))
    common_recipes = set(ratings1.keys()).intersection(set(ratings2.keys()))
    if len(common_recipes)== 0:
        return -2
    l1 = 0
    l2 = 0
    dot = 0
    for recipe_id in common_recipes:
        r1 = ratings1[recipe_id]-user1mean
        r2 = ratings2[recipe_id]-user2mean
        l1+=r1**2
        l2+=r2**2
        dot+=r1*r2
    # If the normalized ratings are all 0 for one of the users,
    # the corresponding length will be 0. We may as well return 0.
    if l1*l2 == 0:
        return 0
    else:
        return dot/np.sqrt(l1*l2)
