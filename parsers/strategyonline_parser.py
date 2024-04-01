import re
import time
import datetime
from bs4 import BeautifulSoup
from tqdm import tqdm
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils.utils import process_data, read_file, load_dict_from_file
from utils.webdriver_config import get_configured_driver


def strategyonline_parser():
    try:
        # Файл для стандартизації назви місяця
        months_file_name = 'months.txt'
        months = load_dict_from_file(months_file_name) 

        excel_path = "parsed_data/strategyonline.xlsx"        
        data = []
        sponsored_added = False
        page = 1
        limit = 15
        parsing_completed = False

        existing_data, existing_titles = read_file(excel_path)
        driver = get_configured_driver()
        
        start_parsing_time = time.time()
        for page in tqdm(range(page, limit + 1), desc="Parsing strategyonline"):
        # for page in range(page, limit+1):
            if parsing_completed:
                break  # Выход из цикла если парсинг завершен

            url = f"https://strategyonline.ca/page/{page}/"
            driver.get(url)
            
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'postTitle')))

            html = driver.page_source
            soup = BeautifulSoup(html, 'html.parser')

            if not soup.title or soup.title.text == "Just a moment...":
                print("Сайт блокує парсинг")
                break

            pattern = re.compile(r'post-\d+ post')
            elements = soup.findAll(class_=pattern)
            for e in elements:
                title = e.find(class_="postTitle").text
                link = e.a.get("href")
                if "days" in e.find(class_="date").text.strip() or "day" in e.find(class_="date").text.strip():
                    days_ago = int(e.find(class_="date").text.strip().split()[0])
                    temp_date = (datetime.date.today() - datetime.timedelta(days=days_ago)).strftime('%d %m %Y').split()
                    temp_date[1] = months.get(temp_date[1].lower())
                    date = " ".join(temp_date) 
                else:
                    temp_date = e.find(class_="date").text.strip().replace(",", "").split()
                    temp_date[0] = months.get(temp_date[0].lower())
                    temp_date[0], temp_date[1] = temp_date[1], temp_date[0]
                    date = " ".join(temp_date)

                if "Sponsored" in e.text:
                    # Если sponsored новость еще не была добавлена, добавляем ее в список данных
                    if not sponsored_added:
                        data.append({
                            "site": "strategyonline.ca",
                            "date": date,
                            "title": title,
                            "link": link,
                        })
                        sponsored_added = True  # Помечаем, что sponsored новость была добавлена
                else:
                    # Для обычных новостей проверяем, добавляли ли мы их ранее, иначе добавляем
                    if title not in existing_titles:
                        data.append({
                            "site": "strategyonline.ca",
                            "date": date,
                            "title": title,
                            "link": link,
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
    strategyonline_parser()
