import uuid
import zeep
from typing import Tuple
from ups_turkey.exceptions import UPSException
from ups_turkey.helpers import to_json


class Result(dict):
    def is_success(self, raise_exception=False):
        error = self.get_error()
        if raise_exception and error[0]:
            raise UPSException(*error)
        return not bool(error[0])

    def get_error(self) -> Tuple[str, str]:
        return self.get('ErrorCode'), self.get('ErrorDefinition')

    def json(self):
        return to_json(self)

    def dict(self):
        return dict(self)


class ResultList(list):
    def has_fail(self, raise_exception=False):
        for r in self:
            if not r.is_success(raise_exception):
                return True
        return False

    def json(self):
        return to_json(self)


class UPSService:
    base_url = 'https://ws.ups.com.tr'
    wsdl = {
        'create': f'{base_url}/wsCreateShipment/wsCreateShipment.asmx?WSDL',
        'query': f'{base_url}/QueryPackageInfo/wsQueryPackagesInfo.asmx?WSDL',
    }

    def __init__(self, customer_number, username, password) -> None:
        self.customer_number = customer_number
        self.username = username
        self.password = password

    def _call(self, service:str, operation:str, *args, **kwargs):
        """
        service: `create` or `query`
        """
        if not operation.startswith('Login'):
            kwargs['SessionID'] = self.get_session_id(service)

        client = zeep.Client(self.wsdl[service])

        result = getattr(client.service, operation)(*args, **kwargs)
        result = zeep.helpers.serialize_object(result)
        result = result if isinstance(result, list) else [result]

        result_list = ResultList()
        for r in result:
            result_list.append(Result(r))
        return result_list

    def create(self, operation:str, *args, **kwargs):
        return self._call('create', operation, *args, **kwargs)

    def query(self, operation:str, *args, **kwargs):
        return self._call('query', operation, *args, **kwargs)

    def login(self, service:str) -> Result:
        credentials = self.customer_number, self.username, self.password
        login_opertaion = {'create': 'Login_Type1', 'query': 'Login_V1'}
        result = self._call(service, login_opertaion[service], *credentials)[0]
        error = result.get('ErrorCode'), result.get('ErrorDefinition')
        if error[0]: raise UPSException(*error)
        return result

    def get_session_id(self, service:str):
        result = self.login(service)
        return uuid.UUID(result['SessionID'])
