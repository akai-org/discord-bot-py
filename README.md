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
7. W tabeli settings w bazie danych zmieniamy bot_channel_id na ID kanału na którym będziemy wydawać polecenia Botowi


## Pomocne linki: 
- [SQLAlchemy](https://docs.sqlalchemy.org/en/14/orm/tutorial.html) - używany ORM  
- [DiscordAPI](https://discordpy.readthedocs.io/en/stable/api.html) - Discord.py sdk
- [Tryb developera na Discordzie](https://www.howtogeek.com/714348/)
- [Discord Developer Portal](https://discord.com/developers/applications/.)

