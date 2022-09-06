# UPS Turkey
Python package for integrate UPS Turkey easily.

[Createshipment V7](https://ws.ups.com.tr/wsCreateShipment/wsCreateShipment.asmx)

[QueryPackageInfo](https://ws.ups.com.tr/QueryPackageInfo/wsQueryPackagesInfo.asmx)

## Install
```sh
pip install ups-turkey
```

## Usage
### Create Shipment
```python
from ups_turkey import UPSService


ups = UPSService('CUSTOMER_NUMBER', 'USERNAME', 'PASSWORD')

shipment_info = {
    'ShipmentInfo': {
        # Gönderen
        'ShipperAccountNumber': 'CUSTOMER_NUMBER',
        'ShipperName': 'ABC Ltd. Şti.',
        'ShipperContactName': 'Mehmet Yılmaz',
        'ShipperAddress': 'Huzur Mh. Barış Cd. No:99',
        'ShipperCityCode': 34,
        'ShipperAreaCode': 5824,
        'ShipperPostalCode': '34000',
        'ShipperPhoneNumber': '0 212 000 00 00',
        'ShipperPhoneExtension': '',
        'ShipperMobilePhoneNumber': '',
        'ShipperEMail': 'info@firma.com',
        'ShipperExpenseCode': '',

        # Alıcı
        'ConsigneeAccountNumber': '',
        'ConsigneeName': 'Mehmet Yılmaz',
        'ConsigneeContactName': '',
        'ConsigneeAddress': 'Memleket Mh. Bilmemne Sk. No:1',
        'ConsigneeCityCode': 34,
        'ConsigneeAreaCode': 1858,
        'ConsigneePostalCode': '34000',
        'ConsigneePhoneNumber': '',
        'ConsigneePhoneExtension': '',
        'ConsigneeMobilePhoneNumber': '05320000000',
        'ConsigneeEMail': 'musteri@eposta.com',
        'ConsigneeExpenseCode': '',

        # Gönderi
        'ServiceLevel': 3,
        'PaymentType': 2,
        'PackageType': 'K',
        'NumberOfPackages': 1,
        'CustomerReferance': 'SIPARISNO',
        'CustomerInvoiceNumber': 'EFATURA000000',
        'DeliveryNotificationEmail': '',
        'DescriptionOfGoods': 'SKU00000',
        'IdControlFlag': 0,
        'PhonePrealertFlag': 0,
        'SmsToShipper': 0,
        'SmsToConsignee': 1,
        'InsuranceValue': 0.00,
        'InsuranceValueCurrency': 'TL',
        'ValueOfGoods': 0,
        'ValueOfGoodsCurrency': 'TL',
        'ValueOfGoodsPaymentType': 1,
        'ThirdPartyAccountNumber': '',
        'ThirdPartyExpenseCode': '',
    }
}

shipment = ups.CreateShipment_Type2(shipment_info, True, True)
```

### Get Shipment Info By Tracking Number

```python
from ups_turkey import UPSService


ups = UPSService('CUSTOMER_NUMBER', 'USERNAME', 'PASSWORD')
result = ups.GetShipmentInfoByTrackingNumber_V2('YOUR_TRACKING_NUMBER')
```