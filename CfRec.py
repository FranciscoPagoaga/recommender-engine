class CfRec():
    def __init__(self, M, X, items, k=10, top_n=5):
        self.X = X
        self.M = M
        self.k = k
        self.top_n = top_n
        self.items = items
        
    def recommend_user_based(self, user):
        try:
            ix = self.M.index.get_loc(user)
            # Use it to index the User similarity matrix
            u_sim = self.X[ix]
            # obtain the indices of the top k most similar posts
            most_similar = self.M.index[u_sim.argpartition(-(self.k+1))[-(self.k+1):]]
            # Obtain the mean ratings of those users for all posts
            rec_items = self.M.loc[most_similar].mean(0).sort_values(ascending=False)
            # Discard already seen posts
            # already seen posts
            seen_mask = self.M.loc[user].gt(0)
            seen = seen_mask.index[seen_mask].tolist()
            rec_items = rec_items.drop(seen).head(self.top_n)
            # return recommendations - top similar users rated posts
            rec_items = rec_items.index.to_frame().reset_index(drop=True).merge(self.items)
            return rec_items.postTitle.tolist()
        except:
            top_n = 10
            mean_ratings = self.M.mean().sort_values(ascending=False)
            # Retrieve the top N highest rated items
            top_items = mean_ratings.nlargest(top_n).index.tolist()

            return(top_items)
        

    def recommend_item_based(self, item):
        liked = self.items.loc[self.items.postId.eq(item), 'title'].item()
        print(f"Because you liked {liked}, we'd recommend you:")
        # get index of post
        ix = self.M.columns.get_loc(item)
        # Use it to index the Item similarity matrix
        i_sim = self.X[ix]
        # obtain the indices of the top k most similar items
        most_similar = self.M.columns[i_sim.argpartition(-(self.k+1))[-(self.k+1):]]
        return (most_similar.difference([item])
                                 .to_frame()
                                 .reset_index(drop=True)
                                 .merge(self.items)
                                 .head(self.top_n))