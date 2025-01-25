import urllib.request as req
import csv
import os
import bs4
os.environ["no_proxy"] = "*"
user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
data = []

def get_page(src_url="string"):
    request = req.Request(src_url, headers = {"Cookie":"over18=1","User-Agent":user_agent})
    with req.urlopen(request) as response:
        page_list = response.read().decode('utf-8')
    root = bs4.BeautifulSoup(page_list,"html.parser")
    articles = root.find_all("div", class_="r-ent")
    page_data = []

    for article in articles:
        title = article.find("div", class_="title")
        if title.a != None:
            like_count_div = article.find("div", class_="nrec")
            like_count = article.find("span", class_="hl") if like_count_div else None
            like_count_value = like_count.string if like_count else "0"
            page_links ="https://www.ptt.cc" + title.a["href"]
            request = req.Request(page_links, headers = {"Cookie":"over18=1","User-Agent":user_agent})
            with req.urlopen(request) as response:
                page_content = response.read().decode('utf-8')
            page_root = bs4.BeautifulSoup(page_content,"html.parser")
            time_meta = page_root.find("span",string="時間") 
            publish_time = ""
            publish_time_elements = time_meta.find_next_sibling("span", class_="article-meta-value") if time_meta else ""
            publish_time = publish_time_elements.string if publish_time_elements else ""
            page_data.append([title.a.string,like_count_value ,publish_time])
    # 先用 page_data 儲存每頁，再反向插入，以處理 PTT 文章每頁倒序問題
    data.insert(0,page_data) 
    previous_page = root.find("a",string="‹ 上頁")
    previous_page_url ="https://www.ptt.cc" + previous_page["href"]
    return previous_page_url

def print_pages(data):
    with open("article.csv","w",encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerows([item for sublist in data for item in sublist])

src_url = "https://www.ptt.cc/bbs/Lottery/index.html"
p = 0
while p < 3:
    src_url = get_page(src_url)
    p+=1

print_pages(data)
