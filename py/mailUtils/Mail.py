class Mail:
    Subject = ''
    To = []
    From = ''
    Date = ''
    Content = ''
    attachments = []
    Type = 'plain'
    charset = 'utf-8'
    uid = ''

    def __str__(self) -> str:
        result = """
From: {0.From!s}
Subject: {0.Subject!s}
To: {0.To!s}
Date: {0.Date!s}
Attachments: {0.attachments!s}
Content: 
{0.Content!s}
        """.format(self)
        return result

