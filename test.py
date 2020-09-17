import unidecode
author = "Gonzalo Armúa and Jean Jores Pierre"
username_pre =''.join(e for e in author if e.isalnum())
username = unidecode.unidecode(username_pre)
print(username_pre)
print(username)