# #!/usr/bin/env python

# # Usage example:
# # python database_setup.py --mongodb localhost:27017 --accounts hillsboro newbury

# import argparse
# import pymongo
# from pymongo import MongoClient
# import pprint
# import os
# import json
# import datetime

# os.environ.setdefault('SCS_MONGO_URL', 'mongodb://10.127.181.188:31234/?readPreference=primary&appname=MongoDB%20Compass&ssl=false')
# MONGODB_REQUIRED = "SCS_MONGO_URL" not in os.environ
# now = datetime.datetime.now()
# dateTimeFormat = now.strftime("%Y-%m-%d %H:%M:%S")

# def mongoElementCollectionDict(workflowElementCollection):
#     try:
#         elementsDictionary = {}
#         resultElements = workflowElementCollection.find()
#         for result in resultElements:
#             if result.get('_rev'):
#                 elementsDictionary[result['_id']] = result['_rev']
#             else:
#                 continue
#         print("Retrieving Mongo Element Collection")
#     except Exception as e:
#         print("Exception: " + str(e))
#     return elementsDictionary

# def mongoFolderCollectionDict(workflowFolderCollection):
#     try:
#         folderDictionary = {}
#         resultFolder = workflowFolderCollection.find()
#         for result in resultFolder:
#             if result.get('_rev'):
#                 folderDictionary[result['_id']] = result['_rev']
#             elif result.get('_rev') is None:
#                 folderDictionary[result['_id']] = 0
#             else:
#                 continue
#         print("\nRetrieving Mongo Folder Collection")
#     except Exception as e:
#         print("Exception: " + str(e))
#     return folderDictionary

# def mongoHistoryCollection(workflowHistoryCollection):
#     resultHistory = workflowHistoryCollection.find()
#     historyResult = ""
#     for result in resultHistory:
#         historyResult = result['_id']
#     print("Retrieving Mongo History Collection")
#     return historyResult
    

# #=======================================================

# ############################
# # MONGO ELEMENT COMMANDS
# ############################
# def createNewElement(info, workflowElementCollection, workflowHistoryCollection):
#     try:
#         workflowElementCollection.insert_one(info)
#         workflowHistoryCollection.insert_one({"_id":info['_id'] + '_rev_' + str(info['_rev']), "value": info, "date": dateTimeFormat})
#     except Exception as e:
#         print("Exception: " + str(e))

# def updateElement(info, workflowElementCollection, workflowHistoryCollection):
#     try:
#         workflowElementCollection.update({
#             '_id': info['_id']
#         },
#         {
#             '$set': info
#         }, multi=True)
#         workflowHistoryCollection.insert_one({"_id":info['_id'] + '_rev_' + str(info['_rev']), "value": info, "date": dateTimeFormat})
#     except Exception as e:
#         print("Exception: " + str(e))

# ############################
# # MONGO FOLDER COMMANDS
# ############################
# def createNewFolder(info, workflowFolderCollection, workflowHistoryCollection):
#     try:
#         workflowFolderCollection.insert_one(info)
#         workflowHistoryCollection.insert_one({"_id":info['_id'] + '_rev_' + str(info['_rev']), "value": info, "date": dateTimeFormat})
#     except Exception as e:
#         print("Exception: " + str(e))

# def updateFolder(info, workflowFolderCollection, workflowHistoryCollection):
#     try:
#         workflowFolderCollection.update({
#             '_id': info['_id']
#         },
#         {
#             '$set': info
#         }, multi=True)
#         workflowHistoryCollection.insert_one({"_id":info['_id'] + '_rev_' + str(info['_rev']), "value": info, "date": dateTimeFormat}) 
#     except Exception as e:
#         print("Exception: " + str(e))
# #=======================================================

# def readElement(elementsDictionary, workflowElementCollection, historyCollection, workflowHistoryCollection):
#     try:
#         print("\nCalling Read Element function")
#         folderDictionary = {}
#         for path, dirs, files in os.walk('./library/activities'):
#             for f in files:
#                 filePath = os.path.join(path, f)
#                 with open(filePath) as json_file:
#                     info = json.load(json_file)
#                     folderDictionary[info['_id']] = info['_rev']
#                     for element in elementsDictionary:
#                         modernHistory = info['_id'] + '_rev_' + str(info['_rev'])
#                         if modernHistory not in historyCollection:
#                             if info['_id'] == element:
#                                 if info['_rev'] == elementsDictionary.get(element):
#                                     print("Nothing to change in element: " + f)
#                                     break
#                                 else:
#                                     updateElement(info, workflowElementCollection, workflowHistoryCollection)
#                                     print("Updating Element from file: " + f)
#                                     break
#                             else:
#                                 if info['_id'] not in elementsDictionary:
#                                     createNewElement(info, workflowElementCollection, workflowHistoryCollection)
#                                     print("Creating new Element from file: " + f)
#                                     break
#                         else:
#                             print("This revision file has already been called : " + f)
#     except Exception as e:
#         print("Exception: " + str(e))



# def readFolder(folderDictionary, workflowFolderCollection, historyCollection, workflowHistoryCollection):
#     try:
#         print("\nCalling Read Folder function")
#         activitiesDictionary = {}
#         for path, dirs, files in os.walk('./library/folders'):
#             for f in files:
#                 filePath = os.path.join(path, f)
#                 with open(filePath) as json_file:
#                     info = json.load(json_file)
#                     activitiesDictionary[info['_id']] = info['_rev']
#                     for folder in folderDictionary:
#                         modernHistory = info['_id'] + '_rev_' + str(info['_rev'])
#                         if modernHistory not in historyCollection:
#                             if info['_id'] == folder:
#                                 if info['_rev'] == folderDictionary.get(folder):
#                                     print("Nothing to change in folder: " + f)
#                                     break
#                                 else:
#                                     for fArray in info['fieldArray']:
#                                         #updateField function
#                                     updateFolder(info,  workflowFolderCollection, workflowHistoryCollection)
#                                     print("Updating Folder from file: " + f)
#                                     break
#                             else:
#                                 if info['_id'] not in folderDictionary:
#                                     createNewFolder(info, workflowFolderCollection, workflowHistoryCollection)
#                                     print("Creating new Folder from file: " + f)
#                                     break
#                         else:
#                             print("This revision file has already been called : " + f)
#                             break

#     except Exception as e:
#         print("Exception: " + str(e))

# #=======================================================

# def run(client, tenant: str):
#     try:
#         tenant_db = client[tenant]
#         workflowFolderCollection = tenant_db["librarygroups"]
#         workflowElementCollection = tenant_db["workflowelement"]
#         workflowHistoryCollection = tenant_db["historyRev"]

#         folderDictionary = mongoFolderCollectionDict(workflowFolderCollection)
#         elementsDictionary = mongoElementCollectionDict(workflowElementCollection)
#         historyCollection = mongoHistoryCollection(workflowHistoryCollection)

#         readFolder(folderDictionary, workflowFolderCollection, historyCollection, workflowHistoryCollection)
#         readElement(elementsDictionary, workflowElementCollection, historyCollection, workflowHistoryCollection)
#     except Exception as e:
#         print("Exception: " + str(e))

# #=======================================================
# if __name__ == "__main__":
#     parser = argparse.ArgumentParser(
#         description="Setup required databases for Workflow Designer"
#     )
#     parser.add_argument(
#         "--mongodb",
#         required=MONGODB_REQUIRED,
#         help="URL of SCS MongoDB instance (or SCS_MONGODB_URL)",
#     )
#     parser.add_argument("--accounts", nargs="+", help="Tenant accounts name")
#     args = parser.parse_args()

#     mongo_db_url = (
#         os.environ.get("SCS_MONGO_URL")
#         if "SCS_MONGO_URL" in os.environ
#         else args.mongodb
#     )
#     accounts = args.accounts

#     print(f"MongoDB: {mongo_db_url}")
#     print(f"Database Accounts: {accounts}")

#     print("Starting...")
#     print("Connecting to Workflow Designer MongoDB")
#     client = pymongo.MongoClient(mongo_db_url, connect=True)

#     run(client, "jominTest")
#     # for tenant in accounts:
#     #     run(client, tenant)
    
    
# #================================================================================
