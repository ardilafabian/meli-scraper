# Mercado Libre Scraper

This is a scraper software that retrieve data from the [Mercado Libre](https://listado.mercadolibre.com.ar/celular-smartphones#D[A:celular%20smartphones]) web page, searching by the words _celular smartphones_ and getting information of all the _Samgung_ items that have the **FULL** service.

The program is developed using _Scrapy Framework_ from Python because at the moment is one of the most powerful frameworks to crawl data from webpages using XPath language.

Since I have some experience using Python, this is my first scraper using _Scrapy_ as a scraper framework and in order to accomplish this I had to complete some courses in record time. One of the biggest challenges was to understand how to use all the tools scrappy give me to develop a very efficient and professional piece of code.

## Content table
1. [Installation](#installation)
2. [Usage](#usage)
3. [License](#license)

## Installation

1. The prerequisite is to have Python installed in your machine. The program was developed with python **v.3.10.1** you can use this one or grater versions to assure corrent behavior.
2. You need to download this repository in your machine. You can clone the repository using Git and running the following command:
```
git clone https://github.com/ardilafabian/meli-scraper.git
```
_If you don't have Git you can download the source code by clicking [here](https://github.com/ardilafabian/meli-scraper/archive/refs/heads/main.zip)._

3. Now you have to access to the folder project. It's really recommended to use a python virtual environment to don't get a conflict while installing the project dependencies. You can check the documentation to initialize and activate a virtual environment with python [here](https://docs.python.org/3/library/venv.html).
4. Once you have your virtual environment activated you need to instal the project dependencies running the following command:
```
pip install -r requirements.txt
```
5. Now that you have followed the steps above successfully you are able to use the scraper

## Usage

When you are in the folder you have to run the following command in order to extract the data:
```
scrapy crawl meli
```

By default the algorithm will extract the data of the first 5 list pages, but you can modify this quantity by sending a parameter indicating the number of pages you want to scrap. To do this you need to run the following command:
```
scrapy crawl meli -a pages=<pages_number>
```
Replace ```<pages_number>``` with the number of pages you want.

When the execution has finished you will have two outputs. 
1. One of them is a ```.json``` file called ```items.json```, you will find it in the root folder of the project. This file contains the structure of the items found that accomplish the conditions mentioned [above](#mercado-libre-scraper) and also you will find the attribute ```quantity``` that indicates the number of items found.
> If you run the algorithm more than once, then remember to delete the ```items.json``` file if you don't want to append the new output in the same file
2. The second output is in a MySQL database that lives in Google Cloud and it is going to be populated once you run the algorithm. The data normalized is seen as follow:

![DB Image](https://github.com/ardilafabian/meli-scraper/tree/main/statics/db_output.png?raw=true)

If you are a tech savvy and you already have a MySQL client installed, then you would like to take a quick look at the ~~48 line~~ of this super secret [file](https://github.com/ardilafabian/meli-scraper/blob/main/meli_scraper/pipelines.py).

## Technical (interesting) facts

- This algorithm was thought to be efficient and because of that the strategy is to internally extract only the nodes that accomplish the condition instead of get all nodes and check conditions after.
- The algorithm verify duplicate elements when validate coincidence between item names and prices, this process is done in order to keep data as reliable as possible.
- Before getting the output, the data extracted goes through two pipelines and one of them is in charge of cleanning the numerical data in order to keep the right type of values in our database. This will be useful at the moment of analyse the data directly in our database.

## License
[MIT](https://choosealicense.com/licenses/mit/)
