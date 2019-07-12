import sys
import discord
from sim.heroes import Team, DummyTeam, Hero
from sim.models import Armor, Helmet, Weapon, Pendant, Rune, Artifact, Familiar
from sim.processing import GameSim, GauntletAttackSim, GauntletDefenseSim, GauntletSim, Game
from sim.tests import friend_boss_test, main_friend_boss_test, master_friend_boss_test, guild_boss_test, \
    main_guild_boss_test, master_guild_boss_test, trial_test, main_trial_test, pvp_test, sim_setup

# List heroes
heroes = [Hero.__dict__[key] for key in Hero.__dict__ if '__' not in key and 'empty' not in key]

# Create teams

TOKEN = 'xxx'

client = discord.Client()

@client.event

async def on_message(message):

    rawHeroes = ['abyss_lord', 'aden', 'blood_tooth', 'centaur', 'chessia', 'dettlaff', 'drow', 'dziewona', 'freya', 'gerald',
          'grand', 'hester', 'lexar', 'lindberg', 'luna', 'mars', 'martin', 'medusa', 'megaw', 'minotaur', 'monkey_king',
          'mulan', 'nameless_king', 'phoenix', 'orphee', 'reaper', 'ripper', 'rlyeh', 'samurai', 'saw_machine', 'scarlet', 'skuld',
          'wolnir', 'xexanoth']

    # we do not want the bot to reply to itself
    if message.author == client.user:
        return

    if message.content.startswith('!sim heroes'):
       heroes = '\n'.join('{}.{}'.format(index, hero) for index, hero in enumerate(rawHeroes))
       await client.send_message(message.channel, '```'+heroes+'```')

    if message.content.startswith('!sim battle'):   
        #Breaks the chat message into an array (with !sym as first value, that's easily solvable so i'll sort later)
        teams = message.content.replace("!sim battle", "").replace(',', ' ').replace(', ', '').split('][')
        print(teams)

        if teams[0] != '':
            rawTeam_1 = teams[0].replace('[','').replace(']','').split()
            #Builds array for battle, needs to pull values from chat message
            team_1 = Team([getattr(Hero, rawHeroes[int(hero_string)])() for hero_string in rawTeam_1])
        else:
            #Fallback to default team if no parameters are specified
            team_1 = Team([Hero.wolnir(),
               Hero.valkyrie(),
               Hero.lindberg(artifact=Artifact.tears_of_the_goddess.O6),
               Hero.skuld(artifact=Artifact.tears_of_the_goddess.O6),
               Hero.mars(artifact=Artifact.tears_of_the_goddess.O6),
               Hero.skuld()])            

        try:
            rawTeam_2 = teams[1].replace('[','').replace(']','').split()
            #Builds array for battle, needs to pull values from chat message
            team_2 = Team([getattr(Hero, rawHeroes[int(hero_string)])() for hero_string in rawTeam_2])
        except IndexError:
            #Fallback to default team if no parameters are specified
            team_2 = Team([Hero.phoenix(),
               Hero.skuld(artifact=Artifact.tears_of_the_goddess.O6),
               Hero.skuld(),
               Hero.drow(artifact=Artifact.tears_of_the_goddess.O6),
               Hero.monkey_king(artifact=Artifact.tears_of_the_goddess.O6),
               Hero.shudde_m_ell()])

        try:
            simNumber=int(teams[2].replace('[','').replace(']',''))
            if simNumber >= 1000:
                simNumber = 1000            
        except IndexError:
            simNumber=500

        print(team_1)
        print(team_2)
        print(simNumber)        
      
        sim = GameSim(team_1, team_2, n_sim=1000)
        #Runs simulation
        sim.process()   

        team1Comp = team_1.comp()
        team2Comp = team_2.comp()

        #Sends results in the chat where request was made      
        await client.send_message(message.channel, '**TEAM #1**'+team1Comp+'\n\n**TEAM #2**'+team2Comp+'\n')                
        await client.send_message(message.channel, '==================')
        await sim.print_winrate(client, message)           
        await client.send_message(message.channel, '==================')

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

client.run(TOKEN)
