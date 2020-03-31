2020-
==========

* Bytte från Akt Direkt API V3 till V4
* Tog bort det gamla ArkenProxy bakåtkompatibla APIet.
* Om du har en existerande config.cfg du vill använda så behöver v3.0 ändas till v4.0 i SERVICE_URL.

2019-06-24
==========

* Improved error handling. When a token update failed the application could
  find itself in a state it could not recover from.
