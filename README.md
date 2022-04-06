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


## Pomocne linki: 
- [SQLAlchemy](https://docs.sqlalchemy.org/en/14/orm/tutorial.html)
- [DiscordAPI](https://discordpy.readthedocs.io/en/stable/api.html) 
Do developmentu trzeba założyć własny serwer discord, oraz aplikacje na platformie developerskiej  
- Do kopiowania ID postów, emotikon etc można enablować tryb developerski w discordzie https://www.howtogeek.com/714348/how-to-enable-or-disable-developer-mode-on-discord/.  

Dane zawarte w bazie danych zawartej na repo również należy zmienić: ustawić własny id kanałow, id postów, emoty etc. Setupu troche jest ale jest intuicyjny. Z głównych rzeczy jest tam używany natywny logger, orm sqlalchemy (choc bardzo amatorsko) oraz discord.py sdk.
