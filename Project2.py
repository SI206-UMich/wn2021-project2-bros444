from bs4 import BeautifulSoup
import requests
import re
import os
import csv
import unittest


def get_titles_from_search_results(filename):
    """
    Write a function that creates a BeautifulSoup object on "search_results.htm". Parse
    through the object and return a list of tuples containing book titles (as printed on the Goodreads website) 
    and authors in the format given below. Make sure to strip() any newlines from the book titles and author names.

    [('Book title 1', 'Author 1'), ('Book title 2', 'Author 2')...]
    """
    file = open("search_results.htm")
    soup = BeautifulSoup(file,"html.parser")
    titles = soup.find_all('a', class_='bookTitle')
    authors = soup.find_all('span', itemprop='author')
    alist =[]
    tlist=[]
    turbolist = []
    for author in authors:
        elements = [i.get_text().strip("\n") for i in author.select('a')]
        alist.append(str(elements[0]).strip())
    for t in titles:
        tlist.append(t.get_text().strip("\n"))
    for thing in range(len(alist)):
        turbolist.append((tlist[thing],alist[thing]))
    return turbolist
    


def get_search_links():
    """
    Write a function that creates a BeautifulSoup object after retrieving content from
    "https://www.goodreads.com/search?q=fantasy&qid=NwUsLiA2Nc". Parse through the object and return a list of
    URLs for each of the first ten books in the search using the following format:

    ['https://www.goodreads.com/book/show/84136.Fantasy_Lover?from_search=true&from_srp=true&qid=NwUsLiA2Nc&rank=1', ...]

    Notice that you should ONLY add URLs that start with "https://www.goodreads.com/book/show/" to 
    your list, and , and be sure to append the full path to the URL so that the url is in the format 
    “https://www.goodreads.com/book/show/kdkd".

    """
    booklist=[]
    r = requests.get("https://www.goodreads.com/search?q=fantasy&qid=NwUsLiA2Nc")
    soup = BeautifulSoup(r.content,"html.parser")
    for link in soup.find_all('a'):
        booklist.append(link.get("href"))
    regex = r"\/book\/show"
    resultlist=[]
    for book in booklist:
        if type(book) == str:
            results = re.findall(regex,book)
            if results:
                resultlist.append(book)
    results =[]
    for book in resultlist:
        if book not in results:
            results.append(book)
    results2=[]
    for book in results:
        results2.append("https://www.goodreads.com"+book)
    results2 = results2[:10]        
    return results2
    


def get_book_summary(book_url):
    """
    Write a function that creates a BeautifulSoup object that extracts book
    information from a book's webpage, given the URL of the book. Parse through
    the BeautifulSoup object, and capture the book title, book author, and number 
    of pages. This function should return a tuple in the following format:

    ('Some book title', 'the book's author', number of pages)

    HINT: Using BeautifulSoup's find() method may help you here.
    You can easily capture CSS selectors with your browser's inspector window.
    Make sure to strip() any newlines from the book title and number of pages.
    """
    p = requests.get(book_url)
    soup = BeautifulSoup(p.content,"html.parser")
    titles = soup.find('h1', id='bookTitle')
    authors = soup.find('a', class_='authorName')
    pages = soup.find('span', itemprop = "numberOfPages")
    p = (titles.get_text().strip().strip("\n"),authors.get_text().strip("\n"),pages.get_text().strip("\n")) 
    return p

    


def summarize_best_books(filepath):
    """
    Write a function to get a list of categories, book title and URLs from the "BEST BOOKS OF 2020"
    page in "best_books_2020.htm". This function should create a BeautifulSoup object from a 
    filepath and return a list of (category, book title, URL) tuples.
    
    For example, if the best book in category "Fiction" is "The Testaments (The Handmaid's Tale, #2)", with URL
    https://www.goodreads.com/choiceawards/best-fiction-books-2020, then you should append 
    ("Fiction", "The Testaments (The Handmaid's Tale, #2)", "https://www.goodreads.com/choiceawards/best-fiction-books-2020") 
    to your list of tuples.
    """
    f = open(filepath,encoding="utf-8") 
    soup = BeautifulSoup(f,"html.parser")
    c = soup.find_all("h4", class_ ="category__copy")
    g = soup.find_all("img",alt=True,class_="category__winnerImage") 
    regex = r"\/choiceawards\/best-(?!books).+" 
    l=[]
    cat =[]
    title=[]
    for link in soup.find_all('a'):
        try:
            match = re.search(regex,link.get('href'))
            if match and link.get('href') not in l:
                l.append(link.get('href').strip("\n"))
        except:
            pass
    for t in g:
        title.append(t.get("alt").strip("\n"))
    for category in c:
        cat.append(category.text.strip("\n"))
    p = zip(cat,title,l)
    f.close()
    return list(p)



def write_csv(data, filename):
    """
    Write a function that takes in a list of tuples (called data, i.e. the
    one that is returned by get_titles_from_search_results()), writes the data to a 
    csv file, and saves it to the passed filename.

    The first row of the csv should contain "Book Title" and "Author Name", and
    respectively as column headers. For each tuple in data, write a new
    row to the csv, placing each element of the tuple in the correct column.

    When you are done your CSV file should look like this:

    Book title,Author Name
    Book1,Author1
    Book2,Author2
    Book3,Author3
    ......

    This function should not return anything.
    """
    with open(filename, mode='w',newline="") as writingfile:
        writer = csv.writer(writingfile)
        writer.writerow(["Book title","Author Name"])
        for row in data:
            writer.writerow(row)



def extra_credit(filepath):
    """
    EXTRA CREDIT

    Please see the instructions document for more information on how to complete this function.
    You do not have to write test cases for this function.
    """
    regex = r"[A-Z]\S{2,}\s[A-Z]\S+"
    f = open(filepath,encoding="utf-8") 
    soup = BeautifulSoup(f,"html.parser")
    c = soup.find_all("div", id ="description")
    list = []
    for thing in c: 
        list.append(thing.select("span"))
    list.sort(reverse=True)
    theone = str(list[0])
    results = re.findall(regex,theone)
    return results

class TestCases(unittest.TestCase):

    # call get_search_links() and save it to a static variable: search_urls
    search_urls = get_search_links()

    def test_get_titles_from_search_results(self):
        # call get_titles_from_search_results() on search_results.htm and save to a local variable
        local = get_titles_from_search_results("search_results.htm")
        # check that the number of titles extracted is correct (20 titles)
        assert(len(local)==20)
        # check that the variable you saved after calling the function is a list
        assert(type(local)==list)
        # check that each item in the list is a tuple
        for item in local:
            assert(type(item)==tuple)
        # check that the first book and author tuple is correct (open search_results.htm and find it)
        assert(local[0] == ('Harry Potter and the Deathly Hallows (Harry Potter, #7)', 'J.K. Rowling'))
        assert(local[-1] == ('Harry Potter: The Prequel (Harry Potter, #0.5)', 'J.K. Rowling'))
        # check that the last title is correct (open search_results.htm and find it)

    def test_get_search_links(self):
        # check that TestCases.search_urls is a list
        assert(type(TestCases.search_urls)==list)
        # check that the length of TestCases.search_urls is correct (10 URLs)
        assert(len(TestCases.search_urls)==10)

        # check that each URL in the TestCases.search_urls is a string
        for word in TestCases.search_urls:
            assert(type(word)==str)
        # check that each URL contains the correct url for Goodreads.com followed by /book/show/
        for word in TestCases.search_urls:
            assert("https://www.goodreads.com/book/show" in word)
    def test_get_book_summary(self):
        # create a local variable – summaries – a list containing the results from get_book_summary()
        # for each URL in TestCases.search_urls (should be a list of tuples)
        summaries = []
        for link in TestCases.search_urls:
            summaries.append(get_book_summary(link))
        # check that the number of book summaries is correct (10)
        assert(len(summaries)==10)
            # check that each item in the list is a tuple
        for item in summaries:
            assert(type(item)==tuple)
            # check that each tuple has 3 elements
        for item in summaries:
            assert(len(item)==3)
            # check that the first two elements in the tuple are string
        for item in summaries:
            assert(type(item[0]==str))
            assert(type(item[1]==str))
            assert(type(item[2]==int))

        assert(summaries[0][2]=="337 pages")
            # check that the third element in the tuple, i.e. pages is an int

            # check that the first book in the search has 337 pages

    def test_summarize_best_books(self):
        # call summarize_best_books and save it to a variable
        p = summarize_best_books("best_books_2020.htm")
        # check that we have the right number of best books (20)
        print(len(p))
        assert(len(p)==20)
            # assert each item in the list of best books is a tuple
        for book in p:
            assert(type(book)==tuple)
            # check that each tuple has a length of 3
            assert(len(book)==3)
        # check that the first tuple is made up of the following 3 strings:'Fiction', "The Midnight Library", 'https://www.goodreads.com/choiceawards/best-fiction-books-2020'
        assert(p[0] == ('Fiction', "The Midnight Library", 'https://www.goodreads.com/choiceawards/best-fiction-books-2020')) 
        # check that the last tuple is made up of the following 3 strings: 'Picture Books', 'Antiracist Baby', 'https://www.goodreads.com/choiceawards/best-picture-books-2020'
        assert(p[-1] ==('Picture Books', 'Antiracist Baby', 'https://www.goodreads.com/choiceawards/best-picture-books-2020'))
        

    def test_write_csv(self):
        # call get_titles_from_search_results on search_results.htm and save the result to a variable
        v = get_titles_from_search_results("search_results.htm")
        # call write csv on the variable you saved and 'test.csv'
        write_csv(v,"test.csv")
        # read in the csv that you wrote (create a variable csv_lines - a list containing all the lines in the csv you just wrote to above)
        w = open("test.csv")
        csv_lines = w.readlines()
        w.close()
        # check that there are 21 lines in the csv 
        assert(len(csv_lines)==21)
        # check that the header row is correct
        assert(csv_lines[0]== "Book title","Author Name")
        
if __name__ == '__main__':
    #print(extra_credit("extra_credit.htm"))
    unittest.main(verbosity=2)



