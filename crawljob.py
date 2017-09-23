from selenium import webdriver
from bs4 import BeautifulSoup as soup


driver = webdriver.Chrome()
driver.get('https://www.glassdoor.com/')
driver.find_element_by_name('sc.keyword').send_keys('Software Intern')
driver.find_element_by_id('LocationSearch').clear()
driver.find_element_by_id('LocationSearch').send_keys('US')
driver.find_element_by_id('HeroSearchButton').click()

# html parsing
html = driver.page_source
page_soup = soup(html, "html.parser")
driver.quit() # close the website

# collect all the containers that contain different jobs
containers = page_soup.findAll("li",{"class":"jl"})
filename = "job.csv"
f = open(filename,"w")
headers = "Title, Company, Location, Salary, Post Date\n"
f.write(headers)
for container in containers:
    flexbox = container.findAll("div",{"class":"flexbox"})
    title = flexbox[0].div.a.text
    #print(title)

    flexboxEmp = container.findAll("div",{"class":"flexbox empLoc"})
    location = flexboxEmp[0].div.span.text.strip()
    company = flexboxEmp[0].div.find(text=True).strip()
    err= flexboxEmp[0].div
    if flexbox[2].div.span:
        salary = flexbox[2].div.span.find('i').previousSibling.strip()
    post_date = flexbox[2].findAll("div")[1].find(text=True).strip()

    f.write(title.replace(",","").replace("-","").replace(":","") + "," + company.replace(",","").replace("–","") + "," + location.replace(",","") + "," + salary.replace(",","") + "," + post_date.replace(",","") + "\n")
f.close()
    #print(err)
    #print(company)
    #print(location)
    #if flexbox[2].div.span:
    #    print(salary)
    #print(post_date)