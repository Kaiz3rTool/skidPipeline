# ****************************************** S K I D     A N I M     U I ******************************************

import maya.cmds as cmds
import maya.mel as mel
import os
import commonTools
from pymel.core import *

# ****************************************** G L O B A L S ******************************************

animScriptsPath = '//Merlin/3d4/skid/09_dev/toolScripts/publish/animScripts'
riggedAssets = ['propsBrevell','characterEthan','propsEthanHelmet','propsWerner','characterAlton','propsAltonHelmet']
chosenRig = 'propsBrevell'
animationWindow = "animationWindow"

# ****************************************** F U N C T I O N S ******************************************

def chooseRig(item,*args):
	global chosenRig
	chosenRig = item

def callImportRig(*args):
	import commonTools
	reload(commonTools)
	commonTools.importAssetMa(chosenRig)

def callContraintCharacterToCar(*args):
	import animationTools
	reload(animationTools)
	animationTools.contraintCharacterToCar(chosenRig)

def callToggleConstraintCar(*args):
	import animationTools
	reload(animationTools)
	animationTools.toggleConstraintCar(chosenRig)

def callPoseCar(*args):
	import animationTools
	reload(animationTools)
	animationTools.poseCar(chosenRig)

# ****************************************** I N T E R F A C E ******************************************

def CreateUI(*args):
	template = uiTemplate('ExampleTemplate', force=True)
	template.define(button, w=300, h=35, align='left')
	template.define(frameLayout, borderVisible=True, labelVisible=True)
	template.define(rowColumnLayout,numberOfColumns=2)
	template.define(optionMenu,w=200,h=30)
	template.define(text,w=100,h=30)

	try :
		cmds.deleteUI(animationWindow)
	except RuntimeError :
		pass

	with window(animationWindow, title='Animation Tools',menuBar=True,menuBarVisible=True) as win:
		with template:
			with columnLayout():

				with frameLayout('Animation Plugins'):
					with columnLayout():
						button(l='bhGhost', \
							c='import maya.mel as mel; \
							mel.eval(\'source "%s/bhGhost.mel"\'); \
							mel.eval(\'bhGhost()\')' %animScriptsPath)
						button(l='dkAnim', \
							c='import maya.mel as mel; \
							mel.eval(\'source "%s/dkAnim-v0.7-.mel"\'); \
							mel.eval(\'dkAnim()\')' %animScriptsPath)
						button(l='arcTracker', \
							c='import maya.mel as mel; \
							mel.eval(\'source "%s/arctracker110.mel"\'); \
							mel.eval(\'arctracker110()\')' %animScriptsPath)
						button(l='Studio Library', \
							c='import studiolibrary; \
							reload(studiolibrary); \
							studiolibrary.main()')
						

				with frameLayout('Animation Tools'):
					with rowColumnLayout():
						text(l='Current asset : ')
						with optionMenu(changeCommand=chooseRig):
							for asset in riggedAssets:
								menuItem(l=asset)
					with columnLayout():
						button(l='Import asset',c=callImportRig)

				# with frameLayout('Character Tools'):
				# 	with columnLayout():
				# 		button(l='Start pose !',c=callPoseCar)

				with frameLayout('Car Tools'):
					with columnLayout():
						button(l='Constraint character to car',c=callContraintCharacterToCar)
						button(l='Toggle constraint',c=callToggleConstraintCar)

						# button(l='Create Speed Attribute', \
						# 	c='import animationTools; \
						# 	reload(animationTools); \
						# 	animationTools.createSpeedAttribute()')
						button(l='Offset selected', \
							c='import maya.mel as mel; \
							mel.eval(\'source "%s/offset_node_multiple.mel"\')'%animScriptsPath)

				with frameLayout('Playblast'):
					with columnLayout():
						button(l='Playblast Animation', \
							c='import animationTools; \
							reload(animationTools); \
							animationTools.playblastAnim(False)')
						
			
				with frameLayout('Publish'):
					with columnLayout():
				# 		button(l='Export Selected', \
				# 			c='import animationTools; \
				# 			reload(animationTools); \
				# 			animationTools.exportAbcRfM()')
						button(l='Publish Playblast', \
							c='import animationTools; \
							reload(animationTools); \
							animationTools.playblastAnim(True)')
						button(l='Publish Camera', \
							c='import animationTools; \
							reload(animationTools); \
							animationTools.publishCamera()')
						button(l='Publish Animation', \
							c='import animationTools; \
							reload(animationTools); \
							animationTools.publishAnimations()')

				with frameLayout('Nomenclatures'):
					button(l='Afficher nomenclatures',h=30, \
						c='import commonTools; \
						reload(commonTools); \
						commonTools.showNomenclatures()')

CreateUI()