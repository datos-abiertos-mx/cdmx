import os
import urllib2
import yaml


def download():
    config = yaml.load_all(file('config.yml', 'r'))
    for c in config:
        for site_name, site in c['sites'].iteritems():
            print(site_name, site)
            for dataset in site['datasets']:
                site['params'].update(dataset=dataset)
                url = site['url'].format(**site['params'])
                print(url)
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


if __name__ == '__main__':
    download()
