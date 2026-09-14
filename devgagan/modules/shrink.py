 
# ---------------------------------------------------
# File Name: shrink.py
# Description: A Pyrogram bot for downloading files from Telegram channels or groups 
#              and uploading them back to Telegram.
# Author: Elexyz
# Created: 2025-01-11
# Last Modified: 2025-01-11
# Version: 2.0.5
# License: MIT License
# ---------------------------------------------------

from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import random
import requests
import string
import aiohttp
import json
from devgagan import app
from devgagan.core.func import *
from devgagan.core.get_func import get_log_topic_id
from datetime import datetime, timedelta
from motor.motor_asyncio import AsyncIOMotorClient
from config import MONGO_DB, WEBSITE_URL, AD_API, LOG_GROUP  
 
 
tclient = AsyncIOMotorClient(MONGO_DB)
tdb = tclient["telegram_bot"]
token = tdb["tokens"]
 
 
async def create_ttl_index():
    await token.create_index("expires_at", expireAfterSeconds=0)
 
 
 
Param = {}
 
 
async def generate_random_param(length=8):
    """Generate a random parameter."""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))


async def get_random_anime_image():
    """Get a random anime image from API."""
    try:
        # Try multiple anime APIs for better reliability
        anime_apis = [
            "https://api.waifu.pics/sfw/waifu",
            "https://api.waifu.pics/sfw/neko", 
            "https://api.waifu.pics/sfw/shinobu",
            "https://api.waifu.pics/sfw/megumin",
            "https://api.waifu.pics/sfw/bully",
            "https://api.waifu.pics/sfw/cuddle",
            "https://api.waifu.pics/sfw/cry",
            "https://api.waifu.pics/sfw/hug",
            "https://api.waifu.pics/sfw/awoo",
            "https://api.waifu.pics/sfw/kiss",
            "https://api.waifu.pics/sfw/lick",
            "https://api.waifu.pics/sfw/pat",
            "https://api.waifu.pics/sfw/smug",
            "https://api.waifu.pics/sfw/bonk",
            "https://api.waifu.pics/sfw/yeet",
            "https://api.waifu.pics/sfw/blush",
            "https://api.waifu.pics/sfw/smile",
            "https://api.waifu.pics/sfw/wave",
            "https://api.waifu.pics/sfw/highfive",
            "https://api.waifu.pics/sfw/handhold",
            "https://api.waifu.pics/sfw/nom",
            "https://api.waifu.pics/sfw/bite",
            "https://api.waifu.pics/sfw/glomp",
            "https://api.waifu.pics/sfw/slap",
            "https://api.waifu.pics/sfw/kill",
            "https://api.waifu.pics/sfw/kick",
            "https://api.waifu.pics/sfw/happy",
            "https://api.waifu.pics/sfw/wink",
            "https://api.waifu.pics/sfw/poke",
            "https://api.waifu.pics/sfw/dance",
            "https://api.waifu.pics/sfw/cringe"
        ]
        
        # Select random API endpoint
        api_url = random.choice(anime_apis)
        
        async with aiohttp.ClientSession() as session:
            async with session.get(api_url, timeout=10) as response:
                if response.status == 200:
                    data = await response.json()
                    if data.get("url"):
                        return data["url"]
        
        # Fallback to alternative API
        async with aiohttp.ClientSession() as session:
            async with session.get("https://nekos.best/api/v2/neko", timeout=10) as response:
                if response.status == 200:
                    data = await response.json()
                    if data.get("results") and len(data["results"]) > 0:
                        return data["results"][0]["url"]
        
        # Final fallback to static images
        fallback_images = [
            "https://i.ibb.co/PsdkZnMp/497a1d136932.jpg",
            "https://i.ibb.co/8XqJYzK/anime1.jpg",
            "https://i.ibb.co/9y8KxL2/anime2.jpg", 
            "https://i.ibb.co/7QpR9sM/anime3.jpg",
            "https://i.ibb.co/4Y8nKxL/anime4.jpg"
        ]
        return random.choice(fallback_images)
        
    except Exception as e:
        # Return fallback image if all APIs fail
        return "https://i.ibb.co/PsdkZnMp/497a1d136932.jpg"
 
 
async def get_shortened_url(deep_link):
    api_url = f"https://{WEBSITE_URL}/api?api={AD_API}&url={deep_link}"
 
     
    async with aiohttp.ClientSession() as session:
        async with session.get(api_url) as response:
            if response.status == 200:
                data = await response.json()   
                if data.get("status") == "success":
                    return data.get("shortenedUrl")
    return None
 
 
async def is_user_verified(user_id):
    """Check if a user has an active session."""
    session = await token.find_one({"user_id": user_id})
    return session is not None
 
 
@app.on_message(filters.command("start"))
async def token_handler(client, message):
    """Handle the /token command."""
    join = await subscribe(client, message)
    if join == 1:
        return
    chat_id = "save_restricted_content_bots"
    msg = await app.get_messages(chat_id, 796)
    user_id = message.chat.id
    if len(message.command) <= 1:
        # Get random anime image for each user
        image_url = await get_random_anime_image()
        join_button = InlineKeyboardButton("Join Channel", url="https://t.me/ElexyzBots")
        DEVLOPER = InlineKeyboardButton("DEVLOPER", url="https://t.me/Elexyz")   
        keyboard = InlineKeyboardMarkup([
            [join_button],   
            [DEVLOPER]    
        ])
         
        await message.reply_photo(
            image_url,
            caption=(
                "**🎌 Konnichiwa! Welcome to Elexyz Bot! 👋**\n\n"
                "> **🌟 I'm your ultimate content saver bot!**\n"
                "> **📱 Save posts from channels/groups where forwarding is disabled**\n"
                "> **🎵 Download videos & audio from YouTube, Instagram & 30+ platforms**\n"
                "> **⚡ Batch processing with premium features**\n"
                "> **🔒 Secure & fast downloads**\n\n"
                "**📋 How to use:**\n"
                "> **• Send any public channel post link**\n"
                "> **• For private channels: use /login**\n"
                "> **• Get help: send /help**\n"
                "> **• Get free token: send /token**\n\n"
                "**🚀 Ready to explore? Let's get started!**\n\n"
                "**__💫 Powered by Elexyz 💫__**"
            ),
            reply_markup=keyboard
        )
        return  
 
    param = message.command[1] if len(message.command) > 1 else None
    freecheck = await chk_user(message, user_id)
    if freecheck != 1:
        await message.reply("You are a premium user no need of token 😉")
        return
 
     
    if param:
        if user_id in Param and Param[user_id] == param:
             
            await token.insert_one({
                "user_id": user_id,
                "param": param,
                "created_at": datetime.utcnow(),
                "expires_at": datetime.utcnow() + timedelta(hours=3),
            })
            del Param[user_id]   
            
            # Send verification success with random anime image
            success_image = await get_random_anime_image()
            await message.reply_photo(
                success_image,
                caption=(
                    "**🎉 Verification Successful! Welcome to Elexyz! 🎉**\n\n"
                    "> **✅ Your free session is now active!**\n"
                    "> **⏰ Duration: 3 hours of unlimited access**\n"
                    "> **🚀 All premium features unlocked**\n"
                    "> **📦 Batch limit: FreeLimit + 20**\n"
                    "> **⚡ No time restrictions**\n\n"
                    "**🎯 What you can do now:**\n"
                    "> **• Download from private channels**\n"
                    "> **• Use batch processing**\n"
                    "> **• Access all bot features**\n"
                    "> **• Enjoy premium experience**\n\n"
                    "**🌟 Happy downloading! 🌟**\n\n"
                    "**__💫 Powered by Elexyz 💫__**"
                )
            )
            return
        else:
            await message.reply("❌ Invalid or expired verification link. Please generate a new token.")
            return

    await get_log_topic_id(user_id, client)
 
@app.on_message(filters.command("token"))
async def smart_handler(client, message):
    user_id = message.chat.id
     
    freecheck = await chk_user(message, user_id)
    if freecheck != 1:
        await message.reply("You are a premium user no need of token 😉")
        return
    if await is_user_verified(user_id):
        # Send active session message with random anime image
        active_image = await get_random_anime_image()
        await message.reply_photo(
            active_image,
            caption=(
                "**🎊 Your Free Session is Already Active! 🎊**\n\n"
                "> **✅ Session Status: ACTIVE**\n"
                "> **⏰ Enjoying unlimited access**\n"
                "> **🚀 All premium features available**\n"
                "> **📦 Enhanced batch processing**\n"
                "> **⚡ No time restrictions**\n\n"
                "**🎯 You can now:**\n"
                "> **• Download from any channel**\n"
                "> **• Use batch commands**\n"
                "> **• Access all bot features**\n"
                "> **• Enjoy premium experience**\n\n"
                "**🌟 Keep exploring and downloading! 🌟**\n\n"
                "**__💫 Powered by Elexyz 💫__**"
            )
        )
    else:
         
        param = await generate_random_param()
        Param[user_id] = param   

         
        deep_link = f"https://t.me/{client.me.username}?start={param}"

         
        shortened_url = await get_shortened_url(deep_link)
        if not shortened_url:
            await message.reply("❌ Failed to generate the token link. Please try again.")
            return

         
        button = InlineKeyboardMarkup(
            [[InlineKeyboardButton("Verify the token now...", url=shortened_url)]]
        )
        
        # Send token generation message with random anime image
        token_image = await get_random_anime_image()
        await message.reply_photo(
            token_image,
            caption=(
                "**🎫 Free Access Token Generated! 🎫**\n\n"
                "> **🔗 Click the button below to verify your token**\n\n"
                "**🎁 What you'll get with this token:**\n"
                "> **⏰ 3 hours of unlimited access**\n"
                "> **📦 Batch limit: FreeLimit + 20**\n"
                "> **🚀 All premium features unlocked**\n"
                "> **⚡ No time restrictions**\n"
                "> **🔒 Access to private channels**\n"
                "> **🎵 Download from 30+ platforms**\n"
                "> **📱 Enhanced batch processing**\n\n"
                "**🎯 Features you'll unlock:**\n"
                "> **• Private channel downloads**\n"
                "> **• Batch processing**\n"
                "> **• Premium download speeds**\n"
                "> **• All bot functions**\n\n"
                "**🌟 Don't miss this opportunity! 🌟**\n\n"
                "**__💫 Powered by Elexyz 💫__**"
            ),
            reply_markup=button
        )


@app.on_message(filters.command("id"))
async def id_handler(client, message):
    """Handle the /id command to show user ID."""
    join = await subscribe(client, message)
    if join == 1:
        return
    
    user_id = message.chat.id
    user = message.from_user
    
    # Get random anime image for the ID display
    id_image = await get_random_anime_image()
    
    # Create user info caption
    caption = (
        "**🆔 Your User Information 🆔**\n\n"
        f"**👤 User ID:** `{user_id}`\n"
        f"**📝 Username:** @{user.username if user.username else 'Not Set'}\n"
        f"**📛 First Name:** {user.first_name if user.first_name else 'Not Set'}\n"
        f"**📛 Last Name:** {user.last_name if user.last_name else 'Not Set'}\n"
        f"**🔗 Profile Link:** [Click Here](tg://user?id={user_id})\n\n"
        "**💡 Tips:**\n"
        "> **• Share your User ID with admins for support**\n"
        "> **• Use this ID for premium activation**\n"
        "> **• Keep your ID safe and private**\n\n"
        "**__💫 Powered by Elexyz 💫__**"
    )
    
    await message.reply_photo(
        id_image,
        caption=caption,
        parse_mode="markdown"
    )
 
