import requests
import os
import asyncio
from telegram import Bot

TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

bot = Bot(token=TOKEN)

BUSCAS = [
    "notebook",
    "iphone",
    "smartphone",
    "air fryer",
    "tv",
    "monitor",
    "ssd",
    "fone bluetooth",
    "cadeira gamer",
    "mouse gamer",
]

produtos_enviados = set()


def buscar_ofertas():

    ofertas = []

    for busca in BUSCAS:

        url = f"https://api.mercadolibre.com/sites/MLB/search?q={busca}&limit=50"

        try:
            res = requests.get(url)
            data = res.json()
        except Exception as e:
            print("Erro na API:", e)
            continue

        resultados = data.get("results", [])

        print(f"{busca}: {len(resultados)} produtos encontrados")

        for item in resultados:

            preco = item.get("price")
            original = item.get("original_price")

            if not original:
                continue

            if original <= preco:
                continue

            desconto = int((original - preco) / original * 100)

            if desconto < 20:
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

    print("Ofertas encontradas:", len(ofertas))

    return ofertas[:10]


async def enviar(ofertas):

    for o in ofertas:

        mensagem = f"""
🔥 OFERTA ENCONTRADA

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
                caption=mensagem
            )

            await asyncio.sleep(2)

        except Exception as e:
            print("Erro ao enviar:", e)


async def executar():

    print("Buscando ofertas...")

    ofertas = buscar_ofertas()

    if ofertas:
        await enviar(ofertas)
    else:
        print("Nenhuma oferta encontrada")


async def main():

    # mensagem de teste
    try:
        await bot.send_message(
            chat_id=CHAT_ID,
            text="🤖 Bot de ofertas iniciado com sucesso!"
        )
    except Exception as e:
        print("Erro ao enviar mensagem inicial:", e)

    while True:

        await executar()

        print("Aguardando 15 minutos...")

        await asyncio.sleep(900)


if __name__ == "__main__":
    asyncio.run(main())