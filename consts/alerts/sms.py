class System:
    SENDER = 'whatsapp:+14155238886'
    RECEIVER = 'whatsapp:+{phone_number}'

class Twilio:
    ACCOUNT_SID = 'ACb7d19b3ab3c7721b90afa5aae45e9cda'
    AUTH_TOKEN = '422e42e095b93a91767b6a6fb1b9db27'

class Templates:
    MATCHED_TICKERS_SMS = """
    Hey {username} 👋
    ⚠️ IStoBot ALERT ⚠️
    
    -------------------
    🚨 Alert from the following filters:
    -------------------
    {filters}
    
    -------------------
    Matched tickers📈
    -------------------
    {matched_wanted_tickers}
    """
    BUYING_ACTION_SMS = """
    IStoBot buy action done 📈:
    {ticker} | {units} units
    """
