from gather.scrape_lists import ListScraper 
from gather.scrape_work import WorkScraper
import yaml

try:
    with open('config.yaml', 'r') as file:
        config = yaml.safe_load(file)
except Exception as e:
    print('Error reading yaml configuration file.')

#works = ListScraper(config)
#works.scrape()

work = WorkScraper(config['test_id'])
work.scrape()
work.print()