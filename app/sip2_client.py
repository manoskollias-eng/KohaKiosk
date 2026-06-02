class DemoSIP2Client:
    def __init__(self):
        self.patrons = {
            "1001": {
                "name": "Demo User",
                "status": "OK",
                "loans": []
            }
        }

        self.items = {
            "B001": {
                "title": "Python για Αρχάριους",
                "status": "available"
            },
            "B002": {
                "title": "Εισαγωγή στο Koha",
                "status": "available"
            }
        }

    def patron_info(self, patron_barcode):
        patron = self.patrons.get(patron_barcode)

        if not patron:
            return {
                "success": False,
                "message": "Το μέλος δεν βρέθηκε"
            }

        return {
            "success": True,
            "message": "Το μέλος βρέθηκε",
            "patron": patron
        }

    def checkout(self, patron_barcode, item_barcode):
        patron = self.patrons.get(patron_barcode)
        item = self.items.get(item_barcode)

        if not patron:
            return {
                "success": False,
                "message": "Το μέλος δεν βρέθηκε"
            }

        if not item:
            return {
                "success": False,
                "message": "Το βιβλίο δεν βρέθηκε"
            }

        if item["status"] != "available":
            return {
                "success": False,
                "message": "Το βιβλίο δεν είναι διαθέσιμο"
            }

        item["status"] = "loaned"
        patron["loans"].append(item_barcode)

        return {
            "success": True,
            "message": "Ο δανεισμός ολοκληρώθηκε",
            "title": item["title"]
        }

    def checkin(self, item_barcode):
        item = self.items.get(item_barcode)

        if not item:
            return {
                "success": False,
                "message": "Το βιβλίο δεν βρέθηκε"
            }

        item["status"] = "available"

        for patron in self.patrons.values():
            if item_barcode in patron["loans"]:
                patron["loans"].remove(item_barcode)

        return {
            "success": True,
            "message": "Η επιστροφή ολοκληρώθηκε",
            "title": item["title"]
        }