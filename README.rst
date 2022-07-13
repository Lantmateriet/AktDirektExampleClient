!!! WARNING
   There is no plan to continue to provide AktDirektExampleClients for API versions after 4.0.
   After the 3.0 and 4.0 APIs are shutdown this repository will be removed from github,
   this removal will probably happen during 2023Q2.

=============================
Example client for Akt Direkt
=============================

English discription:

  This is example client for Swedish Lantmäteriet's contract service Akt Direkt.
  The service makes some of Lantmäteriet's archives available for integration into customers' archives.
  Based on the content of the archives the choice was made to write the documentation in Swedish.


Denna applikation är en exempelklient för Lantmäteriets avtalstjänst Akt Direkt.
Akt Direkt ger kunden tillgång till vissa av Lantmäteriets arkiv för integration i egna system.

Denna applikation är en ganska minimal proxy framför Akt Direkt som tar hand om autentiseringen.
Applikationen har även ett enkelt webb-UI som hjälp för att testa att titta på akter.

Applikation är utvecklad för och testad med Python 3.6 i GNU/Linux miljö.

NOTERA: Denna version av klienten är för version 4 av APIet, för föregånde version se GIT branchen api-v3.

UPPGRADERA: Om du har en existerande config.cfg för api-v3 du vill använda så behöver v3.0
ändras till v4.0 i SERVICE_URL i filen.


Funktioner
==========

* Klientbibliotek för Akt Direkt

  * Använder OAuth consumer_key och secret för att ladda hem token som används vid anropen.
  * Uppdaterar OAuth token vid behov.

* UI på http://localhost:5000/

  * Laddning av sidan testar kommunikationen med Lantmäteriet och inloggningen.
  * Formulär för generering av korrekt URL för att kunna öppna en akt.

* API Proxy ``http://localhost:5000/document/*.djvu``

  * Autentiserande proxy som tar hand om följande anrop:

    * URLarna som genereras av formuläret ovan refererar till http://localhost:5000/document/bundle.djvu samt
      http://localhost:5000/document/djvu_on_error/bundle.djvu med nödvändiga query parametrar.
    * Äldre URL http://localhost:5000/document/index.djvu redirectar nu till ovansående djvu_on_error URL med nödvändiga query parametrar.

  Ex::

    djview "http://localhost:5000/document/bundle.djvu?archive=21&id=2180k-10/11"
    djview "http://localhost:5000/document/bundle.djvu?archive=k21g&id=2180k-10/11"
    djview "http://localhost:5000/document/djvu_on_error/bundle.djvu?archive=k21g&id=2180k-10/11"
    curl http://localhost:5000/ping  (ersätter tidigare /healthcheck)


Files
=====

* ``akt_direkt_proxy/views/startpage.py``: implementation av användargränssnitt
* ``akt_direkt_proxy/views/proxy.py``: exponera APIet lokalt
* ``akt_direkt_proxy/__init__.py``: uppsättning av applikationen
* ``akt_direkt_proxy/client.py``: implementation av själva API Klienten
* ``akt_direkt_proxy/templates/startpage.html``: Jinja2 template för förstasidan med formulär
* ``akt_direkt_proxy/templates/djvu_url.html``: Jinja2 template med sidan som visar genererad URL
* ``config.cfg``: konfigurationsfil du behöver skapa
* ``config.cfg_example``: exempel på konfigurationsfil
* ``Dockerfile``: to build the example as a runnable Docker image
* ``Pipfile``: definierar applikationens beroenden (used by Pipenv)
* ``Pipfile.lock``: detaljerat specifikation över vilka versioner av beroenden som applikationen ska köras (används av Pipenv)
* ``start.sh``: shell skript för att starta applikationen i lokal pipenv
* ``check.sh``: kör statisk kontroll av koden
* ``check_rst.sh``: kontrollera syntax för README.rst


Konfigurering
=============

Innan applikation kan användas behöver du skapa en config.cfg i denna katalog, skapa den genom att kopiera config.cfg_example.
Du behöver byta ut CONSUMER_KEY och CONSUMER_SECRET i filen mot de värden du får från Lantmäteriets API-store.


Köra applikationen i Docker
===========================

För dom flesta är det enklast att köra applikationen i docker.

Du kan bygga exempel applikationen som en Docker bild och köra den:

.. code-block:: bash

    $ docker build -t aktdirekt-example .        # Bygg en docker image med applikationen
    $ docker run -it --rm --env-file ./config.cfg -p 5000:5000 aktdirekt-example  # Starta applikationen i förgrunden
    $ docker run -d --env-file ./config.cfg -p 5000:5000 aktdirekt-example  # eller Starta applikationen i bakgrunden
    $ Öppna http://localhost:5000 i en webbläsare


Kör lokalt utan Docker
======================

Om du har Python 3.6 och `Pipenv <https://docs.pipenv.org/>` installerat så kan du köra applikationen utan Docker:

.. code-block:: bash

    $ pipenv install
    $ pipenv run ./start.sh  # starta HTTP servern
    $ Öppna http://localhost:5000 i en webbläsare


Kontaktinformation
==================

Support för tjänsten ges enligt avtal.


License
=======

   Copyright 2018 Lantmäteriet

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

     http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
