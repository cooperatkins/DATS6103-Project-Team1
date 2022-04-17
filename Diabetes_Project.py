#%%
#Import packages
import numpy as np
import pandas as pd
import os
import mlxtend
import seaborn as sns
import matplotlib.pyplot as plt
import math
import scipy.stats as stats
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import label_binarize
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report
from sklearn.linear_model import LogisticRegression
from mlxtend.plotting import plot_decision_regions
from sklearn import linear_model
from sklearn.svm import SVC, LinearSVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import cross_val_score
from statsmodels.stats.weightstats import ztest as ztest
import warnings
warnings.filterwarnings('always')

#%%
#Let's define some key functions here that'll help us throughout the rest of this

#Violin plot function
def violin_plot_func(data, cat_col, cont_col):
    '''
    Function will take in a dataset and two column names, one categorical and one continuous
    Data: name of pandas dataframe containing the columns
    cat_col: name of column that will be used to split the violin plots
    cont_col: continuous function'''
    for i in range(len(data[cat_col].unique())):
        globals()['group%s' % i] = data[data[cat_col]==i]
    cat_list = []
    for i in range(len(data[cat_col].unique())):
        cat_list.append(list(globals()['group%s' % i][cont_col]))
    pos = np.arange(1,len(data[cat_col].unique())+1)
    pos_list = np.ndarray.tolist(pos)
    plt.violinplot(cat_list, positions = pos_list)
    plt.xlabel(cat_col)
    plt.ylabel(cont_col)
    plt.show()


#Category plot function
def sns_catplot(data, cat_col, cont_col, kind='violin', hue=None, split=False, col=None, col_wrap=2, legend_labels=None,
                xticks=None):
    '''
    Function will take in a datatset and two column names, one categorical and one continuous. Other parameters are
    optional to assist in plot customization.
    :param data: name of pandas dataframe containing the columns
    :param cat_col: x axis value
    :param cont_col: y axis value
    :param kind: kind of sns plot. Default set to violin
    :param hue: name of column to split the violin plot into categories. Default set to None
    :param split: bool to set hue split into two halves. Default set to False
    :param col: categorical variable to facet the grid
    :param col_wrap: wraps the columns at this width. Default set to 2
    :param legend_labels: labels to set for legend. Default set to None
    :param xticks: labels to set for xticks. Default set to None
    '''
    # check if hue is set
    if hue:
        hue = hue
        if data[hue].unique().size == 2:
            split = True

    # check if col is set
    if col:
        col = col

    # create catplot
    sns.set_palette('hls')
    chart = sns.catplot(data=data, x=cat_col, y=cont_col, kind=kind, hue=hue, split=split, col=col, col_wrap=col_wrap)

    # edit legend labels if provided
    if legend_labels:
        for index in range(len(legend_labels)):
            chart._legend.texts[index].set_text(legend_labels[index])

    # edit xticks if provided
    if xticks:
        plt.xticks(xticks[0], xticks[1])

    plt.xlabel(cat_col)
    plt.ylabel(cont_col)
    plt.show()


#Scatter plot function


#Contingency table/heat map functions - non-proportional
def categorical_contigency_base(group1, group2):
    '''
    Function will combine two categorical variables into a contingency table, and then output a heatmap showing both the numbers and a color scheme to represent equality across the cells. Includes margins
    input group1, group2
    group1: categorical variable
    group2: categorical variable
    output: heatmap showing the contingency table with appropriate coloring
    Group here refers to categorical, but not individual level'''
    data_contingency = pd.crosstab(group1, group2, margins = True, margins_name = 'Total')
    print(data_contingency)
    data_contingency=pd.crosstab(group1, group2, margins = False, margins_name = 'Total')
    f, ax = plt.subplots(figsize=(9, 6))
    sns.heatmap(data_contingency, annot=True, fmt="d", linewidths=.5, ax=ax)
    plt.show()
    return

#Contingency table/heat map functions - overall proportional
def categorical_contigency_prop_whole(group1, group2):
    '''
    Function will combine two categorical variables into a contingency table, and then output a heatmap showing both the numbers and a color scheme to represent equality across the cells. Includes margins
    input group1, group2
    group1: categorical variable
    group2: categorical variable
    output: heatmap showing the contingency table with appropriate coloring
    Group here refers to categorical, but not individual level
    If there is an error, try switching group1 and group2'''
    data_contingency = pd.crosstab(group1, group2, margins = True, margins_name = 'Total')
    columns = group1.unique()
    rows = group2.unique()
    df = pd.DataFrame()
    for i in rows:
        for j in columns:
            proportion = data_contingency[i][j]/data_contingency['Total']["Total"]
            df.loc[i,j]=proportion
    df=df.transpose()
    f, ax = plt.subplots(figsize=(9, 6))
    sns.heatmap(df, annot=True, fmt="f", linewidths=.5, ax=ax)
    plt.show()
    return

#Contingency table/heat map functions - column proportional
def categorical_contigency_prop_col(group1, group2):
    '''
    Function will combine two categorical variables into a contingency table, and then output a heatmap showing both the numbers and a color scheme to represent equality across the cells. Includes margins
    input group1, group2
    group1: categorical variable
    group2: categorical variable
    output: heatmap showing the contingency table with appropriate coloring
    Group here refers to categorical, but not individual level'''
    data_contingency = pd.crosstab(group1, group2, margins = True, margins_name = 'Total')
    columns = group1.unique()
    rows = group2.unique()
    df = pd.DataFrame()
    for i in rows:
        for j in columns:
            proportion = data_contingency[i][j]/data_contingency[i]["Total"]
            df.loc[i,j]=proportion
    df=df.transpose()
    f, ax = plt.subplots(figsize=(9, 6))
    sns.heatmap(df, annot=True, fmt="f", linewidths=.5, ax=ax)
    plt.show()
    return


#Contingency table/heat map functions - row proportional
def categorical_contigency_prop_row(group1, group2):
    '''
    Function will combine two categorical variables into a contingency table, and then output a heatmap showing both the numbers and a color scheme to represent equality across the cells. Includes margins
    input group1, group2
    group1: categorical variable
    group2: categorical variable
    output: heatmap showing the contingency table with appropriate coloring
    Group here refers to categorical, but not individual level'''
    data_contingency = pd.crosstab(group1, group2, margins = True, margins_name = 'Total')
    columns = group1.unique()
    rows = group2.unique()
    df = pd.DataFrame()
    for i in rows:
        for j in columns:
            proportion = data_contingency[i][j]/data_contingency['Total'][j]
            df.loc[i,j]=proportion
    df=df.transpose()
    f, ax = plt.subplots(figsize=(9, 6))
    sns.heatmap(df, annot=True, fmt="f", linewidths=.5, ax=ax)
    plt.show()
    return

#Chi-square test function (for testing impact of categorical data on our outcome variables)
def chi_square_test(group1, group2, alpha = 0.05, decimals = 3):
    '''
    Function will combine two categorical variables into a contingency table, and then output a two sided hypothesis test for independence with the chi-square statistic, p-value, and hypothesis test conclusion
    group1: categorical variable
    group2: categorical variable
    alpha: cutoff for p-value, number between 0 and 1, defaults to 0.05 or a 5% cutoff
    decimals: preferred rounding number for chi-square and p-value
    output: chi-square statistic, p-value, and hypothesis test conclusion
    Group here refers to categorical, but not individual level'''
    data_contingency = pd.crosstab(group1, group2, margins = True, margins_name = 'Total')
    chi_square = 0
    columns = group1.unique()
    rows = group2.unique()
    for i in rows:
        for j in columns:
            O = data_contingency[i][j]
            E = data_contingency[i]['Total'] * data_contingency['Total'][j] / data_contingency['Total']['Total']
            chi_square += (O-E)**2/E
    p_value = 1 - stats.chi2.cdf(chi_square, (len(rows)-1)*(len(columns)-1))
    conclusion = "Failed to reject the null hypothesis."
    if p_value <= alpha:
        conclusion = "Null Hypothesis is rejected."
        
    print("chisquare-score is:", round(chi_square,decimals), " and p value is:", round(p_value,decimals))
    return(conclusion)

#two sample Z-test function (for testing impact of continuous data based on diabetes_012)
def two_sample_test(group1, group2, alpha = 0.05, decimals = 3):
    '''
    input group1, group 2, alpha, decimals
    group 1: qualitative variable corresponding to the first group (ie female)
    group 2: qualitative variable corresponding to the second group (ie male)
    alpha: cutoff for p-value, number between 0 and 1, defaults to 0.05 or a 5% cutoff
    decimals: preferred rounding number for z-score and p-value
    outputs: z_score and p_value, plus hypothesis testing determination
    Note: If there are more than 2 levels of a category, it is necessary to run the function for each respective pair of values
    '''
    ztest_vals = ztest(group1, group2)
    z_stat = round(ztest_vals[0],decimals)
    p_value = round(ztest_vals[1],decimals)
    if p_value < 0.05:
        
        print (f"Your z-score was {z_stat} and your p-value was  {p_value}, which is less than 0.05. We therefore reject our null hypothesis")
    else:
        print (f"Your z-score was {z_stat} and your p-value was  {p_value}, which is greater than 0.05. We therefore fail to reject our null hypothesis")
    return 




#%%
#Read in csv
diabetes = pd.read_csv('diabetes_012_health_indicators_BRFSS2015.csv')

#Testing the functions work
# categorical_contigency_base(diabetes['Diabetes_012'], diabetes['HighBP'])
# categorical_contigency_prop_whole(diabetes['Diabetes_012'], diabetes['HighBP'])
# categorical_contigency_prop_col(diabetes['Diabetes_012'], diabetes['HighBP'])
# categorical_contigency_prop_row(diabetes['Diabetes_012'], diabetes['HighBP'])
# chi_square_test(diabetes['Diabetes_012'], diabetes['HighBP'])
# violin_plot_func(diabetes, 'Diabetes_012', 'Age')
# two_sample_test(diabetes[diabetes['Diabetes_012']==0]['Age'], diabetes[diabetes['Diabetes_012']==1]['Age'])
# %%
#Let's add basic summary information here (proportions, averages, etc.)
summary_stats = pd.DataFrame(diabetes.describe())
summary_stats = summary_stats.reset_index()
print(summary_stats.to_markdown())
#%%
#Let's add some summary visualizations here using our few continuous variables. We can put Diabetes_012 as the color and use shape for some other things, or we can make violin plots with diabetes_012 as the splits and maybe do double splits
# BMI vs. Diabetes_012 by Sex and Income
sns_catplot(diabetes, 'Diabetes_012', 'BMI', hue='Sex', col='Income', col_wrap=4, legend_labels=['Male', 'Female'],
            xticks=([0, 1, 2], ['No Diabetes', 'Pre Diabetes', 'Has Diabetes']))

# BMI vs. Diabetes_012 by Sex and HighBP
sns_catplot(diabetes, 'Diabetes_012', 'BMI', hue='Sex', col='HighBP', legend_labels=['Male', 'Female'],
            xticks=([0, 1, 2], ['No Diabetes', 'Pre Diabetes', 'Has Diabetes']))

# BMI vs. Diabetes_012 by Sex and HighChol
sns_catplot(diabetes, 'Diabetes_012', 'BMI', hue='Sex', col='HighChol', legend_labels=['Male', 'Female'],
            xticks=([0, 1, 2], ['No Diabetes', 'Pre Diabetes', 'Has Diabetes']))

# BMI vs. Diabetes_012 by Sex and PhysActivity
sns_catplot(diabetes, 'Diabetes_012', 'BMI', hue='Sex', col='PhysActivity', legend_labels=['Male', 'Female'],
            xticks=([0, 1, 2], ['No Diabetes', 'Pre Diabetes', 'Has Diabetes']))

# Age vs. Diabetes_012 by Sex and Income
sns_catplot(diabetes, 'Diabetes_012', 'Age', hue='Sex', col='Income', col_wrap=4, legend_labels=['Male', 'Female'],
            xticks=([0, 1, 2], ['No Diabetes', 'Pre Diabetes', 'Has Diabetes']))

# Age vs. Diabetes_012 by Sex and HighBP
sns_catplot(diabetes, 'Diabetes_012', 'Age', hue='Sex', col='HighBP', legend_labels=['Male', 'Female'],
            xticks=([0, 1, 2], ['No Diabetes', 'Pre Diabetes', 'Has Diabetes']))

# Age vs. Diabetes_012 by Sex and HighChol
sns_catplot(diabetes, 'Diabetes_012', 'Age', hue='Sex', col='HighChol', legend_labels=['Male', 'Female'],
            xticks=([0, 1, 2], ['No Diabetes', 'Pre Diabetes', 'Has Diabetes']))

# Age vs. Diabetes_012 by Sex and PhysActivity
sns_catplot(diabetes, 'Diabetes_012', 'Age', hue='Sex', col='PhysActivity', legend_labels=['Male', 'Female'],
            xticks=([0, 1, 2], ['No Diabetes', 'Pre Diabetes', 'Has Diabetes']))
#%%
#Let's do some contingency tables/heat maps here and could consider proportions.

#%%
#Test/Train split - we have sufficient data to do a 9/1 or a 4/1 (probably a 4/1 since pre-diabetes is a relatively small category). Make sure we set the random state here so we can repeat it

# xdiabetes = diabetes[['HighBP', 'HighChol', 'CholCheck', 'BMI', 'Smoker', 'Stroke', 'HeartDiseaseorAttack', 'PhysActivity', 'Fruits', 'Veggies', 'HvyAlcoholConsump', 'AnyHealthcare', 'NoDocbcCost', 'GenHlth', 'MentHlth', 'PhysHlth', 'DiffWalk', 'Sex', 'Age', 'Education', 'Income']]
# ydiabetes = diabetes['Diabetes_012']
#xdiabetestrain, xdiabetestest, ydiabetestrain, ydiabetestest = train_test_split(xdiabetes, ydiabetes, train_size = .8, random_state=12345 )

xdiabetes = diabetes[
    ['HighBP', 'HighChol', 'CholCheck', 'BMI', 'Smoker', 'Stroke', 'HeartDiseaseorAttack', 
     'PhysActivity', 'Fruits', 'Veggies', 'HvyAlcoholConsump', 'AnyHealthcare', 'NoDocbcCost', 
     'GenHlth', 'MentHlth', 'PhysHlth', 'DiffWalk', 'Sex', 'Age', 'Education', 'Income']]
ydiabetes = diabetes['Diabetes_012'].values
class_le = LabelEncoder()
ydiabetes = class_le.fit_transform(ydiabetes)

ydiabetes1 = label_binarize(ydiabetes, classes=[0,1,2])
xdiabetestrain, xdiabetestest, ydiabetestrain, ydiabetestest = train_test_split(xdiabetes, ydiabetes, train_size=.8,
                                                                                random_state=12345)
xdiabetestrain1, xdiabetestest1, ydiabetestrain1, ydiabetestest1 = train_test_split(xdiabetes, ydiabetes1, train_size=.8,
                                                                                random_state=12345)

#%%
#First, let's build a basic logistic regression, we'll need to either use sklearn or the function Prof. Lo gave us in quiz 3 for a multinomial response variable

#Model Building - Logistic

#Model summary information (including pseudo-R^2)
#Loop with different cutoff values showing score and confusion matrix

#ROC-AUC


#%%
#Start building more complicated models
#Model Building - Trees, SVM, etc.
#%%
#=========================Decision Tree=========================

from sklearn.multiclass import OneVsRestClassifier

rf1 = DecisionTreeClassifier(max_depth=3, criterion='entropy', random_state=0)
# Fit dt to the training set
rf1 = rf1.fit(xdiabetestrain, ydiabetestrain)
y_test_pred = rf1.predict(xdiabetestest)
y_pred_score = rf1.predict_proba(xdiabetestest)

rf2 = OneVsRestClassifier(DecisionTreeClassifier(max_depth=3, criterion='entropy'))
# Fit dt to the training set
rf2.fit(xdiabetestrain1, ydiabetestrain1)
y_test_pred1 = rf2.predict(xdiabetestest1)
y_pred_score1 = rf2.predict_proba(xdiabetestest1)

print('Decision Tree results')

# Evaluate test-set accuracy
print('test set evaluation: ')
print("Accuracy score: ", accuracy_score(ydiabetestest, y_test_pred) * 100)
print("Confusion Matrix: \n", confusion_matrix(ydiabetestest, y_test_pred,))
print("Classification report:\n", classification_report(ydiabetestest, y_test_pred))

from sklearn.metrics import roc_curve, auc

n_classes=3
fpr = dict()
tpr = dict()
roc_auc = dict()
for i in range(n_classes):
    fpr[i], tpr[i], _ = roc_curve(ydiabetestest1[:, i], y_pred_score1[:, i])
    roc_auc[i] = auc(fpr[i], tpr[i])
    print(f'AUC value of {i} class:{roc_auc[i]}')

# Plot of a ROC curve for a specific class
for i in range(n_classes):
    plt.figure()
    plt.plot(fpr[i], tpr[i], label='ROC curve (area = %0.2f)' % roc_auc[i])
    plt.plot([0, 1], [0, 1], 'k--')
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('Decision Tree ROC')
    plt.legend(loc="lower right")
    plt.show()

#%%
#Random Forest


#%%
#SVM(SVC)


#%%
#Comparison of all models to determine which variables had the largest impacts and which model was best