import requests
import os
import asyncio
from telegram import Bot

TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

bot = Bot(token=TOKEN)

# categorias populares
CATEGORIAS = [
    "MLB1000",  # eletrônicos
    "MLB1055",  # celulares
    "MLB1648",  # informática
    "MLB1574",  # casa
    "MLB1276",  # esportes
]

produtos_enviados = set()


def buscar_ofertas():

    ofertas = []

    for cat in CATEGORIAS:

        url = f"https://api.mercadolibre.com/sites/MLB/search?category={cat}&limit=50"

        try:
            data = requests.get(url).json()
        except:
            continue

        for item in data.get("results", []):

            preco = item.get("price")
            original = item.get("original_price")

            if not original:
                continue

            if original <= preco:
                continue

            desconto = int((original - preco) / original * 100)

            if desconto < 35:
                continue

            link = item.get("permalink")

            if link in produtos_enviados:
                continue

            produtos_enviados.add(link)

            ofertas.append({
                "titulo": item.get("title"),
                "preco": preco,
                "original": original,
                "desconto": desconto,
                "link": link,
                "img": item.get("thumbnail")
            })

    return ofertas[:10]


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

        try:

            await bot.send_photo(
                chat_id=CHAT_ID,
                photo=o["img"],
                caption=msg
            )

            await asyncio.sleep(2)

        except Exception as e:
            print("Erro:", e)


async def loop():

    while True:

        print("Buscando ofertas...")

        ofertas = buscar_ofertas()

        if ofertas:
            await enviar(ofertas)

        print("Aguardando 15 minutos...")

        await asyncio.sleep(900)


async def main():
    await loop()


if __name__ == "__main__":
    asyncio.run(main())