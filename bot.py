import requests
import os
import time
from telegram import Bot
import asyncio

TOKEN = os.getenv("8583131498:AAESbJgz-fC4SyC7VZbjeB120yHcyT6ANZI")
CHAT_ID = os.getenv("1003642280454")

bot = Bot(token=TOKEN)

def buscar_ofertas():
    url = "https://api.mercadolibre.com/sites/MLB/search?q=notebook"
    res = requests.get(url).json()

    ofertas = []

    for item in res["results"]:
        preco = item["price"]
        original = item.get("original_price")

        if original and original > preco:
            desconto = int((original - preco) / original * 100)

            if desconto >= 30:
                ofertas.append({
                    "titulo": item["title"],
                    "preco": preco,
                    "original": original,
                    "desconto": desconto,
                    "link": item["permalink"],
                    "img": item["thumbnail"]
                })

    return ofertas[:5]


async def enviar(ofertas):

    for o in ofertas:

        msg = f"""
🔥 OFERTA

{o['titulo']}

💰 R$ {o['preco']}
🏷️ De R$ {o['original']}
📉 {o['desconto']}% OFF

🛒 {o['link']}
"""

        await bot.send_photo(
            chat_id=CHAT_ID,
            photo=o["img"],
            caption=msg
        )


async def main():
    ofertas = buscar_ofertas()
    await enviar(ofertas)


while True:
    asyncio.run(main())
    time.sleep(900)
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