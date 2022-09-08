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

    def get_session_id(self, query=False):
        credentials = self.customer_number, self.username, self.password

        if query:
            client = zeep.Client(self.wsdl_query)
            result = client.service.Login_V1(*credentials)
        else:
            client = zeep.Client(self.wsdl_create)
            result = client.service.Login_Type1(*credentials)

        result = zeep.helpers.serialize_object(result)

        self._error_handler(result)

        return uuid.UUID(result['SessionID'])

    def CreateShipment_Type2(self, shipment_info:dict,
                        return_label_link:bool = True,
                        return_label_image:bool = True):
        """
        Create shipment with type 2
        """

        shipment_info['SessionID'] = self.get_session_id()
        shipment_info['ReturnLabelLink'] = return_label_link
        shipment_info['ReturnLabelImage'] = return_label_image

        # Request
        client = zeep.Client(self.wsdl_create)
        result = client.service.CreateShipment_Type2(**shipment_info)
        result = zeep.helpers.serialize_object(result)

        self._error_handler(result)

        return result

    def GetShipmentInfoByTrackingNumber_V2(self, tracking_number:str) -> OrderedDict:
        """
        This method is used to query package information for all tracking \
        numbers in a shipment. Any tracking number in a shipment can be sent \
        as a parameter.
        """
        session_id = self.get_session_id(True)
        client = zeep.Client(self.wsdl_query)
        result = client.service.GetShipmentInfoByTrackingNumber_V2(
            session_id, 1, tracking_number)
        result = zeep.helpers.serialize_object(result)[0]

        self._error_handler(result)

        return result

    def GetLastTransactionByTrackingNumber_V1(self, tracking_number:str):
        """
        This method return only the last transaction for a tracking number
        """
        session_id = self.get_session_id(True)
        client = zeep.Client(self.wsdl_query)
        result = client.service.GetLastTransactionByTrackingNumber_V1(
            session_id, 1, tracking_number)
        result = zeep.helpers.serialize_object(result)[0]

        self._error_handler(result)

        return result

    def GetTransactionsByTrackingNumber_V1(self, tracking_number:str):
        """
        This method return only the last transaction for a tracking number
        """
        session_id = self.get_session_id(True)
        client = zeep.Client(self.wsdl_query)
        result = client.service.GetTransactionsByTrackingNumber_V1(
            session_id, 1, tracking_number)
        result = zeep.helpers.serialize_object(result)

        self._error_handler(result)

        return result

    def GetUnreadTransactionsByTrackingNumber_V1(self,
                                                 tracking_number:str,
                                                 record_id:str):
        """
        This method return all transactions with RecordIds greater than the 
        RecordId supplied as a parameter. RecordIds are returned as part of 
        transaction information.
        """
        session_id = self.get_session_id(True)
        client = zeep.Client(self.wsdl_query)
        result = client.service.GetUnreadTransactionsByTrackingNumber_V1(
            session_id, 1, tracking_number, record_id)
        result = zeep.helpers.serialize_object(result)

        self._error_handler(result)

        return result

    def GetTransactionsByList_V2(self, veri):
        """
        This method returns requested transactions by provided list. \
        List can be customer referance number and tracking number. \
        Referance type must be set. Results can be set as last transaction, \
        all transaction and delivery transaction.
        """
        veri['SessionID'] = self.get_session_id(True)

        client = zeep.Client(self.wsdl_query)
        result = client.service.GetTransactionsByList_V2(veri)
        result = zeep.helpers.serialize_object(result)

        # self._error_handler(result)

        return result
