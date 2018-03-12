# coding=utf-8
import os
from os import system
from scrapy.spiders import Spider
from scrapy.http import Request
from scrapy.crawler import CrawlerProcess
import codecs
from blog_item import BlogItem
import hashlib


class DownloadSinaBlogToMdSpider(Spider):
  name = "dsbtm"
  start_urls = []
  prefix = "http://blog.sina.com.cn/s/articlelist_1685464333_0_"
  suffix = ".html"

  def __init__(self, *args, **kwargs):
    super(DownloadSinaBlogToMdSpider, self).__init__(*args, **kwargs)
    for i in (1,2):
        self.start_urls.append(self.prefix + str(i) + self.suffix)
    dir_name = 'blog_md'
    if not os.path.isdir(dir_name):
        os.mkdir(dir_name)

  def parse(self, response):
    artical_list = response.xpath('//span[@class="atc_title"]/a/@href')
    file_path = 'artcical_url.txt'
    f = codecs.open(file_path, 'w', 'utf8')

    for index, artical_url in enumerate(artical_list):
        url = artical_url.extract()
        print url
        yield Request(url, callback=self.parse_post)
#        break

  def parse_post(self, response):
      title = response.xpath('//h2[@class="titName SG_txta"]/text()').extract()[0]
      print "title: " + title
      date = response.xpath('//span[@class="time SG_txtc"]/text()').extract()[0]
      date = date[1 : len(date)-1]
      print "date: " + date
      tags_list = response.xpath('//td[@class="blog_tag"]/h3/a/text()').extract()
      tags = ','.join(tags_list)
      print "tags: " + tags
      ctgs = response.xpath('//td[@class="blog_class"]/a/text()').extract()[0]
      print "ctgs: " + ctgs
      item = BlogItem()
      item['title'] = title
      item['date'] = date
      item['tags'] = tags
      item['ctgs'] = ctgs
      content_list = response.xpath('//div[@class="articalContent   newfont_family"]/div/p')
      if len(content_list) != 0:
          return self.newfont_proc(item, content_list)
      content_list = response.xpath('//div[@class="articalContent   "]/child::*')
      if len(content_list) != 0:
          return self.oldfont_proc(item, content_list)

  def oldfont_proc(self, item, content_list):
      content = ''
      image_urls = []
      for index, p in enumerate(content_list):
          p_f = p.xpath('text()').extract()
          p_img = p.xpath('div/a/img/@real_src').extract()
          if len(p_f) != 0:
              content  += ''.join(p_f) + '\n'
          if len(p_img) != 0:
              image_urls.append(p_img[0])
              content  += '![](/imgs/' + hashlib.sha1(p_img[0]).hexdigest() + '.jpg)\n'
      #print content
      item['content'] = content
      item['image_urls'] = image_urls
      yield item

  def newfont_proc(self, item, content_list):
      content = ''
      image_urls = []
      for index, p in enumerate(content_list):
          p_f = p.xpath('./descendant::*/text()').extract()
          p_img = p.xpath('a/img/@real_src').extract()
          if len(p_f) != 0:
              content  += ''.join(p_f) + '\n\n'
          if len(p_img) != 0:
              image_urls.append(p_img[0])
              content  += '![](/imgs/' + hashlib.sha1(p_img[0]).hexdigest() + '.jpg)\n'
      #print content
      item['content'] = content
      item['image_urls'] = image_urls
      yield item

