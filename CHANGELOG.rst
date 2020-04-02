2020-
==========

* Bytte från Akt Direkt API V3 till V4
* Tog bort det gamla ArkenProxy bakåtkompatibla APIet.
* Om du har en existerande config.cfg du vill använda så behöver v3.0 ändras till v4.0 i SERVICE_URL.
* Storleken på nedladdade filer är betydligt större än med den nya versionen så dom strömmas nu.
* Gjort det tydligare på startsidan när kommunikationstestet misslyckats.
* Gjort det möjligt att skicka med argument till flask run via start.sh skriptet.

2019-06-24
==========

* Improved error handling. When a token update failed the application could
  find itself in a state it could not recover from.
