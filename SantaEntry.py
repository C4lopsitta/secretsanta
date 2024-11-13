
class SantaEntry:
    def __init__(self,
                 email_address: str,
                 name: str,
                 store_id: str):
        self.email_address = email_address
        self.name = name
        self.store_id = store_id

    def to_dict(self):
        return {
            "name": self.name,
            "email_address": self.email_address
        }

