import requests
import os
from telegram import Bot

TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

bot = Bot(token=TOKEN)

def buscar_ofertas():
    url = "https://api.mercadolibre.com/sites/MLB/search?q=eletronicos"

    res = requests.get(url).json()

    ofertas = []

    for item in res["results"]:
        preco = item["price"]
        original = item.get("original_price")

        if original and original > preco:
            desconto = round((original - preco) / original * 100)

            if desconto >= 30:
                ofertas.append({
                    "titulo": item["title"],
                    "preco": preco,
                    "original": original,
                    "desconto": desconto,
                    "link": item["permalink"],
                    "imagem": item["thumbnail"]
                })

    return ofertas[:5]


def enviar_telegram(ofertas):
    for o in ofertas:

        mensagem = f"""
🔥 OFERTA ENCONTRADA

{ o['titulo'] }

💰 R$ {o['preco']}
🏷️ De: R$ {o['original']}
📉 Desconto: {o['desconto']}%

🛒 Comprar:
{o['link']}
"""

        bot.send_photo(
            chat_id=CHAT_ID,
            photo=o["imagem"],
            caption=mensagem
        )


def main():
    ofertas = buscar_ofertas()
    enviar_telegram(ofertas)


if __name__ == "__main__":
    main()