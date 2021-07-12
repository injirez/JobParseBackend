from celery import shared_task
from .models import Jobs

from selenium import webdriver
import time
from selenium.webdriver import ActionChains


@shared_task
def addTest():
    chromedriver = '/Users/rodionibragimov/Documents/jobparseBackend/chromedriver'
    # options.add_argument('headless')  # для открытия headless-браузера

    options = webdriver.ChromeOptions()
    bot = webdriver.Chrome(executable_path=chromedriver)
    bot.get('https://facultetus.ru/jobfinder')
    bot.maximize_window()
    time.sleep(3)

    j = 1
    count = 25

    bot.execute_script("choseSelfSpec()")
    time.sleep(3)
    element = bot.find_element_by_xpath("/html/body/div[2]/div/div[2]/div/div/div[2]")
    bot.execute_script("arguments[0].click();", element)
    time.sleep(3)
    bot.execute_script("setChosenSpecs()")
    time.sleep(2)

    for i in range(30):
        btn = bot.find_element_by_xpath("//*[@id='loadmorebutton']/button")
        actions = ActionChains(bot)

        while (j < count):
            bot.execute_script("arguments[0].click();", bot.find_element_by_xpath(
                "/html/body/div[3]/div[3]/div[2]/div[2]/div[{}]/div[1]/div/div[2]/h1/span".format(j + 1)))
            time.sleep(3)

            title = bot.find_element_by_xpath("/html/body/div[2]/div/div[2]/div/div[1]/h3")

            city = bot.find_element_by_class_name("geocitydata")

            img = bot.find_element_by_xpath("/html/body/div[2]/div/div[2]/div/div[3]/div/div[1]/img")

            company = bot.find_element_by_xpath("/html/body/div[2]/div/div[2]/div/div[2]/div/div[2]/h1")

            vacLink = bot.find_element_by_xpath("/html/body/div[2]/div/div[2]/div/p/input")

            try:
                salary = bot.find_element_by_xpath("/html/body/div[2]/div/div[2]/div/div[1]/h4").text.split("\n")
                salary = salary[1].replace('руб/мес', '').split()
                if salary[2] == '-':
                    salaryFrom = salary[0] + salary[1]
                    salaryTo = salary[3] + salary[4]
                else:
                    salaryFrom = salary[0] + salary[1]
                    salaryTo = salaryFrom
            except:
                salaryFrom = 0
                salaryTo = 0

            # print(title.text)
            # print(company.text)
            # print(city.text)
            # print(salaryFrom)
            # print(salaryTo)
            # print(img.get_attribute('src'))
            # print(vacLink.get_attribute('value'))
            # print('\n')
            newObject = Jobs.objects.create(title=title.text, city=city.text, image=img.get_attribute('src'),
                                            siteName='Факультетус', vacLink=vacLink.get_attribute('value'),
                                            salaryFrom=salaryFrom, salaryTo=salaryTo, currency='₽',
                                            companyName=company.text
                                            )

            bot.execute_script("arguments[0].click();",
                               bot.find_element_by_xpath("/html/body/div[2]/div/div[1]/table/tbody/tr/td[2]/img"))
            time.sleep(5)

            j += 1

        # print('\n')
        time.sleep(1)
        bot.execute_script("loadJobs({0})".format(count))
        count += 25
        time.sleep(10)

    return newObject.title, newObject.siteName, newObject.siteLink
