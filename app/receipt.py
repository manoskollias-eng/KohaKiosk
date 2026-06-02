from pathlib import Path
from datetime import datetime


RECEIPTS_DIR = Path("receipts")


def create_receipt(patron_barcode, books):

    RECEIPTS_DIR.mkdir(exist_ok=True)

    timestamp = datetime.now()

    filename = (
        f"receipt_{timestamp.strftime('%Y%m%d_%H%M%S')}.txt"
    )

    filepath = RECEIPTS_DIR / filename

    with open(filepath, "w", encoding="utf-8") as f:

        f.write("==================================\n")
        f.write("          ΒΙΒΛΙΟΘΗΚΗ\n")
        f.write("==================================\n\n")

        f.write(f"Μέλος: {patron_barcode}\n\n")

        f.write("Δανεισμένα βιβλία\n\n")

        for book in books:
            f.write(f"- {book}\n")

        f.write("\n")
        f.write(
            f"Ημερομηνία: "
            f"{timestamp.strftime('%d/%m/%Y %H:%M:%S')}\n"
        )

        f.write("\n==================================\n")

    return str(filepath)