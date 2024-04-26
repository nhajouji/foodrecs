[A relatable problem](https://www.youtube.com/watch?v=6edlBZ64TDk)

# Recipe recommender

We set out to construct a recommendation engine that suggests recipes using [this data](https://www.kaggle.com/datasets/irkaal/foodcom-recipes-and-reviews). 

* We succeeded!
* But not everything we tried worked.

This repository contains our main results.

### Second repository 
The dataset we started with exceeds GitHub's size limits.
* We originally tried to get around this using GitLFS, but ran out of bandwidth.
* This repository contains the cleaned data we need for modeling purposes, and notebooks explaining how we obtained the clean data from the original data. To run the data cleaning notebooks, one would also need to download the original datasets from Kaggle, or clone our second repository on huggingface.

## Introduction 
### Data

We started off with two datasets:
* A dataset with recipe features - each entry corresponds to one of the recipes, and contains information like the ingredient list, cooking instructions, cook time, nutrtion, etc.
* A dataset with reviews. Each entry has an associated reviewer (that we call "the user") and recipe, and includes a numerical rating (between 0 and 5), a review, and some additional metadata.

 Our goal is to take this data, and somehow characterize the set of recipes that we think each user is likely to interact with. 


### Concrete Problem

For each user, we want a ranking of the recipe list that is catered to that users preferences.

* To obtain such a ranking, we want a function $f : U \times R \to \mathbb{R}$ (here $U$ is the set of users, $R$ the set of recipes and $\mathbb{R}$ the set of real numbers) that captures each user's preferences: the idea is if $f(u, r) < f(u,r')$, then we rank $r'$ higher than $r$ for user $u$.
* One way we can obtain such an $f$ is by finding embeddings of $U, R$ into a vector space, and defining $f(u,r)$ to be the dot product of the vectors associated to $u,r$.

Now, it is not hard to write a map from a set to a vector space - so we need to make sure our embeddings actually capture the user's preferences somehow. 
Here is how that's going to work:
* We do a train-test split of the review dataset, stratifying by user so that we can make predictions for each user.
* We use the training portion of the review dataset, together with the full recipe dataset, to obtain embeddings $U \to V$ and $R \to V$.
Once we have these embeddings, we can compute $f(u,r)$ for any user-recipe pair. 

We will compare the mean scores assigned to user-recipe pairs that were in the holdout set, to the mean value of $f$. 
* The "effectiveness" of $f$ does not change if we rescale $f$ by a positive number - the rankings will be the same either way.
* To ensure the scores of our models are comparable, we will scale $f$ so that the mean score given to user-recipe pairs in the training set is 1.

The process is summarized in the following picture:



## Obtaining Models




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

## Usage

#### Data sources
Our raw data files (`recipes.parquet` and `reviews.parquet`) have been managed using [GitHub File Large System (FLS)](https://docs.github.com/en/repositories/working-with-files/managing-large-files/about-large-files-on-github). This means that GitHub has a reference to the files rather than hosting the files themselves. Hence, in order to access to the files (for example, loding them with `pandas`) you need to set up Git LFS in your machine so that your computer knows what to do with the GitHub provided reference. Once you have the setup ready, there won't be need to deal with Git FLS unless you are trying to modify the raw data or if you are trying to push a new large file into GitHub.

__Git FLS setup__

Check if you have `git lfs` installed in your machine by running `git lfs version` in your terminal. In case you don't have it yet, you can follow the instructions [here](https://docs.github.com/en/repositories/working-with-files/managing-large-files/installing-git-large-file-storage) to install it. Once it is installed, run `git lfs install` to activate it. This will enable the Git LFS functionality globally. After that, any repository you interact with on that system will have Git LFS enabled. 

Finally, to be able to read `parquet` files using `pandas` we need to install the [pyarrow](https://arrow.apache.org/docs/python/install.html) or [fastparquet](https://pypi.org/project/fastparquet/) python libraries. To install the first one you can use the command below in your terminal. Make sure you have your project virtual environment.
```
conda install -c conda-forge pyarrow
```
