#!/usr/bin/env python

# Usage example:
# python database_setup.py --mongodb localhost:27017 --accounts hillsboro newbury

import argparse
import pymongo
from pymongo import MongoClient
import pprint
import os
import json

os.environ.setdefault('SCS_MONGO_URL', 'mongodb://10.127.181.188:31234/?readPreference=primary&appname=MongoDB%20Compass&ssl=false')
MONGODB_REQUIRED = "SCS_MONGO_URL" not in os.environ

def mongoElementCollectionDict(workflowElementCollection):
    elementsDictionary = {}
    resultElements = workflowElementCollection.find()
    for result in resultElements:
        if result.get('_rev'):
            elementsDictionary[result['_id']] = result['_rev']
        else:
            continue
    print("Retrieving Mongo Element Collection")
    return elementsDictionary

def mongoFolderCollectionDict(workflowFolderCollection):
    folderDictionary = {}
    resultFolder = workflowFolderCollection.find()
    for result in resultFolder:
        if result.get('_rev'):
            folderDictionary[result['_id']] = result['_rev']
        else:
            continue
    print("Retrieving Mongo Folder Collection")
    return folderDictionary

def mongoHistoryCollection(workflowHistoryCollection):
    resultHistory = workflowHistoryCollection.find()
    for result in resultHistory:
        historyResult = result['_id']
    print("Retrieving Mongo Folder Collection")
    return historyResult
    

#=======================================================
def createNewElement(info, filename, workflowElementCollection, workflowHistoryCollection):
    workflowElementCollection.insert_one(info)
    workflowHistoryCollection.insert_one({"_id":info['_id'] + '_rev_' + info['_rev'], "value": info})
    print("Creating new Element from file: " + filename)

def updateElement(info, filename, workflowElementCollection, workflowHistoryCollection):
    workflowElementCollection.update({
        '_id': info['_id']
    },
    {
        '$set': info
    }, multi=True)
    workflowHistoryCollection.insert_one({"_id":info['_id'] + '_rev_' + info['_rev'], "value": info})
    print("Updating Element from file: " + filename)

def createNewFolder(info, filename, workflowFolderCollection, workflowHistoryCollection):
    workflowFolderCollection.insert_one(info)
    workflowHistoryCollection.insert_one({"_id":info['_id'] + '_rev_' + info['_rev'], "value": info})
    print("Creating new Folder from file: " + filename)

def updateFolder(info, filename, workflowFolderCollection, workflowHistoryCollection):
    workflowFolderCollection.update({
        '_id': info['_id']
    },
    {
        '$set': info
    }, multi=True)
    workflowHistoryCollection.insert_one({"_id":info['_id'] + '_rev_' + info['_rev'], "value": info})
    print("Updating Folder from file: " + filename)
#=======================================================

def readElement(elementsDictionary, workflowElementCollection, workflowHistoryCollection):
    try:
        print("Calling Read Element function")
        folderDictionary = {}
        for path, dirs, files in os.walk('./library/activities'):
            for f in files:
                filePath = os.path.join(path, f)
                with open(filePath) as json_file:
                    info = json.load(json_file)
                    folderDictionary[info['_id']] = info['_rev']
                    for element in elementsDictionary:
                        if info['_id'] == element:
                            if info['_rev'] == elementsDictionary.get(element):
                                print("Nothing to change in folder: " + f)
                                break
                            else:
                                updateElement(info, f, workflowElementCollection, workflowHistoryCollection)
                                break
                        else:
                            if info['_id'] not in elementsDictionary:
                                createNewElement(info, f, workflowElementCollection, workflowHistoryCollection)
                                break
    except Exception as e:
        print("Exception: " + str(e))



def readFolder(folderDictionary, workflowFolderCollection, workflowHistoryCollection):
    try:
        print("Calling Read Folder function")
        activitiesDictionary = {}
        for path, dirs, files in os.walk('./library/folder'):
            for f in files:
                filePath = os.path.join(path, f)
                with open(filePath) as json_file:
                    info = json.load(json_file)
                    activitiesDictionary[info['_id']] = info['_rev']
                    for folder in folderDictionary:
                        if info['_id'] == folder:
                            if info['_rev'] == folderDictionary.get(folder):
                                print("Nothing to change in activities: " + f)
                                break
                            else:
                                updateFolder(info, f, workflowFolderCollection, workflowHistoryCollection)
                                break
                        else:
                            if info['_id'] not in folderDictionary:
                                createNewFolder(info, f, workflowFolderCollection, workflowHistoryCollection)
                                break
    except Exception as e:
        print("Exception: " + str(e))


def run(client, tenant: str):
    tenant_db = client[tenant]
    workflowFolderCollection = tenant_db["librarygroups"]
    workflowElementCollection = tenant_db["workflowelement"]
    workflowHistoryCollection = tenant_db["historyRev"]

    folderDictionary = mongoFolderCollectionDict(workflowFolderCollection)
    elementsDictionary = mongoElementCollectionDict(workflowElementCollection)
    historyCollection = mongoHistoryCollection(workflowHistoryCollection)

    readFolder(folderDictionary, workflowFolderCollection, workflowHistoryCollection)
    readElement(elementsDictionary, workflowElementCollection, workflowHistoryCollection)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Setup required databases for Workflow Designer"
    )
    parser.add_argument(
        "--mongodb",
        required=MONGODB_REQUIRED,
        help="URL of SCS MongoDB instance (or SCS_MONGODB_URL)",
    )
    parser.add_argument("--accounts", nargs="+", help="Tenant accounts name")
    args = parser.parse_args()

    mongo_db_url = (
        os.environ.get("SCS_MONGO_URL")
        if "SCS_MONGO_URL" in os.environ
        else args.mongodb
    )
    accounts = args.accounts

    print(f"MongoDB: {mongo_db_url}")
    print(f"Database Accounts: {accounts}")

    print("Starting...")
    print("Connecting to Workflow Designer MongoDB")
    client = pymongo.MongoClient(mongo_db_url, connect=True)

    run(client, "jominTest")
    # for tenant in accounts:
    #     run(client, tenant)
    
    
#================================================================================
