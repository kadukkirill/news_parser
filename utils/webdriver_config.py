from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def get_configured_driver(disable_javascript=True):
    chrome_options = Options()
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument("--headless")  # Запуск в headless режиме
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36")
    chrome_options.add_argument("--disable-gpu")  # Отключает GPU hardware acceleration
    chrome_options.add_argument("--disable-images")  # Отключает загрузку изображений
    chrome_options.add_argument("--disable-extensions")  # Отключает расширения
    chrome_options.add_argument("--no-sandbox")  # Отключает режим песочницы
    chrome_options.add_argument("--log-level=3")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])

    #Отключает выполнение JavaScript на странице. Если на странице данные подгружаются динамически, эту строчку отключить
    if disable_javascript:
        chrome_options.add_experimental_option("prefs", {"profile.managed_default_content_settings.javascript": 2})


    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option("useAutomationExtension", False)

    driver = webdriver.Chrome(options=chrome_options)

    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument",{
        "source": """
        delete window.cdc_adoQpoasnfa76pfcZLmcfl_Array;
        delete window.cdc_adoQpoasnfa76pfcZLmcfl_JSON;
        delete window.cdc_adoQpoasnfa76pfcZLmcfl_Object;
        delete window.cdc_adoQpoasnfa76pfcZLmcfl_Promise;
        delete window.cdc_adoQpoasnfa76pfcZLmcfl_Proxy;
        delete window.cdc_adoQpoasnfa76pfcZLmcfl_Symbol;
    """  
    })

    return driver
