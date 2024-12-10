import discord
from discord import app_commands
import requests
from datetime import datetime, timedelta

id_do_servidor =   # Coloque aqui o ID do seu servidor
cohere_api_key = ''  # Coloque aqui sua chave da API Cohere

class client(discord.Client):
    def __init__(self):
        super().__init__(intents=discord.Intents.default())
        self.synced = False  # Nós usamos isso para o bot não sincronizar os comandos mais de uma vez

    async def on_ready(self):
        await self.wait_until_ready()
        if not self.synced:  # Checar se os comandos slash foram sincronizados
            await tree.sync(guild=discord.Object(id=id_do_servidor))  # Você também pode deixar o id do servidor em branco para aplicar em todos servidores, mas isso fará com que demore de 1~24 horas para funcionar.
            self.synced = True
        print(f"Entramos como {self.user}.")

aclient = client()
tree = app_commands.CommandTree(aclient)

@tree.command(guild=discord.Object(id=id_do_servidor), name='teste', description='Testando')  # Comando específico para seu servidor
async def slash2(interaction: discord.Interaction):
    await interaction.response.send_message(f"Estou funcionando!", ephemeral=True)

@tree.command(guild=discord.Object(id=id_do_servidor), name='ban', description='Banir um usuário do servidor')
@app_commands.checks.has_permissions(ban_members=True)
async def ban(interaction: discord.Interaction, member: discord.Member, reason: str = None):
    await member.ban(reason=reason)
    await interaction.response.send_message(f'{member.mention} foi banido.', ephemeral=True)

@tree.command(guild=discord.Object(id=id_do_servidor), name='unban', description='Desbanir um usuário do servidor')
@app_commands.checks.has_permissions(ban_members=True)
async def unban(interaction: discord.Interaction, user_id: int):
    user = await aclient.fetch_user(user_id)
    await interaction.guild.unban(user)
    await interaction.response.send_message(f'{user.mention} foi desbanido.', ephemeral=True)

@tree.command(guild=discord.Object(id=id_do_servidor), name='expulsar', description='Expulsar um membro')
async def expulsar(interaction: discord.Interaction, member: discord.Member, reason: str = None):
    try:
        await member.kick(reason=reason)
        await interaction.response.send_message(f'{member} foi expulso.', ephemeral=True)
    except Exception as e:
        await interaction.response.send_message(f'Erro ao tentar expulsar {member}: {str(e)}', ephemeral=True)    
    
@tree.command(guild=discord.Object(id=id_do_servidor), name='clear', description='Deletar um certo número de mensagens')
@app_commands.checks.has_permissions(manage_messages=True)
async def clear(interaction: discord.Interaction, amount: int):
    if amount < 1 or amount > 100:
        await interaction.response.send_message('Você deve especificar um número entre 1 e 100.', ephemeral=True)
        return
    deleted = await interaction.channel.purge(limit=amount)
    await interaction.response.send_message(f'{len(deleted)} mensagens foram deletadas.', ephemeral=True)

@tree.command(guild=discord.Object(id=id_do_servidor), name='mute', description='Mutar um usuário do servidor')
@app_commands.checks.has_permissions(mute_members=True)
async def mute(interaction: discord.Interaction, member: discord.Member, reason: str = None):
    muted_role = discord.utils.get(interaction.guild.roles, name="Muted")
    if not muted_role:
        muted_role = await interaction.guild.create_role(name="Muted")

        for channel in interaction.guild.channels:
            await channel.set_permissions(muted_role, speak=False, send_messages=False)

    await member.add_roles(muted_role, reason=reason)
    await interaction.response.send_message(f'{member.mention} foi mutado.', ephemeral=True)

@tree.command(guild=discord.Object(id=id_do_servidor), name='unmute', description='Desmutar um usuário do servidor')
@app_commands.checks.has_permissions(mute_members=True)
async def unmute(interaction: discord.Interaction, member: discord.Member):
    muted_role = discord.utils.get(interaction.guild.roles, name="Muted")
    if muted_role in member.roles:
        await member.remove_roles(muted_role)
        await interaction.response.send_message(f'{member.mention} foi desmutado.', ephemeral=True)
    else:
        await interaction.response.send_message(f'{member.mention} não está mutado.', ephemeral=True)

@tree.command(guild=discord.Object(id=id_do_servidor), name='addrole', description='Atribuir uma função a um usuário')
@app_commands.checks.has_permissions(manage_roles=True)
async def addrole(interaction: discord.Interaction, member: discord.Member, role: discord.Role):
    await member.add_roles(role)
    await interaction.response.send_message(f'{role.name} foi atribuído a {member.mention}.', ephemeral=True)

@tree.command(guild=discord.Object(id=id_do_servidor), name='removerole', description='Remover uma função de um usuário')
@app_commands.checks.has_permissions(manage_roles=True)
async def removerole(interaction: discord.Interaction, member: discord.Member, role: discord.Role):
    await member.remove_roles(role)
    await interaction.response.send_message(f'{role.name} foi removido de {member.mention}.', ephemeral=True)

@tree.command(guild=discord.Object(id=id_do_servidor), name='createchannel', description='Criar um novo canal')
@app_commands.checks.has_permissions(manage_channels=True)
async def createchannel(interaction: discord.Interaction, channel_name: str, channel_type: str):
    guild = interaction.guild
    if channel_type.lower() == 'text':
        await guild.create_text_channel(channel_name)
    elif channel_type.lower() == 'voice':
        await guild.create_voice_channel(channel_name)
    else:
        await interaction.response.send_message('Tipo de canal inválido. Use "text" ou "voice".', ephemeral=True)
        return
    await interaction.response.send_message(f'Canal {channel_name} criado com sucesso!', ephemeral=True)

@tree.command(guild=discord.Object(id=id_do_servidor), name='deletechannel', description='Deletar um canal')
@app_commands.checks.has_permissions(manage_channels=True)
async def deletechannel(interaction: discord.Interaction, channel: discord.TextChannel):
    await channel.delete()
    await interaction.response.send_message(f'Canal {channel.name} deletado com sucesso!', ephemeral=True)

@tree.command(guild=discord.Object(id=id_do_servidor), name='movechannel', description='Mover um canal para uma categoria')
@app_commands.checks.has_permissions(manage_channels=True)
async def movechannel(interaction: discord.Interaction, channel: discord.TextChannel, category: discord.CategoryChannel):
    await channel.edit(category=category)
    await interaction.response.send_message(f'Canal {channel.name} movido para a categoria {category.name}.', ephemeral=True)

@tree.command(guild=discord.Object(id=id_do_servidor), name='addcomand', description='Adiciona um novo comando')
async def addcomand(interaction: discord.Interaction, comando: str, resposta: str):
    # Aqui você precisa implementar a lógica para adicionar o comando
    # Isso pode envolver salvar os comandos em um arquivo, banco de dados, etc.
    await interaction.response.send_message(f"Comando '{comando}' adicionado com a resposta '{resposta}'!", ephemeral=True)

@tree.command(guild=discord.Object(id=id_do_servidor), name='removecomand', description='Remove um comando existente')
async def removecomand(interaction: discord.Interaction, comando: str):
    # Aqui você precisa implementar a lógica para remover o comando
    # Isso também pode envolver a atualização do armazenamento de comandos
    await interaction.response.send_message(f"Comando '{comando}' removido!", ephemeral=True)

@tree.command(guild=discord.Object(id=id_do_servidor), name='ver_membros', description='Mostra a lista de membros do servidor')  # Novo comando para ver membros
async def ver_membros(interaction: discord.Interaction):
    membros = [member.name for member in interaction.guild.members]
    await interaction.response.send_message(f"Membros do servidor: {', '.join(membros)}")

@tree.command(guild=discord.Object(id=id_do_servidor), name='ping', description='Verificar o ping')  # Comando específico para seu servidor
async def ping(interaction: discord.Interaction):
    bot_latency = round(aclient.latency * 1000)  # Latência do bot em ms
    await interaction.response.send_message(f'Pong! Latência do Bot: {bot_latency}ms', ephemeral=True)

@tree.command(guild=discord.Object(id=id_do_servidor), name='help', description='Listar todos os comandos disponíveis')
async def help(interaction: discord.Interaction):
    comandos = [
        {'name': 'teste', 'description': 'Testando'},
        {'name': 'ban', 'description': 'Banir um usuário do servidor'},
        {'name': 'unban', 'description': 'Desbanir um usuário do servidor'},
        {'name': 'expulsar', 'description': 'expulsar um usuário do servidor'},
        {'name': 'clear', 'description': 'Deletar um certo número de mensagens'},
        {'name': 'mute', 'description': 'Mutar um usuário do servidor'},
        {'name': 'unmute', 'description': 'Desmutar um usuário do servidor'},
        {'name': 'addrole', 'description': 'Atribuir uma função a um usuário'},
        {'name': 'removerole', 'description': 'Remover uma função de um usuário'},
        {'name': 'createchannel', 'description': 'Criar um novo canal'},
        {'name': 'deletechannel', 'description': 'Deletar um canal'},
        {'name': 'movechannel', 'description': 'Mover um canal para uma categoria'},
        {'name': 'addcomand', 'description': 'Adiciona um novo comando'},
        {'name': 'removecomand', 'description': 'Remove um comando existente'},
        {'name': 'ver_membros', 'description': 'Mostra a lista de membros do servidor'},
        {'name': 'ping', 'description': 'Verificar o ping'},
        {'name': 'ia', 'description': 'Faça uma pergunta à Inteligência artificial'},
        {'name': 'setconfig', 'description': 'Configurar um novo valor para um campo de configuração'},
        {'name': 'serverinfo', 'description': 'Obter informações sobre o servidor'},
    ]
    
    resposta = "Aqui estão os comandos disponíveis:\n\n"
    for comando in comandos:
        resposta += f"/{comando['name']}: {comando['description']}\n"

    await interaction.response.send_message(resposta, ephemeral=True)

@tree.command(guild=discord.Object(id=id_do_servidor), name='setconfig', description='Configurar um novo valor para um campo de configuração')
@app_commands.checks.has_permissions(administrator=True)
async def setconfig(interaction: discord.Interaction, field: str, value: str):
    # Supondo que você tenha um arquivo config.json e uma função para atualizar o arquivo
    import json

    try:
        with open('config.json', 'r') as f:
            config = json.load(f)

        config[field] = value

        with open('config.json', 'w') as f:
            json.dump(config, f, indent=4)

        await interaction.response.send_message(f'Configuração {field} atualizada para {value}.', ephemeral=True)
    except Exception as e:
        await interaction.response.send_message(f'Erro ao atualizar a configuração: {e}', ephemeral=True)

@tree.command(guild=discord.Object(id=id_do_servidor), name='serverinfo', description='Obter informações sobre o servidor')
async def serverinfo(interaction: discord.Interaction):
    guild = interaction.guild
    embed = discord.Embed(title=f"Informações do Servidor {guild.name}", color=0x00ff00)
    embed.add_field(name="Servidor Criado em", value=guild.created_at.strftime("%d/%m/%Y"), inline=True)
    embed.add_field(name="Dono", value=guild.owner, inline=True)
    embed.add_field(name="Número de Membros", value=guild.member_count, inline=True)
    embed.add_field(name="ID do Servidor", value=guild.id, inline=True)
    embed.set_thumbnail(url=guild.icon.url)
    await interaction.response.send_message(embed=embed, ephemeral=True)      

@tree.command(guild=discord.Object(id=id_do_servidor), name='ia', description='Faça uma pergunta')
async def slash2(interaction: discord.Interaction, pergunta: str):
    try:
        # Verifica se a pergunta é sobre data e hora
        if 'hora' in pergunta.lower() or 'data' in pergunta.lower():
            # Obtendo a data e hora local sem usar pytz
            local_now = datetime.utcnow() - timedelta(hours=3)  # Ajustando para o fuso horário de Brasília
            hora_local = local_now.strftime("%H:%M:%S")
            data_local = local_now.strftime("%Y-%m-%d")
            message = f"Data e Hora Local: {data_local} {hora_local}"
        else:
            # Fazendo a requisição para a API de inteligência artificial
            response = requests.post(
                'https://api.cohere.ai/v1/generate',
                headers={'Authorization': f'Bearer {cohere_api_key}', 'Content-Type': 'application/json'},
                json={'model': 'command-xlarge-nightly', 'prompt': pergunta, 'max_tokens': 100, 'temperature': 0.7}
            )
            response.raise_for_status()  # Isso irá lançar um erro se a requisição falhar
            data = response.json()
            message = data.get('generations', [{'text': 'Desculpe, não consegui processar sua pergunta no momento.'}])[0]['text']

        await interaction.response.send_message(message, ephemeral=True)
    except requests.exceptions.RequestException as e:
        await interaction.response.send_message(f'Erro ao se comunicar com a API: {e}', ephemeral=True)
       
# Os outros comandos ficam aqui...

aclient.run('')
