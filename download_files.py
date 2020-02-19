import datetime
import logging
import os
import urllib2
import yaml


if not os.path.exists('log/'):
    os.makedirs('log/')
logger = logging.getLogger('')
hdlr = logging.FileHandler('log/{date}.log'.format(date=datetime.datetime.utcnow().strftime('%Y%m%d_%H%M%S')))
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
logger.setLevel(logging.INFO)


def download():
    config = yaml.load_all(file('config.yml', 'r'))
    for c in config:
        for site_name, site in c['sites'].iteritems():
            print(site_name, site)
            for dataset in site['datasets']:
                site['params'].update(dataset=dataset)
                url = site['url'].format(**site['params'])
                print(url)
                logger.info(url)
                filedata = urllib2.urlopen(url)
                datatowrite = filedata.read()
                path = 'data/{site}/'.format(site=site_name)
                if not os.path.exists(path):
                    os.makedirs(path)
                filename = '{path}/{dataset}.{format}'.format(path=path, dataset=dataset,
                                                              format=site['params']['format'])
                with open(filename, 'wb') as f:
                    f.write(datatowrite)
                print(filename)
                logger.info(filename)


if __name__ == '__main__':
    download()
