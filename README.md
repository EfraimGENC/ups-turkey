[![Build Status](https://img.shields.io/github/workflow/status/EfraimGENC/ups-turkey/Publish%20UPS%20Turkey%20distributions%20to%20PyPI%20and%20TestPyPI?logo=GitHub&label=build)](https://github.com/EfraimGENC/ups-turkey/actions/workflows/publish-to-test-pypi.yml) [![Made With](https://img.shields.io/badge/%3C%2F%3E-Python-blue)](https://github.com/EfraimGENC/ups-turkey/blob/master/requirements.txt) [![License](https://img.shields.io/badge/license-mit-blue.svg)](https://github.com/EfraimGENC/ups-turkey/blob/master/LICENSE.md) [![Latest Relase](https://img.shields.io/github/v/release/EfraimGENC/ups-turkey?sort=semver)](https://github.com/EfraimGENC/ups-turkey/releases)

# UPS Turkey
Python package for integrate UPS Turkey easily.

UPS Türkiye yutriçi gönderileri için `ups.com/upsdeveloperkit`'ten ayrı bir sistem kullanmaktadır. `ups.com/upsdeveloperkit` sadece yurtdışı gönderile için kullanılmaktadır. UPS Türkiye'nin API'ları ise WebService (SOAP) ile çalışmaktadır. Bu hafif python pakedi, UPS Türkiye'nin web servisini kolayca kullanabilmenize olanak sağlar.

UPS Türkiye'nin oluşturma([Createshipment V7](https://ws.ups.com.tr/wsCreateShipment/wsCreateShipment.asmx)) ve sorgulama([QueryPackageInfo](https://ws.ups.com.tr/QueryPackageInfo/wsQueryPackagesInfo.asmx)) işlemleri için iki ayrı servisi bulunmaktadır.

---
## Table of Contents
- [Installation](#Installation)
- [Usage](#Usage)
  - [Inıtilaize Service](#InıtilaizeService)
    - [Service Helpers](#ServiceHelpers)
  - [Operations](#Operations)
    - [List](#List)
    - [Parameter Dictionary](#ParameterDictionary)
    - [Examples](#Examples)

---

## Installation <a name="Installation"></a>
```sh
pip install ups-turkey
```

## Usage <a name="Usage"></a>
### Inıtilaize Service <a name="InıtilaizeService"></a>
```python
from ups_turkey import UPSService

ups = UPSService('CUSTOMER_NUMBER', 'USERNAME', 'PASSWORD')
```
#### Service Helpers <a name="ServiceHelpers"></a>
```python
result = ups.ANY_OPERATIONS(**payload)
```
Operartions resturn list of dict as `ResultList[Result]`. ResultList and Result have some helpers like below.
- `Result(dict)`
  - Convert result to JSON: `result.json()`
  - Convert result to dictionary: `result.dict()`
  - Checks is result is have an error: `result.is_success()` returns bool.
    If you want to raise `UPSException(ERROR_CODE, ERROR_DEFINATION)` pass `raise_exception=True` param like `result.is_success(raise_exception=True)`
  - `result.get_error()` for getting result's error code and defination as tuple if has
- `ResultList(list)`
  - Convert result to JSON: `result.json()`
  - Checks is any result in list is have an error: `result.has_fail()` returns bool.
    If you want to raise `UPSException(ERROR_CODE, ERROR_DEFINATION)` pass `raise_exception=True` param like `result.has_fail(raise_exception=True)`

### Operations <a name="Operations"></a>
#### List <a name="List"></a>
- Create Service
  - Cancel_Shipment_V1
  - CreateShipment_Type1
  - [CreateShipment_Type2](#CreateShipment_Type2)
  - CreateShipment_Type2TRT
  - CreateShipment_Type3
  - CreateShipment_Type3_XML
  - CreateShipment_Type3_ZPL
  - CreateShipment_Type3_ZPL_Types
  - CreateShipment_Type4
  - CustomerShipmentLimitDetail
  - OnDemandPickupRequest_Type1
  - TransferShipmentList_Type1
- Query Service
  - GetLastTransactionByTrackingNumber_V1
  - GetPackageInfoByDatePeriod_V1
  - GetPackageInfoByReferance_V1
  - GetPackageInfoByTrackingNumber_V1
  - GetShipmentInfoByTrackingNumber_V1
  - [GetShipmentInfoByTrackingNumber_V2](#GetShipmentInfoByTrackingNumber_V2)
  - GetTiNTInformationByTrackingNumberList_V1
  - GetTiNTInformationByTrackingNumber_V1
  - GetTransactionsByCustomerCode_V1
  - GetTransactionsByList_V1
  - [GetTransactionsByList_V2](#GetTransactionsByList_V2)
  - GetTransactionsByPackagePickupDate_V1
  - [GetTransactionsByTrackingNumber_V1](#GetTransactionsByTrackingNumber_V1)
  - GetUnreadTransactionsByTrackingNumber_V1

#### Parameter Dictionary <a name="ParameterDictionary"></a>
##### ExpenseCode
Gönderici tarafından sağlanan gider kodu. Paketleri daha fazla sınıflandırmak için raporlamada kullanılır (genellikle maliyet ölçümü için).
##### CityCode
UPS tarafından tanımlıdır. Türkiye'deki şehirler için plaka numarası.
##### ThirdPartyAccountNumber
Navlun üçüncü bir şahıs tarafından ödeniyorsa, bu UPS müşteri hesap numarasıdır.
##### IdControlFlag
Gönderici kimlik teyidi ile teslimat talep ederse “1”, aksi takdirde “0”.
##### PhonePrealertFlag
Gönderici, alıcının teslimattan önce telefonla uyarılmasını talep ederse “1”, aksi halde “0”.

#### Examples <a name="Examples"></a>
##### CreateShipment_Type2 <a name="CreateShipment_Type2"></a>
```python
payload = {
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

shipment = ups.CreateShipment_Type2(**payload)
```

##### GetShipmentInfoByTrackingNumber_V2 <a name="GetShipmentInfoByTrackingNumber_V2"></a>
```python
payload = {
    'InformationLevel': 1,
    'TrackingNumber': 'YOUR_TRACKING_NUMBER'
}

result = ups.GetShipmentInfoByTrackingNumber_V2(**payload)
```

##### GetTransactionsByTrackingNumber_V1 <a name="GetTransactionsByTrackingNumber_V1"></a>
```python
payload = {
    'InformationLevel': 1,
    'TrackingNumber': 'YOUR_TRACKING_NUMBER'
}

result = ups.GetTransactionsByTrackingNumber_V1(**payload)
```

##### GetTransactionsByList_V2 <a name="GetTransactionsByList_V2"></a>
```python
payload = {
    'InformationLevel': 1,
    'refList': {
        'referansType': 'WAYBILL_TYPE',
        'referansList': ['YOUR_UPSReferance_CODE']
    },
    'trnType': 'ALL_TRANSACTIONS'
}

result = ups.GetTransactionsByList_V2(**payload)
```