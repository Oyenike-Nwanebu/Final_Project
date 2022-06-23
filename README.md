The aim of this project is to predict the success of a Kickstarter project campaign and deploy an app that users can interact with to get predictions and the probability for success.

### Background

[Kickstarter](https://www.kickstarter.com) is a powerful crowdfunding platform started in April 2009. Since its inception till date (June 23, 2022), 222,311 projects have been sucessfully funded with over $6.1 billion dollars raised in pledges. However, compared to most other crowdfunding platforms, it is based on an all-or-nothing model which means if a project is unable to raise upto its set goal amount by the deadline, the creators do not get paid. Creators do want to succeed as a failed campaign implies wasted time and resources and Backers will like to know campaigns that are likely succeed so that they do not miss out on opportunities.

### Data Collection
Data was collected from [web robots website](https://webrobots.io/kickstarter-datasets) which uses a scraper robot to crawl Kickstarter projects once per month.

### Data Exploration
For the purpose of this project, only completed projects launched between 25 April 2009 and 11 May 2022 were analyzed. After cleaning the data and removing duplicate campaigns, the dataset had 59.5% successful projects and 40.5% failed projects. 

### Feature Engineering
Time traveled features such as Spotlight, Number of backers, Amount pledged etc were not used for modeling as the creators will not have access to this information before the campaign launch date.

Features like goal amount in USD, Staff pick (whether a campaign is selected to be feature or not), prep_time (number of days between campaign creation date and launch date), campaign duration (number of days between launch date and campaign deadline), project category, Location of the creator (Country), number of words in the project description and project name were used.

### Modeling
Classification models like Logistic Regression, Random Forest and XGBoost were used and their hyperparameters tuned using gridsearch to avoid overfitting

### Model Evaluation
Since there is an imbalance in the dataset and the cost of False positive and False negatives are the same, the optimal threshold for class prediction was tuned by threshold moving using R0C curve and the classification models were compared using roc-auc score and F1 score.

XGBoost was the best performing model with auc score of 0.83 and F1 score of 0.79. The confusion matrix also showed that the model was able to capture a lot of the True Negatives, which is the minority class, using a threshold of 0.599

### Model Interpretation
The output of the XGBoost model was interpreted using [SHAP](https://towardsdatascience.com/interpretable-machine-learning-with-xgboost-9ec80d148d27) values to determine which features have higher importance for campaign success. 

The SHAP summary plot showed that: 
1. Campaigns with low goal amount (USD) are more likely to succeed
2. Being selected as Staff pick improves the likelihood of success
3. Campaigns with longer prep time are successful
4. Campaigns with shorter duration are successful
5. The choice of project category matters as projects in the category of Film & video, games, comic were more successful than projects in the category of crafts, technology and jounalism

### Model Deployment
A streamlit [app](https://share.streamlit.io/oyenike-nwanebu/final_project/Kickstarter_app.py) was built to deploy the xgboost model.

Please feel free to interact with the app at the link below:
https://share.streamlit.io/oyenike-nwanebu/final_project/Kickstarter_app.py