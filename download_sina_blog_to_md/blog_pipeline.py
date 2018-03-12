import codecs

class BlogPipeline(object):
    dir_name = 'blog_md'

    def process_item(self, item, spider):
        file_path = self.dir_name + "/" + item['date'].encode('utf-8').split()[0] + "-" + item['title'].encode('utf-8') + ".md"
        f = codecs.open(file_path, 'w', 'utf8')
        f.write('---\n')
        f.write('layout: post_page\n')
        f.write('title: ' + item['title'] + '\n')
        f.write('date: ' + item['date'] + '\n')
        f.write('categories: ' + item['ctgs'] + '\n')
        f.write('tags: [' + item['tags'] + ']\n')
        f.write('---\n')
        f.write('\n')
    	line = item['content']+'\n'
    	f.write(line)
    	f.close()
        return item
