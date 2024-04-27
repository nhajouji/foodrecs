[A relatable problem](https://www.youtube.com/watch?v=6edlBZ64TDk)

# Recipe recommender

We set out to construct a recommendation engine that suggests recipes for a user based on things we can learn from [this data](https://www.kaggle.com/datasets/irkaal/foodcom-recipes-and-reviews). 

* We succeeded in creating an engine that does what we want!
* Not everything we tried along the way worked.

This repository contains our main results.

#### Minor Note
The dataset we started with exceeds GitHub's size limits. We originally tried to get around this using GitLFS, but ran out of bandwidth.

This repository contains the cleaned data we need for modeling purposes, and notebooks explaining how we obtained the clean data from the original data. To run the data cleaning notebooks, one would also need to download the original datasets from Kaggle, or clone our [second repository on huggingface](https://huggingface.co/erdos-sp-2024-foodrecs/food-recs).


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

(add picture)


## Obtaining our Model

To obtain our model, we used what is becoming a standard tool in recommender systems: a matrix factorization, obtained from the singular value decomposition of an affinity matrix. Note that this only requires the review dataset, not the recipe dataset.

1. First, we encode the training portion of our review data into an "affinity matrix": each row corresponds to a user, each column to a recipe, each entry is 0 or 1, with a 1 indicating that a user has reviewed a recipe. Let's call this matrix $M'$. Note that $M'$ is an $m \times n$ matrix, where $m$ is the number of users and $n$ the number of recipes.
2. We obtain a normalized version of $M'$ by subtracting the mean value of each row from that row, so the rows have mean 0. Call this matrix $M$. 
3. We compute the singular value decomposition of $M$: this is going to be a factorization of $M$ as $M = ADB$, where $D$ is a $k\times k$ diagonal matrix with nonnegative eigenvalues, and $A,B$ are matrices of shape $m \times k, k\times n$, respectively. Here, $k$ denotes the rank of $M$.
4. We set $U = A \sqrt{D}$ and $R = (\sqrt{D} B)^{tr}$ to obtain a pair of matrices of shape $m \times k$ and $n \times k$. We interpret these as the desired maps from the set of users and the set of recipes to a common vector space (of dimension $k$).

Now, the matrices $U, R$ have the right shape - we could, if we wanted, take them to be our model, and the code would work fine.
However, the scores we obtain with these matrices are horribly overfit to the training data: by design, $f(u,r) = 1$ if $u,r$ is in the training set and $f(u,r) = 0$ otherwise. The mean score assigned to recipes in the holdout set is going to be 0, which is less than the mean score overall. 

To obtain better models, we use TruncatedSVD instead of "complete" SVD as you'd learn about in linear algebra. This means we're going to replace $D$ by a matrix of lower rank by replacing all but the $r$ largest eigenvalues with 0, and define $U, R$ as we did with the original $D$. The product $UR^{tr}$ will have rank $r$ - in particular, this means it can no longer be equal to $M$.
The hope is that when we pass to these lower rank factorizations, the scores for user recipe pairs in the holdout set increase, but the global average of $f$ stays the same. This is based on the following assumptions:
* The "true affinity matrix" is a matrix $M_0$ of low rank.
* The matrix we started with is $M_0 + \mathrm{ noise}$.
* The product $UR^{tr}$ is closer to $M_0$ than $M$.

This is exactly what we saw when we did our cross validation.
(See the SVD notebook in the "Models" folder for details.)

### Final Model

The scores were highest for the $r = 2$ model, so that is the model we settled on. 

* The mean score assigned to user-recipe pairs in the holdout set was 0.803.
* The mean score overall is effectively 0 (the actual number is $5 \cdot 10^{-18}$.)
 
The final score is surprisingly high. Even in the cross validation phase, the $r = 2$ model had an average score of 0.7 and dropped off steeply as the rank went up, with all scores below $0.3$ once we get to $r>7$.

### Exploring Final Model
The model that worked best was surprisingly simpler than we would have expected. It also required very little data to construct, so one can't help but be curious about how it ended up predicting recipe pairs that were in the holdout set.

There are various ways of playing around with the final model to see what it's actually doing.

* We can visualize the recipe space by plotting the SVD vectors in $\mathbb{R}^2$.
* Our main goal is to obtain rankings of the recipes that are catered to the tastes of a given user; however, we can just as easily use our model to rank recipes based on how similar they are to a given recipe.

## User Interface

Most people are not going to open up a Jupyter notebook to figure out what they're going to buy from the grocery store. Consequently, we designed a web interface that generates suggestions based on both a query and a user history. We used a sentence transformer to convert both the query and the recipe descriptions into vectors, and then assigned to each recipe a weighted score of the query dot product and the SVD dot product.

Recommendations

![AppPhoto1](https://github.com/nhajouji/foodrecs/assets/96888276/eff201ad-fd8e-44c1-9d16-c4206a95c955)

User-tuned Search

![AppPhoto2](https://github.com/nhajouji/foodrecs/assets/96888276/0407232a-483a-4453-9b6b-e36211199508)
