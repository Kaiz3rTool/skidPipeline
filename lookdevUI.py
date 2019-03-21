# ****************************************** S K I D     L O O K D E V    U I ******************************************
import maya.cmds as cmds
import os
from functools import partial
from pymel.core import *

# ****************************************** G L O B A L S ******************************************

lookdevScenePath = os.path.abspath('//merlin/3d4/skid/09_dev/toolScripts/lookdev/lookdevSetup/LookdevSetup.ma')
hdri_folder = os.path.abspath('//Merlin/3d4/skid/04_asset/SkidLibrary/HDRI')
hdri_files = os.listdir(hdri_folder)
hdriTurnGrp = 'LookdevSetup:NEWBIE_TOOLS_GRP'
turnLocator = 'turn_locator'
grpName = 'LookdevSetup:GRP_LookdevSetup'
lookdevPreset = 'SKID_LookdevSetup'
scenePath = cmds.workspace(sn=True,q=True)
turnDurations = [8,50,100]

# ****************************************** F U N C T I O N S ******************************************

def chooseHDRfile(item,*args):
	resolveHDRpath = os.path.join(hdri_folder,item)
	cmds.setAttr('LookdevSetup:PxrDomeLight_HDRI.lightColorMap','%s' %resolveHDRpath,type='string')

# ****************************************** I N T E R F A C E ******************************************

def CreateUI(*args):
	# Try loading renderman and check version
	cmds.evalDeferred("cmds.loadPlugin(\"RenderMan_for_Maya.py\")")
	from rfm2.config import cfg
	rmanversion = cfg().rfm_env['versions']['rfm']
	print rmanversion
	if rmanversion != "22.3" :
		import commonTools
		commonTools.areeeeett()
		cmds.evalDeferred("cmds.warning('Wrong Renderman for Maya version (installed version is %s), should be 22.3')" % rmanversion)
	else :
		# define template
		template = uiTemplate(force=True)
		template.define(button,h=35,w=300,align='left')
		template.define(optionMenu,h=35,w=300)
		template.define(frameLayout, borderVisible=True, labelVisible=True)
		template.define(text,h=25)
		template.define(rowLayout)
		template.define(checkBox,h=35)

		try :
			cmds.deleteUI('lookdevWindow')
		except RuntimeError :
			pass

		with window('lookdevWindow', title="Skid Lookdev Tools",menuBar=True,menuBarVisible=True) as win:
			with template:
				with frameLayout(l='Project'):
					text('PROJECT IS SET TO')
					text(scenePath)

				with frameLayout('Scene Setup'):
					with columnLayout():
						with rowLayout(numberOfColumns=3,ad3=1):
							button(label='Import lookdev scene',w=198,\
								c='import lookdevTools; \
								reload(lookdevTools); \
								lookdevTools.importLookdevScene()')
							button(label='Hide',w=48, \
								c='import lookdevTools; \
								reload(lookdevTools); \
								lookdevTools.hideLookdevScene()')
							button(label='Reload',w=49, \
								c='import lookdevTools; \
								reload(lookdevTools); \
								lookdevTools.reloadLookdevScene()')
						button(l='Load Render Settings', \
							c='import commonTools; \
							reload(commonTools); \
							commonTools.loadRenderSettings("%s")' %lookdevPreset)
						optionMenu(changeCommand=chooseHDRfile)
						for file in hdri_files:
							menuItem(label=file)

				with frameLayout('Geometries'):
					with rowLayout(numberOfColumns=2):
							button(label='Attach Subdiv Scheme',w=149, \
								c='import commonTools; \
								reload(commonTools); \
								commonTools.RfMsubdivScheme(1)')
							button(label="Detach Subdiv Scheme",w=148, \
								c='import commonTools; \
								reload(commonTools); \
								commonTools.RfMsubdivScheme(0)')

				with frameLayout('Shading'):
					with columnLayout():
						with rowLayout(numberOfColumns=2,ad2=1):
							with columnLayout():
								button(l='Create PxrSurface network', \
									c='import lookdevTools; \
									reload(lookdevTools); \
									lookdevTools.createPxrSurfaceNetwork()')
								button(l='Create PxrLayer network', \
									c='import lookdevTools; \
									reload(lookdevTools); \
									lookdevTools.createPxrLayerNetwork()',en=False)
								button(l='Convert PxrSurface to PxrLayer', \
									c='import lookdevTools; \
									reload(lookdevTools); \
									lookdevTools.convertPxrSurfaceToLayer()')

				with frameLayout('Turn locator'):
					with columnLayout():
						with rowLayout(numberOfColumns=2,ad2=1):
							button(label="Create turn locator",w=248, \
								c='import lookdevTools; \
								reload(lookdevTools); \
								lookdevTools.initTurn("%s")' % turnLocator)
							button(label="Delete",  w=49, \
								c='import lookdevTools; \
								reload(lookdevTools); \
								lookdevTools.delete_turn_loc()')
						with rowLayout(numberOfColumns=3,ad3=2):
							for i in turnDurations: # Create one button for each possible turn duration
								button(label="%i frames" % i, w=98, \
									c='import lookdevTools; \
									reload(lookdevTools); \
									lookdevTools.changeFrameRange("%s",%i)' % (turnLocator,i))

				with frameLayout('Turn Lighting'):
					with columnLayout():
						with rowLayout(numberOfColumns=3,ad3=2):
							for i in turnDurations: # Create one button for each possible turn duration
								button(label="%i frames" % i, w=98, \
									c='import lookdevTools; \
									reload(lookdevTools); \
									lookdevTools.changeFrameRange("%s",%i); \
									lookdevTools.changeFrameRange("%s",%i,%i)' % (turnLocator,i,hdriTurnGrp,i,i))
						with rowLayout(numberOfColumns=1):
							button(label='Disable lighting turn', \
								c='import lookdevTools; \
								reload(lookdevTools); \
								lookdevTools.disableTurn("%s")' % hdriTurnGrp)

				with frameLayout('Nomenclatures'):
					button(label='Afficher nomenclatures',h=30, \
						c='import commonTools; \
						reload(commonTools); \
						commonTools.showNomenclatures()')

CreateUI()