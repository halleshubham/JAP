# JAP

An automation tool for creating and publishing posts on WordPress using the REST API. Supports automated compilation of HTML newsletter emails, WhatsApp messages, and Facebook post scheduling.

## Dependencies

```bash
pip install python-docx mammoth beautifulsoup4 awesome-slugify Pillow unidecode requests
```

Or run the setup script:

```bash
python setup.py
```

## Configuration

### 1. Create `jap_config.json`

Copy the sample and fill in your credentials:

```bash
cp article_publishing/Configs/jap_config.sample.json article_publishing/Configs/jap_config.json
```

Edit `jap_config.json`:

```json
{
    "wp_username": "your-wordpress-email@example.com",
    "wp_app_password": "xxxx xxxx xxxx xxxx xxxx xxxx",
    "google_api_key": "<google_api_key>",
    "google_project_cx": "<search_engine_ID>"
}
```

**`wp_app_password`** is a WordPress Application Password (not your login password). To generate one:
1. Go to WordPress Admin → Users → Profile
2. Scroll to **Application Passwords**
3. Enter a name (e.g. "JAP Script") and click **Add New Application Password**
4. Copy the generated password (spaces are fine, include them)

To verify your credentials work:

```bash
python test_auth.py
```

### 2. Create `issue_params.json`

The file is at `article_publishing/Configs/issue_params.json`. Update it for each issue:

```json
{
    "summaryfile": "/path/to/Summary.docx",
    "articles_folder_path": "/path/to/articles/folder/",
    "images_folder_path": "/path/to/images/folder/",
    "publish_date": "YYYY-MM-DD",
    "volume_number": "80",
    "issue_number": "9",
    "print_edition_articles": [0, 0],
    "blog_edition_articles": [1, 27],
    "article_categories": {
        "1": [521, 2029, 59],
        "2": [521, 2029, 7]
    }
}
```

**Field notes:**

| Field | Description |
|---|---|
| `summaryfile` | Full path to the issue's `Summary.docx` |
| `articles_folder_path` | Folder containing **only** the numbered article `.docx` files |
| `images_folder_path` | Folder containing images named `1.jpg`, `2.jpg`, … `N.jpg` |
| `publish_date` | Issue date in `YYYY-MM-DD` format |
| `print_edition_articles` | `[first, last]` article numbers for the print edition (`[0,0]` if none) |
| `blog_edition_articles` | `[first, last]` article numbers for the online blog |
| `article_categories` | *(optional)* Per-article category ID arrays (max 3). Falls back to `521` (Online Blog) if omitted |

**Important:**
- Article files in `articles_folder_path` must be named starting with the article number followed by a dash, e.g. `1-article-title.docx`.
- Image files must be named by article number: `1.jpg`, `2.jpg`, etc.
- All `.doc` files must be converted to `.docx` — the script does not support `.doc`.
- On Windows, use forward slashes `/` in all paths.

## Running the scripts

All scripts must be run from the **project root** (`JAP/`), not from a subdirectory.

### Create draft posts

```bash
python article_publishing/create_post.py
```

This will:
1. Parse the summary file for titles, authors, and excerpts
2. Create/find WordPress author accounts
3. Upload and optimise article images
4. Convert each `.docx` to HTML and create a draft post with the correct publish timestamp, category, and featured image

Posts are timestamped in reverse article order (article 1 gets the latest minute, article N gets the earliest) so they appear in correct sequence on the site.

### Generate newsletter and WhatsApp messages

```bash
python "article_publishing/generate_whatsapp_posts_ and_newsletter.py"
```

Outputs:
- `Newsletter.html` — HTML email newsletter
- WhatsApp message text for Janata, Lokayat, and Abhivyakti channels

### Utility scripts

| Script | Purpose |
|---|---|
| `test_auth.py` | Verify WordPress Application Password credentials |
| `replace_images.py` | Bulk-replace post featured images (e.g. from Wikimedia Commons) |
| `revert_images.py` | Revert featured images back to the original article images |

## WordPress category IDs (janataweekly.org)

| Category | ID |
|---|---|
| Online Blog | 521 |
| Indian Politics | 2029 |
| World Politics | 11 |
| Economy | 6 |
| Fascism | 7 |
| USA | 1996 |
| China | 2031 |
| Communalism | 59 |
| Caste | 2032 |
| Gender Issues | 1932 |
| Climate Change | 9 |
| Culture | 13 |
| People's Movements | 2033 |
| Socialism | 10 |
| Press Release | 1927 |
| Print Issue | 669 |
