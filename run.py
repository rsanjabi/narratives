from gather.scrape_lists import ListScraper 
from gather.scrape_work import PageScraper
import yaml

try:
    with open('config.yaml', 'r') as file:
        config = yaml.safe_load(file)
except Exception as e:
    print('Error reading yaml configuration file.')

#works = ListScraper(config)
#works.scrape()

page = PageScraper(config['test_id'])
page.scrape()
page.print()