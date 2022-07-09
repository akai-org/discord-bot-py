# AKAI DISCORD BOT

## Funkcje:

- zarządzanie rolami
- nadawanie ról projektowych i technologicznych
- system punktów
- wrzucanie wydarzeń z AKAI-owego kalendarza Google na serwer jako wydarzenia Discord
- automatycznie tworzenie wątków na kanale informacyjnym


## Setup do testów:
1. Załóż serwer discord o podobnej strukturze do serwera AKAI
   1. Wymagane kanały (nazwy nie mają znaczenia):
      1. `cli` - kanał do tworzenia roli na kanałach przez komendy
      2. `projects` - kanał, na którym pojawiają się wiadomości o projektach
      3. `tech` - kanał, na którym pojawiają się wiadomości o technologiach
      4. `thread` - kanał, na którym mają się automatycznie tworzyć wątki przy każdej wiadomości
      5. `ranking` - kanał z rankingiem najbardziej pomocnych członków
   2. Wymagane role:
      1. Role uzyskiwane za pomoc innym, nie musi być ich dużo, byle było co wkleić w kroku 7.
   3. Wymagane emoji:
      1. Przynajmniej jedno customowe, przypisane do ilości punktów za pomoc
   4. Opcjonalne kanały:
      1. `log` - kanał z logami, id podawane w `.env`
2. Na discordzie włącz tryb developera, by umożliwić kopiowanie ID postów i emotikonów - [Jak to zrobić?](https://www.howtogeek.com/714348/how-to-enable-or-disable-developer-mode-on-discord/)
3. Stworzyć nową aplikację na [Discord Developer Portal](https://discord.com/developers/applications/.)
4. Po wejściu w aplikację na portalu dodać bota w zakładce Bot, w sekcji Privileged Gateway Intents zaznaczyć wszystkie 3 *intenty*.
5. W zakładce OAuth2 zaznaczyć Authorization Method na In-App Authorization ustawić scope jako bot i applications.commands a w Bot Permissions ustawić Administrator
6. Uzupełniamy plik `.env`.
   1. Token zdobędziemy w zakładce Bot na portalu
   2. `DISCORD_LOG_CHANNEL` zaś to ID kanału tekstowego na naszym serwerze gdzie będą wysyłane logi 
7. W pliku `db.yaml` ustawiamy wartości potrzebne do działania każdej z usług (więcej w przykładowym pliku) i ustawiamy flagę `DB_LOAD_YAML_ON_START` na wartość `1`.


## Odpalanie bota

### Python
1. `python -m venv env` - tworzymy environment w root folderze
2. Aktywujemy environment
   1. `source ./env/Scripts/activate` - Linux 
   2. `.\env\Scripts\activate.ps1` - Windows
3. `pip install -r requirements.txt` - instalujemy dependencies
4. `python app.py` - odpalamy bota

### Docker
1. `docker build -t akai-discord-bot:latest .` - budujemy image z `Dockerfile`
2. `docker run -d --name=akai-discord-bot akai-discord-bot` - tworzymy i odpalamy w tle kontener
3. Działanie z kontenerem
   1. `docker stop akai-discord-bot` zatrzymuje kontener
   2. `docker start akai-discord-bot` włącza kontener ponownie
   3. `docker exec -it akai-discord-bot bash` wbija bashem do kontenera
4. Remarks
   1. Aplikacja jest pod path `/app/`
   2. `docker rm {id kontenera sprawdzone np. docker ps}` w razie co, gdyby potrzeba kontener usunąć (nowy build i tak nadpisuje poprzedni, więc pewnie nie będzie trzeba tego używać)


## Pomocne linki: 
- [SQLAlchemy](https://docs.sqlalchemy.org/en/14/orm/tutorial.html) - używany ORM  
- [DiscordAPI](https://discordpy.readthedocs.io/en/stable/api.html) - Discord.py SDK
- [Discord Developer Portal](https://discord.com/developers/applications/.)

Dane zawarte w bazie danych zawartej na repo również należy zmienić: ustawić własny id kanałów, emoty etc. Setupu trochę jest, ale jest on intuicyjny. Z głównych rzeczy: używamy natywnego loggera, orm sqlalchemy oraz discord.py SDK.


## Baza danych

Baza danych składa się z 6 tabel, każda z kolumn ma property not null. Możemy je dodatkowo podzielić na te zarządzane
przez admina i te zarządzane wyłącznie przez bota.

* Tabele admina:
   1. **commands** - mapuje _"quick-response-only"_ komendy wpisane przez użytkownika po znaku $, do krótkich
      odpowiedzi;
      - `command` - TEXT
      - `response` - TEXT
   2. **helper_ranges** - określa dolne przedziały ról dla rang helpera;
      - `bottom_threshold` - INT - PK
      - `role_id` - INT
   3. **settings** - zawiera pary key:value do konfiguracji bota
      - `key` - TEXT - PK
      - `value` - TEXT
* Tabele bota:
   1. **helper_ranking** - przechowuje ilość punktów zdobytych przez każdego użytkownika;
      - `user_id` - INT - PK
      - `points` - INT - default 0
   2. **helper_rewards** - mapuje reakcje pod odpowiedziami na pytania do punktów, którymi nagradzany jest
      odpowiadający;
      - `emoji_name` - TEXT - PK (trzeba tu podawać nazwy jedynie custom-owych emoji, te Discordowe są parsowane z UTF-8 znaków emotkowych)
      - `reward` - INT
   3. **messages_to_roles** - mapuje id wiadomości projektowej do roli, która została dla tego projektu utworzona;
      - `message_id` - INT - PK
      - `role_id` - INT

Dodatkowo możemy załadować wartości z YAML-a do bazy danych lub ją wyczyścić ustawiając odpowiednią flagę w `.env`.
