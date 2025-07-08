from dotenv import load_dotenv
load_dotenv()

import os
import re
import discord
from scraper import MusinsaAPI

# --- Discord 봇 기본설정 ----
intents = discord.Intents.default()
intents.message_content = True # 메시지 내용을 읽어오기 위한 권한 설정
client = discord.Client(intents=intents) 
# Disscord 클라이언트 인스턴스 생성


# --- 메시지 생성 디스플레이 화면(개발자) 헬퍼함수 --- #
def build_message(item):
    embed = discord.Embed(type="rich", title=item["name"], url=item["linkUrl"] )
    embed.set_thumbnail(url=item["imageUrl"])
    embed.description = item["brand"]
    embed.add_field(name="정가", value=item["normalPrice"], inline=True)
    embed.add_field(name="할인가", value=item["saleprice"], lnline=True)
    return embed


# --- bot이 실행될때 1회 호출되는 이벤트 -----
@client.event
async def on_ready():
    print("running file:", __file__)
    print(f"Loggid in as {client.user}") # 개발자가 디버그용으로 출력

last_recommendations: dict[int, dict] = {}

@client.event
async def on_message(message):
    # 봇 자신의 메시지에 반응하지 않도록 처리
    if message.author == client.user:
        return
    
    content = message.content.strip() # 채팅 내용 읽어오기 
    content_lower = content.lower() # 일관성 있게 소문자로 변환
    channel_id = message.channel.id # 채널 분기처리
    print(f"[디버그] 메시지 수신: {content!r}")

    # -- 기본 인사 및 간단 명령 분기 --
    if content_lower.startswith("$hello"):
        await message.channel.send("Hello!")
    elif content_lower.startswith("$hi"): 
        await message.channel.send("hi there!!") 
        return  

    GREEIINGS = {"안녕하세요", "안녕", "안녕하십니까"}
    if content_lower in GREEIINGS:
        await message.channel.send(f"{message.author.display_name}님, 안녕하세요!")
        return

    # 신발 추천 분기
    if ("신발추천" in content_lower or "신발 추천" in content_lower or content_lower == "신발"):
        await handle_recommendation(channel_id, message, "신발")
        return

    # 반팔추천 반팔 추천 티셔츠추천 티셔츠 추천
    if any(
        cmd in content_lower
        for cmd in ("반팔추천","반팔 추천","티셔츠추천","티셔츠 추천")
    ):
        await handle_recommendation(channel_id, message, "반팔")
        return
        # 필수: channel_id, message, keyword / 



# --- 헨들러 함수 모음 ---
async def handle_recommendation(
        channel_id, message, keyword, size=5, icon="👟", title=None
):
    """신발/반팔 등 추천 목록을 가져와서 전송"""
    page = 1 
    item = MusinsaAPI(keyword=keyword, page=page, size=size).fetch()
    last_recommendations[channel_id] = {
        "keyword" : keyword,
        "page" : page,
        "item" : item,
    }

    header = title or f"{icon} **{keyword} 추천 TOP{size}**"
    body = "\n".join(f"{i+1}. {it['name']} - {it['saleprice']}" for i, it in enumerate(item))
    # 1. 아디다스 - 68,000 제품설명

    # await message.channel.send(f"{header}\n{body}")
    await message.channel.send(f"{header}")
    for it in item:
        embed = build_message(it)
        await message.channel.send(embed=embed)


# -- 실행 진입점 ---
if __name__ == "__main__":
    token = os.getenv("DISCORD_TOKEN")
    if not token:
        raise RuntimeError("DISCORD_TOKEN 환경변수가 설정되지 않았습니다.")  
    client.run(token)