import time
from tqdm import tqdm
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementClickInterceptedException
from utils.utils import process_data, read_file, load_dict_from_file
from utils.webdriver_config import get_configured_driver

def blog_uamaster_analytics():
    try:
        # Файл для стандартизації назви місяця
        months_file_name = 'months.txt'
        months = load_dict_from_file(months_file_name) 
        
        excel_path = "parsed_data/blog_uamaster_analytics.xlsx"        
        data = []

        start_parsing_time = time.time()

        existing_data, existing_titles = read_file(excel_path)
    
        driver = get_configured_driver(disable_javascript=False)
        url = "https://blog.uamaster.com/category/analytics/"
        driver.get(url)
        
        # Очікування провантаження сторінки (код чекає поки HTML сторінки з'явиться клас із шуканим ім'ям)
        try:
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'card')))
        except:
            print("loading error")
            
        # for _ in tqdm(range(5), desc="Parsing blog_uamaster_analytics"):
        for i in range(5):
            try:
                button_more = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.ID, "btn-more")))
                button_more.click()
                time.sleep(3)  # Даем время для подгрузки контента и возможного появления модального окна
            except ElementClickInterceptedException:
                close_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, ".mc-closeModal")))
                close_button.click()
                time.sleep(1.5)  # Даем время для закрытия модального окна
                button_more.click()  # Попробуем еще раз нажать на кнопку после закрытия модального окна

        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')

        if not soup.title or soup.title.text == "Just a moment...":
            print("Сайт блокує парсинг")

        elements = soup.find(class_="cards-list isotope-grid cards-list-mobile").findAll("a", class_="card")
        for e in elements:
            title = e.find(class_="card__text").text
            if title not in existing_titles:
                temp_date = e.find(class_="card__title").text.replace(".", " ").split()
                temp_date[1] = months.get(temp_date[1].lower())
                date = " ".join(temp_date)
                link = e.get("href")
                data.append({
                    "site": "blog.uamaster.com/category/analytics",
                    "date": date,
                    "title": title,
                    "link": link,
                })
            else:
                break

        process_data(data, existing_data, excel_path)
        parsing_time = round(time.time()-start_parsing_time)
        print(f"Час парсингу blog_uamaster_analytics: {parsing_time} сек")
    except Exception as e:
        print("Error blog_uamaster_analytics:", e)
    finally:
        driver.close()
        driver.quit()

if __name__ == "__main__":
    blog_uamaster_analytics()