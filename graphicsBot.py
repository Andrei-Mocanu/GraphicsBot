import discord
import numpy as np
import random
import json
from PIL import Image
from discord.ext import commands
from discord.ext.commands.cooldowns import BucketType

TOKEN = "OTQ1MDU2MDMxODk2MTQxODc0.YhKmBA.aFT8x8ZSpQoZO3tmOyp97X295cY"

client = discord.Client()
client = commands.Bot(command_prefix = ['gpu ','Gpu'])

@client.event
async def on_ready():
    print("Bot is ready")


@client.command()
async def grayscale(ctx):
    filename = (ctx.author.name + "avatar.png")
    await ctx.author.avatar_url.save(filename)
    image = Image.open(filename)
    imgArray = np.array(image)
    print(imgArray.shape)
    for i in imgArray:
        for j in i:
            culoare = 0.21 * j[0] + 0.71 * j[1] + 0.07 * j[2]
            j[0] = culoare
            j[1] = culoare
            j[2] = culoare
    im = Image.fromarray(imgArray)
    im.save(ctx.author.name + "avatarGreyscale.png")
    await ctx.send(file=discord.File(ctx.author.name + "avatarGreyscale.png"))

@client.command()
async def sobel(ctx):
    filename = (ctx.author.name + "avatar.png")
    await ctx.author.avatar_url.save(filename)
    image = Image.open(filename)
    imgArray = np.array(image)
    sobelArray = np.zeros_like(imgArray)
    shape = imgArray.shape
    for i in range(shape[0]):
        for j in range(shape[1]):
            if i < shape[0] - 1 and j < shape[1] - 1 and i > 1 and j > 1:
                dX = abs(offsetToGreyscale(imgArray,i + 1 , j + 1)
                    + 2 * offsetToGreyscale(imgArray,i + 1 ,j)
                    + offsetToGreyscale(imgArray, i + 1 , j - 1)
                    - offsetToGreyscale(imgArray,i - 1 , j + 1)
                    - 2 *offsetToGreyscale(imgArray,i - 1, j)
                    - offsetToGreyscale(imgArray,i - 1,j - 1))

                dY = abs(offsetToGreyscale(imgArray,i + 1 , j + 1)
                    + 2 * offsetToGreyscale(imgArray,i  ,j + 1)
                    + offsetToGreyscale(imgArray, i - 1 , j + 1)
                    - offsetToGreyscale(imgArray,i + 1 , j - 1)
                    - 2 *offsetToGreyscale(imgArray,i , j - 1)
                    - offsetToGreyscale(imgArray,i - 1,j - 1))

                sobelValue = dX + dY
                sobelArray[i][j][0] = sobelValue
                sobelArray[i][j][1] = sobelValue
                sobelArray[i][j][2] = sobelValue
    im = Image.fromarray(sobelArray)
    im.save(ctx.author.name + "avatarSobel.png")
    await ctx.send(file=discord.File(ctx.author.name + "avatarSobel.png"))

@client.command()
async def roberts(ctx):
    filename = (ctx.author.name + "avatar.png")
    await ctx.author.avatar_url.save(filename)
    image = Image.open(filename)
    imgArray = np.array(image)
    robertsArray = np.zeros_like(imgArray)
    shape = imgArray.shape
    for i in range(shape[0]):
        for j in range(shape[1]):
            if i < shape[0] - 1 and j < shape[1] - 1 and i > 1 and j > 1:
                dPlus = abs(offsetToGreyscale(imgArray,i + 1, j + 1))
                - offsetToGreyscale(imgArray,i,j)
                dMinus = abs(offsetToGreyscale(imgArray,i , j + 1)) 
                - offsetToGreyscale(imgArray, i + 1, j)
                d = dPlus + dMinus
                robertsArray[i][j][0] = d
                robertsArray[i][j][1] = d
                robertsArray[i][j][2] = d
    im = Image.fromarray(robertsArray)
    im.save(ctx.author.name + "avatarRoberts.png")
    await ctx.send(file=discord.File(ctx.author.name + "avatarRoberts.png"))


@client.command()
async def prewitt(ctx):
    filename = (ctx.author.name + "avatar.png")
    await ctx.author.avatar_url.save(filename)
    image = Image.open(filename)
    imgArray = np.array(image)
    prewittArray = np.zeros_like(imgArray)
    shape = imgArray.shape
    for i in range(shape[0]):
        for j in range(shape[1]):
            if i < shape[0] - 1 and j < shape[1] - 1 and i > 1 and j > 1:
                dX = abs(offsetToGreyscale(imgArray,i + 1 , j + 1)
                    +  offsetToGreyscale(imgArray,i + 1 ,j)
                    + offsetToGreyscale(imgArray, i + 1 , j - 1)
                    - offsetToGreyscale(imgArray,i - 1 , j + 1)
                    - offsetToGreyscale(imgArray,i - 1, j)
                    - offsetToGreyscale(imgArray,i - 1,j - 1))

                dY = abs(offsetToGreyscale(imgArray,i + 1 , j + 1)
                    + offsetToGreyscale(imgArray,i  ,j + 1)
                    + offsetToGreyscale(imgArray, i - 1 , j + 1)
                    - offsetToGreyscale(imgArray,i + 1 , j - 1)
                    - offsetToGreyscale(imgArray,i , j - 1)
                    - offsetToGreyscale(imgArray,i - 1,j - 1))

                prewittValue = dX + dY
                prewittArray[i][j][0] = prewittValue
                prewittArray[i][j][1] = prewittValue
                prewittArray[i][j][2] = prewittValue
    im = Image.fromarray(prewittArray)
    im.save(ctx.author.name + "avatarPrewitt.png")
    await ctx.send(file=discord.File(ctx.author.name + "avatarPrewitt.png"))

def offsetToGreyscale(array,iOffset,jOffset):
    return array[iOffset][jOffset][0] * 0.21 + array[iOffset][jOffset][1] * 0.71 + array[iOffset][jOffset][2] * 0.07


@client.command()
async def cartoon(ctx):
    filename = (ctx.author.name + "avatar.png")
    await ctx.author.avatar_url.save(filename)
    image = Image.open(filename)
    imgArray = np.array(image)
    imgArray[np.where((imgArray < 150) & (imgArray > 50))] = 90
    imgArray[np.where((imgArray < 50) & (imgArray > 30))] = 40
    imgArray[imgArray < 30] = 10
    
    im = Image.fromarray(imgArray)
    im.save(ctx.author.name + "avatarGreyscale.png")
    await ctx.send(file=discord.File(ctx.author.name + "avatarGreyscale.png"))


client.run(TOKEN)