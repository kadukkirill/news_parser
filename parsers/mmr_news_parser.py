import time
from bs4 import BeautifulSoup
from tqdm import tqdm
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils.utils import process_data, read_file
from utils.webdriver_config import get_configured_driver



def mmr_news_parser():
    try:
        excel_path = "parsed_data/mmr_news.xlsx"        
        data = []
        page = 1
        limit = 15

        existing_data, existing_titles = read_file(excel_path)
        driver = get_configured_driver(disable_javascript=False, headless=False)
        parsing_completed = False
        
        start_parsing_time = time.time()

        # for page in tqdm(range(page, limit + 1), desc="Parsing mmr_news"):
        for page in range(page, limit+1):
            if parsing_completed:
                break  # Выход из цикла если парсинг завершен

            url = f"https://mmr.ua/news/page/{page}"
            driver.get(url)
            
            WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, 'def-article')))

            html = driver.page_source
            soup = BeautifulSoup(html, 'html.parser')

            if not soup.title or soup.title.text == "Just a moment...":
                print("Сайт блокує парсинг")
                break

            elements = soup.findAll(class_="def-article")
            
            for e in elements:
                title = e.find(class_="def-article__title").text.strip()
                if title not in existing_titles:
                    data.append({
                        "site": "mmr.ua/news",
                        "date": e.find(class_="def-article__date").text.strip(),
                        "title": title,
                        "link": e.find(class_="def-article__title-inner").get("href"),
                    })
                else:
                    parsing_completed = True
                    break
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
    mmr_news_parser()