import uuid
import zeep
from collections import OrderedDict
from ups_turkey.exceptions import UPSException


class UPSService:
    def __init__(self, customer_number, username, password) -> None:
        self.customer_number = customer_number
        self.username = username
        self.password = password
        self.wsdl_create = 'https://ws.ups.com.tr/wsCreateShipment/wsCreateShipment.asmx?WSDL'
        self.wsdl_query = 'https://ws.ups.com.tr/QueryPackageInfo/wsQueryPackagesInfo.asmx?WSDL'

    @staticmethod
    def _error_handler(response):
        def _handler(res):
            error_code = res.get('ErrorCode')
            error_definition = res.get('ErrorDefinition')
            if error_code != 0 and error_code is not None:
                raise UPSException(error_code, error_definition)

        if isinstance(response, list):
            list(map(_handler, response))
        else:
            _handler(response)

    def call_service(self, service:str, query=False, *args, **kwargs):
        if not service.startswith('Login'):
            kwargs['SessionID'] = self.get_session_id(query)
        wdsl = self.wsdl_query if query else self.wsdl_create
        client = zeep.Client(wdsl)
        result = getattr(client.service, service)(*args, **kwargs)
        result = zeep.helpers.serialize_object(result)
        self._error_handler(result)
        return result

    def get_session_id(self, query=False):
        credentials = self.customer_number, self.username, self.password
        if query:
            result = self.call_service('Login_V1', True, *credentials)
        else:
            result = self.call_service('Login_Type1', False, *credentials)
        return uuid.UUID(result['SessionID'])

    def CreateShipment_Type2(self, *args, **kwargs):
        """
        Create shipment with type 2
        """
        return self.call_service('CreateShipment_Type2', False, *args, **kwargs)

    def GetShipmentInfoByTrackingNumber_V2(self, *args, **kwargs) -> OrderedDict:
        """
        This method is used to query package information for all tracking \
        numbers in a shipment. Any tracking number in a shipment can be sent \
        as a parameter.
        """
        return self.call_service('GetShipmentInfoByTrackingNumber_V2', True, *args, **kwargs)

    def GetLastTransactionByTrackingNumber_V1(self, *args, **kwargs):
        """
        This method return only the last transaction for a tracking number
        """
        return self.call_service('GetLastTransactionByTrackingNumber_V1', True, *args, **kwargs)

    def GetTransactionsByTrackingNumber_V1(self, *args, **kwargs):
        """
        This method return only the last transaction for a tracking number
        """
        return self.call_service('GetTransactionsByTrackingNumber_V1', True, *args, **kwargs)

    def GetUnreadTransactionsByTrackingNumber_V1(self, *args, **kwargs):
        """
        This method return all transactions with RecordIds greater than the 
        RecordId supplied as a parameter. RecordIds are returned as part of 
        transaction information.
        """
        return self.call_service('GetUnreadTransactionsByTrackingNumber_V1', True, *args, **kwargs)

    def GetTransactionsByList_V2(self, *args, **kwargs):
        """
        This method returns requested transactions by provided list. \
        List can be customer referance number and tracking number. \
        Referance type must be set. Results can be set as last transaction, \
        all transaction and delivery transaction.
        """
        return self.call_service('GetTransactionsByList_V2', True, *args, **kwargs)
