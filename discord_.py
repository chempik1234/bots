import discord
from discord.ext import commands
import logging, requests, asyncio

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

langs = """Abkhazian	ab
Afar	aa
Afrikaans	af
Akan	ak
Albanian	sq
Amharic	am
Arabic	ar
Aragonese	an
Armenian	hy
Assamese	as
Avaric	av
Avestan	ae
Aymara	ay
Azerbaijani	az
Bambara	bm
Bashkir	ba
Basque	eu
Belarusian	be
Bengali	bn
Bislama	bi
Bosnian	bs
Breton	br
Bulgarian	bg
Burmese	my
Catalan, Valencian	ca
Chamorro	ch
Chechen	ce
Chichewa, Chewa, Nyanja	ny
Chinese	zh
Church Slavic, Old Slavonic, Church Slavonic, Old Bulgarian, Old Church Slavonic	cu
Chuvash	cv
Cornish	kw
Corsican	co
Cree	cr
Croatian	hr
Czech	cs
Danish	da
Divehi, Dhivehi, Maldivian	dv
Dutch, Flemish	nl
Dzongkha	dz
English	en
Esperanto	eo
Estonian	et
Ewe	ee
Faroese	fo
Fijian	fj
Finnish	fi
French	fr
Western Frisian	fy
Fulah	ff
Gaelic, Scottish Gaelic	gd
Galician	gl
Ganda	lg
Georgian	ka
German	de
Greek, Modern (1453–)	el
Kalaallisut, Greenlandic	kl
Guarani	gn
Gujarati	gu
Haitian, Haitian Creole	ht
Hausa	ha
Hebrew	he
Herero	hz
Hindi	hi
Hiri Motu	ho
Hungarian	hu
Icelandic	is
Ido	io
Igbo	ig
Indonesian	id
Interlingua (International Auxiliary Language Association)	ia
Interlingue, Occidental	ie
Inuktitut	iu
Inupiaq	ik
Irish	ga
Italian	it
Japanese	ja
Javanese	jv
Kannada	kn
Kanuri	kr
Kashmiri	ks
Kazakh	kk
Central Khmer	km
Kikuyu, Gikuyu	ki
Kinyarwanda	rw	kin
Kirghiz, Kyrgyz	ky
Komi	kv
Kongo	kg
Korean	ko
Kuanyama, Kwanyama	kj
Kurdish	ku
Lao	lo
Latin	la
Latvian	lv
Limburgan, Limburger, Limburgish	li
Lingala	ln
Lithuanian	lt
Luba-Katanga	lu
Luxembourgish, Letzeburgesch	lb
Macedonian	mk
Malagasy	mg
Malay	ms
Malayalam	ml
Maltese	mt
Manx	gv
Maori	mi
Marathi	mr
Marshallese	mh
Mongolian	mn
Nauru	na
Navajo, Navaho	nv
North Ndebele	nd
South Ndebele	nr
Ndonga	ng
Nepali	ne
Norwegian	no
Norwegian Bokmål	nb
Norwegian Nynorsk	nn
Sichuan Yi, Nuosu	ii
Occitan	oc
Ojibwa	oj
Oriya	or
Oromo	om
Ossetian, Ossetic	os
Pali	pi
Pashto, Pushto	ps
Persian	fa
Polish	pl
Portuguese	pt
Punjabi, Panjabi	pa
Quechua	qu
Romanian, Moldavian, Moldovan	ro
Romansh	rm
Rundi	rn
Russian	ru
Northern Sami	se
Samoan	sm
Sango	sg
Sanskrit	sa
Sardinian	sc
Serbian	sr
Shona	sn
Sindhi	sd
Sinhala, Sinhalese	si
Slovak	sk
Slovenian	sl
Somali	so
Southern Sotho	st
Spanish, Castilian	es
Sundanese	su
Swahili	sw
Swati	ss
Swedish	sv
Tagalog	tl
Tahitian	ty
Tajik	tg
Tamil	ta
Tatar	tt
Telugu	te
Thai	th
Tibetan	bo
Tigrinya	ti
Tonga (Tonga Islands)	to
Tsonga	ts
Tswana	tn	
Turkish	tr
Turkmen	tk
Twi	tw
Uighur, Uyghur	ug
Ukrainian	uk
Urdu	ur
Uzbek	uz
Venda	ve
Vietnamese
Volapük	vo
Walloon	wa
Welsh	cy
Wolof	wo
Xhosa	xh
Yiddish	yi
Yoruba	yo
Zhuang, Chuang	za
Zulu	zu"""
langs_list = [i.split()[-1] for i in langs.split('\n')]
intents = discord.Intents.default()
intents.members = True
dashes = ['\u2680', '\u2681', '\u2682', '\u2683', '\u2684', '\u2685']
data = {}


def translator(word, lang):
    try:
        url = "https://translated-mymemory---translation-memory.p.rapidapi.com/api/get"
        querystring = {"langpair": lang, "q": word}
        headers = {
            'x-rapidapi-key': "24fd2ead8amshc203cd479b8fa8bp18d9b1jsnb8779c61c6a3",
            'x-rapidapi-host': "translated-mymemory---translation-memory.p.rapidapi.com"
        }
        response = requests.request("GET", url, headers=headers, params=querystring)
        output = response.json()
        new = output['responseData']['translatedText']
        return new
    except Exception as err:
        return 'Ошибка ' + err.__class__.__name__.__str__() + ': ' + err.__str__()


class Translator(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='help_bot')
    async def help_bot(self, ctx):
        res = ['Commands:', '!!help_bot - get info about using bot',
               '!!set_lang *langpair_divided_by_dash* - change language (TYPE IT YOURSELF, E.G. en-ru or eu-pl',
               '!!text *text* - translate']
        data[ctx.channel] = 'en|ru'
        await ctx.send("\n".join(res))
        await ctx.send("Languages:")
        await ctx.send(langs[: 2000])
        await ctx.send(langs[2000:])

    @commands.command(name='set_lang')
    async def set_lang(self, ctx, lang_pair_):
        lang_pair = lang_pair_.split('-')
        if len(lang_pair) != 2 or lang_pair[0] not in langs_list or lang_pair[1] not in langs_list:
            await ctx.send("Language doesn't exist")
            return
        data[ctx.channel] = '|'.join(lang_pair)

    @commands.command(name='text')
    async def text(self, ctx, *args):
        if ctx.channel not in data.keys():
            data[ctx.channel] = 'en|ru'
        text_ = ' '.join(args)
        await ctx.send(translator(text_, data[ctx.channel]))


bot = commands.Bot(command_prefix='!!', intents=intents)
bot.add_cog(Translator(bot))
TOKEN = "OTU3NTM2MjE1MDQzODA5Mjgw.YkANFw.VUDBQHMImasDVYqOTITooNDIv00"
bot.run(TOKEN)