#!/usr/bin/env python

# Usage example:
# python database_setup.py --mongodb localhost:27017 --accounts hillsboro newbury

import argparse
import pymongo
from pymongo import MongoClient
import pprint
import os
import uuid
import json

os.environ.setdefault('SCS_MONGO_URL', 'mongodb+srv://admin:admin@cluster0.9ygx5.mongodb.net/')
#os.environ.setdefault('SCS_MONGO_URL', 'mongodb://10.127.181.197:27017/admin?readPreference=primary&appname=MongoDB%20Compass&ssl=false')
MONGODB_REQUIRED = "SCS_MONGO_URL" not in os.environ

def mongoElementCollectionDict(workflowElementCollection):
    try:
        elementsDictionary = {}
        resultElements = workflowElementCollection.find()
        for result in resultElements:
            if result.get('_rev'):
                elementsDictionary[result['_id']] = result['_rev']
            else:
                continue
        print("Retrieving Mongo Element Collection")
    except Exception as e:
        print("Exception in 'mongoElementCollectionDict' function: " + str(e))
    return elementsDictionary

def mongoFolderCollectionDict(workflowFolderCollection):
    try:
        folderDictionary = {}
        resultFolder = workflowFolderCollection.find()
        for result in resultFolder:
            if result.get('_rev'):
                folderDictionary[result['_id']] = result['_rev']
            elif result.get('_rev') is None:
                folderDictionary[result['_id']] = 0
            else:
                continue
        print("\nRetrieving Mongo Folder Collection")
    except Exception as e:
        print("Exception in 'mongoFolderCollectionDict' function: " + str(e))
    return folderDictionary
#========================================================================================================================
############################
# MONGO FIELDS/PARAMETERS COMMANDS
############################
def createIndex(workflowBrickCollection):
    try:
        workflowBrickCollection.create_index([("$**", "text")], name='TextIndex', default_language='english')
        print("Index Created")
    except Exception as e:
        print("Exception in 'createIndex' function: " + str(e))

############################
# MONGO ELEMENT COMMANDS
############################
def createNewElement(info, workflowElementCollection):
    try:
        workflowElementCollection.insert_one(info)
        print("Activity Created")
    except Exception as e:
        print("Exception in 'createNewElement' function: " + str(e))

def getElement(id, workflowCollection):
    try:
        result = workflowCollection.find( {"_id": id} )
        print("\nRetrieving Mongo Folder Collection")
    except Exception as e:
        print("Exception in 'mongoFolderCollectionDict' function: " + str(e))
    return result

############################
# MONGO BRICK COMMANDS
############################

def getBrickByElementId(id, workflowCollection):
    try:
        result = workflowCollection.find( {'elementId': id} )
        print("\nRetrieving Mongo Folder Collection")
    except Exception as e:
        print("Exception in 'mongoFolderCollectionDict' function: " + str(e))
    return result

############################
# MONGO FOLDER COMMANDS
############################
def createNewFolder(info, workflowFolderCollection):
    try:
        workflowFolderCollection.insert_one(info)
        print("Folder Created")
    except Exception as e:
        print("Exception in 'createNewFolder' function: " + str(e))

############################
# MONGO FIELDS/PARAMETERS COMMANDS
############################

def bricksExtraParam(array, workflowBrickCollection):
    try:
        array.get('value')["brickId"] = ""
        array.get('value')["addNewItem"] = False
        array.get('value')["editable"] = True
        array.get('value')["shouldRender"] = True
        array.get('value').pop('elementId')
        array.get('value').pop('webService')
    except Exception as e:
        print("Exception in 'bricksExtraParam' function: " + str(e))
    return array

def bricksExtraPorts(array, workflowBrickCollection):
    try:
            array.get('value')["portId"] = uuid.uuid4().hex
            array.get('value')["disabled"] = False
            array.get('value')["links"] = []
    except Exception as e:
        print("Exception in 'bricksExtraPorts' function: " + str(e))
    return array

def actionFields(array):
    try:
        if 'type' not in array:
            array['type'] = array.get('name')
        if 'label' not in array:
            array['label'] = array.get('name')
        if 'subType' not in array:
            array['subType'] = '...'
        if 'function' not in array:
            array['function'] = '...'
        if 'groupId' not in array:
            array['groupId'] = " "
        if 'caption' not in array:
            array['caption'] = " "
        if 'isStartNode' not in array:
            array['isStartNode'] = False
        if 'bgColor' not in array:
            array['bgColor'] = '0xe4e4e4'
        if 'webserviceValidator' not in array:
            array['webserviceValidator'] = None
        if 'canAddPorts' not in array:
            array['canAddPorts'] = False
        if 'headerColor' not in array:
            array['headerColor'] = '0x181F6D'
        if 'icon' not in array:
            array['icon'] = './icons/3rd/gv.png'
        if 'deletable' not in array:
            array['deletable'] = False
        if 'deleted' not in array:
            array['deleted'] = False
        if 'fromElementId' not in array:
            array['fromElementId'] = None    
        if 'parameters' not in array:
            array['parameters'] = []
        if 'ports' not in array:
            array['ports'] = []
    except Exception as e:
        print("Exception in 'actionFields' function: " + str(e))
    return array

def actionParameter(array):
    try:
        for parameter in array:
            if 'elementId' not in parameter:
                parameter['elementId'] = None
            if 'isVisible' not in parameter:
                parameter['isVisible'] = True
            if 'webService' not in parameter:
                parameter['webService'] = None
            if 'value' not in parameter:
                parameter['value'] = None
            if 'ordernum' not in parameter:
                parameter['ordernum'] = 0
    except Exception as e:
        print("Exception in 'actionParameter' function: " + str(e))
    return array


def actionPort(array):
    try:
        for port in array:
            if 'mutable' not in port:
                port['mutable'] = False
            if 'ordernum' not in port:
                port['ordernum'] = 0
    except Exception as e:
        print("Exception in 'actionPort' function: " + str(e))
    return array
#####################################################################################

############################
# MONGO FIELDS/PARAMETERS COMMANDS
############################

def updateField(id, fArray, revision, workflowCollection, workflowBrickCollection):
    try:
        fArray =  {k.lower(): v for k, v in fArray.items()}
        if fArray.get('action') == "add" or fArray.get('action') == "update":
            workflowCollection.update_many({
            '_id': id
            },
            {
                '$set': {
                    fArray['targetkey'] : fArray['value'],
                    "_rev": revision
                }
            })
            if workflowBrickCollection is not None:
                workflowBrickCollection.update_many({
                'elementId': id
                },
                {
                    '$set': {
                        fArray['targetkey'] : fArray['value'],
                    }
                })
            if fArray.get('action') == "add":
                print("Field Added")
            if fArray.get('action') == "update":
                print("Field Updated")
        elif fArray.get('action') == "delete":
            if fArray.get('targetkey') is None:
                print("Delete action cannot delete without empty field key")
                return
            if fArray.get('value') is None:
                fArray['value'] = ''
            workflowCollection.update_many({
            '_id': id
            },
            {
                '$unset': {
                    fArray['targetkey']:""
                },
                '$set': {
                        "_rev": revision
                }
            })
            if workflowBrickCollection is not None:
                workflowBrickCollection.update_many({
                'elementId': id
                },
                {
                    '$unset': {
                        fArray['targetkey']:""
                    }
                })
            print("Field Deleted")
    except Exception as e:
        print("Exception in 'updateField' function: " + str(e))

def updateParameterOrPort(id, pArray, revision, updatePfunctions, workflowCollection, workflowBrickCollection):
    try:
        pArray =  {k.lower(): v for k, v in pArray.items()}
        specificElementCollection = getElement(id, workflowCollection)
        specificBrickCollection = getBrickByElementId(id, workflowBrickCollection)

        resultCollection, resultBCollection, portsResultColl = [], [], []
        paramResultColl = {}
        for result in specificElementCollection:
            resultCollection = result
        for result in specificBrickCollection:
            resultBCollection.append(result)

        for paramResult in resultCollection['parameters']:
            paramResultColl[paramResult['label']] = paramResult['type']
        for portsResult in resultCollection['ports']:
            portsResultColl.append(portsResult['label'])
        


        if pArray.get('action') == "add": #ADD Parameter/Port
            if pArray.get('value').get('label') is None:
                print("Unable to add " + updatePfunctions + " without label")
                return
            if updatePfunctions == "parameters":
                if pArray.get('value').get('type') is None:
                    print("Unable to add " + updatePfunctions + " without type")
                    return
                if pArray.get('value').get('label') in paramResultColl and paramResultColl.get(pArray.get('value').get('label')) == pArray.get('value').get('type'): # Avoid adding parameter label with already added ones
                    print("Unable to add " + updatePfunctions + " due to label already being saved")
                    return
            if updatePfunctions == "ports":
                if pArray.get('value').get('label') in portsResultColl: # Avoid adding ports label with already added ones
                    print("Unable to add " + updatePfunctions + " due to label already being saved")
                    return
            

            # setting ELEMENT UPDATE
            workflowCollection.update_many({ 
            '_id': id
            },
            {
                '$set': {
                        "_rev": revision
                },
                '$push': {
                    updatePfunctions: pArray['value'] # instead of curly braces under pArray
                }
            })
            bricksExP = bricksExtraPorts(pArray, workflowBrickCollection)
            if updatePfunctions == "parameters":
                updatePfunctions = "param"
                bricksExP = bricksExtraParam(pArray, workflowBrickCollection)
            
            # setting BRICKS UPDATE JOMIN
            #for document in workflowBrickCollection.find({"keyword":{"$regex":'^[0-9]', "$options":'i'}}):
            for document in workflowBrickCollection.find({'elementId': id, 'deleted': False}):
                bricksExP['value']['brickId'] = document['_id']
                workflowBrickCollection.update_one({
                    'elementId': id,
                    'deleted': False
                    },
                    {
                        '$push': {
                            updatePfunctions: bricksExP['value']
                        }
                    })
            print(updatePfunctions + " Added")

        elif pArray.get('action')== "update": #UPDATE Parameter/Port by name
            # setting ELEMENT UPDATE
            workflowCollection.update_many({
            '_id': id,
            updatePfunctions: {
                "$elemMatch" : {"label" : pArray['label']}
                }
            },
            {
                '$set': {
                    updatePfunctions + ".$." + pArray['targetkey']: pArray['value'],
                    "_rev": revision
                }
            })

            # setting BRICK UPDATE
            if updatePfunctions == "parameters":
                updatePfunctions = "param"
            workflowBrickCollection.update_many({
            'elementId': id,
            'deleted': False,
            updatePfunctions: {
                "$elemMatch" : {"label" : pArray['label']}
                }
            },
            {
                '$set': {
                    updatePfunctions + ".$." + pArray['targetkey']: pArray['value']
                }
            })
            print(updatePfunctions + " field Updated")

        elif pArray.get('action') == "delete": # Delete action
            if pArray.get('label') is None:
                print("Unable to delete " + updatePfunctions + " without label")
                return
            if pArray.get('value') is None:
                pArray['value'] = ''
            
            for resultBrick in resultBCollection:
                if resultBrick.get('ports'):
                    for eachPorts in resultBrick.get('ports'):
                        if pArray.get('label') == eachPorts.get('label'):
                            if eachPorts.get('links'):
                                print("\nUnable to delete port due to link already in placed in brick: " + resultBrick.get('name'))
                                return


            # setting ELEMENT UPDATE
            workflowCollection.update_many({
            '_id': id
            },
            {
                '$set': {
                        "_rev": revision
                },
                '$pull': {
                    updatePfunctions: {
                        "label": pArray['label']
                    }
                }
            })

            # setting BRICK UPDATE
            if updatePfunctions == "parameters":
                updatePfunctions = "param"
            workflowBrickCollection.update_many({
            'elementId': id,
            'deleted': False
            },
            {
                '$pull': {
                    updatePfunctions: {
                        "label": pArray['label']
                    }
                }
            })
            print(updatePfunctions + " Deleted")

    except Exception as e:
        print("Exception in 'updateParameterOrPort' function: " + str(e))

def deleteDocument(guid, workflowCollection):
    try:
        workflowCollection.update_one(
            {
                "_id": guid
            },
            {
                '$set': {
                    'deleted': True
                }
            }
        )
        print("Document Deleted")
    except Exception as e:
        print("Exception in 'addOrUpdateHistory' function: " + str(e))

#========================================================================================================================

def readElement(elementsDictionary, workflowElementCollection, workflowBrickCollection):
    try:
        print("\nCalling Read Element function")
        folderDictionary = {}
        updatePfunctions = ""
        for path, dirs, files in os.walk('./library/activities'):
            for f in files:
                filePath = os.path.join(path, f)
                if (f.split('_rev_')[0] == f):
                    print("\nUnable to process further with this filename: " + f + " Due to spaces between '_rev_'. \nAs unable to seperate ID and revision.")
                else: 
                    print(f)
                    guid = f.split('_rev_')[0]
                    revision = f.split('_rev_')[1].replace('.json','')
                    with open(filePath) as json_file:
                        info = json.load(json_file)
                        folderDictionary[guid] = revision
                        if guid not in elementsDictionary:
                            if '_id' in info:
                                print("\nCreating new Activity from file: " + f + ":-")
                                createNewElement(info, workflowElementCollection)
                            else:
                                print("\n_id is not present in "+ f + " to create Activity")
                        elif bool(elementsDictionary):
                            for element in elementsDictionary:
                                if guid == element:
                                    if revision == elementsDictionary.get(element):
                                        print("Nothing to change in element: " + f)
                                    else:
                                        if '_id' not in info:
                                            if info.get('fields'): # root fields
                                                print("\nUpdating Field actions in: " + f + ":-") 
                                                for fArray in info['fields']:
                                                    updateField(guid, fArray, revision, workflowElementCollection, workflowBrickCollection)
                                            if info.get('parameters'): # parameter arrays
                                                print("\nUpdating Parameter actions in: " + f + ":-")
                                                updatePfunctions = "parameters"
                                                for pArray in info['parameters']:
                                                    updateParameterOrPort(guid, pArray, revision, updatePfunctions, workflowElementCollection, workflowBrickCollection)
                                            if info.get('ports'):
                                                print("\nUpdating Port actions in: " + f + ":-")
                                                updatePfunctions = "ports" # port arrays
                                                for pArray in info['ports']:
                                                    updateParameterOrPort(guid, pArray, revision, updatePfunctions, workflowElementCollection, workflowBrickCollection)
                                            if info == {"action":"delete"}: # delete document
                                                print("\nDeleting document in: " + f + ":-")
                                                deleteDocument(guid, workflowElementCollection)
                            
    except Exception as e:
        print("Exception: " + str(e))

def readFolder(folderDictionary, workflowFolderCollection):
    try:
        print("\nCalling Read Folder function")
        activitiesDictionary = {}
        for path, dirs, files in os.walk('./library/folders'):
            for f in files:
                filePath = os.path.join(path, f)
                if (f.split('_rev_')[0] == f):
                    print("\nUnable to process further with this filename: " + f + " Due to spaces between '_rev_'. \nAs unable to seperate ID and revision.")
                else: 
                    guid = f.split('_rev_')[0]
                    revision = f.split('_rev_')[1].replace('.json','')
                    with open(filePath) as json_file:
                        info = json.load(json_file)
                        activitiesDictionary[guid] = revision
                        if guid not in folderDictionary:
                            if '_id' in info:
                                print("\nCreating new Folder from file: " + f + ":-")
                                createNewFolder(info, workflowFolderCollection)
                            else:
                                print("\n_id is not present in "+ f + " to create Folder")
                        elif bool(folderDictionary):
                            for folder in folderDictionary:
                                if guid == folder:
                                    if revision == folderDictionary.get(folder):
                                        print("\nNothing to change in folder: " + f)
                                    else:
                                        if '_id' not in info:
                                            if info.get('fields'): # root fields
                                                print("\nUpdating Field actions in: " + f + ":-") 
                                                for fArray in info['fields']:
                                                    updateField(guid, fArray, revision, workflowFolderCollection, None)
                                            if info == {"action":"delete"}: # delete document
                                                print("\nDeleting document in: " + f + ":-")
                                                deleteDocument(guid, workflowFolderCollection)
                            
    except Exception as e:
        print("Exception: " + str(e))



#========================================================================================================================


def run(client, tenant: str):
    try:
        tenant_db = client[tenant]
        workflowFolderCollection = tenant_db["librarygroups"]
        workflowElementCollection = tenant_db["workflowelement"]
        workflowBrickCollection = tenant_db["bricks"]

        folderDictionary = mongoFolderCollectionDict(workflowFolderCollection)
        elementsDictionary = mongoElementCollectionDict(workflowElementCollection)

        readFolder(folderDictionary, workflowFolderCollection)
        readElement(elementsDictionary, workflowElementCollection, workflowBrickCollection)

        createIndex(workflowBrickCollection)
    except Exception as e:
        print("Exception: " + str(e))

#=======================================================
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

    run(client, "romstr1")
    # for tenant in accounts:
    #     run(client, tenant)
    
    