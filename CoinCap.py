import requests
import json
import datetime
from datetime import timezone, datetime, timedelta, date

BASE_URL = 'https://api.coincap.io/v2/'


class CoinCap(object):
    """
    Object to interact with coincap API
    """

    def __init__(self, base_url=BASE_URL):
        self.base_url = base_url

    def _query_coincap(self, endpoint):
        """
        Hits the coincap.io endpoint
        :param endpoint: endpoint to hit
        :return: response as JSON
        """
        response = requests.get(self.base_url + endpoint)

        if response.status_code != 200:
            raise Exception('The server has responded with an error')
        response = json.loads(response.text)
        return response

    def get_assets(self):
            """
            Returns list of assets
            """
            return self._query_coincap('assets/')
        
    def get_asset_history(self, asset_id, interval='d1', start=None, end=None):
        """
        Returns history of an asset. Asset_id can be symbol or name. 
        Start and end are based on what the interval is.
        """
        supported_intervals = ['m1', 'm5', 'm15', 'm30', 'h1', 'h2', 'h6', 'h12', 'd1']
        if interval not in supported_intervals:
            raise Exception('{} interval not supported, please pick from {}'.format(interval, supported_intervals))
        
        dict = {
            'm1' : 86400000,
            'm5' : 86400000,
            'm30' : 604800000,
            'h1' : 604800000,
            'h2' : 604800000,
            'h6' : 2419200000,
            'h12' : 2419200000,
            'd1' : 2419200000
        }
        
        if start == None:
            end = int(datetime.now().replace(tzinfo=timezone.utc).timestamp()*1000)
            start = (end - dict[interval])
            
        return self._query_coincap('assets/{}/history?interval={}&start={}&end={}'.format(asset_id, interval, str(start), str(end)))