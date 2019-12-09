from gather.ListOfWorks import ListOfWorks 
import yaml

try:
    with open('config.yaml', 'r') as file:
        config = yaml.safe_load(file)
        #output_file = config['files']['output']
except Exception as e:
    print('Error reading yaml configuration file.')

works = ListOfWorks(config)
print(config['params'])
works.scrape()

#works_list.get_works_list (output_file, "The Mandalorian (TV)", type_of='works', sort='date_posted', date_from='')
#works_list.get_works_list ("Star Wars - All Media Types", type_of='works', sort='date_posted', date_from='2019-12-04')