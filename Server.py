from flask import Flask
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from CfRec import CfRec

def loadData():
    ratings_df = pd.read_csv('ratings.csv')


    posts_df = pd.read_csv('posts.csv')

    merged_df = pd.merge(ratings_df, posts_df, on='postId')

    userPostMatrix = merged_df.pivot_table(index='userId', columns='postTitle', values='rating').fillna(0)
    xUser = cosine_similarity(userPostMatrix)


    rec = CfRec(userPostMatrix, xUser, posts_df )
    return rec
    
app = Flask(__name__)

@app.route("/rc/user/<userId>", methods=['GET'])
def getRecommendations(userId):
    return rec.recommend_user_based(userId)


if __name__ == "__main__":
    rec = loadData()
    app.run(port=5001, debug=True)