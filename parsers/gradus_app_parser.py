import time
from tqdm import tqdm
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from utils.utils import process_data, read_file, load_dict_from_file
from utils.webdriver_config import get_configured_driver

def gradus_app_parser():
    try:
        # Файл для стандартизації назви місяця
        months_file_name = 'months.txt'
        months = load_dict_from_file(months_file_name) 
        
        excel_path = "parsed_data/gradus_app.xlsx"        
        data = []

        start_parsing_time = time.time()

        existing_data, existing_titles = read_file(excel_path)
    
        driver = get_configured_driver(False)
        url = "https://gradus.app/uk/open-reports/"
        driver.get(url)
        
        # Очікування провантаження сторінки (код чекає поки HTML сторінки з'явиться клас із шуканим ім'ям)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'reports__list-item')))

        # Так як інформація на сайті з'являється динамічно, прокручуємо N раз сторінку
        find_element = driver.find_element(By.CLASS_NAME, "footer")
        # for _ in tqdm(range(1, 11), desc="Parsing gradus_app"):
        for _ in range(1, 11):
            action = ActionChains(driver)
            action.move_to_element(find_element).perform()
            time.sleep(1)
        
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')

        if not soup.title or soup.title.text == "Just a moment...":
            print("Сайт блокує парсинг")

        elements = soup.find("ul", class_="reports__list").findAll("li", class_="reports__list-item")
        
        for e in elements:
            title = e.find(class_="reports__list-item__details__title").text
            temp_date = e.find(class_="reports__list-item__details__date").text.split()
            temp_date[0] = months.get(temp_date[0].lower())
            date = " ".join(temp_date)
            link = url[:-17] + e.find(class_="reports__list-item__link").get("href")
            if title not in existing_titles:
                data.append({
                    "site": "gradus.app/uk/open-reports",
                    "date": date,
                    "title": title,
                    "link": link,
                })
            else:
                break

        process_data(data, existing_data, excel_path)
        parsing_time = round(time.time()-start_parsing_time)
        print(f"Час парсингу: {parsing_time} сек")
    except Exception as e:
        print("Error:", e)
    finally:
        driver.close()
        driver.quit()

if __name__ == "__main__":
    gradus_app_parser()