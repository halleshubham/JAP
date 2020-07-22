# JAP
An automation tool for creating draft posts on Wordpress using Rest API.

## Configuration 
### (When using this for the first time after clonning) 
1. Create a **jap_config.json** file in **JAP_Authentication** folder  with following content:
 
            {
                 
                "client_key": <client key>,  

                "client_secret": <client secret>
                 
            } 

2. Run **authorize.py** from **JAP_Authentication** folder and then follow the instructions.
3. Once done, check the **jap_config.json** again, it should now have **resource_owner_key** and **resource_owner_secret** keys.
4. Done! You are all set now.


## Creating draft posts
1.  Update following strings in **create_post.py** :
    - ***summaryfile*** : Full path to summary.docx file. 
    - ***articles_folder_path*** : Full path to the folder containing only articles files for the current issue.
    - ***images_folder_path*** : Full path to the folder containing only images for the current issue.  
    - ***publish_date*** : Issue date in YYYY-MM-DD format  

    <br> 

    >
    >
    >### Important:
    >
    >Name of the images should be the article number e.g 1.png/1.jpeg. 
    >
    >If runnig the script in Windows machine, replace '\\' with '/' in the all the folder/file paths.
    > 
    >
2. Run **create_post.py**