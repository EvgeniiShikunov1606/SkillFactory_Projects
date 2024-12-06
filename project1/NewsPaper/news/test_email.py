import smtplib

server = smtplib.SMTP_SSL('smtp.yandex.ru', 465)
server.login('evgeniishikunov1998@ya.ru', 'imhhtexgtapbewlg')
server.sendmail(
    'evgeniishikunov1998@ya.ru',
    ['recipient@example.com'],
    'Subject: Test\n\nHello!'
)
server.quit()
