import time
from bs4 import BeautifulSoup
from tqdm import tqdm
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils.utils import process_data, read_file, load_dict_from_file
from utils.webdriver_config import get_configured_driver


def mix_digital_news_parser_ua():
    try:
        months_file_name = 'months.txt'
        months = load_dict_from_file(months_file_name)
        
        excel_path = "parsed_data/mix_digital_news_ua.xlsx"        
        data = []
        page = 1
        limit = 10
        parsing_completed = False

        existing_data, existing_titles = read_file(excel_path)
        driver = get_configured_driver()
        
        start_parsing_time = time.time()

        # for page in tqdm(range(page, limit + 1), desc="Parsing mix_digital_news_ua"):
        for page in range(page, limit+1):
            if parsing_completed:
                break  # Выход из цикла если парсинг завершен
            
            url = f"https://mixdigital.com.ua/blog/category/news-ua/page/{page}/"
            driver.get(url)
            
            try:
                WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, "mix-hot-post")))
            except:
                break
                
            html = driver.page_source
            soup = BeautifulSoup(html, 'html.parser')

            if not soup.title or soup.title.text == "Just a moment...":
                print("Сайт блокує парсинг")
                break

            # на сторінці присутні 6 новин + 1 головна новина в окремому боксі
            # main_element відповідає за головну новину
            main_element = soup.find(class_="mix-hot-post-content")

            title = main_element.find(class_="mix-hot-post-title").a.text
            if title not in existing_titles:
                link = main_element.find(class_="mix-hot-post-title").a.get("href")
                temp_date = main_element.find(class_="mix-hot-post-date").text.replace(",", "").split()
                # в replace відбувається заміна англійської і на українську і(для коду вони різні)
                temp_date[1] = months.get(temp_date[1].lower().replace("i", "і")) 
                date = " ".join(temp_date)
            
                data.append({
                    "site": "mixdigital.com.ua/blog/category/news-ua/",
                    "date": date,
                    "title": title,
                    "link": link,
                })
            else:
                parsing_completed = True
                break


            elements = soup.findAll(class_="col-xl-4 col-lg-4 col-md-6 col-sm-6")
            for e in elements:
                title = e.find(class_="mix-post-box-title").text
                if title not in existing_titles:
                    link = e.find(class_="mix-post-box-title").a.get("href")
                    temp_date = e.find(class_="mix-post-box-date").text.replace(",", "").split()
                    temp_date[1] = months.get(temp_date[1].lower().replace("i", "і"))
                    date = " ".join(temp_date)
                    data.append({
                        "site": "mixdigital.com.ua/ru/blog/category/news",
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
        print(f"Час парсингу mix_digital_news_parser_ua: {parsing_time} сек")
    except Exception as e:
        print("Error mix_digital_news_parser_ua:", e)
    finally:
        driver.close()
        driver.quit()


if __name__ == "__main__":
    mix_digital_news_parser_ua()
