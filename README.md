# AKAI DISCORD BOT

## Funkcje:

- zarządzanie rolami
- nadawanie ról projektowych i technologicznych
- Komunikat Pomocy
- System punktów


## Setup do testów:
1. Załóż serwer discord o podobnej strukturze do serwera AKAI
2. Na discordzie włącz tryb developera, by umożliwić kopiowanie ID postów i emotikonów - [Jak to zrobić?](https://www.howtogeek.com/714348/how-to-enable-or-disable-developer-mode-on-discord/)
3. Stworzyć nową aplikację na [Discord Developer Portal](https://discord.com/developers/applications/.)
4. Po wejściu w aplikację na portalu dodać bota w zakładce Bot, dać mu. W sekcji Privileged Gateway Intents zaznaczyć wszystkie 3 *intenty*.
5. W zakładce OAuth2 zaznaczyć Authorization Method na In-App Authorization ustawić scope jako bot i applications.commands a w Bot Permissions ustawić Administrator
6. Uzupełniamy plik .env by Token zdobędziemy w zakładce Bot na portalu discord_log_channel zaś to ID kanału tekstowego na naszym serwerze gdzie będą wysyłane logi (pobrać to ID możemy klikając prawym przyciskiem myszy na kanał, jeśli aktywowaliśmy ustawienia developerskie)
7. W pliku db.yaml ustawiamy wartości wartości potrzebne do działania każdej z usług (więcej w przykładowym pliku) i ustawiamy flagę DB_LOAD_YAML_ON_START=true


## Odpalanie bota

### Python
1. `python -m venv env` - tworzymy environment w root folderze
2. Aktywujemy environment
   1. `./env/Scripts/activate` - Linux 
   2. `./env/Scripts/activate.ps1` - Windows
3. `pip install -r requirements.txt`  instalujemy dependencies
4. `python app.py` odpalamy bota

### Docker
1. `docker build -t akai-discord-bot:latest .` - budujemy image z `Dockerfile`
2. `docker run -d --name=akai-discord-bot akai-discord-bot` - tworzymy i odpalamy w tle kontener
3. Działanie z kontenerem
   1. `docker stop akai-discord-bot` zatrzymuje kontener
   2. `docker start akai-discord-bot` włącza kontener ponownie
   3. `docker exec -it akai-discord-bot bash` wbija bashem do kontenera
4. Remarks
   1. Aplikacja jest pod pathem `/app/`
   2. `docker rm {id kontenera sprawdzone np. docker ps}` w razie co gdyby potrzeba kontener usunąć (nowy build i tak nadpisuje poprzedni, więc pewnie nie będzie trzeba tego używać)


## Pomocne linki: 
- [SQLAlchemy](https://docs.sqlalchemy.org/en/14/orm/tutorial.html) - używany ORM  
- [DiscordAPI](https://discordpy.readthedocs.io/en/stable/api.html) - Discord.py sdk
- [Tryb developera na Discordzie](https://www.howtogeek.com/714348/)
- [Discord Developer Portal](https://discord.com/developers/applications/.)

Dane zawarte w bazie danych zawartej na repo również należy zmienić: ustawić własny id kanałow, id postów, emoty etc. Setupu troche jest ale jest intuicyjny. Z głównych rzeczy jest tam używany natywny logger, orm sqlalchemy (choc bardzo amatorsko) oraz discord.py sdk.


## Baza danych
Baza danych składa się z 6 tabel, każda z kolumn ma property not null:
 1. **commands** - mapuje komendy wpisane przez użytkownika po znaku $ do odpowiedzi;
    - command - TEXT
    - response - TEXT
 2. **helper_ranges** - określa dolne przedziały ról dla  rang helpera;
    - bottom_threshold - INT - PK
    - role_id - INT
 3. **helper_ranking** - przechowuje ilość punktów zdobytych przez każdego użytkownika;
    - user_id - INT - PK
    - points - INT - default 0
 4. **helper_rewards** - mapuje reakcje pod odpowiedziami na pytania do punktów którymi nagradzany jest odpowiadający;
    - emoji_name - TEXT - PK
    - reward - INT
 5. **messages_to_roles** - mapuje id wiadomości projektowej do roli która została dla tego projektu utworzona;
    - message_id - INT - PK
    - role_id - INT
 6. **settings** - zawiera pary key:value do konfiguracji bota
    - key - TEXT - PK
    - value - TEXT
Dodatkowo możemy wpisać wartości z YAML'a do bazy danych oraz ją wyczyścić ustawiając odpowiednią flagę w .env
