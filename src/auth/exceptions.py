USER_EXISTS = "User %s already exists."
AFTER_REGISTER = "User %s has registered."
AFTER_LOGIN = "You have successfully logged in."
PASSWORD_LEN_ERROR = "Password should be at least 8 and at most 64 characters."
PASSWORD_UNIQUE_ERROR = "Password should not contain e-mail."
PASSWORD_STRENGTH_ERROR = "Password must contain a lowercase letter, uppercase letter, a number and a special symbol."
PASSWORD_CHANGE_SUCCESS = "The password has been changed."
OLD_PASS_INCORRECT = "Old password is incorrect."
PASSWORD_NOT_MATCH = "New passwords do not match."
DB_ERROR = "An unknown database error occurred."
UNIQUE_ERROR = "A user with this phone number already exists."
PASSWORD_DESC = "It should contain at least one lowercase, uppercase letter, one digit.\
                It should contain at least one special character from the following: @, #, $, %, ^, &, +, =, !. \
                The password should not be similar to the email name (the part before the @ symbol in the email address)."
EMAIL_BODY = """
<!DOCTYPE html>
<html lang="uk">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <style>
    .recovery-button {
      display: inline-block;
      padding: 10px 20px;
      text-decoration: none;
      border-radius: 5px;
      background-color: #d66600;
      color: #fff;
    }
    b {
    color: #fff;
    }
  </style>
</head>
<body>

<p>Вітаємо!</p>

<p>Ви отримали цього листа, тому що зробили запит на відновлення паролю для вашого облікового запису на сайті Cats for Future.</p>

<p>Для відновлення паролю, будь ласка, натисніть на кнопку нижче:</p>

<a class="recovery-button" href="https://localhost:3000/login/password-recovery/%s" target="_blank">
  <b>відновити пароль</b>
</a>

<p>Якщо ви не робили запит на відновлення паролю, просто проігноруйте це повідомлення.</p>

<p>З повагою,<br>Команда Cats for Future.</p>

</body>
</html>
"""
