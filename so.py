import requests
from bs4 import BeautifulSoup
URL = f"https://stackoverflow.com/jobs/companies?q=python"

def get_last_page():
  result=requests.get(URL)
  soup = BeautifulSoup(result.text, "html.parser")
  pages = soup.find("div", {"class":"s-pagination"})("a")
  last_page = pages[-2].get_text(strip=True)
  return int(last_page)

def extract_job(html):
  title = html.find("h2", {"class":"fs-body2 mb4"}).find("a", {"class":"s-link"}).text
  location_company = html.find("div", {"class":"d-flex gs12 gsx ff-row-wrap fs-body1"}).get_text(strip = "\n")
  job_id = html.find("h2", {"class":"fs-body2 mb4"}).find("a")["href"]
  return {'title':title, 'location&company' : location_company, "link":f"https://stackoverflow.com/{job_id}"}



def extract_jobs(last_page):
  jobs=[]
  for page in range(last_page):
    print(f"Scrapping SO : Page {page}")
    result=requests.get(f"{URL}&pg={page+1}")
    soup=BeautifulSoup(result.text, "html.parser")
    results = soup("div", {"class":"flex--item fl1 text mb0"})
    for result in results:
      job= extract_job(result)
      jobs.append(job)
  return jobs

def get_jobs():
  last_page = get_last_page()
  jobs = extract_jobs(last_page)
  return jobs
  