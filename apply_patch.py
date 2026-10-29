path = "libraries/nestjs-libraries/src/integrations/social/instagram.provider.ts"

with open(path, "r") as f:
    content = f.read()

old1 = """        const collaborators =
          firstPost?.settings?.collaborators?.length && !isStory
            ? `&collaborators=${JSON.stringify(
                firstPost?.settings?.collaborators.map((p) => p.label)
              )}`
            : ``;"""

new1 = """        // collaborators are only allowed on single-media posts, NOT on carousel children
        // For carousels, collaborators are added to the container creation call instead
        const isCarouselItem = (firstPost?.media?.length || 0) > 1 && !isStory;
        const collaborators =
          firstPost?.settings?.collaborators?.length && !isStory && !isCarouselItem
            ? `&collaborators=${JSON.stringify(
                firstPost?.settings?.collaborators.map((p) => p.label)
              )}`
            : ``;"""

old2 = """      const { id: containerId, ...all3 } = await (
        await this.fetch(
          `https://${type}/v20.0/${id}/media?caption=${encodeURIComponent(
            firstPost?.message
          )}&media_type=CAROUSEL&children=${encodeURIComponent(
            medias.join(',')
          )}&access_token=${accessToken}`,
          {
            method: 'POST',
          }
        )
      ).json();"""

new2 = """      // Add collaborators to the carousel container (where IG's Graph API accepts them)
      const carouselCollaborators =
        firstPost?.settings?.collaborators?.length && !isStory
          ? `&collaborators=${JSON.stringify(
              firstPost?.settings?.collaborators.map((p: { label: string }) => p.label)
            )}`
          : ``;
      const { id: containerId, ...all3 } = await (
        await this.fetch(
          `https://${type}/v20.0/${id}/media?caption=${encodeURIComponent(
            firstPost?.message
          )}&media_type=CAROUSEL&children=${encodeURIComponent(
            medias.join(',')
          )}${carouselCollaborators}&access_token=${accessToken}`,
          {
            method: 'POST',
          }
        )
      ).json();"""

c1 = content.count(old1)
c2 = content.count(old2)
print(f"Ocorrencias bloco 1 (collaborators): {c1}")
print(f"Ocorrencias bloco 2 (carousel container): {c2}")

if c1 != 1 or c2 != 1:
    print("ABORTADO: texto original nao bateu exatamente (esperado 1 ocorrencia de cada). Nenhuma alteracao foi feita.")
else:
    content = content.replace(old1, new1)
    content = content.replace(old2, new2)
    with open(path, "w") as f:
        f.write(content)
    print("PATCH APLICADO COM SUCESSO.")
