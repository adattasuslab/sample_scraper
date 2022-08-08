class Scraper1:
    import warnings
    warnings.filterwarnings('ignore')
    import requests
    from bs4 import BeautifulSoup
    import pandas as pd
    import time
    from selenium import webdriver
    from selenium.webdriver.support.ui import WebDriverWait

    url = "https://quotes.toscrape.com/"
    driver = webdriver.Chrome('drivers/chromedriver.exe')
    max = 21

    driver.get(url)
    df_final = pd.DataFrame()
    count = 1

    while (count < max):
        url = driver.current_url
        driver.get(url)
        result = requests.get(url)

        soup = BeautifulSoup(result.text, 'lxml')
        # quotes
        cases_q = soup.find_all('div', class_='quote')
        quotes = []
        for i in cases_q:
            span = i.find('span')
            quotes.append(span.string)

        df_quotes = pd.DataFrame(data=quotes, columns = ['Quotes'])

        # tags
        cases_t = soup.find_all('div', class_='tags')
        df_tag = pd.DataFrame()
        # columns = ['Tag1','Tag2','Tag3','Tag4','Tag5','Tag6','Tag7','Tag8','Tag9'])
        for i in cases_t:
            list_tag = []
            span = i.find_all('a', class_='tag')
            for j in span:
                list_tag.append(j.string)
            df_tag_p = pd.DataFrame(data=list_tag)
            df_tag = df_tag.append(df_tag_p.transpose())

        df_combined = pd.DataFrame()
        index = pd.Index(range(count, count+len(quotes), 1))
        df_quotes = df_quotes.set_index(index)
        df_tag = df_tag.set_index(index)
        df_combined = pd.concat([df_quotes, df_tag], axis=1)

        # add to final df
        df_final = pd.concat([df_final, df_combined], axis = 0, join = 'outer')

        # to go to next page
        #time.sleep(2)
        count = count + len(quotes)
        element = driver.find_element("xpath", "//li/a[text() = 'Next ']")
        element.click()


    df_final.to_csv('Data.csv')
