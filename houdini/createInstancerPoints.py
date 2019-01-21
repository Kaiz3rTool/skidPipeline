# hython createInstancerPoints.py 'seq0010_sh0050'


import sys, os

# Get params from shell command
currentShot = sys.argv[1] # Current shot (camera name)
fstart = float(sys.argv[2]) # Start Frame
fend = float(sys.argv[3]) # End Frame
mtop = float(sys.argv[4]) # Margin top
mright = float(sys.argv[5]) # Margin right
mbot = float(sys.argv[6]) # Margin bot
mleft = float(sys.argv[7]) # Margin left

# Convert margins to houdini values
mright += 1
mtop += 1
mleft = - mleft
mbot = - mbot

print('Generating instancer with arguments :\n')
print('currentShot : '+currentShot,type(currentShot))
print('fstart : ',fstart,type(fstart))
print('fend : ',fend,type(fend))
print('mtop : ',mtop,type(mtop))
print('mright : ',mright,type(mright))
print('mbot : ',mbot,type(mbot))
print('mleft : ',mleft,type(mleft))


# 1. Load scene containing setGleitenstrassen, toolCamImport
houScenePath = '//Merlin/3d4/skid/09_dev/toolScripts/publish/houdini/createInstancerPoints.hipnc'
hou.hipFile.load(houScenePath,suppress_save_prompt=True)
obj = hou.node('/obj')
print('Scene contents :')
for node in obj.allItems():
    print node.path()
print('Loaded scene succesfully')


# 2. Set toolCamImport to current shot

# VERIFIER SI LE FICHIER ABC DE LA CAM EXISTE PARCE QUE HOUDINI LE FAIT PAS

cam = '/obj/CameraImport1/'
hou.parm(cam+'fileName').set('$SHOT/%s/abc/%s.abc'%(currentShot,currentShot))
hou.parm(cam+'buildHierarchy').pressButton()
# hou.node(cam+'/obj/geo1/file1').parm('reload').pressButton() # Si la ligne au dessus ne marche pas
print('Camera imported succesfully')


# 3. Set up volume parameters
# Set camera path
volumePath = '/obj/setGleitenstrasse1/export_to_Maya/export_shot_scatterPoints_to_maya/volume2/'
camPath = '/obj/CameraImport1/shotCamera/%s/%sShape'%(currentShot,currentShot)
hou.parm(volumePath+'camera').set(camPath)
# Set margins
hou.parm(volumePath+'winxmin').set(str(mleft))
hou.parm(volumePath+'winxmax').set(str(mright))
hou.parm(volumePath+'winymin').set(str(mbot))
hou.parm(volumePath+'winymax').set(str(mtop))
print('Volume setup done')


# 4. Set framerange
hou.playbar.setFrameRange(fstart,fend)
hou.playbar.setPlaybackRange(fstart,fend)
hou.setFrame(fend)
# Verifier que le timeshift a bien $FEND en value
print('Frame range set to %s-%s'%(fstart,fend))


# 5. Filecache
fcPath = '/obj/setGleitenstrasse1/export_to_Maya/export_shot_scatterPoints_to_maya/fc_pointsToMaya/'
bgeoPath = '$SHOT/%s/geo/fileCache/%s_instancerPts.bgeo.sc'%(currentShot,currentShot)
hou.parm(fcPath+'file').set(str(bgeoPath))
print('Caching instancer points to : '+bgeoPath)
hou.parm(fcPath+'execute').pressButton()
print('Done !')
os.system('pause')


# 6. Check if bgeo exists
if not os.path.exist(bgeoPath):
	print('Point cloud cache failed for '+currentShot)
	os.system('pause')
	hou.exit(exit_code=1, suppress_save_prompt=True)
else :
	print('Point cloud was succesfully cached for '+currentShot)
	os.system('pause')
	hou.exit(exit_code=0, suppress_save_prompt=True)