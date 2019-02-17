import requests
from bs4 import BeautifulSoup
import re
import os

def get_url():
	"""得到所有的url存入urls.txt"""
	for page in range(1,231):
		page_url = 'https://bmcgenomics.biomedcentral.com/articles?page=' + str(page)
		soup_results = bp_url(page_url)
		for soup_result in soup_results:
			url = 'https://bmcgenomics.biomedcentral.com' + soup_result.get('href')
			print(url)
			with open('text/urls.txt', 'a') as f:
				 		f.write(url+'\n')


def get_content():
	"""得到文章内容并以年份存入文件"""
	with open('text/urls.txt', 'r') as urls:
		for url in urls:
			if '*' not in url:
				print('........................................................')
				print('正在获取：' + url)

				#获取文章年份
				year = year_article(url.strip())
				#只爬取2005到2018
				if int(str(year)) < 2005:
					print("------------已经爬取了所有内容-----------------")
					os._exit(0)

				contents = bp_article(url.strip())
				for content in contents:		
					print(content.get_text())


					# 将内容写入文件
					with open('text/' + str(year)+'.txt', 'a') as f:
					 	f.write(content.get_text())

				#用*标记爬完的url
				mark_url(url)		



def bp_article(url):
	"""匹配文章内容"""
	try:
		response = requests.get(url,timeout=20)
		#打印状态码
		print(response.status_code)
	except Exception as e:
		get_content()
	else:
		soup = BeautifulSoup(response.text,'lxml')
		results = soup.find_all(name='div',attrs={'class':'FulltextWrapper'})
		soup_p = BeautifulSoup(str(results), 'lxml')
		p_results = soup_p.find_all('p')
		return p_results

def bp_url(url):
	"""获取每篇文章的链接"""
	response = requests.get(url)
	soup = BeautifulSoup(response.text,'lxml')
	soup_results = soup.find_all(name='a',attrs={'data-track-action':'Click Fulltext'})
	return soup_results

def year_article(url):
	"""取出每篇文章的出版的年份"""
	year = ''
	try:
		response = requests.get(url)
	except Exception as e:
		get_content()
	else:
		soup = BeautifulSoup(response.text,'lxml')
		soup_results = soup.find_all(name='span',attrs={'itemprop':'datePublished'})
		for soup_result in soup_results:
			year = soup_result.get_text()
		#获取years里的数字
		years = re.findall(r'\d*',year)

		#匹配出年份
		for year in years:
			if len(year) > 0:
				if int(str(year)) > 50:
					return year


def mark_url(url):
	"""
	mark_url函数用来标记已经读取了内容的url,如果出现爬取中断，
	可以从未被标记的地方爬去，不用重新爬
	"""
	url_edit = ''
	with open('text/urls.txt', 'r+') as f:
		for line in f:
			if line==url:
				line = '*' + line
			url_edit = url_edit + line
	with open('text/urls.txt', 'r+') as f:
		f.writelines(url_edit)

def make_file():
	"""创建2005.txt到2018.txt的文件,用来存储爬去的文章"""
	for i in range(2005,2019):
		with open('text/' + str(i) + '.txt','w') as f:
			f.close


def make_dir():
	try:
		os.mkdir('text')
	except FileExistsError:
		print("text文件夹已经存在，请删除后再运行,或者注释掉make_dir()函数")
		os._exit(0)

def main():
	#创建text文件夹
	##get_url()
	#创建文件存储内容
	#make_file()
	#匹配文章内容存入文件
	get_content()


if __name__ == '__main__':
    main()

