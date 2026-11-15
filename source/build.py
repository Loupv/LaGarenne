"""Exporte le canevas Claude Design (source/canvas/project/Main.dc.html) en site statique pour GitHub Pages.

Usage : python3 source/build.py   (depuis la racine du dépôt)
"""
import re, shutil, sys, pathlib

HERE = pathlib.Path(__file__).resolve().parent
OUT = HERE.parent
src = (HERE / "canvas/project/Main.dc.html").read_text(encoding="utf-8")
photos = HERE / "photos"

BLOBS = {
    "1fb9ebafa1d4dab9522dbb122b4bfee8": "accueil.jpg",
    "33d848ecd4bae84416b68730a48be90b": "bouquetin.jpg",
    "eef2257faeac4a08f49c2501c3db0162": "buse.jpg",
    "97a99b60a9381b2e4419eadd65340b00": "castor.jpg",
    "6530bc05ca611f350f126ecf0c3d3ff3": "cerf.jpg",
    "6c38c5923eb3775e7574aa6648abc879": "chat.jpg",
    "d6e85b2d24e34153389e3882a40a4378": "chevre-app.jpg",
    "9d2b729853a6799e90c2088d371d0e3a": "cigogne.jpg",
    "4f470b3be543f40df23b3aa819b2855d": "cistude.jpg",
    "6bd1b6d8957190ac86a10e074fa1f003": "cochon.jpg",
    "06508402371b3ab03718262dfe4e261b": "crapaud.jpg",
    "0c2357313425878bea935b7d6a9b403f": "ecureuil.jpg",
    "bdd7babda58c1a2e3e9dba255bbbe0a6": "effraie.jpg",
    "a215c34c8346b84f02f9175f6e4556cd": "etourneau.jpg",
    "2f6f11c7e461fc13f1e75a08cbee7882": "fouine.jpg",
    "81d4aef349165ac65fedfda6176dbe0f": "grandduc.jpg",
    "c71af5f60a7ad42f78ef27e309fe088e": "grande-chevre.jpg",
    "66a3892402a6dd561bce9a74872a9882": "gypaete.jpg",
    "7336fe72b9751637aaf67a1f72ae88e2": "herisson.jpg",
    "74d133431c94b992588f7cdd854e2cec": "ibis.jpg",
    "a2532fb5ac16430d967f7743ff45afa6": "lievre.jpg",
    "b7f0db46a31c4e0475f6769707973116": "loup.jpg",
    "13c1bcce25694fe2d7a3c4349799aa89": "loutre.jpg",
    "9981c8ebfab053bf6288b85af0e0167a": "lynx-card.jpg",
    "045c8b4e09c842ef029efd7a167f8475": "marmotte.jpg",
    "31bdb25de781aaa9d948672e9b63ddf0": "merle.jpg",
    "92f18bdeeef98509d3425acf394b0577": "milan.jpg",
    "22f56326a3883df62d44ddf77bd62411": "mouton.jpg",
    "46789c3b1546a393231c2683cdc97894": "oie.jpg",
    "db06346665230db58dbefd99d0732781": "pigeon.jpg",
    "5fe9bd3bcc047b91fcd1c9056464a664": "poule-app.jpg",
    "5ace5a4329d3ba6057216c97d7e27897": "poule-suisse.jpg",
    "7ce0b3cd4189964a00b1419dcaecf437": "raton.jpg",
    "03aa0e415e0a5348bf7b99c871b39d6d": "renard.jpg",
    "d9050b3a113bc687e89b778658feb697": "salamandre.jpg",
    "bdc7de5e5c66c43b1fb03fb8abd5e0ef": "sanglier-card.jpg",
    "29f73790d5706ff6c6ab9c29c78097bc": "sonneur.jpg",
    "25915005d56d9dd55baef2cd371c6637": "tortue.jpg",
    "3dd7b28576a1a2533d753476807b5321": "vautour.jpg",
}

used = set()
def blob(m):
    name = BLOBS[m.group(1)]
    used.add(name)
    return "assets/" + pathlib.Path(name).name
src = re.sub(r"/_blob/([0-9a-f]{32})", blob, src)

helmet = re.search(r"<helmet>(.*?)</helmet>", src, re.S).group(1)
body = re.search(r"</helmet>(.*?)</x-dc>", src, re.S).group(1)
logic = re.search(r"<script type=\"text/x-dc\"[^>]*>(.*?)</script>", src, re.S).group(1)

page = f"""<!doctype html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Carnet de faune — La Garenne</title>
<meta name="description" content="Les animaux du parc La Garenne (Le Vaud) : catalogue, fiches ludiques pour le public et les naturalistes, plan du parc.">
{helmet.strip()}
</head>
<body>
<div id="app"></div>
<template id="dc">{body}</template>
<script type="text/x-dc" id="dc-logic">{logic}</script>
<script src="dc-runtime.js"></script>
</body>
</html>
"""
(OUT / "index.html").write_text(page, encoding="utf-8")
(OUT / "assets").mkdir(exist_ok=True)
for name in sorted(used):
    shutil.copyfile(photos / name, OUT / "assets" / pathlib.Path(name).name)
(OUT / ".nojekyll").write_text("")
print(len(used), "photos copiées")
