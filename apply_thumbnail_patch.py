path = "libraries/nestjs-libraries/src/integrations/social/instagram.provider.ts"

with open(path, "r") as f:
    content = f.read()

old = """              : `video_url=${m.path}&media_type=REELS&thumb_offset=${
                  m?.thumbnailTimestamp || 0
                }`"""

new = """              : `video_url=${m.path}&media_type=REELS&thumb_offset=${
                  m?.thumbnailTimestamp || 0
                }${m?.thumbnail ? `&cover_url=${m.thumbnail}` : ''}`"""

count = content.count(old)
print(f"Ocorrencias encontradas: {count}")

if count != 1:
    print("ABORTADO: texto nao bateu exatamente (esperado 1 ocorrencia). Nenhuma alteracao feita.")
else:
    content = content.replace(old, new)
    with open(path, "w") as f:
        f.write(content)
    print("PATCH DE THUMBNAIL APLICADO COM SUCESSO.")
