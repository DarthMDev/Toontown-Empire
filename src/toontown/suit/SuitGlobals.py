# SuitGlobals are used to set the appearance of Cogs.
from toontown.suit import SuitDNA
from panda3d.core import VBase4

SCALE_INDEX = 0 # The scale of the cog
HAND_COLOR_INDEX = 1 # The hand color
HEADS_INDEX = 2 # A list of heads
HEAD_TEXTURE_INDEX = 3 # The texture to use for the head
HEIGHT_INDEX = 4 # The height of the cog

#These are used for setting the cogs height in size events.
Normal = 0
Small = 1
Big = 2


if base.config.GetBool('want-tiny-cogs'):
 heightindex = Small 
 aSize = 12.12
 bSize = 10.58
 cSize = 8.28
elif base.config.GetBool('want-big-cogs'):
 heightindex = Big
 aSize = 2.03
 bSize = 2.795
 cSize = 2.07 
else:
 heightindex = Normal
 aSize = 6.06 # Size of body type 'a'
 bSize = 5.29 # Size of body type 'b'
 cSize = 4.14 # Size of body type 'c'
 
if heightindex == Small:
 #Sellbots
 CCHeight = 2.315
 TMHeight = 2.62
 NDHeight = 2.99
 GHHeight = 3.2
 MSHeight = 3.35
 TFHeight = 3.475
 MHeight = 3.805
 MRHHeight = 4.475
 #Bossbots
 FHeight = 2.44
 PHeight = 2.5
 YMHeight = 2.64
 MMHeight = 1.625
 DSHeight = 3.04
 HHHeight = 3.725
 CRHeight = 4.115
 TBCHeight = 4.67
 #Cashbots
 SCHeight = 2.385
 PPHeight = 2.63
 TWHeight = 2.705
 BCHeight = 2.975
 NCHeight = 3.61
 MBHeight = 3.485
 LSHeight = 4.29
 RBHeight = 4.475
 #Lawbots
 BFHeight = 2.405
elif heightindex == Big:
 #Sellbots
 CCHeight = 9.26
 TMHeight = 10.48
 NDHeight = 11.96
 GHHeight = 12.8
 MSHeight = 13.4
 TFHeight = 13.9
 MHeight = 15.22
 MRHHeight = 17.9
 #Bossbots
 FHeight = 9.76
 PHeight = 10.0
 YMHeight = 10.56
 MMHeight = 6.50
 DSHeight = 12.16
 HHHeight = 14.90
 CRHeight = 16.46
 TBCHeight = 18.68
 #Cashbots
 SCHeight = 9.54
 PPHeight = 10.52
 TWHeight = 10.82
 BCHeight = 11.90
 NCHeight = 14.44
 MBHeight = 13.94
 LSHeight = 17.16
 RBHeight = 17.90
 #Lawbots
 BFHeight = 9.62
elif heightindex == Normal:
 #Sellbots
 CCHeight = 4.63
 TMHeight = 5.24
 NDHeight = 5.98
 GHHeight = 6.4
 MSHeight = 6.7
 TFHeight = 6.95
 MHeight = 7.61
 MRHHeight = 8.95
 #Bossbots
 FHeight = 4.88
 PHeight = 5.0
 YMHeight = 5.28
 MMHeight = 3.25
 DSHeight = 6.08
 HHHeight = 7.45
 CRHeight = 8.23
 TBCHeight = 9.34
 #Cashbots
 SCHeight = 4.77
 PPHeight = 5.26
 TWHeight = 5.41
 BCHeight = 5.95
 NCHeight = 7.22
 MBHeight = 6.97
 LSHeight = 8.58
 RBHeight = 8.95
 #Lawbots
 BFHeight = 4.81
else:
 pass

ColdCallerHead = VBase4(0.25, 0.35, 1.0, 1.0) # Head used by Cold Caller

            # Bossbots
suitProperties = {'f': (4.0 / cSize, SuitDNA.corpPolyColor, ['flunky', 'glasses'], '', FHeight),
                  'p': (3.35 / bSize, SuitDNA.corpPolyColor, ['pencilpusher'], '', PHeight),
                  'ym': (4.125 / aSize, SuitDNA.corpPolyColor, ['yesman'], '', YMHeight),
                  'mm': (2.5 / cSize, SuitDNA.corpPolyColor, ['micromanager'], '', MMHeight),
                  'ds': (4.5 / bSize, SuitDNA.corpPolyColor, ['beancounter'], '', DSHeight),
                  'hh': (6.5 / aSize, SuitDNA.corpPolyColor, ['headhunter'], '', HHHeight),
                  'cr': (6.75 / cSize, VBase4(0.85, 0.55, 0.55, 1.0), ['flunky'], 'corporate-raider.jpg', CRHeight),
                  'tbc': (7.0 / aSize, VBase4(0.75, 0.95, 0.75, 1.0), ['bigcheese'], '', TBCHeight),
                  # Lawbots
                  'bf': (4.0 / cSize, SuitDNA.legalPolyColor, ['tightwad'], 'bottom-feeder.jpg', BFHeight),
                  'b': (4.375 / bSize, VBase4(0.95, 0.95, 1.0, 1.0), ['movershaker'], 'blood-sucker.jpg', 6.17),
                  'dt': (4.25 / aSize, SuitDNA.legalPolyColor, ['twoface'], 'double-talker.jpg', 5.63),
                  'ac': (4.35 / bSize, SuitDNA.legalPolyColor, ['ambulancechaser'], '', 6.39),
                  'bs': (4.5 / aSize, SuitDNA.legalPolyColor, ['backstabber'], '', 6.71),
                  'sd': (5.65 / bSize, VBase4(0.5, 0.8, 0.75, 1.0), ['telemarketer'], 'spin-doctor.jpg', 7.9),
                  'le': (7.125 / aSize, VBase4(0.25, 0.25, 0.5, 1.0), ['legaleagle'], '', 8.27),
                  'bw': (7.0 / aSize, SuitDNA.legalPolyColor, ['bigwig'], '', 8.69),
                  # Cashbots
                  'sc': (3.6 / cSize, SuitDNA.moneyPolyColor, ['coldcaller'], '', SCHeight),
                  'pp': (3.55 / aSize, VBase4(1.0, 0.5, 0.6, 1.0), ['pennypincher'], '', PPHeight),
                  'tw': (4.5 / cSize, SuitDNA.moneyPolyColor, ['tightwad'], '', TWHeight),
                  'bc': (4.4 / bSize, SuitDNA.moneyPolyColor, ['beancounter'], '', BCHeight),
                  'nc': (5.25 / aSize, SuitDNA.moneyPolyColor, ['numbercruncher'], '', NCHeight),
                  'mb': (5.3 / cSize, SuitDNA.moneyPolyColor, ['moneybags'], '', MBHeight),
                  'ls': (6.5 / bSize, VBase4(0.5, 0.85, 0.75, 1.0), ['loanshark'], '', LSHeight),
                  'rb': (7.0 / aSize, SuitDNA.moneyPolyColor, ['yesman'], 'robber-baron.jpg', RBHeight),
                  # Sellbots
                  'cc': (3.5 / cSize, VBase4(0.55, 0.65, 1.0, 1.0), ['coldcaller'], '', CCHeight),
                  'tm': (3.75 / bSize, SuitDNA.salesPolyColor, ['telemarketer'], '', TMHeight),
                  'nd': (4.35 / aSize, SuitDNA.salesPolyColor, ['numbercruncher'], 'name-dropper.jpg', NDHeight),
                  'gh': (4.75 / cSize, SuitDNA.salesPolyColor, ['gladhander'], '', GHHeight),
                  'ms': (4.75 / bSize, SuitDNA.salesPolyColor, ['movershaker'], '', MSHeight),
                  'tf': (5.25 / aSize, SuitDNA.salesPolyColor, ['twoface'], '', TFHeight),
                  'm': (5.75 / aSize, SuitDNA.salesPolyColor, ['twoface'], 'mingler.jpg', MHeight),
                  'mh': (7.0 / aSize, SuitDNA.salesPolyColor, ['yesman'], '', MRHHeight),
                  }
