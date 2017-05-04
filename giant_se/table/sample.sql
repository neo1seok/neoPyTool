INSERT INTO company
(seq, cmp_uid, company_no, ftk_uid, name, description, url, url_img, updt_date, reg_date, comment) VALUES
(1, 'cmp_uid', 'ictk0001', 'ftk_1', '',
'ICTK(ICTK Co., Ltd.) is a global testing service & security solution provider serving more than 200 clients worldwide, including manufacturers, banks and government agencies. As an international testing laboratory and consultant, ICTK has been working on the fields of payment, transportation, value-added network and mobile sector. ICTK has fully satisfied all of the specified standards required by from EMVCo, Visa, JCB, Discover, Global Platform, NFC Forum and KOLAS (ISO/IEC 17025). In addition, ICTK has been dedicated to -developing customized testing solutions such as testing tools and validation system, thereby contributing to product stability and interoperability.',
'Intent://ictk#Intent;scheme=nfc;package=ictk.nfc_test;end',
'img/ictk_logo.png',now(), now(), '')


INSERT INTO giant_se.factory_key(
   seq
  ,ftk_uid
  ,factory_key_id
  ,factory_key
  ,updt_date
  ,reg_date
  ,comment
) VALUES
(1, 'ftk_1', 'EDB0', 'C84F402D68CD7AC93ADB078D85E0877F', '2017-04-12 18:13:01', '2017-04-12 18:13:01', '')