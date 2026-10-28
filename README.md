# Automower 310 med ESPHome og ESP32-C3

Norsk ESPHome-konfigurasjon for Husqvarna Automower 310 via AUX1/UART og ESP32-C3 Super Mini. Basert på brukerens v3.8 «smart polling»-YAML. Dette er et uoffisielt hobbyprosjekt, ikke et Husqvarna-produkt.

## Funksjoner

- Status, arbeidsmodus, batteri, hjulmotorer, knivmotor, støt, løft og helning.
- Fordelt polling: status/hjul/kniv omtrent hvert 2. sekund; øvrige data sjeldnere.
- AUTO/MAN/HOME, separat START og STOPP, PIN-autentisering og manuell klokkesynk.
- Ingen GPS, vekkerelé eller automatisk START ved oppstart. Modusendring kan likevel utløse bevegelse, avhengig av klipperens firmware.

## Oppsett

1. Klon repoet, eller last ned ZIP fra GitHubs **Code**-knapp:

   ```sh
   git clone https://github.com/captnalex/esphome_automower_3g.git
   cd esphome_automower_3g
   ```
2. Kopier `automower-310.yaml` til ESPHome-konfigurasjonsmappen.
3. Kopier `secrets.example.yaml` til `secrets.yaml` i samme mappe. Har du allerede en slik fil, legg til nøklene uten å overskrive eksisterende oppsett.
4. Fyll inn egen `automower_pin` som **fire sifre i anførselstegn**, eget Wi-Fi-navn og passord, en ny API-krypteringsnøkkel og et langt, unikt OTA-passord. PIN med innledende null støttes. Ikke bruk plassholderne.
5. Generer API-nøkkelen med ESPHomes veiviser eller lokalt med Python:

   ```sh
   python -c "import base64,secrets; print(base64.b64encode(secrets.token_bytes(32)).decode())"
   ```

6. Kontroller kort, kabling og forsyning før første installasjon. Standard er DHCP, navn `automower-310` og tidssone `Europe/Oslo`. Endre navn ved flere enheter og tidssone ved behov. Ingen privat fast IP følger med.
7. Valider og kompiler i ESPHome Device Builder, eller bruk kommandolinjen:

   ```sh
   esphome config automower-310.yaml
   esphome compile automower-310.yaml
   ```

8. Installer første gang via USB. Koble deretter enheten til Home Assistants ESPHome-integrasjon med API-nøkkelen fra din egen `secrets.yaml`. Senere OTA-installasjoner krever OTA-passordet. Ved overgang fra tidligere firmware må API-integrasjonen eventuelt oppdateres med den nye nøkkelen.
9. Test først avlesning, PIN-status og STOPP under fysisk tilsyn. Test START/modus kun når arbeidsområdet er fritt og det er trygt at klipperen beveger seg.

Manglende secrets gir konfigurasjonsfeil. PIN som ikke er fire desimalsifre blokkerer autentisering i firmware. PIN er ikke en redigerbar Home Assistant-entitet; endring krever ny kompilering/installasjon. Ikke legg C++-uttrykk eller anførselstegn inne i PIN-verdien.

## Kabling – bekreft på egen maskin

Følgende er rapportert fysisk testet i originalfilen på én Automower 310. Kontaktretning og revisjon må kontrolleres på din maskin; dette er ikke en universell pinout-garanti.

| AUX1 | ESP32-C3 |
| --- | --- |
| Pinne 1 | GPIO4 (RX) |
| Pinne 2 | GPIO5 (TX) |
| Pinne 3 | GND |

UART: 115200 baud, 8 databiter, ingen paritet, 1 stoppbit. Kontroller signalnivåer før tilkobling; ESP32-C3 GPIO skal ikke tilføres 5 V. Originalfilen oppgir målt 5 V på AUX1 pinne 6, men strømkapasitet og oppførsel i dvale er ikke verifisert. Bruk en egnet, stabil og regulert forsyning til kortet. **AUX1 pinne 7 er oppgitt til omtrent 18 V og må aldri kobles direkte til ESP32-kortet.** Koble fra strøm før inngrep.

## Sikkerhet og begrensninger

- Bruk kun på egen klipper eller en du har tillatelse til å styre. Inngrep kan skade elektronikk og påvirke garanti og tetthet.
- Programvaren er ikke et sikkerhetssystem. Behold alle originale sikkerhetsfunksjoner. STOPP via Wi-Fi/UART er ingen erstatning for fysisk stopp og sikker frakobling ved vedlikehold. Hold personer og dyr unna ved testing.
- `secrets.yaml` skiller hemmeligheter fra kildekoden, men krypterer dem ikke på disk. PIN og øvrige hemmeligheter bygges inn i firmware. Ikke del firmware, byggemapper, generert C++, konfigurasjonsutskrifter, sikkerhetskopier eller rå UART-logger. UART-autentisering inneholder PIN-data.
- `.gitignore` beskytter mot vanlig utilsiktet innsjekking; den fjerner ikke allerede sporede filer eller Git-historikk. Kontroller innholdet før hver publisering. Roter hemmeligheter som faktisk er eksponert.
- Bruk API-kryptering, unike passord og et betrodd lokalt nett. Ikke videresend API- eller OTA-porter til internett.
- Ved manglende UART-svar i 60 sekunder markeres kontakt tapt. Gamle sensorverdier kan fortsatt vises og må behandles som historiske. Klipperens dvale eller bortfall av strøm til ESP32 kan gi «utilgjengelig» i Home Assistant. Oppsettet kan ikke vekke en strømløs enhet.
- Automatisk autentisering forsøkes etter ferskt svar når det ikke allerede er forsøkt i sesjonen. Ved avvist PIN: kontroller oppsettet; ikke trykk gjentatte ganger på autentisering. Klipperens egen låsing og begrensning av PIN-forsøk gjelder.
- Klokkesynk er manuell, gjelder bare klokkeslett og krever godkjent PIN, HA-tid og fersk status Parkert/Lader. Originalfilen rapporterer vellykket test under lading og avvisning under klipping. Dato og tidsplan skrives ikke.
- Protokolltolkning og kompatibilitet med andre modeller/firmware er ikke garantert. En kompilering erstatter ikke fysisk funksjonstest.

## Endringer fra v3.8

- Personlig PIN og API-nøkkel fjernet; verdier leses via `!secret`.
- PIN behandles som fire desimalsifre, også med innledende null; ugyldig format sender ingen PIN-kommando.
- OTA-passord via `!secret`; privat statisk nettverksoppsett erstattet med DHCP.
- Automatisk autentisering krever UART-svar yngre enn 30 sekunder.
- Originalfilen beholdes utenfor repoet. Kun den rensede konfigurasjonen distribueres.

## Opphav og dokumentasjon

Originalfilen krediterer Robomower V0.8, Wall-E v1.20 og diagnostikkideer fra AMConnect. Det medfølger ikke kildeadresser eller lisensdokumentasjon for disse bidragene. Derfor gis ingen ny åpen kildekode-lisens for hele materialet her; opphav og vilkår må avklares før videre lisensiering. Offentlig tilgjengelighet er ikke i seg selv en lisens.

- [ESPHome: YAML og secrets](https://esphome.io/guides/yaml/)
- [ESPHome: substitutions](https://esphome.io/components/substitutions/)
- [ESPHome: API-kryptering](https://esphome.io/components/api/)

Se `VALIDATION.md` for utførte kontroller og gjenværende begrensninger.

Repo-navnet viser til Generasjon 3; dette oppsettet er laget for Automower 310. Støtte for alle Gen3-modeller er ikke bekreftet.

