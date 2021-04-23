from collections import namedtuple

GuildSettings = namedtuple('GuildSettings', ['id', 'verification'])
Verification = namedtuple('Verification', ['plaintext', 'encoded', 'cipher'])