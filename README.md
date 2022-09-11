[![Build Status](https://img.shields.io/github/workflow/status/EfraimGENC/ups-turkey/Publish%20UPS%20Turkey%20distributions%20to%20PyPI%20and%20TestPyPI?logo=GitHub&label=build)](https://github.com/EfraimGENC/ups-turkey/actions/workflows/publish-to-test-pypi.yml) [![Made With](https://img.shields.io/badge/%3C%2F%3E-Python-blue)](https://github.com/EfraimGENC/ups-turkey/blob/master/requirements.txt) [![License](https://img.shields.io/badge/license-mit-blue.svg)](https://github.com/EfraimGENC/ups-turkey/blob/master/LICENSE.md) [![Latest Relase](https://img.shields.io/github/v/release/EfraimGENC/ups-turkey?sort=semver)](https://github.com/EfraimGENC/ups-turkey/releases)

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
        'ShipperCityCode': 34, # UPS tarafından tanımlanmıştır. Türkiye'deki şehirler için resmi numara.
        'ShipperAreaCode': 5824, # UPS tarafından tanımlanmıştır.
        'ShipperPostalCode': '34000',
        'ShipperPhoneNumber': '0 212 000 00 00',
        'ShipperPhoneExtension': '',
        'ShipperMobilePhoneNumber': '',
        'ShipperEMail': 'info@firma.com',
        'ShipperExpenseCode': '', # Gönderici tarafından sağlanan gider kodu. Paketleri daha fazla sınıflandırmak için raporlamada kullanılır (genellikle maliyet ölçümü için).

        # Alıcı
        'ConsigneeAccountNumber': '',
        'ConsigneeName': 'Mehmet Yılmaz',
        'ConsigneeContactName': '',
        'ConsigneeAddress': 'Memleket Mh. Bilmemne Sk. No:1',
        'ConsigneeCityCode': 34, # UPS tarafından tanımlanmıştır. Türkiye'deki şehirler için resmi numara.
        'ConsigneeAreaCode': 1858, # UPS tarafından tanımlanmıştır.
        'ConsigneePostalCode': '34000',
        'ConsigneePhoneNumber': '',
        'ConsigneePhoneExtension': '',
        'ConsigneeMobilePhoneNumber': '05320000000',
        'ConsigneeEMail': 'musteri@eposta.com',
        'ConsigneeExpenseCode': '', # Gönderici tarafından sağlanan gider kodu. Paketleri daha fazla sınıflandırmak için raporlamada kullanılır (genellikle maliyet ölçümü için).

        # Gönderi
        'ServiceLevel': 3,
        'PaymentType': 2,
        'PackageType': 'K',
        'NumberOfPackages': 1,
        'CustomerReferance': 'SIPARISNO',
        'CustomerInvoiceNumber': 'EFATURA000000',
        'DeliveryNotificationEmail': '',
        'DescriptionOfGoods': 'SKU00000',
        'IdControlFlag': 0, # Gönderici kimlik teyidi ile teslimat talep ederse “1”, aksi takdirde “0”.
        'PhonePrealertFlag': 0, # Gönderici, alıcının teslimattan önce telefonla uyarılmasını talep ederse “1”, aksi halde “0”.
        'SmsToShipper': 0,
        'SmsToConsignee': 1,
        'InsuranceValue': 0.00, # Sigorta değeri. Müşteri tarafından beyan edilir.
        'InsuranceValueCurrency': 'TL', # TL, EUR, USD
        'ValueOfGoods': 0, # Ürün fiyatı. Müşteri tarafından beyan edilir.
        'ValueOfGoodsCurrency': 'TL', # TL, EUR, USD
        'ValueOfGoodsPaymentType': 1,
        'ThirdPartyAccountNumber': '', # Navlun üçüncü bir şahıs tarafından ödeniyorsa, bu UPS müşteri hesap numarasıdır.
        'ThirdPartyExpenseCode': '', # Gönderici tarafından sağlanan gider kodu. Paketleri daha fazla sınıflandırmak için raporlamada kullanılır (genellikle maliyet ölçümü için).
    },
    'ReturnLabelLink': True,
    'ReturnLabelImage': True
}

shipment = ups.CreateShipment_Type2(shipment_info, True, True)
```

### Get Shipment Info By Tracking Number
```python
from ups_turkey import UPSService


ups = UPSService('CUSTOMER_NUMBER', 'USERNAME', 'PASSWORD')

payload = {
    'InformationLevel': 1,
    'TrackingNumber': 'YOUR_TRACKING_NUMBER'
}

result = ups.GetShipmentInfoByTrackingNumber_V2(**payload)

```

You can convert to JSON if you like
```python
import json
from decimal import Decimal

# This for encode decimal values
class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return json.JSONEncoder.default(self, obj)

print(json.dumps(result, ensure_ascii=False, cls=DecimalEncoder))
```

### Get Transactions By Tracking Number
```python
from ups_turkey import UPSService


ups = UPSService('CUSTOMER_NUMBER', 'USERNAME', 'PASSWORD')

payload = {
    'InformationLevel': 1,
    'TrackingNumber': '1ZE3184E6800392064'
}

result = ups.GetTransactionsByTrackingNumber_V1(**payload)
```

### Get Transactions By List
```python
from ups_turkey import UPSService


ups = UPSService('CUSTOMER_NUMBER', 'USERNAME', 'PASSWORD')

payload = {
    'SessionID': '',
    'InformationLevel': 1,
    'refList': {
        'referansType': 'WAYBILL_TYPE',
        'referansList': ['YOUR_UPSReferance_CODE']
    },
    'trnType': 'ALL_TRANSACTIONS'
}

result = ups.GetTransactionsByList_V2(**payload)
```