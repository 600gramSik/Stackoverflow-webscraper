import requests
from bs4 import BeautifulSoup
LIMIT=50
URL = f"https://kr.indeed.com/%EC%B7%A8%EC%97%85?q=python&limit={LIMIT}"

def get_last_pages():
  result = requests.get(URL)
  soup = BeautifulSoup(result.text,"html.parser") 
  pagination = soup.find("ul", {"class":"pagination-list"})
  links = pagination("li") 
  pages=[]
  for link in links[:-1]:
    pages.append(int(link.string))
  max_page = pages[-1]
  return max_page

def extract_job(html):
  title = html.find("h2", {"class":"jobTitle"}, {"class":"jobTitle jobTitle-newJob"}).find("span", title=True).text
  company = html.find("span", {"class":"companyName"}).find("a", {"class":"companyOverviewLink"}).text
  location = html.find("div",{"class":"companyLocation"}).text
  #job_id = html["data-jk"]
  
  print ({"title":title, "company":company, "location":location})
  
def extract_jobs(last_page):
  jobs=[]
  for page in range(last_page):
    print(f"Scrapping Indeed : Page {page}")
    result=requests.get(f"{URL}&start={page*LIMIT}")
    soup = BeautifulSoup(result.text,"html.parser")
    results=soup("div",{"class":"tapItem"})
    for result in results:
      job = extract_job(result)
      jobs.append(job)
  return jobs

def get_jobs():
  last_page = get_last_pages()
  jobs = extract_jobs(last_page)
  return jobs