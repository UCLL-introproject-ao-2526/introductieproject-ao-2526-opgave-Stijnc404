## 27/05/2026 startdatum

Vandaag ben ik begonnen aan de tutorial om een blackjackspel te maken in Pygame.Ik heb eerder al een Snake-game en een Pac-Man-project heb gemaakt, voelde de basis van Pygame redelijk vertrouwd aan. Daardoor ging de start vlotjes.

Tijdens het maken van de knoppen liep ik tegen mijn eerste fout aan. Was even verwarrend want de tekst van de knop “STAND” verscheen bovenop “HIT ME”. Mijn eerste gedachte was dat er iets mis was met coordinaten en dat was ook zo ik had de coordinaten gecopy-paste van "HIT ME" en vergeten aan te passen.

## 28/05/2026

Vandaag heb ik verder gewerkt aan mijn blackjack project in pygame. Vergeleken met gisteren is het project al veel uitgebreider geworden. Ik heb functies toegevoegd voor het delen van kaarten, het berekenen van scores, het tonen van de kaarten op het scherm en het tonen van de score van zowel de speler als de dealer. Ik merk dat de code ondertussen groot genoeg wordt dat ik nood heb om mijn functies toe te klappen want anders nam het me veel meer tijd om fouten te zoeken. Want die lange functies waren in het begin wat frustrerend, omdat ik gewoon een vogelnest zag.

Het moeilijkste vandaag was niet echt het programmmeren, maar volgen wat de tutorial precies deed. Soms veranderde de maker van de tutorial zelf stukken code omdat hij vond dat iets niet klopte of niet nodig was. Daardoor had ik een paar momenten waar mijn game plots crashte terwijl ik dacht dat ik alles correct had overgenomen. Ik moest dus zelf beginnen nadenken over waarom iets fout liep in plaats van gewoon de tutorial letterlijk te volgen.

Een fout waar ik lang op gezocht heb zat in deze lijn:

if hand[i] in cards[8]['10', 'J', 'Q', 'K']
(kreeg een syntax error in de lijn maar hij zei specifiek niet waar de fout zat wanneer ik het runde)

Ik dacht eerst dat het probleem was door een dubbel punt misschien niet geplaatst te hebben of dat de kaarten verkeerd gedeeld werden. Uiteindelijk bleek dat de syntax gewoon fout was. Het moest eigenlijk zijn:

if hand[i] in ['10', 'J', 'Q', 'K']

Toen ik dat aangepast had werkte de scoreberekening meteen correct. ik heb mij beseft erna dat dus een klein syntax error de hele game kan doen crashen haha.

Ik heb ook een paar andere bugs gehad waarbij functies niet de juiste argumenten kregen of waarbij variabelen door elkaar gebruikt werden. In plaats van direct random dingen te veranderen ben ik deze keer meer beginnen kijken naar de foutmeldingen in de terminal. Dat hielp veel meer dan ik verwacht had. Vaak stond de oplossing eigenlijk bijna letterlijk in de error message, maar in het begin negeerde ik die te veel.

Wat ik in de toekomst anders wil doen is vaker kleine stukken code testen in plaats van heel veel tegelijk toe te voegen. Vandaag merkte ik dat bugs veel makkelijker te vinden zijn wanneer ik na elke kleine aanpassing het programma opnieuw run. Ook wil ik beter opletten wanneer een tutorialmaker iets aanpast, want soms veranderde ik niet alles mee waardoor stukken code niet meer overeenkwamen.
