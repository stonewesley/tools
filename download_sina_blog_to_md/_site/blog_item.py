from scrapy.item import Item, Field

class BlogItem(Item):
    # define the fields for your item here like:
    # name = Field()
    title = Field() # title
    date = Field()
    tags = Field()
    ctgs = Field()
    content = Field() #content
    image_urls = Field()
    images = Field()
    pass
