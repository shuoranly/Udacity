# -*- coding: utf-8 -*-
"""
@file  : DoubanCrawler.py
@brief : Select your three favorite categories from the douban.com web page and collect the names, 
         ratings, links to movie pages and links to movie posters from various regions.
         Get what is the percentage of the top three of each movie category that you have chosen, 
         and what percentage of the total number of films in this category.
@author: Idego
@date  : Dec 13 2017
"""
from selenium import webdriver
from bs4 import BeautifulSoup
import time
import csv

class Movie:
    """Represents a movie.
    
    Attributes:
        name: A string representing the movie name.
        rate: A floating number representing the movie rating. 
        location: A string representing the movie area.
        category: A string representing category of movies.
        info_link: A string representing movie page link.
        cover_link: A string representing movie poster picture link.
    """
    
    def __init__(self, name, rate, location, category, info_link, cover_link):
        """Initializes the data."""
        self.name = name
        self.rate = rate
        self.location = location
        self.category = category
        self.info_link = info_link
        self.cover_link = cover_link

def getMovieUrl(category, location):
    """Get the url with the given category and location.
    
    Args:
        category: A string representing category of movies.
        location: A string representing the movie area.
            
    Returns:
        A string which include the given category and location.
    """
    url = "https://movie.douban.com/tag/\#/?sort=S&range=9,10&tags=电影,{},{}".format(category, location)
    
    return url

def getHtml(url, loadmore = False, waittime = 2):
    """Get the html from the url.
    
    Args:
        url: A string representing a douban page url we will get html from.
        loadmore: A boolean representing whether or not click load more on the bottom.
        waittime: An integer count of the seconds the broswer will wait after intial load.
        
    Returns:
        A string include the whole html content.
    """
    browser = webdriver.Chrome('chromedriver')
    browser.get(url)
    time.sleep(waittime)
    if loadmore:
        while True:
            try:
                next_button = browser.find_element_by_class_name("more")
                next_button.click()
                time.sleep(waittime)
            except:
                break
    html = browser.page_source
    browser.quit()
    return html
              
def getMovies(category, location):
    """Get a list of Movie objects with the given category and location.
    
    Args:
        category: A string representing category of movies.
        location: A string representing the movie area.
        
    Returns:
        A list of Movie objects.
    """
    url = getMovieUrl(category, location)
    html = getHtml(url, loadmore = True, waittime = 2)
    soup = BeautifulSoup(html, "html.parser")
    content_div_list = soup.find_all("div", class_="list-wp")
    content_div = content_div_list[0]
    Movie_Obj_list = []
    for tag in content_div("a"):
        tag_span = tag.p.find_all('span')
        name = tag_span[0].get_text()
        rate = tag_span[1].get_text()
        info_link = tag['href']
        cover_link = tag.img['src']
        Movie_Obj = Movie(name, rate, location, category, info_link, cover_link)
        Movie_Obj_list.append(Movie_Obj)
        
    return Movie_Obj_list

def getAllLocation():
    """Get the all location.
    """
    all_location_url = "https://movie.douban.com/tag/#/?sort=S&range=9,10&tags=电影,剧情"
    html = getHtml(all_location_url, loadmore = False, waittime = 2)
    soup = BeautifulSoup(html, "html.parser")
    locationList=[]
    for child in soup.find(class_='tags').find(class_='category').next_sibling.next_sibling:
        location=child.find(class_='tag').get_text()
        if location!='全部地区':
            locationList.append(location)
    
    return locationList

def getMovieInfoTable():
    """Write movie Info Table to "movies.csv".
    
    Choose your favorite three film type, and then for every region of the film information.
    We can obtain a list of objects which contains three types, all regions, film scores more 
    than 9 points, then write it to the file list "movies.csv".
    """
    #爱情，动作，青春
    category_list = ["爱情", "动作", "青春"]
    #location
    location_list = getAllLocation()
    #Get a list of complete movie objects with three types, all regions, which rate is more than 9 points. 
    All_Movie_Obj_list = []
    for category in category_list:
        for location in location_list:
            per_Movie_Obj_list = getMovies(category, location)
            for per_Movie_Obj in per_Movie_Obj_list:
                All_Movie_Obj_list.append(per_Movie_Obj)

    #write All_Movie_Obj_list to "movies.csv"
    f = open("movies.csv", "w", encoding='utf-8')
    writer = csv.writer(f)
    for element in All_Movie_Obj_list:
        context_list = [element.name, element.rate, element.info_link, element.cover_link]
        writer.writerow(context_list)
    f.close()
    

def getFilmData():
    """Write movie related data to "output.txt".
    
    Get what is the percentage of the top three of each movie category that you have chosen, 
    and what percentage of the total number of films in this category.
    """
    category_list = ["爱情", "动作", "青春"]
    location_list = getAllLocation()
    #count_dict={category:{location:count}}
    count_dict = dict()
    temp_dict = dict()
    #sum_dict={category:sum}
    sum_dict = dict()
    for i in range(3):
        sum_count = 0
        temp_dict = {}
        for location in location_list:
            per_Movie_Obj_list = getMovies(category_list[i], location)
            temp_dict[location] = temp_dict.get(location, 0) + len(per_Movie_Obj_list)
            count_dict[category_list[i]] = temp_dict
            sum_count += len(per_Movie_Obj_list)
        sum_dict[category_list[i]] = sum_count
    #sort top three place of per category and write the related data into "output.txt".
    f = open("output.txt", "w", encoding='utf-8')
    for key in count_dict:
        temp = count_dict[key]
        sort_list = sorted(temp.items(), key=lambda d:d[1], reverse=True)
        sort_list = sort_list[:3]
        f.write(key)
        f.write(":\n")
        f.write("The top three location: {}, {}, {}\n".format(sort_list[0][0], sort_list[1][0], sort_list[2][0]))
        #Percentage of the total number of films in this category.
        per1 = (sort_list[0][1] / sum_dict[key]) * 100
        per2 = (sort_list[1][1] / sum_dict[key]) * 100
        per3 = (sort_list[2][1] / sum_dict[key]) * 100
        f.write("Percentage of the total number of films in this category: {}, {}, {}\n".format('%.2f'%per1, '%.2f'%per2, '%.2f'%per3))
    f.close
   
#main entry of function
def main():
    getMovieInfoTable()
    getFilmData()
    
if __name__ == "__main__":
    main()
    


       




    




    
        
        
            

