import json
import uuid
import zeep
from typing import OrderedDict, Tuple
from collections.abc import Iterable
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
    wsdl_create = base_url + '/wsCreateShipment/wsCreateShipment.asmx?WSDL'
    wsdl_query = base_url + '/QueryPackageInfo/wsQueryPackagesInfo.asmx?WSDL'

    def __init__(self, customer_number, username, password) -> None:
        self.customer_number = customer_number
        self.username = username
        self.password = password

    def call_service(self, service:str, query=False, *args, **kwargs):
        if not service.startswith('Login'):
            kwargs['SessionID'] = self.get_session_id(query)

        wdsl = self.wsdl_query if query else self.wsdl_create
        client = zeep.Client(wdsl)

        result = getattr(client.service, service)(*args, **kwargs)
        result = zeep.helpers.serialize_object(result)
        result = result if isinstance(result, list) else [result]

        result_list = ResultList()
        for r in result:
            result_list.append(Result(r))
        return result_list

    def login(self, query=False):
        credentials = self.customer_number, self.username, self.password
        if query:
            result = self.call_service('Login_V1', True, *credentials)[0]
        else:
            result = self.call_service('Login_Type1', False, *credentials)[0]
        error = result.get('ErrorCode'), result.get('ErrorDefinition')
        if error[0]: raise UPSException(*error)
        return result

    def get_session_id(self, query=False):
        result = self.login(query)
        return uuid.UUID(result['SessionID'])

    # Creation Services #######################################################

    def CreateShipment_Type2(self, *args, **kwargs):
        """
        Create shipment with type 2
        """
        return self.call_service(
            'CreateShipment_Type2', False, *args, **kwargs)

    def OnDemandPickupRequest_Type1(self, *args, **kwargs):
        """
        OnDemand Pickup Request Type 1
        """
        return self.call_service(
            'OnDemandPickupRequest_Type1', False, *args, **kwargs)

    def CustomerShipmentLimitDetail(self):
        """
        Customer Shipment LimitDetail
        """
        return self.call_service(
            'CustomerShipmentLimitDetail', False)

    # Query Services ##########################################################

    def GetLastTransactionByTrackingNumber_V1(self, *args, **kwargs):
        """
        This method return only the last transaction for a tracking number
        """
        return self.call_service(
            'GetLastTransactionByTrackingNumber_V1', True, *args, **kwargs)

    def GetPackageInfoByDatePeriod_V1(self, *args, **kwargs):
        """
        This method is used to query all of the packages information, 
        under an account number, in a given date period. As SessionId 
        obtained through Login is specific to a customer account number, 
        account number is not needed as a parameter.
        Parameters: `SessionID`, `InformationLevel`, `Startdate`, `EndDate`
        """
        return self.call_service(
            'GetPackageInfoByDatePeriod_V1', True, *args, **kwargs)

    def GetPackageInfoByTrackingNumber_V1(self, *args, **kwargs):
        """
        This method is used to query package information by tracking number.
        Parameters: `SessionID`, `InformationLevel`, `TrackingNumber`
        """
        return self.call_service(
            'GetPackageInfoByTrackingNumber_V1', True, *args, **kwargs)

    def GetShipmentInfoByTrackingNumber_V1(self, *args, **kwargs):
        """
        This method is used to query package information for all tracking 
        numbers in a shipment. Any tracking number in a shipment can be sent 
        as a parameter.
        """
        return self.call_service(
            'GetShipmentInfoByTrackingNumber_V1', True, *args, **kwargs)

    def GetShipmentInfoByTrackingNumber_V2(self, *args, **kwargs):
        """
        This method is used to query package information for all tracking 
        numbers in a shipment. Any tracking number in a shipment can be sent 
        as a parameter.
        """
        return self.call_service(
            'GetShipmentInfoByTrackingNumber_V2', True, *args, **kwargs)

    def GetTiNTInformationByTrackingNumberList_V1(self, *args, **kwargs):
        """
        This method used to query time in transit information for a package.
        Pickup date also included in dataset.
        Parameters: `SessionID`, `InformationLevel`,
        `TrackingNumberList[WaybillList[Waybill]]`
        """
        return self.call_service(
            'GetTiNTInformationByTrackingNumberList_V1', True, *args, **kwargs)

    def GetTiNTInformationByTrackingNumber_V1(self, *args, **kwargs):
        """
        This method used to query time in transit information for a package.
        Pickup date also included in dataset.
        Parameters: `SessionID`, `InformationLevel`, `TrackingNumber`
        """
        return self.call_service(
            'GetTiNTInformationByTrackingNumber_V1', True, *args, **kwargs)

    def GetTransactionsByCustomerCode_V1(self, *args, **kwargs):
        """
        Parameters: `SessionID`, `InformationLevel`, `RecordId`
        """
        return self.call_service(
            'GetTransactionsByCustomerCode_V1', True, *args, **kwargs)

    def GetTransactionsByList_V1(self, *args, **kwargs):
        """
        This method returns requested transactions by provided list. 
        List can be customer referance number and tracking number. 
        Referance type must be set. Results can be set as last transaction, 
        all transaction and delivery transaction.
        """
        return self.call_service(
            'GetTransactionsByList_V1', True, *args, **kwargs)

    def GetTransactionsByList_V2(self, *args, **kwargs):
        """
        This method returns requested transactions by provided list. 
        List can be customer referance number and tracking number. 
        Referance type must be set. Results can be set as last transaction, 
        all transaction and delivery transaction.
        """
        return self.call_service(
            'GetTransactionsByList_V2', True, *args, **kwargs)

    def GetTransactionsByPackagePickupDate_V1(self, *args, **kwargs):
        """
        This method is used to query all of the packages transactions, 
        under an account number, in a given date period. Results can be set 
        as last transaction, all transaction and delivery transaction.
        Parameters: `SessionID`, `InformationLevel`, `StartDate`, `EndDate`, 
        `TransactionType`
        """
        return self.call_service(
            'GetTransactionsByPackagePickupDate_V1', True, *args, **kwargs)

    def GetTransactionsByTrackingNumber_V1(self, *args, **kwargs):
        """
        This method return only the last transaction for a tracking number
        """
        return self.call_service(
            'GetTransactionsByTrackingNumber_V1', True, *args, **kwargs)

    def GetUnreadTransactionsByTrackingNumber_V1(self, *args, **kwargs):
        """
        This method return all transactions with RecordIds greater than the 
        RecordId supplied as a parameter. RecordIds are returned as part of 
        transaction information.
        """
        return self.call_service(
            'GetUnreadTransactionsByTrackingNumber_V1', True, *args, **kwargs)
