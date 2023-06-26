import time
import requests
from selenium import webdriver 
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from JAP_Utilities.summary_parser import get_general_summary
from JAP_Utilities.params_parser import get_params
from PIL import Image
import io, base64
from multiprocessing import Pool, cpu_count
import datetime as dt


def download_image(args):
    (url, count) = args
    try:
        if url.startswith("data:"):
            imgdata = url.split('base64,')[1]
            image_from_web = Image.open(io.BytesIO(base64.decodebytes(bytes(imgdata, "utf-8")))).convert("RGB")
        else:
            headers = {
                            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'
                        }
            response = requests.get(url, stream = True, headers= headers)
            image_from_web = Image.open(response.raw).convert("RGB")
        image_from_web.save(params['images_folder_path'] +str(count)+'.jpg', 'jpeg')
        print('Image saved successfully!')
            
    except Exception as e:
        print(e, 'Image Couldn\'t be retreived\n')

def get_image_url(args):
    (search_text, image_number) = args
    options = Options()
    options.add_argument('--headless=new')
    driver = webdriver.Chrome(options=options)
    driver.get('https://www.google.com/imghp')

    # get the image source
    searchTextbox = driver.find_element("xpath",'//*[@title="Search"]')   
    searchTextbox.send_keys(search_text)
    searchButton = WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH,'//*[@aria-label="Google Search"]')))
    searchButton.click()

    try:
        img = WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="islrg"]/div[1]/div[1]/a[1]/div[1]/img')))
        img.click()

    except Exception as e:
        driver.close() 
        return { 'url' : '', 'image_number': image_number}

    #time.sleep(10)

    try: 
        imageBiggerSize = WebDriverWait(driver,20).until(EC.presence_of_element_located((By.XPATH,'//*[@id="Sva75c"]/div[2]/div/div[2]/div[2]/div[2]/c-wiz/div/div/div/div[3]/div[1]/a/img[1]')))
    except Exception as e:
        print (e)
        img = WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH,'/html/body/div[2]/c-wiz/div[3]/div[1]/div/div/div/div/div[1]/div[1]/div[1]/a[1]/div[1]/img')))
        img.click()
        imageBiggerSize = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH,'//*[@id="Sva75c"]/div/div/div[3]/div[2]/c-wiz/div/div[1]/div[1]/div/div[2]/a/img')))

    url = imageBiggerSize.get_attribute("src")
    driver.close()  
    print('url returned for: ', str(image_number))
    return { 'url' : url, 'image_number': image_number}

def getImages(summary):

    # download the image
    total_download_payload = []
    total_get_url_payload = []
    for i in range(0,len(summary["titles"])):
        searchAuthor = summary["authors"][i]
        if (';' in searchAuthor):
            searchAuthor = searchAuthor.split(';',1)
            searchAuthor = searchAuthor[0]
        if (',' in searchAuthor):
            searchAuthor = searchAuthor.split(',',1)
            searchAuthor = searchAuthor[0]

        searchTitle = summary["titles"][i]
        if ('Two' in searchTitle):
            searchTitle = searchTitle.split('Two',1)
            searchTitle = searchTitle[0]
      
        search_text = searchTitle + " " + searchAuthor
        total_get_url_payload.append((search_text, i+1))
    with Pool(cpu_count()-2) as pool:
            urls_results = pool.map(get_image_url, total_get_url_payload)

    for result in urls_results:
        if result['url'] != '':
            total_download_payload.append((result['url'], result['image_number'])) 

    with Pool() as pool:
        results = pool.map(download_image, total_download_payload)

    return total_download_payload

params = get_params()
summary = get_general_summary(params['summaryfile'])

if __name__=='__main__':
    start_time = dt.datetime.now()
    a = getImages(summary)
    end_time = dt.datetime.now()
    print('Time taken to download the images: '+str((end_time - start_time).seconds)+ ' seconds.')