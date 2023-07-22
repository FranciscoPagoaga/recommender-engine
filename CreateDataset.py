from dotenv import load_dotenv, find_dotenv
import os
import csv
from pymongo import MongoClient
load_dotenv(find_dotenv())

connection_string = os.environ.get("MONGO_URI")
client = MongoClient(connection_string)
dbs = client.GradProject
userCollection = dbs.users
postCollection = dbs.posts
collections = dbs.list_collection_names()

# def find_all_users():
#     users = userCollection.find()
#     posts = postCollection.find()
#     matrix = []
#     array = []
#     headers = []
#     headers.append("userId")
#     counter = 1
#     for user in users:
#         array.append(str(user['_id']))
#         for post in posts:
#             if(counter == 1):
#                 headers.append(str(post['_id']))

#             if str(user['_id']) in post['rating']:
#                 array.append(post['rating'][str(user['_id'])])
#             else:
#                 array.append(0)
#         counter = counter + 1
#         posts.rewind()
#         matrix.append(array)
#         array=[]
#     users.rewind()
#     print(headers)
#     print(matrix)    
#     writeCSV(matrix,headers)

def find_all_users():
    users = userCollection.find()
    posts = postCollection.find()
    matrixRatings = []
    arrayRatings = []
    matrixPosts = []
    arrayPosts = []
    headers = []
    headers.append("userId")
    counter = 1
    for user in users:
        counterId = 1
        for post in posts:
            if(counter == 1):
                arrayPosts.append(str(counterId))
                arrayPosts.append(str(post['_id']))
                matrixPosts.append(arrayPosts)
                arrayPosts = []

            if str(user['_id']) in post['rating']:
                arrayRatings.append(str(user['_id']))
                arrayRatings.append(str(counterId))
                arrayRatings.append(post['rating'][str(user['_id'])])
                matrixRatings.append(arrayRatings)
                arrayRatings=[]
            counterId = counterId + 1
        
        counter = counter + 1
        posts.rewind()
    users.rewind()
    writeCSVs(matrixRatings,matrixPosts)

def writeCSVs(matrixRatings, matrixPosts):
    with open('ratings.csv', 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['userId', 'postId', 'rating'])
        writer.writerows(matrixRatings)
    
    with open('posts.csv', 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['postId', 'postTitle'])
        writer.writerows(matrixPosts)



find_all_users()