import time
from bs4 import BeautifulSoup
from tqdm import tqdm
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils.utils import process_data, read_file, load_dict_from_file
from utils.webdriver_config import get_configured_driver

def insiderintelligence_parser():
    try:
        # Файл для стандартизації назви місяця
        months_file_name = 'months.txt'
        months = load_dict_from_file(months_file_name) 
        excel_path = "parsed_data/insiderintelligence.xlsx"        
        data = []
        page = 1
        limit = 10
        parsing_completed = False

        existing_data, existing_titles = read_file(excel_path)
        driver = get_configured_driver()
        
        start_parsing_time = time.time()
        for page in tqdm(range(page, limit + 1), desc="Parsing insiderintelligence"):
        # for page in range(page, limit+1):
            if parsing_completed:
                break  # Выход из цикла если парсинг завершен

            url = f"https://www.emarketer.com/articles/archive/{page}"
            driver.get(url)
            
            # WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'Content__ContentMiddle-sc-133d3wq-4 JTHCW')))

            html = driver.page_source
            soup = BeautifulSoup(html, 'html.parser')

            if not soup.title or soup.title.text == "Just a moment...":
                print("Сайт блокує парсинг")
                break
           
            elements = soup.findAll(class_="AssetCard__Card-sc-196nwfu-0 gFkhWf")
            for e in elements:
                title = e.find("h2", class_="AssetCard__CardTitle-sc-196nwfu-4 lpvcqB").contents[0].strip()
                if title not in existing_titles:
                    link = e.find(class_="AssetCard__CardTitleLink-sc-196nwfu-3 jpvTSi").get("href")
                    time.sleep(0.8)
                    driver.get(link)    
                    article_html = driver.page_source
                    article_soup = BeautifulSoup(article_html, "html.parser")
                    temp_date = article_soup.find(class_="Headerstyles__ArticleDate-sc-8w2n0v-7 evMHyr spec_article_date").text.replace(",", "").split()
                    temp_date[0] = months.get(temp_date[0].lower())
                    temp_date[0], temp_date[1] = temp_date[1], temp_date[0]
                    date = " ".join(temp_date)
                    data.append({
                        "site": "insiderintelligence.com/articles",
                        "date": date,
                        "title": title,
                        "link": link,
                    })
                else:
                    parsing_completed = True
                    break
            time.sleep(5)
            page += 1
        

        process_data(data, existing_data, excel_path)
        parsing_time = round(time.time()-start_parsing_time)
        print(f"Час парсингу: {parsing_time} сек")
    except Exception as e:
        print("Error:", e)
    finally:
        driver.close()
        driver.quit()



if __name__ == "__main__":
    insiderintelligence_parser()