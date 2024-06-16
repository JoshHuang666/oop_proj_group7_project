import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def read_scores_from_csv(filename='best_scores.csv'):
    # Read the scores from the CSV file into a DataFrame
    df = pd.read_csv(filename, index_col='Rank')
    return df

def calculate_average_and_std_error(df):
    # Calculate average score and standard error (assuming scores are a sample from a population)
    sample_mean = df['Score'].mean()
    sample_std = df['Score'].std()
    n = len(df)
    standard_error = sample_std / np.sqrt(n)

    return sample_mean, standard_error

def plot_scores_with_error_and_annotations(df):
    # Calculate average score and standard error
    sample_mean, standard_error = calculate_average_and_std_error(df)

    # Plotting using Matplotlib with error bars (standard error)
    plt.figure(figsize=(10, 6))
    plt.bar(df.index, df['Score'], yerr=standard_error, capsize=5, color='blue', alpha=0.7)
    plt.axhline(y=sample_mean, color='red', linestyle='--', label='Average Score')  # Horizontal line for average score
    plt.xlabel('Rank')
    plt.ylabel('Score')
    plt.title('Best Scores with Average and Standard Error')
    plt.xticks(df.index)
    plt.legend()
    plt.grid(True)
    
    # Adding annotations for average score and standard error
    plt.text(len(df)+0.5, sample_mean, f'Average Score: {sample_mean:.2f}', color='red')
    plt.text(len(df)+0.5, sample_mean - standard_error*2, f'Standard Error: {standard_error:.2f}', color='red')

    plt.tight_layout()
    plt.show()

    return sample_mean, standard_error

# Use the read_scores_from_csv function and plot the scores with average and standard error
if __name__ == "__main__":
    scores_df = read_scores_from_csv()
    print("Best Scores from CSV:")
    print(scores_df)

    # Plotting the scores with average and standard error
    average_score, standard_error = plot_scores_with_error_and_annotations(scores_df)

    print(f"\nAverage Score: {average_score}")
    print(f"Standard Error: {standard_error}")