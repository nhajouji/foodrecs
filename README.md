# Food recommender

The goal of this repository is to construct a recommender for recipes using [this data](https://www.kaggle.com/datasets/irkaal/foodcom-recipes-and-reviews).

## General Framework

We have a list of users $U$ and a list of recipes $R$.
The reviews dataset contains reviews for a small subset of $U \times R$.

Our goal is to quantify how likely a user is to interact with a recipe they haven't reviewed,
using information gleaned from the set of recipes they have reviewed.
There are two independent ways one can go about doing this:
* User-based (collaborative filtering): A user is likely to interact with a recipe if there are similar users who have interacted with that recipe. 
We can obtain an algorithm of this type that does better than a random ranking using only the reviews dataset.
* Item-based: A user is likely to interact with a recipe if it is similar to other recipes they've reviewed. 
To use this, we need to condense the information in the recipes dataset into a map from the set of recipes $R$ to a metric space, so that we can quantify similarity between recipes.

We can obtain the necessary embedding by doing the following:
* Each recipe comes equipped with a list of keywords, and the total list of words that appear as a keyword is roughly 300.
* We fix an ordering on the list of keywords, and we represent each recipe using the vector whose $n$th entry is 1 if the $n$th keyword is a keyword for that recipe and 0 otherwise.

We will need to do a good amount of cleaning to ensure that two recipes with a similar list of keywords represent similar recipes: many recipes are "missing keywords", but we can try to add these missing keywords by checking whether there are any keywords appear in the recipe instructions, description, title, etc. 

Once we've embedded our recipes in a vector space, we can obtain vectors that represent each user: for each user $u$, we take the average of all recipes $r_1,.., r_n$ that have been reviewed by that user. If our keyword embedding is "good", then:

* Similar recipes have vectors that are close.
* Users who gravitate towards the same types of recipes will have vectors that are close to each other (even if the users haven't rated any of the same recipes).
* A user is likely to have interacted with a recipe if their associated vectors are close.


## Keyword Categories
The keyword list can be partitioned into categories like cook time (under 30 mins, under 1 hour..), nutrition (high protein, low fat, ..), regions, appliances (stovetop, oven, grill/broil..). 
Two of these categories (nutrition, cooktime) represent continuous data in a noncontinuous form - these will be treated separately, since the recipes dataframe contains information about nutrition and cooktimes.

To start, we should try to split the keywords up into categories and do some EDA to determine which ones we think we want to include in the model.

