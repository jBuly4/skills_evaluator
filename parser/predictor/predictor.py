import csv
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler


def prepare_data(path_to_skillset):
    """Get only skills and salaries from prepared skillset."""
    with open(path_to_skillset, 'r') as source:
        reader = csv.reader(source)
        with open('./dataset/skill_dataset.csv', 'w') as dest:
            writer = csv.writer(dest)
            writer.writerow(['skill', 'salary'])
            for row in reader:
                if row[0] != 'keyword':
                    skills_lst = [skill.strip() for skill in row[2].split(',')]
                    for sk in skills_lst:
                        writer.writerow([sk, round(float(row[-1]), 2)])


# prepare_data('../clean_csv/cleaned_data/skill_sets/indeed_skill_set_final.csv')
# For now it is hardcoded. Will be changed in future
prepare_data('../clean_csv/cleaned_data/skill_sets/indeed_skill_set.csv')

df = pd.read_csv('./dataset/skill_dataset.csv')

skills_series = df['skill'].str.split(',', expand=True).stack()
top_10_skills = skills_series.value_counts().head(10).index.tolist()
print(top_10_skills)

# Filter the dataset to include only the top 10 skills
df_filtered = df.copy()
for skill in top_10_skills:
    df_filtered[skill] = df['skill'].str.contains(skill).astype(int)

# Preparing X and y
X = df_filtered[top_10_skills]
y = df_filtered['salary']

# Standardizing the features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Perform K-Means clustering
kmeans = KMeans(n_clusters=3, random_state=0)
clusters = kmeans.fit_predict(X_scaled)
df_filtered['cluster'] = clusters

# Visualizing the clusters
plt.scatter(df_filtered.iloc[:, 0], df_filtered.iloc[:, 1], c=df_filtered['cluster'], cmap='viridis')
plt.title('Clusters of Top 10 Skills')
plt.xlabel('Skill')
plt.ylabel('Salary')
plt.show()

# Analyze clusters
for i in range(kmeans.n_clusters):
    cluster_data = df_filtered[df_filtered['cluster'] == i]
    avg_salary = cluster_data['salary'].mean()
    print(f'Cluster {i} - Average Salary: {avg_salary}')

# Using PCA to reduce dimensions to 2 for visualization
pca = PCA(n_components=2)
X_pca = pca.fit_transform(X_scaled)

# Visualizing the clusters with PCA components
plt.scatter(X_pca[:, 0], X_pca[:, 1], c=df_filtered['cluster'], cmap='viridis')
plt.title('Clusters of Top 10 Skills (PCA)')
plt.xlabel('PCA Component 1')
plt.ylabel('PCA Component 2')
plt.show()

plt.figure(figsize=(8, 6))
for i in np.unique(clusters):
    plt.scatter(X_pca[clusters == i, 0], X_pca[clusters == i, 1], label=f'Cluster {i}')
plt.title('Clusters of Skills (PCA)')
plt.xlabel('PCA Component 1')
plt.ylabel('PCA Component 2')
plt.legend()
plt.show()


# Assuming df_filtered is your DataFrame with one-hot encoded top 10 skills and salary
X = pd.get_dummies(df_filtered[top_10_skills])
y = df_filtered['salary']

# Splitting the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=0)

# Training the Linear Regression model
model = LinearRegression()
model.fit(X_train, y_train)

# Making predictions
y_pred = model.predict(X_test)

# Evaluating the model
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f"Mean Squared Error: {mse}")
print(f"R-squared: {r2}")

plt.scatter(y_test, y_pred, alpha=0.5)
plt.title('Actual vs Predicted Salaries')
plt.xlabel('Actual Salary')
plt.ylabel('Predicted Salary')
plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'k--', lw=2)  # Diagonal line for reference
plt.show()

# Splitting the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)

# Instantiate the Random Forest Regressor
random_forest_model = RandomForestRegressor(n_estimators=100, random_state=0)  # n_estimators can be tuned

# Train the model
random_forest_model.fit(X_train, y_train)

# Make predictions
y_pred_rf = random_forest_model.predict(X_test)

# Evaluate the model
mse_rf = mean_squared_error(y_test, y_pred_rf)
r2_rf = r2_score(y_test, y_pred_rf)

print(f"Random Forest - Mean Squared Error: {mse_rf}")
print(f"Random Forest - R-squared: {r2_rf}")

# Scatter plot of actual vs predicted salaries
plt.scatter(y_test, y_pred_rf, alpha=0.5)
plt.title('Random Forest: Actual vs Predicted Salaries')
plt.xlabel('Actual Salary')
plt.ylabel('Predicted Salary')
plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'k--', lw=2)  # Diagonal line for reference
plt.show()

# Filter the dataset for entries that include top 10 skills
top_10_skills_mask = X_test[top_10_skills].sum(axis=1) > 0
X_top_10 = X_test[top_10_skills_mask]
y_top_10_actual = y_test[top_10_skills_mask]

# Predict salaries for these entries
y_top_10_pred = random_forest_model.predict(X_top_10)

# Compare predictions with actual values
plt.scatter(y_top_10_actual, y_top_10_pred, alpha=0.5)
plt.title('Random Forest: Actual vs Predicted Salaries for Top 10 Skills')
plt.xlabel('Actual Salary')
plt.ylabel('Predicted Salary')
plt.plot([y_top_10_actual.min(), y_top_10_actual.max()], [y_top_10_actual.min(), y_top_10_actual.max()], 'k--', lw=2)
plt.show()
