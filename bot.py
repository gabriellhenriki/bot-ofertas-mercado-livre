import requests
import os
import asyncio
from telegram import Bot
from bs4 import BeautifulSoup

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
    "mouse gamer"
]

produtos_enviados = set()


def buscar_ofertas():

    ofertas = []

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    for busca in BUSCAS:

        url = f"https://lista.mercadolivre.com.br/{busca}"

        try:

            res = requests.get(url, headers=headers, timeout=15)

            if res.status_code != 200:
                print("Erro status:", res.status_code)
                continue

            soup = BeautifulSoup(res.text, "html.parser")

        except Exception as e:
            print("Erro:", e)
            continue

        produtos = soup.select(".ui-search-result")

        print(f"{busca}: {len(produtos)} produtos encontrados")

        for p in produtos[:10]:

            try:

                titulo = p.select_one(".ui-search-item__title").text

                preco = p.select_one(".price-tag-fraction").text

                link = p.select_one("a")["href"]

                img = p.select_one("img")["src"]

                if link in produtos_enviados:
                    continue

                produtos_enviados.add(link)

                ofertas.append({
                    "titulo": titulo,
                    "preco": preco,
                    "link": link,
                    "img": img
                })

            except:
                continue

    print("Ofertas encontradas:", len(ofertas))

    return ofertas[:5]


async def enviar(ofertas):

    for o in ofertas:

        mensagem = f"""
🔥 OFERTA

{o['titulo']}

💰 R$ {o['preco']}

🛒 Comprar:
{o['link']}
"""

        try:

            await bot.send_photo(
                chat_id=CHAT_ID,
                photo=o["img"],
                caption=mensagem
            )

            await asyncio.sleep(2)

        except Exception as e:
            print("Erro Telegram:", e)


async def executar():

    print("Buscando ofertas...")

    ofertas = buscar_ofertas()

    if ofertas:
        await enviar(ofertas)
    else:
        print("Nenhuma oferta encontrada")


async def main():

    try:
        await bot.send_message(
            chat_id=CHAT_ID,
            text="🤖 Bot de ofertas iniciado!"
        )
    except Exception as e:
        print("Erro mensagem inicial:", e)

    while True:

        await executar()

        print("Aguardando 15 minutos...")

        await asyncio.sleep(900)


if __name__ == "__main__":
    asyncio.run(main())