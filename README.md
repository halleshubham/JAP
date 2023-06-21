# JAP

An automation tool for creating draft posts on Wordpress using Rest API.

## Configuration

### Installing dependencies
Run the setup.py script.

### (When using this for the first time after clonning)

1.  Create a **jap_config.json** file in **JAP_Utilities/JAP_Authentication** folder with following content:

            {

                "client_key": <client key>,

                "client_secret": <client secret>

            }

2.  Run **authorize.py** from **JAP_Utilities/JAP_Authentication** folder and then follow the instructions.
3.  Once done, check the **jap_config.json** again, it should now have **resource_owner_key** and **resource_owner_secret** keys.
4.  Done! You are all set now.

## Creating draft posts

1.  Create **issue_params.json** if not already present in the **root folder** where **create_post.py** is present and update the fields accordingly:

            {

                "summaryfile" : "path/to/summaryfile",

                "articles_folder_path" : "path/to/articles/folder",

                "images_folder_path" : "path/to/images/folder",

                "publish_date" : "YYYY-MM-DD",

                "print_edition_articles" : [<print edition first article number>,<print edition last article number>],

                "blog_edition_articles" : [<blog edition first article number>,<blog edition last article number>]
            }


    Note :

    - **_summaryfile_** : Full path to summary.docx file.
    - **_articles_folder_path_** : Full path to the folder containing only articles files for the current issue.
    - **_images_folder_path_** : Full path to the folder containing only images for the current issue.
    - **_publish_date_** : Issue date in YYYY-MM-DD format

    <br>

    > ### Important:
    >
    > 1. Name of the images should be the article number e.g 1.png/1.jpeg.
    >
    > 2. If runnig the script in Windows machine, **replace '\\' with '/'** in the all the folder/file paths.
    >
    > 3. All **.doc** files should be converted to **.docx** file. This script won't work on **.doc** files.

2.  Run **create_post.py**
