from prefect import Flow, task, Parameter
#import sys
#sys.path.append('/Users/rebecca/projects/personal/fan related/AO3Scraper')

import ao3_work_ids as ids
import ao3_get_fanfics as works

@task
def get_IDs():
    url = "https://archiveofourown.org/tags/The%20Mandalorian%20(TV)/works"
    output_file = "data/mando"
    limit = 10
    header_info = ""
    ids.scrape(url, output_file, limit, header_info)
    return

@task
def get_works():

    '''
    you can also query a single fic id, `python ao3_get_fanfics.py 5937274`, 
    or enter an arbitrarily sized list of them, `python ao3_get_fanfics.py 5937274 7170752`.
    --restart 012345` (the work_id).  The scraper will start from the given id. 
    
    input_file = "data/mando.csv"
    output_file = "data/mando_works.csv"
    header = ""
    works.scrape(fic_ids, output_file, header, restart, is_csv, True)
    '''
    pass
    return


@task
def get_meta():
    #extract_metadata.py
    pass
    return

with Flow("Scrape Meta Data") as flow:
    ID = get_IDs()
    works = get_works()
    meta = get_meta()

state = flow.run()

flow.visualize()
