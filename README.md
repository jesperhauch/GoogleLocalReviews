# Exam Project 

####  42578 Advanced Business Analytics

**Group members:** 

Ann-Katrine Christiansen (s184287)\
Jesper Hauch (s174287)\
Johanne Juul Iversen (s174308)\
Toke Holst Møller (s172827)




## Introduction

Have you ever been urban travelling? Then you have most likely used Google Maps, Yelp or TripAdvisor for good recommendations and tips on where to go, where to eat and where to stay. Here you might have been swarmed with contradicting opinions and different experiences from reviewers across the globe, which only creates further confusion. If you can relate to this, then you will appreciate the solution developed in this project.

This solution aims to tailor a guide for urban travellers to help them find exciting areas for their next holiday. This is achieved by comparing their favorite establishments in their local areas to areas at their next destination. This project acts as a proof-of-concept (POC) considering Manhattan in New York City (NYC) and London. The guide is based on establishments in the two metropolises along with their reviews.

The project uses the [Google Local](https://cseweb.ucsd.edu/~jmcauley/datasets.html#google_local) data published by Professor Julian McAuley from University of California, San Diego. The data contains reviews on establishments along with their price ranges and geographical location. The raw data has 3.116.785 establishments and 11.453.845 reviews, which spans locations across the world.

The guide is a recommender system based on a space embeddings model, where area embeddings are created based on its characteristics. The embeddings for an area represents the amount of establishments in an area, their price ranges, ratings, review sentiments and more. In essence, similar embeddings represents similar areas, which is utilized for cross-border comparisons.

Finally, the model is deployed in collaboration with 2021.ai using their AI platform Grace. Here, users can input their ratings for establishments they have visited and get recommendations on what areas to visit in either NYC or London.

## How to read this report

The report consist of four main notebooks besides this README notebook, which should be read in the order indicated below. If the working directory is set to the source file location, the notebooks can be accessed by clicking the links below.

1. [Descriptive Statistics](./DescriptiveStatistics.ipynb)
2. [NLP Classification](./NLPClassification_withSHAP.ipynb)
3. [Space Embeddings](./SpaceEmbeddings.ipynb)
4. [Recommender System](./RecommenderSystem.ipynb)

Additionally, the following notebooks contains the download and preprocessing of data along with a tutorial of the model deployment in Grace. These are available for the interested reader, but are not necessary to understand the outcome of the project.

- [Data Download](./DataDownload.ipynb)
- [Data Preprocessing](./DataProcessing.ipynb)
- [Grace API tutorial](./deployment/GraceAPI.ipynb)


## Discussion

The four notebooks above contains the suggested recommender system supporting the POC highlighted in the introduction. During the project, multiple assumptions were made in order to develop the POC. Therefore, there are several points that have altered the outcome of this project.

During the data processing stage, multiple anomalies were found in the data. First, several establishments had erronous coordinates which could be contradicting with their addresses. A thorough attempt was made to clean these and increase the data quality. However, it cannot be guaranteed that all anomalies are removed, since validation of individiual establishments is required to fulfill this. Additionally, the establishments' price ranges were flipped, as `$$$` is expected to represent expensive establishments. After manual inspection, it was found that `$$$` represented cheap establishments, such as fast food chains. Furthermore, the majority of the establishments' price ranges were missing in the data. Due to these data issues, questions arise regarding whether the data quality is sufficient for the purpose of this project. As a result of this, the data processing can highly influence the outcome of the recommendations, since the model relies on aggregated area characteristics. 

To increase the data quality, a NLP model was developed to predict missing price ranges of establishments based on their reviews. It was necessary to fit this model with establishments with reported price ranges, which primarily consisted of bars and restaurants. Therefore, it is questionable whether the NLP model is appropriate for predicting price ranges of establishments in other sectors, which might be incomparable. To better predict the price range, it might be beneficial to include the city of the establishments, since the price distribution differs significantly from London to New York. Furthermore, instead of a BoW representation with 1-grams, one could have considered modeling 2-grams, since many reviewers use negation before adjectives, e.g. "it was not excellent". This would require a removal of negation words from the list of stopwords, such as "not".

The performance of the final NLP model had a F1-score of 0.61, which outperformed a dummy classifier with a F1-score of 0.40. Thus, a significant improvement was obtained on the price range prediction on a review basis. However, it is challenging to provide the performance on an establishment level, due to how the train-test split is performed. This makes it difficult to evaluate majority voting as reviews for the same establishment can occur in all splits of the data. Since the NLP model was used to enrich data used for the space embeddings model, the highlighted issues might affect the final recommendations.

The space embedding model is based on the placement of a grid over each metropolis, dividing them into equal-size areas. This grid structure is a rigid separation, since city areas are rarely divided into equal sizes in reality. This could be alleviated by using shape files for the different areas and computing space embeddings for these. This would be an interesting extension of the model that would make it more user friendly and interpretable. Additionally, one can argue that the grid placed over Manhattan should have been rotated to parallely align with the existing infrastructure. Another issue regarding the grid structure, is the differences in the establishment density between the cities. NYC is only represented by Manhattan, which is extremely dense, whereas London includes both dense city and spacious suburbs. In hindsight, it would be sensical to only compare similar city structures, i.e. by including the New York suburbs in our analysis.

The space embedding model works by taking the grid cells as input and trying to fit this to the features of the individual grid cells. Therefore, the embeddings calculated are highly influenced by the features that represent the grid cells. One could argue that the number of features included in this analysis is not sufficient for encapsulating the area characteristics in low dimensional embeddings. Furthermore, since the features for each grid cell are aggregations, they might not be unique enough to significantly separate areas from one another. In this project, two space embedding models were developed and compared by calculating the cosine similarity of areas assumed to be similar across NYC and London. Since it is difficult to assess the performance of embeddings, additional similarity measures could have been implemented, such as euclidian distance. It was chosen to develop a recommender system based on the embeddings of the discrete model, which required a discretization of the continuous features. The discretization has been conducted in an attempt to make uniformly distributed bins without accounting for the width of these. This meant that areas with very different characteristics could end up in the same bin, making it hard to distinguish them. Moreover, a large number of features could not be discretized in uniform bins, due to the large amount of zeros in the features. 

The discrete space embeddings are used to create a recommender system. The recommender system takes a user's reviewed establishments along with their provided rating, which is used to recommend areas in the opposite city. The recommended areas are the ones most similar to the average of the area embeddings, in which establishments have been reviewed. The embeddings are weighted by the average of the ratings provided by the user in these reviews. Thereby, reviews with low ratings have an undesirable influence on the final recommendations. A user who has only provided reviews with low ratings is recommended areas with similar establishments to the disliked ones. This can influence the performance of the recommender system and its recommendations. 

The provided recommendations are validated using hypothetical personas based on stereotypes, which are somewhat extreme. It is therefore questionable whether the recommender system is appropriate for the average user. Weaker recommendations would likely be provided to the average person that has less strong opinions. Ideally, validation should have been conducted on users who have provided reviews in both cities. In this approach, one could validate whether recommendations align with actual user preferences.

## Conclusion

In conclusion, this project has proven that a recommender system built on space embeddings can be used to recommend cross-border travel destinations based on user preferences. This is done by combining several different fields within business analytics, resulting in a usable proof of concept with the aim of helping travellers decide what to do on their next trip.

The final outcome of the project is a recommender system, which is considered a success due to the sensible recommendations made by the model. These are validated through three stereotypical personas, whose recommendations are inspected through qualitative area research. From the validation, it is concluded that the developed model performed according to the expectations.

In collaboration with 2021.ai and their AI platform Grace, the model is deployed and callable by an API post request. This adds to the potential business opportunity, as the deployment makes it closer to being a minimum viable product.

To enable the full potential of the recommender system, a range of reflections made throughout the project should be implemented and tested. 
The rigid grids placed on top of the two cities are found inappropriate to make accurate predictions. Instead, the cities should be divided into areas following existing infrastructure e.g. by using shape files. 
Likewise, the data should include an equal amount of dense and suburban areas in respect to the size of the cities to ensure comparability.
Another aspect to investigate, is the possible change in performance if additional and less aggregated features are included. 
These initiatives can help conclude whether the current setup is desirable for making recommendations or whether a different structure is better suited. 

Finally, this project has been an exciting endeavour, which we have enjoyed working on. Additionally, we are thankful for the opportunity to deploy the recommender system and gain valuable experiences with Grace as a result.


## Individual contribution

The table below is a representation of the work contribution, where the (x) indicate the main responsible within each analysis conducted. Throughout the project all subjects has been discussed, and challenges and big decisions has been resolved in collaboration with all group members. 


| Section | Ann-Katrine (s184287)| Jesper (s174287) | Johanne (s174308) | Toke (s172827) | 
|:---: |:-: | :-: | :-: | :-: |
|Data downloading | x | x | | |
|Data preprocessing | x |  | | |
|Sentiment analysis |  | | | x |
|Descriptive analysis | | | x | x |
|NLP features| x | x | ||
|NLP prediction model |  | x | | x |
|SHAP intrepetation |  | | x | |
|Aggregation of data |  | | x | |
|Space embedding |  | x | | x |
|Recommender system | x | | x |  |
|Recommender validation | x | | x | |
|Model deployment |  | x | | |


The README file, containing an introduction, discussion and conclusion as well as the Executive summary have been written as a joint effort, to include all relevant aspects and thereby obtain the best possible outcome :)
