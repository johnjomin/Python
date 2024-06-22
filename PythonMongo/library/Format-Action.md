## **This file is used to define how to write up format for python script to initialize library in workflow designer.**
\
&nbsp;
The document should be renamed as:
"<activity_Id/folder_Id>_rev_<revision no.>.json"

* In which replace <...> with actual value. An example of this could be: *11afac1778c1d14d2177103596003bb0_rev_1.json*
* Where this refers to the document id that it is being targeted (fixed value) and revision that is being changed from time to time (value to be changed after each revision).
\
&nbsp;

The basic format of either adding/updating/deleting fields is:
```
{
    "fields":[    ],
    "parameters":[   ],
    "ports":[    ]
}
```
\
&nbsp;
In each list, we can have *multiple actions* for example:
```
"fields":[
    {
        <!--- action 1 --->
    },
    {
        <!--- action 2 --->
    }
    {
         <!--- action x --->
    }
]
```
\
&nbsp;
The action format for *fields* are:
```
{
    "targetKey": "Key name",
    "action": "add",
    "value": "Diva Activity"
}
```
\
&nbsp;
The action format for *parameters/ports* are:
```
{
    "label": "Parameter 1"
    "targetKey": "caption",
    "action": "add",
    "value": "Diva Activity"
}
```

&nbsp;
1. **"action"**: the actions are _add_, _update_, _delete_
2. **"targetKey"**: if action is "add" then it refers to the field key and 'value' to be added
    * if action is 'update' then it refers to the key in which 'value' to be changed
    * if action is 'delete' then it refers to the key to be deleted. Its up to the user whether to add value or not. But *recommended* not to include the value.
3. **"label"**: this line is **ONLY** to be added in either *parameters or ports* action in which 'label' refers to the key of parameter in which actions needs to take ie add field line in parameter, update/change value, delete a field in parameter etc
4. **"value"**: refers to the 'value' to be either add or update value
\
\
\
&nbsp;
## **_NOTE:-_**
* If document contains only:
```
{
    "action": "delete"
}
```
This refers to the document to be deleted as a _whole_
\
\
\
If you would like to implement or overwrite json for library, then ignore format action and simply add respective json file ie 
* Activity json:
```
{
    "_id": "sample-activity-Id",
    "name": "Sample Activity",
    "type": "Sample Activity",
    "label": "Sample Activity",
    "_rev": "1",
    "groupId": "sample-folder-Id"
    ...
}
```
&nbsp;
* Folder json:
```
{
    "_id": "sample-folder-Id",
    "label": "Sample Folder",
    "_rev": 1
}
```
In which the script automatically picks up document containing **'_id'** and add either create/overwrite json
\
\
\
&nbsp;
## **_Example's of Format Document_**
If you navigate through scripts/database_setup/library/template-json/, you will find example of template json located under this directory. The example of these json files are:-

**_Note:_** Since comments are not allowed in json file, comments in this section can be found as '//' to define better what each key and value does in formatting document. 

&nbsp;
* 1. fields.json
```
{
    "fields" : [{
        "targetKey": "caption", // Define the key to be added from 'action' field
        "action": "add", // Defines the action
        "value" : "New Activity" // The value which is to be added

        // Result of this action is adding field of 'caption' to the value of 'New Activity': 
        {
            "caption": "New Activity"
        }
    },

    {
        "targetKey": "caption", // Define the key to be target to change the value
        "action": "update",
        "value" : "Modified Activity" // New value to be changed

        // Result of this action is updating field of 'caption' to the new value of 'Modified Activity': 
        {
            "caption": "Modified Activity"
        }
    },

    {
        "targetKey": "caption", // Defines the key to a target field/key in which to be deleted
        "action": "delete"

        // Result of this action is deleting field of 'caption': 
    }]
}
```
&nbsp;
* 2. parameter.json
```
{
    "parameters" : [{
        "action": "add", // Defines the action in which parameter to be added
        "value" : { // The value contains json format of newly parameter to be created
                "elementId": null,
                "label": "Workflow Name",
                "type": "string",
                "isVisible": true,
                "webService": null,
                "value": "John's Workflow",
                "ordernum": 0
        }

        //result of this action is adding parameter of label 'Workflow Name': 
    },

    {
        "label": "Workflow Name", // Since there can be multiple parameters under Activity, in order to target specific key, label field is added to target specific Parameter
        "targetKey": "value", // Define the key to be target to change the value
        "action": "update", 
        "value" : "Mike's Workflow" // New value to be changed

        // Result of this action is updating specific parameter in which in this case is 'Workflow Name' parameter and changing value of targetkey: 
        {
            "value": "Mike's Workflow"
        }

        // In which the old value when it was added was "John's Workflow"
    },

    {
        "label": "Mike's Workflow", // To target specific Parameter
        "action": "delete"

        // Result of this action is deleting specific parameter named "Mike's Workflow"
    }]
}
```
&nbsp;
* 2. ports.json
```
{
    "ports" : [{
        "action": "add", // Defines the action in which port to be added
        "value" : { // The value contains json format of newly port to be created
            "label": "Maybe",
            "mutable": false,
            "ordernum": 0
        }
    },

    {
        "label": "Maybe", // Since there can be multiple port under Activity, in order to target specific key, label field is added to target specific Port
        "targetKey": "mutable", // Define the key to be target to change the value
        "action": "update",
        "value" : true // New value to be changed

        // Result of this action is updating specific port in which in this case is 'Maybe' port and changing value of targetkey: 
        {
            "mutable": true
        }

        // In which the old value when it was added was "false"
    },
    {
        "label": "Never", // To target specific Port
        "action": "delete"

        // Result of this action is deleting specific port named "Maybe"
    }]
}
```
&nbsp;
* 2. fields-param-port.json
```
// This example is showed of how fields, parameters and ports comes together if user would like to edit different section from each parts.

// Though key thing to remember is if you are to add more than one section ie fields, parameters and/or ports then add them under brackets "[]"

// If you would like to understand what each actions do for each array then example of this are shown under 1. fields.json, 2. parameter.json and 3. ports.json

{
        "fields" : [{
            "targetKey": "caption",
            "action": "add",
            "value" : "New Activity"
        },
        {
            "targetKey": "caption",
            "action": "update",
            "value" : "Modified Activity"
        },
        {
            "targetKey": "caption",
            "action": "delete"
        }],

    "parameters" : [{
        "action": "add",
        "value" : {
                "elementId": null,
                "label": "Workflow Name",
                "type": "string",
                "isVisible": true,
                "webService": null,
                "value": "John's Workflow",
                "ordernum": 0
        }
    },
    {
        "label": "Workflow Name",
        "targetKey": "label",
        "action": "update",
        "value" : "Mike's Workflow"
    },
    {
        "label": "Mike's Workflow",
        "action": "delete"
    }],

    "ports" : [{
        "action": "add",
        "value" : {
            "label": "Maybe",
            "mutable": false,
            "ordernum": 0
        }
    },
    {
        "label": "Maybe",
        "targetKey": "label",
        "action": "update",
        "value" : "Never"
    },
    {
        "label": "Never",
        "action": "delete"
    }]
}
```
&nbsp;
* 2. delete-document.json
```
// This format document has been explained under "NOTE:-" subsection

{
    "action": "delete"
}

// Result: Where if you were to add only this format action then script will delete document based on fileId and updated revision.

// Else it would ignore if revision has been called before or if anything else is added in this document.
```
&nbsp;