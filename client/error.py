class AccessError(Exception):
    def __init__(self):
        error = "L'identifiant de la personne n'existe ou la personne n'a pas accès à la salle"
        super().__init__(error)


class PwdError(Exception):
    def __init__(self):
        error = "Mot de passe incorrect après 3 tentative connexion interrompue"
        super().__init__(error)


class RoomError(Exception):
    def __init__(self):
        error = "L'identifiant de la salle n'existe pas"
        super().__init__(error)


class ConnectError(Exception):
    def __init__(self, host, port):
        self.host = host
        self.port = str(port)
        super().__init__(self)

    def __str__(self):
        return "Echec de connection vers le serveur (" + self.host + "," + self.port + ")"


class TimeOutServer(Exception):
    def __init__(self):
        message = "[CONNECTION INTERRUPTED] Le serveur a mis trop de temps à répondre"
        super().__init__(message)
