def MatchBrand(products):
	"""match the brand for each product"""
	SpecialBrands={
	'leica':['leica'],
	'alpa':['alpa'],
	'benq':['benq'],
	'dnt':['dnt'],
	'lego':['lego'],
	'okaa':['okaa'],
	'qoer':['qoer'],
	'vibe':['vibe'],
	'aee':['aee'],
	'detu':['detu'],
	'dji':['dji'],
	'dxg':['dxg'],
	'jvc':['jvc'],
	'rca':['rca'],
	'svp':['svp'],
	'lg':['lg'],
	'hp':['hp']
	}
	Brands={
	'aiptek':['aiptek'],
	'aquapix':['aquapix'],
	'argus':['argus'],
	'bell&howell':['bell&howell','bell howell','bell+howell'],
	'blackmagic':['blackmagic'],
	'brinno':['brinno'],
	'canon':['canon','cannon','powershot','eos','ds 6041'],
	'casio':['casio'],
	'celestron':['celestron'],
	'cende':['cende'],
	'changhong':['changhong'],
	'chobi':['chobi cam','chobi mini'],
	'cokin':['cokin'],
	'coleman':['coleman'],
	'contax':['contax'],
	'contour':['contour'],
	'cotuo':['cotuo'],
	'crayola':['crayola'],
	'dahua':['dahua'],
	'digital blue':['digital blue'],
	'disney':['disney'],
	'drift':['drift','ghost-s'],
	'easypix':['easypix'],
	'emerson':['emerson'],
	'epson':['epson'],
	'fujifilm':['fuji','fugi','fu','fujifilm','finepix','hello kitty'],
	'fujitsu':['fujitsu'],
	'fvanor':['fvanor'],
	'garmin':['garmin'],
	'gateway':['gateway'],
	'general electric':['general electric','ge'],
	'global dc':['global dc','bonzart'],
	'gopro':['gopro','go pro','hero4','sj4000'],
	'hasselblad':['hasselblad'],
	'hikvision':['hikvision','ds-2'],
	'iclick':['iclick'],
	'intova':['intova'],
	'kodak':['kodak'],
	'konica minolta':['konica','minolta'],
	'lowrance':['lowrance'],
	'lytro':['lytro'],
	'minox':['minox'],
	'mikona':['mikona'],
	'motorola':['motorola'],
	'mustek':['mustek'],
	'nikon':['nikon','coolpix','nikkor'],
	'obsbot':['obsbot'],
	'olympus':['olympus','olymus'],
	'oregon scientific':['oregon scientific'],
	'panasonic':['panasonic'],
	'phase one':['phase one'],
	'philips':['philips','philip'],
	'pioneer':['pioneer'],
	'polaroid':['polaroid'],
	'pentax':['pentax'],
	'ricoh':['ricoh'],
	'rollei':['rollei'],
	'sakar':['sakar'],
	'samsung':['samsung'],
	'sanyo':['sanyo'],
	'sealife':['sealife'],
	'sioeye':['sioeye'],
	'sjcam':['sjcam'],
	'shetu':['shetu'],
	'shimano':['shimano'],
	'sony':['sony'],
	'toshiba':['toshiba'],
	'vivitar':['vivitar','vivicam'],
	'vistaquest':['vistaquest'],
	'vizio':['vizio'],
	'vtech':['vtech'],
	'wildgame':['wildgame'],
	'wingscapes':['wingscapes'],
	'zmodo':['zmodo']
	}
	accessory_words=[
	'bag',
	'case',
	'monopod',
	'sd card',
	'memory card',
	'battery',
	'light meter',
	'keychain',
	'lens',
	'backpack'
	]
	Brands.update(SpecialBrands)
	brands,pds_with_bds,pds_without_bds,bds=dict(),dict(),dict(),dict()
	num=0
	for pid in products.keys():
		is_find=False
		for pkey in ['brand','brand name','manufacturer','manufacture']:
			if is_find==False and pkey in products[pid].keys() and products[pid][pkey]!='oem':
				for key in Brands.keys():
					if is_find==False:
						for brand in Brands[key]:
							if is_find==False and brand==products[pid][pkey]:
								num+=1
								brands[pid]=key
								if key in pds_with_bds.keys():
									pds_with_bds[key][pid]=dict(products[pid])
								else:
									pds_with_bds[key]=dict()
									pds_with_bds[key][pid]=dict(products[pid])
								if key in bds:
									bds[key].append(pid)
								else:
									bds[key]=[pid]
								is_find=True
								break
					else:
						break
		if is_find:
			continue
		
		title=' '+products[pid].get('<page title>')+' '
		copy_p=products[pid].copy()
		copy_p.pop('<page title>')
		new_source=[]
		source_process(list(copy_p.values()),new_source)
		description=' '+' '.join(new_source)+' '
		for source in [title,description]:
			if is_find==False:
				for key in sorted(list(Brands.keys()),key=comp,reverse=True):
					if is_find==False:
						for brand in Brands[key]:
							if is_find==False and (' '+brand+' ') in source:
								is_error=False
								for aw in accessory_words:
									if brand+' '+aw in source:
										is_error=True
										break
								if not is_error:
									num+=1
									brands[pid]=key
									if key in pds_with_bds.keys():
										pds_with_bds[key][pid]=dict(products[pid])
									else:
										pds_with_bds[key]=dict()
										pds_with_bds[key][pid]=dict(products[pid])
									if key in bds:
										bds[key].append(pid)
									else:
										bds[key]=[pid]
									is_find=True
								break	
					else:
						break
		if not is_find:
			pds_without_bds[pid]=products[pid]
	print('pds_with_bds num:',len(pds_with_bds.keys()))
	for brand in pds_with_bds.keys():
		print(brand,':',len(pds_with_bds[brand].keys()))
	print('pds_without_bds num:',len(pds_without_bds.keys()))
	print(list(pds_without_bds.keys()))
	del products
	return (brands,pds_with_bds,pds_without_bds,bds)

