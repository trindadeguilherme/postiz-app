path = "libraries/nestjs-libraries/src/integrations/social.abstract.ts"

with open(path, "r") as f:
    content = f.read()

old = """    throw new BadBody(
      identifier,
      json,
      options.body!,
      handleError?.value || 'Unknown Error'
    );"""

new = """    console.error(
      `[SocialAbstract] Unmapped error response for ${identifier} - status ${request.status}:`,
      json
    );
    throw new BadBody(
      identifier,
      json,
      options.body!,
      handleError?.value || 'Unknown Error'
    );"""

count = content.count(old)
print(f"Ocorrencias encontradas: {count}")

if count != 1:
    print("ABORTADO: texto nao bateu exatamente (esperado 1 ocorrencia). Nenhuma alteracao feita.")
else:
    content = content.replace(old, new)
    with open(path, "w") as f:
        f.write(content)
    print("PATCH DE LOG APLICADO COM SUCESSO.")
