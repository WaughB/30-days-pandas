import pandas as pd

data = [[1, 3, 5, '2019-08-01'], [1, 3, 6, '2019-08-02'], [2, 7, 7, '2019-08-01'], [2, 7, 6, '2019-08-02'], [4, 7, 1, '2019-07-22'], [3, 4, 4, '2019-07-21'], [3, 4, 4, '2019-07-21']]
views = pd.DataFrame(data, columns=['article_id', 'author_id', 'viewer_id', 'view_date']).astype({'article_id':'Int64', 'author_id':'Int64', 'viewer_id':'Int64', 'view_date':'datetime64[ns]'})

# Function to see which authors are viewing their own articles.
def article_views(views: pd.DataFrame) -> pd.DataFrame:
    
    # I don't need the article_id or view_date columns.
    views = views.drop(["article_id", "view_date"], axis=1)

    # I need to see if the author_id is the same as the viewer_id.
    views = views[views["author_id"] == views["viewer_id"]]

    # I need to return the author_id column as a DataFrame.
    return views[["author_id"]].drop_duplicates().sort_values(by="author_id")

print(article_views(views))
