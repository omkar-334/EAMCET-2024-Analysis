import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

df = pd.read_excel("colleges.xlsx", sheet_name="Sheet1")


def average_rank_per_college(n: int, df: pd.DataFrame):
    avg_rank = df[df["Rank"] <= n].groupby("College")["Rank"].mean()
    students = df[df["Rank"] < n].groupby("College").size()

    comparison_df = (
        pd.DataFrame({"College": avg_rank.index, "Average Rank": avg_rank.values, "Number of Students": students.reindex(avg_rank.index, fill_value=0).values})
        .reset_index(drop=True)
        .nsmallest(20, "Average Rank")
    )

    comparison_df.sort_values(by="Average Rank", inplace=True)

    plt.figure(figsize=(12, 6))

    plt.subplot(1, 2, 1)
    sns.barplot(data=comparison_df, x="College", y="Average Rank", palette="viridis")
    plt.xticks(rotation=90)
    plt.title(f"Average Rank per College (Rank < {n})")
    plt.xlabel("College")
    plt.ylabel("Average Rank")

    plt.subplot(1, 2, 2)
    sns.barplot(data=comparison_df, x="College", y="Number of Students", palette="magma")
    plt.xticks(rotation=90)
    plt.title(f"Number of Students per College (Rank < {n})")
    plt.xlabel("College")
    plt.ylabel("Number of Students")

    plt.tight_layout()
    plt.savefig(f"images/arc{n}.png")


def top_n_per_college(df):
    top_100 = df.sort_values("Rank").groupby("College").head(100)
    avg_100 = top_100.groupby("College")["Rank"].mean()

    top_10 = df.sort_values("Rank").groupby("College").head(10)
    avg_10 = top_10.groupby("College")["Rank"].mean()

    comparison_df = pd.DataFrame({"Top 100 Avg Rank": avg_100, "Top 10 Avg Rank": avg_10}).reset_index().sort_values(by="Top 10 Avg Rank").head(20)
    comparison_df.fillna({"Top 100 Avg Rank": np.nan, "Top 10 Avg Rank": np.nan}, inplace=True)
    comparison_df.sort_values(by="Top 10 Avg Rank", inplace=True)

    plt.figure(figsize=(12, 6))
    sns.barplot(data=comparison_df.melt(id_vars="College", var_name="Student Group", value_name="Average Rank"), x="College", y="Average Rank", hue="Student Group", palette="pastel")
    plt.xticks(rotation=90)
    plt.title("Comparison of Average Rank of Top 100 and Top 10 Students per College")
    plt.xlabel("College")
    plt.ylabel("Average Rank")
    plt.legend(title="Student Group")
    plt.savefig("images/topnc.png")
