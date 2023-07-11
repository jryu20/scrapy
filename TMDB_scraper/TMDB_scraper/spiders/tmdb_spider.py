# to run 
# scrapy crawl tmdb_spider -o movies.csv

import scrapy

class TmdbSpider(scrapy.Spider):
    name = 'tmdb_spider'
    
    start_urls = ['https://www.themoviedb.org/tv/2316-the-office/']
    
    def parse(self, response):
        """
        directs to the cast page given the starting tv/movie site
        """
        
        yield scrapy.Request("https://www.themoviedb.org/tv/2316-the-office/cast", callback = self.parse_full_credits)
        
    def parse_full_credits(self,response): 
        """
        goes through each actor in the cast page 
        """
     
        actors_list = response.css('ol.people.credits:not(.crew) a::attr(href)').getall()
        for actor in actors_list:
            yield response.follow(actor, callback = self.parse_actor_page)
            
    def parse_actor_page(self, response):
        """
        parses through each actor and creates a dictionary containing movies/shows the actor has been in
        """
        
        actor_name = response.css("h2 a::text").get()
        for movie_or_TV_name in response.css("div.credits_list bdi::text").getall():
            yield {
                "actor": actor_name,
                "movie_or_TV_name": movie_or_TV_name
            }