#  Copyright (c)Slurmking 2020
import discord
from discord.ext import commands
import random

Major = [
    {'name': 'The Fool',
     'suit': 'Major',
     'meaning': 'Beginnings, Innocence, Leap of faith, Originality, Spontaneity',
     'reversed': 'Chaos, Folly, Lack of direction, Naivety, Poor judgement, Stupidity'},
    {'name': 'The Magician',
     'suit': 'Major',
     'meaning': 'Determined, Dexterity, Resourceful, Skilled, Strong powerful man',
     'reversed': 'Communication blocks, Confusion, Deceit, Ill intentions, Lack of energy'},
    {'name': 'The High Priestess',
     'suit': 'Major',
     'meaning': ' Hidden talents, Intuition, Mystery, Spiritual insight, Things yet to be revealed',
     'reversed': 'Information withheld, Lack of personal harmony, Secrets'},
    {'name': 'The Empress',
     'suit': 'Major',
     'meaning': 'Fruitfulness, action, initiative, length of days; the unknown, clandestine; also difficulty, doubt, '
                'ignorance',
     'reversed': 'Light, truth, the unraveling of involved matters, public rejoicings; according to another reading, '
                 'vacillation'},
    {'name': 'The Emperor',
     'suit': 'Major',
     'meaning': 'Stability, power, protection, realization; a great person; aid, reason, conviction also authority '
                'and will',
     'reversed': 'Benevolence, compassion, credit; also confusion to enemies, obstruction, immaturity'},
    {'name': 'The Hierophant',
     'suit': 'Major',
     'meaning': 'Marriage, alliance, captivity, servitude; by another account, mercy, and goodness; inspiration; the '
                'man to whom the Querent has recourse',
     'reversed': 'Society, good understanding, concord, over kindness, weakness'},
    {'name': 'The Lovers',
     'suit': 'Major',
     'meaning': 'Attraction, love, beauty, trials overcome',
     'reversed': 'Failure, foolish designs'},
    {'name': 'The Chariot',
     'suit': 'Major',
     'meaning': 'Succour, providence; also war, triumph, presumption, vengeance, trouble',
     'reversed': 'Riot, quarrel, dispute, litigation, defeat'},
    {'name': 'Strength',
     'suit': 'Major',
     'meaning': 'Power, energy, action, courage, magnanimity; also complete success and honours',
     'reversed': 'Despotism, abuse of power, weakness, discord, sometimes even disgrace'},
    {'name': 'The Hermit',
     'suit': 'Major',
     'meaning': 'Prudence, circumspection; also and especially treason, dissimulation, roguery, corruption',
     'reversed': 'Concealment, disguise, policy fear, unreasoned caution'},
    {'name': 'Wheel of Fortune',
     'suit': 'Major',
     'meaning': 'Destiny, fortune, success, elevation, luck, felicity',
     'reversed': 'Increase, abundance, superfluity'},
    {'name': 'Justice',
     'suit': 'Major',
     'meaning': 'Equity, rightness, probity, executive; triumph of the deserving side in law',
     'reversed': 'Law in all its departments, legal complications, bigotry, bias, excessive severity'},
    {'name': 'The Hanged Man',
     'suit': 'Major',
     'meaning': 'Wisdom, circumspection, discernment, trials, sacrifice, intuition, divination, prophecy',
     'reversed': 'Selfishness, the crowd, body politic'},
    {'name': 'Death',
     'suit': 'Major',
     'meaning': 'End, mortality, destruction, corruption; also, for a man, the loss of a benefactor; for a woman, '
                'many contrarieties; for a maid, failure of marriage projects',
     'reversed': 'Inertia, sleep, lethargy, petrifaction, somnambulism; hope destroyed'},
    {'name': 'Temperance',
     'suit': 'Major',
     'meaning': 'Economy, moderation, frugality, management, accommodation',
     'reversed': 'Things connected with churches, religions, sects, the priesthood, sometimes even the priest who '
                 'will marry Querent; also disunion, unfortunate combinations, competing interests'},
    {'name': 'The Devil',
     'suit': 'Major',
     'meaning': 'Ravage, violence, vehemence, extraordinary efforts, force, fatality; that which is predestined but '
                'is not for this reason evil',
     'reversed': 'Evil fatality, weakness, pettiness, blindness'},
    {'name': 'The Tower',
     'suit': 'Major',
     'meaning': 'Misery, distress, indigence, adversity, calamity, disgrace, deception, ruin. It is a card in '
                'particular of unforeseen catastrophe',
     'reversed': 'Negligence, absence, distribution, carelessness, apathy, nullity, vanity'},
    {'name': 'The Star',
     'suit': 'Major',
     'meaning': 'Loss, theft, privation, abandonment; another reading says--hope bright prospects',
     'reversed': 'Arrogance, haughtiness, impotence'},
    {'name': 'The Moon',
     'suit': 'Major',
     'meaning': 'Hidden enemies, danger, calumny, darkness, terror, deception, occult forces, error.',
     'reversed': 'Instability, inconstancy, silence, lesser degrees of deception and error'},
    {'name': 'The Sun',
     'suit': 'Major',
     'meaning': 'Enlightment, Joy, Marriage, Material happiness, Success, Vitality',
     'reversed': 'False impressions, Lack of clarity, Low Vitality, Sadness'},
    {'name': 'Judgement',
     'suit': 'Major',
     'meaning': 'Awakening, Decision making, Redemption, Reincarnation, Renewal, Transition',
     'reversed': 'Poor logic, Poor or hasty judgement, Self-doubt, Stagnation'},
    {'name': 'The World',
     'suit': 'Major',
     'meaning': 'Achievement, Fulfillment, Possibilities, Successful conclusions',
     'reversed': 'Delayed success, Failed plans, Lack of completion, Stagnation'},
]

Cups = [
    {'name': 'Ace of Cups',
     'suit': 'Cups',
     'meaning': 'new feelings, spirituality, intuition',
     'reversed': 'emotional loss, blocked creativity, emptiness'},
    {'name': 'Two of Cups',
     'suit': 'Cups',
     'meaning': 'unity, partnership, connection',
     'reversed': 'imbalance, broken communication, tension'},
    {'name': 'Three of Cups',
     'suit': 'Cups',
     'meaning': 'friendship, community, happiness',
     'reversed': 'overindulgence, gossip, isolation'},
    {'name': 'Four of Cups',
     'suit': 'Cups',
     'meaning': 'apathy, contemplation, disconnectedness',
     'reversed': 'sudden awareness, choosing'},
    {'name': 'Five of Cups',
     'suit': 'Cups',
     'meaning': 'loss, grief, self-pity',
     'reversed': 'acceptance, moving on, finding peace'},
    {'name': 'Six of Cups',
     'suit': 'Cups',
     'meaning': 'familiarity, happy memories, healing',
     'reversed': 'moving forward, leaving home, independence'},
    {'name': 'Seven of Cups',
     'suit': 'Cups',
     'meaning': 'searching for purpose, choices, daydreaming',
     'reversed': 'lack of purpose, diversion'},
    {'name': 'Eight of Cups',
     'suit': 'Cups',
     'meaning': 'walking away, disillusionment, leaving behind',
     'reversed': 'avoidance, fear of change, fear of loss'},
    {'name': 'Nine of Cups',
     'suit': 'Cups',
     'meaning': 'satisfaction, emotional stability, luxury',
     'reversed': 'lack of inner joy, smugness, dissatisfaction'},
    {'name': 'Ten of Cups',
     'suit': 'Cups',
     'meaning': 'inner happiness, fulfillment, dreams coming true',
     'reversed': 'shattered dreams, broken family'},
    {'name': 'Page of Cups',
     'suit': 'Cups',
     'meaning': 'happy surprise, dreamer, sensitivity',
     'reversed': 'emotional immaturity, insecurity'},
    {'name': 'Knight of Cups',
     'suit': 'Cups',
     'meaning': 'following the heart, idealist, romantic',
     'reversed': 'moodiness, disappointment'},
    {'name': 'Queen of Cups',
     'suit': 'Cups',
     'meaning': 'compassion, calm, comfort',
     'reversed': 'martyrdom, insecurity, dependence'},
    {'name': 'King of Cups',
     'suit': 'Cups',
     'meaning': 'compassion, control, balance',
     'reversed': 'coldness, moodiness, bad advice'}
]

Swords = [
    {'name': 'Ace of Swords',
     'suit': 'Swords',
     'meaning': 'breakthrough, clarity, sharp mind',
     'reversed': 'confusion, brutality, chaos'},
    {'name': 'Two of Swords',
     'suit': 'Swords',
     'meaning': 'difficult choices, indecision, stalemate',
     'reversed': 'lesser of two evils, no right choice, confusion'},
    {'name': 'Three of Swords',
     'suit': 'Swords',
     'meaning': 'heartbreak, suffering, grief,',
     'reversed': 'Recovery, forgiveness, moving on '},
    {'name': 'Four of Swords',
     'suit': 'Swords',
     'meaning': 'rest, restoration, contemplation',
     'reversed': 'restlessness, burnout, stress'},
    {'name': 'Five of Swords',
     'suit': 'Swords',
     'meaning': 'unbridled ambition, win at all costs, sneakiness',
     'reversed': 'reconciliation, resolution, compromise, revenge, regret, remorse, cutting losses'},
    {'name': 'Six of Swords',
     'suit': 'Swords',
     'meaning': 'transition, leaving behind, moving on',
     'reversed': 'emotional baggage, unresolved issues,'},
    {'name': 'Seven of Swords',
     'suit': 'Swords',
     'meaning': 'deception, trickery, tactics and strategy',
     'reversed': 'coming clean, rethinking approach'},
    {'name': 'Eight of Swords',
     'suit': 'Swords',
     'meaning': 'imprisonment, entrapment, self-victimization',
     'reversed': 'self acceptance, new perspective, freedom'},
    {'name': 'Nine of Swords',
     'suit': 'Swords',
     'meaning': 'anxiety, hopelessness, trauma',
     'reversed': ' hope, reaching out, despair'},
    {'name': 'Ten of Swords',
     'suit': 'Swords',
     'meaning': 'failure, collapse, defeat',
     'reversed': 'can\'t get worse, only upwards, inevitable end'},
    {'name': 'Page of Swords',
     'suit': 'Swords',
     'meaning': 'curiosity, restlessness, mental energy',
     'reversed': 'scatterbrained, cynical, sarcastic, gossipy, insulting, rude, lack of planning'},
    {'name': 'Knight of Swords',
     'suit': 'Swords',
     'meaning': 'action, impulsiveness, defending beliefs',
     'reversed': 'rude, tactless, forceful, bully, aggressive, vicious, ruthless, arrogant'},
    {'name': 'Queen of Swords',
     'suit': 'Swords',
     'meaning': 'complexity, perceptiveness, clear mindedness',
     'reversed': 'cold hearted, cruel, bitterness'},
    {'name': 'King of Swords',
     'suit': 'Swords',
     'meaning': 'head over heart, discipline, truth',
     'reversed': 'manipulative, cruel, weakness'}
]

Wands = [
    {'name': 'Ace of Wands',
     'suit': 'Wands',
     'meaning': 'creation, willpower, inspiration, desire',
     'reversed': 'lack of energy, lack of passion, boredom'},
    {'name': 'Two of Wands',
     'suit': 'Wands',
     'meaning': 'planning, making decisions, leaving home',
     'reversed': 'fear of change, playing safe, bad planning'},
    {'name': 'Three of Wands',
     'suit': 'Wands',
     'meaning': 'looking ahead, expansion, rapid growth,',
     'reversed': 'obstacles, delays, frustration'},
    {'name': 'Four of Wands',
     'suit': 'Wands',
     'meaning': 'community, home, celebration',
     'reversed': 'lack of support, transience, home conflicts'},
    {'name': 'Five of Wands',
     'suit': 'Wands',
     'meaning': 'competition, rivalry, conflict',
     'reversed': 'avoiding conflict, respecting differences'},
    {'name': 'Six of Wands',
     'suit': 'Wands',
     'meaning': 'victory, success, public reward',
     'reversed': 'excess pride, lack of recognition, punishment'},
    {'name': 'Seven of Wands',
     'suit': 'Wands',
     'meaning': '',
     'reversed': ''},
    {'name': 'Eight of Wands',
     'suit': 'Wands',
     'meaning': 'rapid action, movement, quick decisions',
     'reversed': 'panic, waiting, slowdown'},
    {'name': 'Nine of Wands',
     'suit': 'Wands',
     'meaning': 'resilience, grit, last stand',
     'reversed': 'exhaustion, fatigue, questioning motivations'},
    {'name': 'Ten of Wands',
     'suit': 'Wands',
     'meaning': 'accomplishment, responsibility, burden,',
     'reversed': 'inability to delegate, overstressed, burnt out'},
    {'name': 'Page of Wands',
     'suit': 'Wands',
     'meaning': 'exploration, excitement, freedom',
     'reversed': 'lack of direction, procrastination, creating '},
    {'name': 'Knight of Wands',
     'suit': 'Wands',
     'meaning': '',
     'reversed': ''},
    {'name': 'Queen of Wands',
     'suit': 'Wands',
     'meaning': 'courage, determination, joy',
     'reversed': 'selfishness, jealousy, insecurities'},
    {'name': 'King of Wands',
     'suit': 'Wands',
     'meaning': 'big picture, leader, overcoming challenges',
     'reversed': ' impulsive, overbearing, unachievable'}
]

Pentacles = [
    {'name': 'Ace of Pentacles',
     'suit': 'Pentacles',
     'meaning': 'opportunity, prosperity, new venture',
     'reversed': 'lost opportunity, missed chance, bad investment '},
    {'name': 'Two of Pentacles',
     'suit': 'Pentacles',
     'meaning': 'balancing decisions, priorities, adapting to change',
     'reversed': ' loss of balance, disorganized, overwhelmed '},
    {'name': 'Three of Pentacles',
     'suit': 'Pentacles',
     'meaning': 'teamwork, collaboration, building,',
     'reversed': 'lack of teamwork, disorganized, group conflict'},
    {'name': 'Four of Pentacles',
     'suit': 'Pentacles',
     'meaning': 'conservation, frugality, security',
     'reversed': 'greediness, stinginess, possessiveness'},
    {'name': 'Five of Pentacles',
     'suit': 'Pentacles',
     'meaning': 'need, poverty, insecurity',
     'reversed': 'recovery, charity, improvement'},
    {'name': 'Six of Pentacles',
     'suit': 'Pentacles',
     'meaning': 'charity, generosity, sharing,',
     'reversed': 'strings attached, stinginess, power and domination'},
    {'name': 'Seven of Pentacles',
     'suit': 'Pentacles',
     'meaning': 'hard work, perseverance, diligence',
     'reversed': 'work without results, distractions, lack of rewards'},
    {'name': 'Eight of Pentacles',
     'suit': 'Pentacles',
     'meaning': 'apprenticeship, passion, high standards',
     'reversed': 'lack of passion, uninspired, no motivation'},
    {'name': 'Nine of Pentacles',
     'suit': 'Pentacles',
     'meaning': 'fruits of labor, rewards, luxury',
     'reversed': 'reckless spending, living beyond means, false success'},
    {'name': 'Ten of Pentacles',
     'suit': 'Pentacles',
     'meaning': 'legacy, culmination, inheritance',
     'reversed': 'leeting success, lack of stability, lack of resources'},
    {'name': 'Page of Pentacles',
     'suit': 'Pentacles',
     'meaning': 'ambition, desire, diligence',
     'reversed': 'lack of commitment, greediness, laziness'},
    {'name': 'Knight of Pentacles',
     'suit': 'Pentacles',
     'meaning': 'efficiency, hard work, responsibility',
     'reversed': 'laziness, obsessiveness, work without'},
    {'name': 'Queen of Pentacles',
     'suit': 'Pentacles',
     'meaning': 'practicality, creature comforts, financial security',
     'reversed': 'self-centeredness, jealousy, smothering'},
    {'name': 'King of Pentacles',
     'suit': 'Pentacles',
     'meaning': 'abundance, prosperity, security',
     'reversed': 'greed, indulgence, sensuality'}
]


def show(number,list):
    if list != Major:
        number = number - 1
        im = Image.open(f"images/tarot/{list[number]['suit']}/{str(number+1).zfill(2)}.png")
        im.show()
    else:
        im = Image.open(f"images/tarot/{list[number]['suit']}/{str(number).zfill(2)}.png")
        im.show()
    return list[number]

class Tarot(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        print(f"\033[92m[COG]\033[0m{self.qualified_name}:loaded")

    async def cog_check(self, ctx):
        if ctx.channel.type == discord.ChannelType.private:
            return False
        else:
            return True

    @commands.command()
    async def Tarot(self, ctx):
        Arcana = [Major, Wands, Swords, Cups, Pentacles]
        Deck = (random.choice(Arcana))
        Coin = random.randint(0, 1)
        Card = random.randint(0, len(Deck) - 1)
        folder = f"images/tarot/{Deck[Card]['suit']}/"
        if Coin == 1:
            cardName = (Deck[Card]['name'])
            cardDesc = ((Deck[Card]['meaning']))
            cardLoc = (f"{folder}{str(int(Card)).zfill(2)}.png")
        else:
            cardName = (f"{Deck[Card]['name']} Reversed")
            cardDesc = ((Deck[Card]['reversed']))
            cardLoc = (f"{folder}{str(int(Card)).zfill(2)}-r.png")

        embed = discord.Embed(title=cardName, description=cardDesc)
        file = discord.File(f"{cardLoc}")
        embed.set_image(url=f"attachment://{cardLoc}")
        await ctx.send(embed=embed,file = file)

def setup(bot):
    bot.add_cog(Tarot(bot))
