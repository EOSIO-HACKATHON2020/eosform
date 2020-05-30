import logging
import requests
from config.models import Settings
from surveys.models import Participation


logger = logging.getLogger(__name__)


class EOS:

    def __init__(self):
        self.settings = Settings.get_solo()
        self.uri = self.settings.eosgate
        self.api = self.settings.eos_node_uri

    def get_table_rows(self, table: str) -> list:
        """
        https://developers.eos.io/manuals/eos/latest/nodeos/plugins/
        chain_api_plugin/api-reference/index#operation/get_table_rows
        :param table:
        :return: requests response with the rows
        """
        payload = {
            'code': self.settings.eos_account,
            'table': table,
            'scope': self.settings.eos_account,
            'json': True,
            'encode_type': 'dec',
            'reverse': False,
            'show_payer': False,
            # Note: that is to show how to communicate with EOS NODE RPC API
            # in production we would store how many surveys active at the
            # moment and how many responses provided (incrementing/
            # decrementing that value)
            'limit': 10000
        }
        resp = requests.post(
            f'{self.api}/v1/chain/get_table_rows',
            json=payload
        )
        if resp.status_code == 200:
            return resp.json()['rows']
        logger.error(f'EOS get_table_rows: {resp.content.decode()}')
        return []

    def forms(self) -> int:
        """
        That is just demonstration how to request table data using EOS Node API
        :return: how many forms were created
        """
        return len(self.get_table_rows('form'))

    def responses(self) -> int:
        """
        :return: How many responses were given
        """
        return Participation.objects.count()
