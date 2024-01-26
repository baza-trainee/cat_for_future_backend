AFTER_CAT_CREATE = "Cat section has created successfully."
NO_DATA_FOUND = "Cats not found"
SERVER_ERROR = "Server error has occurred."
CAT_EXISTS = "Cat with name: %s already exists."
NO_RECORD = "Cat not found."
SUCCESS_DELETE = "Cat with id: `%s` was successfully deleted."
DATE_ERROR = "Invalid date format. Expected format: %d-%m-%Y"
RESERVED = "Cat reserved successfully."
RESERVED_ERROR = "Cat is already reserved."
CANCELED = "Cat reservation canceled."
CANCEL_ERROR = "You can't cancel reservation for this cat."
CAT_MAIL = """
<!DOCTYPE html>
<html lang="uk">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
    </head>
    <body>
        <p>Вітаємо!</p>
        <p>Кота %s заброньовано 😊 </p>
        <p>Контактні дані майбутнього власника:</p>
        <p>Ім'я: %s</p>
        <p>Номер телефону: %s.</p>
        <p>Пошта: %s.</p>
        <p>Зв'яжіться з ним найближчим часом, щоб узгодити деталі.</p>
        <p>З повагою,<br>Команда Cats for Future.</p>
    </body>
</html>
"""
