import time
from selenium import webdriver
from bs4 import BeautifulSoup as soup

# utilize PhantomJS to run browser in the background
#driver = webdriver.PhantomJS('C:/Users/Jia En Chua/PycharmProjects/land_dreamjob/phantomjs.exe')
#driver.set_window_size(1920,1080) # set the window size to avoid error
driver = webdriver.Chrome()
try:
    driver.get('https://www.glassdoor.com/')
except Exception as e:
    driver.save_screenshot('debugjobscrawler.png') # capture error for debugging

job = "Software Intern"
driver.find_element_by_name('sc.keyword').send_keys(job)
driver.find_element_by_id('LocationSearch').clear()
driver.find_element_by_id('LocationSearch').send_keys('US')
driver.find_element_by_id('HeroSearchButton').click()

# html parsing
html = driver.page_source
page_soup = soup(html, "html.parser")
driver.quit() # close the website

# collect all the containers that contain different jobs
containers = page_soup.findAll("li",{"class":"jl"})

# generate spreadsheet
filename = job.replace(" ", "_") + ".csv"
f = open(filename,"w")
headers = "Title, Company, Location, Salary, Post Date\n"
f.write(headers)

for container in containers:
    flexbox = container.findAll("div",{"class":"flexbox"})
    title = flexbox[0].div.a.text

    flexboxEmp = container.findAll("div",{"class":"flexbox empLoc"})
    location = flexboxEmp[0].div.span.text.strip()
    location = flexboxEmp[0].div.span.text.strip()
    company = flexboxEmp[0].div.find(text=True)
    if flexbox[2].div.span:
        salary = flexbox[2].div.span.find('i').previousSibling.strip()
    else:
        salary = "Not provided"
    if flexbox[2].findAll("div")[1].find(text=True):
        post_date = flexbox[2].findAll("div")[1].find(text=True)
    else:
        post_date = "N/A"
    f.write(title.replace(",","").replace("-","").replace(":","") + "," + company.replace(",","").replace("–","") + "," + location.replace(",","") + "," + salary.replace(",","") + "," + post_date + "\n")

f.close()
