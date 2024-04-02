import time
import datetime
from tqdm import tqdm
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from utils.utils import process_data, read_file, load_dict_from_file
from utils.webdriver_config import get_configured_driver

def campaignlive_parser():
    try:
        # Файл для стандартизації назви місяця
        months_file_name = 'months.txt'
        months = load_dict_from_file(months_file_name) 
        
        excel_path = "parsed_data/campaignlive.xlsx"        
        data = []

        start_parsing_time = time.time()

        existing_data, existing_titles = read_file(excel_path)
    
        driver = get_configured_driver()
        url = "https://www.campaignlive.co.uk/news"
        driver.get(url)
        
        # Очікування провантаження сторінки (код чекає поки HTML сторінки з'явиться клас із шуканим ім'ям)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'x-large')))

        # Так як інформація на сайті з'являється динамічно, прокручуємо N раз сторінку
        find_element = driver.find_element(By.CLASS_NAME, "x-large")
        action = ActionChains(driver)
        action.move_to_element(find_element).perform()
        time.sleep(2)
        
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')

        if not soup.title or soup.title.text == "Just a moment...":
            print("Сайт блокує парсинг")
            
        elements = soup.find("div", class_="group1").findAll(class_="storyContent clearfix")
        for e in elements:
            title = e.find(class_="contentWrapper contentDetails").find("a", attrs={'title': True})["title"]
            if title not in existing_titles:
                if "days" in e.find(class_="articleDate").text.strip() or "day" in e.find(class_="articleDate").text.strip():
                    days_ago = int(e.find(class_="articleDate").text.strip().split()[0])
                    temp_date = (datetime.date.today() - datetime.timedelta(days=days_ago)).strftime('%d %m %Y').split()
                    temp_date[1] = months.get(temp_date[1].lower())
                    date = " ".join(temp_date) 
                elif "week" in e.find(class_="articleDate").text.strip() or "weeks" in e.find(class_="articleDate").text.strip():
                    days_ago = int(e.find(class_="articleDate").text.strip().split()[0])
                    days_ago *= 7
                    temp_date = (datetime.date.today() - datetime.timedelta(days=days_ago)).strftime('%d %m %Y').split()
                    temp_date[1] = months.get(temp_date[1].lower())
                    date = " ".join(temp_date) 
                elif "hour" in e.find(class_="articleDate").text.strip() or "hours" in e.find(class_="articleDate").text.strip() or "minute" in e.find(class_="articleDate").text.strip()  or "minutes" in e.find(class_="articleDate").text.strip():
                    temp_date = datetime.date.today().strftime('%d %m %Y').split()
                    temp_date[1] = months.get(temp_date[1].lower())
                    date = " ".join(temp_date)   
                else:
                    temp_date = e.find(class_="articleDate").text.strip().replace(",", "").split()
                    temp_date[0] = months.get(temp_date[0].lower())
                    temp_date[0], temp_date[1] = temp_date[1], temp_date[0]
                    date = " ".join(temp_date)
                link = e.find(class_="contentWrapper contentDetails").find("a", attrs={"data-url": True})["data-url"]
                data.append({
                    "site": "campaignlive.co.uk/news",
                    "date": date,
                    "title": title,
                    "link": link,
                })
            else:
                break

        process_data(data, existing_data, excel_path)
        parsing_time = round(time.time()-start_parsing_time)
        print(f"Час парсингу campaignlive_parser: {parsing_time} сек")
    except Exception as e:
        print("Error campaignlive_parser:", e)
    finally:
        driver.close()
        driver.quit()

if __name__ == "__main__":
    campaignlive_parser()