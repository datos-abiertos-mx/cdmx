import datetime
import logging
import os
import subprocess
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
                try:
                    filedata = urllib2.urlopen(url)
                    datatowrite = filedata.read()
                    path = 'data/{site}/{dataset}/'.format(site=site_name, dataset=dataset)
                    if not os.path.exists(path):
                        os.makedirs(path)
                    filename = '{path}{dataset}.{format}'.format(path=path, dataset=dataset,
                                                                 format=site['params']['format'])
                    with open(filename, 'wb') as f:
                        f.write(datatowrite)
                    print(filename)
                    logger.info(filename)
                    cmd = 'split -l 70000 {filename} {dataset}_'.format(filename=filename, dataset=dataset)
                    subprocess.call(cmd, shell=True)
                    cmd = 'mv {dataset}_* {path}.'.format(path=path, dataset=dataset)
                    subprocess.call(cmd, shell=True)
                    os.remove(filename)
                except Exception as ex:
                    print(ex)
                    logging.error("\n{}\nERROR".format('-' * 30), exc_info=ex)


if __name__ == '__main__':
    download()
