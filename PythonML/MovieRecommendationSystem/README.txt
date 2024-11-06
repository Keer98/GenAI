Project Title: Movie Recommendation System
This project aims to build a robust movie recommendation system capable of providing personalized recommendations to users based on their viewing history and preferences.
Data Preparation:
1. Data Cleaning: 
o Handled missing values and inconsistencies in the dataset.
2. Synthetic Data Generation: 
o Created a synthetic dataset with customer IDs to simulate user-item interactions.
o Assigned random customer IDs to each show to create a diverse user-item matrix.
Model Development:
1. User-Item Matrix: 
o Constructed a user-item matrix to represent user-show interactions.
2. Association Rule Mining: 
o Utilized the Apriori algorithm to discover frequent itemsets (co-watched shows).
o Derived association rules to identify relationships between shows.
o Content-Based Filtering: 
* Used the discovered association rules to recommend shows that are frequently watched together with a user's previously watched shows.
3. Collaborative Filtering: 
o Identified similar users based on their viewing history.
o Recommended shows that similar users have watched but the target user hasn't.
4. Hybrid Recommendation: 
o Combined content-based and collaborative filtering approaches to provide a more comprehensive and accurate recommendation system.
o Weighted the recommendations from both approaches to achieve a balanced and personalized experience.

