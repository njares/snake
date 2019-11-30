import sys
import pygame
import random
import pdb#; pdb.set_trace()
# Definiciones

usage='\nUso:\n'
usage+='python3 main.py <ancho> <alto> <AI>\n'
usage+=' <ancho> : <int> \n'
usage+=' <alto> : <int>\n'
usage+=' <AI> : {on | off} \n'

nargs=4
black = 0, 0, 0
up=273
le=276
do=274
ri=275

dir_up=[0,-10]
dir_le=[-10,0]
dir_do=[0,10]
dir_ri=[10,0]

conex_flag=True
turn_flag=0
hambre=0

# chequeo inicial

if len(sys.argv)!=nargs:
	print(usage)
	sys.exit()
else:
	width = int(sys.argv[1])*10
	height = int(sys.argv[2])*10
	AI = sys.argv[3]

if AI=='on':
	AI=True
elif AI=='off':
	AI=False

# AI

def vecinos(r,new):
	if abs(r[0]-new[0])+abs(r[1]-new[1]) <11:
		return True
	else:
		return False

def cuenta_cc(snake):
	# agarro todos los cuadraditos
	cuad=[]
	for i in range(width//10):
		for j in range(height//10):
			cuad+=[[i*10,j*10]]
	# saco los de la viborita de ahora
	for r in snake:
		if r in cuad:
			cuad.pop(cuad.index(r))
		else:
			print('TODO MAL!!')
			pdb.set_trace()
	#pdb.set_trace()
	# elijo uno como descubierto
	desc=[]
	vec=[]
	conex_comps=[]
	while len(cuad):
		if not desc:
			#elijo un nodo inicial y lo saco
			new=cuad.pop()
			for r in cuad:
				#agrego sus vecinos no descubiertos
				if vecinos(r,new) and r not in vec:
					vec+=[r]
			#lo pongo en descubiertos
			desc=[new]
		else:
			#veo si quedan vecinos
			if vec:
				#elijo un vecino y lo saco
				new=vec.pop()
				cuad.pop(cuad.index(new))
				for r in cuad:
					#agrego sus vecinos no descubiertos
					if vecinos(r,new) and r not in vec:
						vec+=[r]
				#lo pongo en descubiertos
				desc+=[new]
			#si no quedan vecinos
			else:
				#termine una componente
				#acomodo para empezar una nueva
				conex_comps+=[desc]
				desc=[]
				vec=[]
	conex_comps+=[desc]
	return conex_comps

def hay_mas_de_n(sn_dir,snake,n):
	dire=sn_dir
	for i in range(1,n+1):
		head=pygame.Rect(snake[0][0]+dire[0]*i,snake[0][1]+dire[1]*i,10,10)
		sn_he=[snake[0][0]+dire[0]*i,snake[0][1]+dire[1]*i]
		if head.left < 0 or head.right > width or head.top < 0 or head.bottom > height or sn_he in snake:
			return False
	return True

def AI_dir(sn_dir,snake,com,conex_flag,turn_flag,hambre):
	direcciones=[dir_up,dir_le,dir_do,dir_ri]
	#descartar direccion actual
	direcciones.pop(direcciones.index([-sn_dir[0],-sn_dir[1]]))
	#descartar direccion de pared
	#descartar direccion de cuerpo
	dir_desc=[]
	for dire in direcciones:
		head=pygame.Rect(snake[0][0]+dire[0],snake[0][1]+dire[1],10,10)
		if head.left < 0 or head.right > width or head.top < 0 or head.bottom > height or [snake[0][0]+dire[0],snake[0][1]+dire[1]] in snake:
			dir_desc.append(dire)
	if direcciones==dir_desc:
		sn_ta=snake[-1]
		if vecinos(sn_ta,snake[0]):
			print('modo kamikaze PURO!!!!')
			#input()
			return conex_flag,turn_flag,[sn_ta[0]-snake[0][0],sn_ta[1]-snake[0][1]]
		print('oh! resignacion')
		#input()
		return conex_flag,turn_flag,sn_dir
	for dire in dir_desc:
		direcciones.pop(direcciones.index(dire))
	# contar componentes conexas actuales
	cur_conex_comp=cuenta_cc(snake)
	if ((width//10)*(height//10))-len(snake)<=3 and not JustEat:
		for comp in cur_conex_comp:
			if com in comp:
				print('COMIENDO Cerca del final FINAL')
				print(direcciones)
				#input()
				cur_dir=direcciones[0]
				dire=cur_dir
				sn_he=[snake[0][0]+dire[0],snake[0][1]+dire[1]]
				cur_dist= abs(sn_he[0]-com[0])+abs(sn_he[1]-com[1])
				new_dirs=[cur_dir]
				for dire in direcciones:
					sn_he=[snake[0][0]+dire[0],snake[0][1]+dire[1]]
					new_dist= abs(sn_he[0]-com[0])+abs(sn_he[1]-com[1])
					if new_dist<cur_dist:
						cur_dist=new_dist
						new_dirs=[dire]
					elif new_dist==cur_dist and dire not in new_dirs:
						new_dirs+=[dire]
				if len(new_dirs)==1:
					return conex_flag,turn_flag,new_dirs[0] # [left,up]
				else:
					return conex_flag,turn_flag,new_dirs[random.randrange(0,2)] # [left,up]
	if len(cur_conex_comp)==1 and len(snake)/((width//10)*(height//10))>0.9:
		conex_flag=False
	if len(cur_conex_comp)==1:
		if vecinos(snake[-1],snake[0]) and not JustEat and not (random.randrange(0,hambre+1)>len(snake) and random.randrange(0,2)):
			print('modo kamikaze COLA!!!! (1 comp)')
			#input()
			return conex_flag,turn_flag,[snake[-1][0]-snake[0][0],snake[-1][1]-snake[0][1]]
		comp=cur_conex_comp[0]
		if len(comp)<=6 and ((width//10)*(height//10))-len(snake)<=6 and not JustEat:
			if com in comp:
				print('COMIENDO Cerca del final')
				print(direcciones)
				#input()
				cur_dir=direcciones[0]
				dire=cur_dir
				sn_he=[snake[0][0]+dire[0],snake[0][1]+dire[1]]
				cur_dist= abs(sn_he[0]-com[0])+abs(sn_he[1]-com[1])
				new_dirs=[cur_dir]
				for dire in direcciones:
					sn_he=[snake[0][0]+dire[0],snake[0][1]+dire[1]]
					new_dist= abs(sn_he[0]-com[0])+abs(sn_he[1]-com[1])
					if new_dist<cur_dist:
						cur_dist=new_dist
						new_dirs=[dire]
					elif new_dist==cur_dist and dire not in new_dirs:
						new_dirs+=[dire]
				return conex_flag,turn_flag,new_dirs[0] # [left,up]
		if len(snake)/((width//10)*(height//10))>0.6:
			# descartar direcciones que incrementen las componentes conexas
			dir_desc=[]
			for dire in direcciones:
				new_conex_comp=cuenta_cc([[snake[0][0]+dire[0],snake[0][1]+dire[1]]]+snake)
				if len(new_conex_comp)>len(cur_conex_comp):
					dir_desc.append(dire)
			if len(direcciones)>len(dir_desc):
				if len(dir_desc):
					print('esquivando incrementar componentes conexas')
					print(direcciones)
					print(dir_desc)
					#input()
					for dire in dir_desc:
						direcciones.pop(direcciones.index(dire))
		# esquivar la cola
		if len(snake)/((width//10)*(height//10))>0.8:
			cur_dir=direcciones[0]
			dire=cur_dir
			sn_he=[snake[0][0]+dire[0],snake[0][1]+dire[1]]
			cur_dist= abs(sn_he[0]-snake[-1][0])+abs(sn_he[1]-snake[-1][1])
			new_dirs=[cur_dir]
			for dire in direcciones:
				sn_he=[snake[0][0]+dire[0],snake[0][1]+dire[1]]
				new_dist= abs(sn_he[0]-snake[-1][0])+abs(sn_he[1]-snake[-1][1])
				if new_dist>cur_dist:
					cur_dist=new_dist
					new_dirs=[dire]
				elif new_dist==cur_dist and dire not in new_dirs:
					new_dirs+=[dire]
			if len(new_dirs)==1 and not vecinos(snake[0],snake[-1]):
				print('queda una sola opcion segun la norma 1 (COLA)(1 comp)')
				print(new_dirs[0])
				#input()
				return conex_flag,turn_flag,new_dirs[0] # [left,up]
		if random.randrange(0,hambre+1)>len(snake)+width and len(direcciones)>1:
			i_r=random.randrange(0,len(direcciones))
			print('locura de hambre!')
			#input()
			return conex_flag,turn_flag,direcciones[i_r]
		# comida y cola en la misma componente
		if len(snake)/((width//10)*(height//10))<0.9:
			print('Todo bien, comiendo')
			#input()
			cur_dir=direcciones[0]
			dire=cur_dir
			sn_he=[snake[0][0]+dire[0],snake[0][1]+dire[1]]
			cur_dist= abs(sn_he[0]-com[0])+abs(sn_he[1]-com[1])
			new_dirs=[cur_dir]
			for dire in direcciones:
				sn_he=[snake[0][0]+dire[0],snake[0][1]+dire[1]]
				new_dist= abs(sn_he[0]-com[0])+abs(sn_he[1]-com[1])
				if new_dist<cur_dist:
					cur_dist=new_dist
					new_dirs=[dire]
				elif new_dist==cur_dist and dire not in new_dirs:
					new_dirs+=[dire]
			if len(new_dirs)==1:
				print('queda una sola opcion segun la norma 1')
				print(new_dirs[0])
				#input()
				return conex_flag,turn_flag,new_dirs[0] # [left,up]
			# sino, voy hacia la pared mas cercana
			if random.randrange(0,3)==1:
				if new_dirs[0][0]<new_dirs[1][0]:
					print('yendo a alguna pared')
					return conex_flag,turn_flag,new_dirs[0]
				elif new_dirs[0][0]>new_dirs[1][0]:
					print('yendo a alguna pared')
					return conex_flag,turn_flag,new_dirs[1]
			elif random.randrange(0,3):
				if new_dirs[0][1]<new_dirs[1][1]:
					print('yendo a alguna pared')
					return conex_flag,turn_flag,new_dirs[0]
				elif new_dirs[0][1]>new_dirs[1][1]:
					print('yendo a alguna pared')
					return conex_flag,turn_flag,new_dirs[1]
			# sino, elijo la de menor distancia absoluta
			direcciones=new_dirs
			new_dir=direcciones[0]
			dire=new_dir
			sn_he=[snake[0][0]+dire[0],snake[0][1]+dire[1]]
			cur_dist= abs(sn_he[0]-com[0])**2+abs(sn_he[1]-com[1])**2
			for dire in direcciones:
				sn_he=[snake[0][0]+dire[0],snake[0][1]+dire[1]]
				new_dist= abs(sn_he[0]-com[0])**2+abs(sn_he[1]-com[1])**2
				if new_dist<cur_dist:
					cur_dist=new_dist
					new_dir=dire
			print('yendo con norma 2')
			return conex_flag,turn_flag,new_dir
	#si hay mas de una componente conexa, veo si alguna tiene la cola
	if len(cur_conex_comp)>1:# and (max([len(comp) for comp in cur_conex_comp])<len(snake) or not random.randrange(0,10)):
		aux_conex_comp=cur_conex_comp.copy()
		sn_ta=snake[-1]
		ta_up=[sn_ta[0]+dir_up[0],sn_ta[1]+dir_up[1]]
		ta_do=[sn_ta[0]+dir_do[0],sn_ta[1]+dir_do[1]]
		ta_le=[sn_ta[0]+dir_le[0],sn_ta[1]+dir_le[1]]
		ta_ri=[sn_ta[0]+dir_ri[0],sn_ta[1]+dir_ri[1]]
		for i in range(len(aux_conex_comp)):
			if ta_up in aux_conex_comp[i] or ta_do in aux_conex_comp[i] or ta_le in aux_conex_comp[i] or ta_ri in aux_conex_comp[i]:
				aux_conex_comp[i]+=[sn_ta]
		dir_desc=[]
		for dire in direcciones:
			sn_he=[snake[0][0]+dire[0],snake[0][1]+dire[1]]
			not_in_any_comp=True
			for comp in aux_conex_comp:
				if sn_he in comp and sn_ta in comp:
					not_in_any_comp=False
					break
			if not_in_any_comp:
				dir_desc+=[dire]
		if direcciones==dir_desc:
			print('cola no accesible!!!')
			if vecinos(sn_ta,snake[0]) and not JustEat:
				print('modo kamikaze COLA!!!!')
				#input()
				return conex_flag,turn_flag,[sn_ta[0]-snake[0][0],sn_ta[1]-snake[0][1]]
		else:
			if len(dir_desc):
				print('buscando la cola')
				print(direcciones)
				print(dir_desc)
				#input()
			for dire in dir_desc:
				direcciones.pop(direcciones.index(dire))
		# si queda mas de una direccion, las que no vayan a la componente conexa mas grande
		if len(direcciones)>1 and len(cur_conex_comp)>1:
			cur_dir=direcciones[0]
			dire=cur_dir
			new_dirs=[dire]
			sn_he=[snake[0][0]+dire[0],snake[0][1]+dire[1]]
			for comp in cur_conex_comp:
				if sn_he in comp:
					cur_size=len(comp)
					break
			for dire in direcciones:
				sn_he=[snake[0][0]+dire[0],snake[0][1]+dire[1]]
				for comp in cur_conex_comp:
					if sn_he in comp:
						new_size=len(comp)
						break
				if new_size>cur_size:
					cur_dir=dire
					new_dirs=[dire]
				elif new_size==cur_size and dire not in new_dirs:
					new_dirs+=[dire]
			if len(new_dirs)==1:					
				new_dir=new_dirs[0]
				print('yendo para donde hay mas espacio')
				print(new_dirs)
				print(new_dir)
				#input()
				return conex_flag,turn_flag,new_dir
			direcciones=new_dirs
	# ~ if len(snake)/((width//10)*(height//10))>0.8:
		# ~ # descartar direcciones que incrementen las componentes conexas
		# ~ dir_desc=[]
		# ~ for dire in direcciones:
			# ~ new_conex_comp=cuenta_cc([[snake[0][0]+dire[0],snake[0][1]+dire[1]]]+snake)
			# ~ if len(new_conex_comp)>len(cur_conex_comp):
				# ~ dir_desc.append(dire)
		# ~ if len(direcciones)>len(dir_desc):
			# ~ if len(dir_desc):
				# ~ print('esquivando incrementar componentes conexas')
				# ~ print(direcciones)
				# ~ print(dir_desc)
				# ~ #input()
				# ~ for dire in dir_desc:
					# ~ direcciones.pop(direcciones.index(dire))
	# Al final solo esquivar la cola
	if len(snake)/((width//10)*(height//10))>0.9:
		cur_dir=direcciones[0]
		dire=cur_dir
		sn_he=[snake[0][0]+dire[0],snake[0][1]+dire[1]]
		cur_dist= abs(sn_he[0]-snake[-1][0])+abs(sn_he[1]-snake[-1][1])
		new_dirs=[cur_dir]
		for dire in direcciones:
			sn_he=[snake[0][0]+dire[0],snake[0][1]+dire[1]]
			new_dist= abs(sn_he[0]-snake[-1][0])+abs(sn_he[1]-snake[-1][1])
			if new_dist>cur_dist:
				cur_dist=new_dist
				new_dirs=[dire]
			elif new_dist==cur_dist and dire not in new_dirs:
				new_dirs+=[dire]
		if len(new_dirs)==1  and not vecinos(snake[0],snake[-1]):
			print('queda una sola opcion segun la norma 1 (COLA)(2 comp)')
			print(new_dirs[0])
			#input()
			return conex_flag,turn_flag,new_dirs[0] # [left,up]
		if random.randrange(0,2) and random.randrange(0,hambre+1)>len(snake)+width*2:
			print('HAMBRE (COLA)(2 comp)')
			if len(new_dirs)==1:
				return conex_flag,turn_flag,new_dirs[0] # [left,up]
			else:
				return conex_flag,turn_flag,new_dirs[random.randrange(0,2)] # [left,up]
		# sino, elijo la de menor distancia absoluta
		direcciones=new_dirs
		new_dir=direcciones[0]
		dire=new_dir
		sn_he=[snake[0][0]+dire[0],snake[0][1]+dire[1]]
		cur_dist= abs(sn_he[0]-snake[-1][0])**2+abs(sn_he[1]-snake[-1][1])**2
		for dire in direcciones:
			sn_he=[snake[0][0]+dire[0],snake[0][1]+dire[1]]
			new_dist= abs(sn_he[0]-snake[-1][0])**2+abs(sn_he[1]-snake[-1][1])**2
			if new_dist>cur_dist:
				cur_dist=new_dist
				new_dir=dire
		print('yendo con norma 2 (COLA)(2 comp)')
		return conex_flag,turn_flag,new_dir
	#si hay mas de una componente conexa, y ambas con cola, pánico
	if len(cur_conex_comp)>1 or turn_flag:
		if turn_flag==0:
			print('Ingrese al modo survival!')
			if len(snake)/((width//10)*(height//10))>=0.7:
				print('Para siempre...')
				#input()
			print(direcciones)
			#input()
			turn_flag=random.randrange(0,2)*2-1
			# intento girar a algun lado
			if turn_flag==1:
				gir = [-sn_dir[1],sn_dir[0]]
			elif turn_flag==-1:
				gir = [sn_dir[1],-sn_dir[0]]
			if gir in direcciones:
				return conex_flag,turn_flag,gir
			# intento girar al otro lado
			turn_flag=-turn_flag
			if [-gir[0],-gir[1]] in direcciones:
				return conex_flag,turn_flag,[-gir[0],-gir[1]]
		else:
			# intento seguir girando
			if turn_flag==1:
				gir = [-sn_dir[1],sn_dir[0]]
			elif turn_flag==-1:
				gir = [sn_dir[1],-sn_dir[0]]
			if abs(turn_flag)==1:
				if (not random.randrange(0,2)) and random.randrange(0,hambre+1)>len(snake)+width*2 and (conex_flag or ((width//10)*(height//10))<hambre):
					gir2=[-gir[0],-gir[0]]
					if gir2 in direcciones:
						turn_flag*=-1
						gir=gir2
						print('girando... ooosooo')
						print(direcciones)
						#input()
						if len(cur_conex_comp)==1 and len(snake)/((width//10)*(height//10))<0.7:
							print('SALI DE MODO SURVIVAL!')
							#input()
							turn_flag=0
						else:
							return conex_flag,turn_flag,gir
				if gir in direcciones:
					print('girando girando')
					print(direcciones)
					#input()
					if len(cur_conex_comp)==1 and len(snake)/((width//10)*(height//10))<0.7:
						print('SALI DE MODO SURVIVAL!')
						#input()
						turn_flag=0
					else:
						return conex_flag,turn_flag,gir
			# intento seguir derecho
			if len(snake)/((width//10)*(height//10))<0.33:
				n=3
			elif len(snake)/((width//10)*(height//10))<0.66:
				n=2
			else:
				n=1
			if sn_dir in direcciones and hay_mas_de_n(sn_dir,snake,n):
				if abs(turn_flag)==1:
					turn_flag*=2
				print('siguiendo derecho!')
				print(direcciones)
				#input()
				if len(cur_conex_comp)==1 and len(snake)/((width//10)*(height//10))<0.70:
					print('SALI DE MODO SURVIVAL!')
					#input()
					turn_flag=0
				else:
					return conex_flag,turn_flag,sn_dir
			# cambio el sentido de giro
			if ((not random.randrange(0,width//20)) or not turn_flag):# and n!=1:
				turn_flag=random.randrange(0,2)*2-1
			else:
				turn_flag=-turn_flag//abs(turn_flag)
			if turn_flag==1:
				gir = [-sn_dir[1],sn_dir[0]]
			elif turn_flag==-1:
				gir = [sn_dir[1],-sn_dir[0]]
			if gir in direcciones:
				print('cambiando giro!')
				print(direcciones)
				print(sn_dir)
				#input()
				if len(cur_conex_comp)==1 and len(snake)/((width//10)*(height//10))<0.7:
					print('SALI DE MODO SURVIVAL!')
					#input()
					turn_flag=0
				else:
					return conex_flag,turn_flag,gir
	#  buscar las direcciones disponibles mas cercanas al destino
	if random.randrange(0,hambre+1)>len(snake)+width and len(direcciones)>1:
		i_r=random.randrange(0,len(direcciones))
		print('locura de hambre! (cuidado)')
		#input()
		return conex_flag,turn_flag,direcciones[i_r]
	# comida y cola en la misma componente
	print('comiendo con cuidado...')
	#input()
	cur_dir=direcciones[0]
	dire=cur_dir
	sn_he=[snake[0][0]+dire[0],snake[0][1]+dire[1]]
	cur_dist= abs(sn_he[0]-com[0])+abs(sn_he[1]-com[1])
	new_dirs=[cur_dir]
	for dire in direcciones:
		sn_he=[snake[0][0]+dire[0],snake[0][1]+dire[1]]
		new_dist= abs(sn_he[0]-com[0])+abs(sn_he[1]-com[1])
		if new_dist<cur_dist:
			cur_dist=new_dist
			new_dirs=[dire]
		elif new_dist==cur_dist and dire not in new_dirs:
			new_dirs+=[dire]
	if len(new_dirs)==1:
		print('queda una sola opcion segun la norma 1 (cuidado)')
		print(new_dirs[0])
		#input()
		return conex_flag,turn_flag,new_dirs[0] # [left,up]
	else:
	# si da lo mismo, voy hacia la pared mas cercana
		if random.randrange(0,3)==1:
			if new_dirs[0][0]<new_dirs[1][0]:
				print('yendo a alguna pared (cuidado)')
				return conex_flag,turn_flag,new_dirs[0]
			elif new_dirs[0][0]>new_dirs[1][0]:
				print('yendo a alguna pared (cuidado)')
				return conex_flag,turn_flag,new_dirs[1]
		elif random.randrange(0,3):
			if new_dirs[0][1]<new_dirs[1][1]:
				print('yendo a alguna pared (cuidado)')
				return conex_flag,turn_flag,new_dirs[0]
			elif new_dirs[0][1]>new_dirs[1][1]:
				print('yendo a alguna pared (cuidado)')
				return conex_flag,turn_flag,new_dirs[1]
	# sino, elijo la de menor distancia absoluta
	direcciones=new_dirs
	new_dir=direcciones[0]
	dire=new_dir
	sn_he=[snake[0][0]+dire[0],snake[0][1]+dire[1]]
	cur_dist= abs(sn_he[0]-com[0])**2+abs(sn_he[1]-com[1])**2
	for dire in direcciones:
		sn_he=[snake[0][0]+dire[0],snake[0][1]+dire[1]]
		new_dist= abs(sn_he[0]-com[0])**2+abs(sn_he[1]-com[1])**2
		if new_dist<cur_dist:
			cur_dist=new_dist
			new_dir=dire
	print('yendo con norma 2 (cuidado)')
	return conex_flag,turn_flag,new_dir

# inicio propiamente dicho

pygame.init()

size = width, height
screen = pygame.display.set_mode(size)

snake = [[10*(width//20),10*(height//20-1)],[10*(width//20)-10,10*(height//20-1)],[10*(width//20)-20,10*(height//20-1)],[10*(width//20)-30,10*(height//20-1)]]

comida = [[snake[0][0]+dir_do[0]*3,snake[0][1]+dir_do[1]*3]]

sn_dir=dir_ri

JustEat=False

print("Presione una tecla para empezar")
input()

while 1:
	dir_upd=False
	for event in pygame.event.get():
		if event.type == pygame.QUIT: sys.exit()
	#actualizar dirección con controles
		if event.type == pygame.KEYDOWN and not AI:
			if event.dict['key']==up and sn_dir!=dir_do:
				new_dir=dir_up
				dir_upd=True
			elif event.dict['key']==le and sn_dir!=dir_ri:
				new_dir=dir_le
				dir_upd=True
			elif event.dict['key']==do and sn_dir!=dir_up:
				new_dir=dir_do
				dir_upd=True
			elif event.dict['key']==ri and sn_dir!=dir_le:
				new_dir=dir_ri
				dir_upd=True

	#actualizar direccion con AI
	if AI:
		conex_flag,turn_flag,new_dir=AI_dir(sn_dir,snake,comida[-1],conex_flag,turn_flag,hambre)
		dir_upd=True
		if new_dir==dir_up:
			print('up')
		elif new_dir==dir_do:
			print('do')
		elif new_dir==dir_ri:
			print('ri')
		elif new_dir==dir_le:
			print('le')

	#mover snake
	if dir_upd:
		sn_dir=new_dir
	if JustEat:
		JustEat=False
	else:
		snake.pop(-1)
	snake=[[snake[0][0]+sn_dir[0], snake[0][1]+sn_dir[1]]]+snake
	
	head=pygame.Rect(snake[0][0],snake[0][1],10,10)

	#ver si comio
	if [snake[0][0],snake[0][1]]==comida[-1]:
		new_comida=comida[-1]
		while new_comida in snake and len(snake)<((width//10)*(height//10)):
			new_comida=[random.randrange(0,width,10),random.randrange(0,height,10)]
		comida=comida+[new_comida]
		JustEat=True
		hambre=0
		print('comio!')
	hambre+=1
	
	#chequear si perdio
	if head.left < 0 or head.right > width or head.top < 0 or head.bottom > height:
		if ((width//10)*(height//10))-len(snake)<1:
			pygame.time.wait(500)
			print('VICTORIA!!!!')
		else:
			print("choque con pared")
			print(((width//10)*(height//10))-len(snake))
		input()
		sys.exit()
	elif [snake[0][0],snake[0][1]] in snake[1:]:
		if ((width//10)*(height//10))-len(snake)<1:
			pygame.time.wait(500)
			print('VICTORIA!!!!')
		else:
			print("choque consigo misma")
			print(((width//10)*(height//10))-len(snake))
		input()
		sys.exit()
	if ((width//10)*(height//10))-len(snake)<1:
		pygame.time.wait(500)
		print('VICTORIA!!!!')
		input()
		sys.exit()

	# dibujar
	if not AI:
		pygame.time.wait(25)
	else:
		if (abs((((width//10)*(height//10))-len(snake)))**1.5)<100:
			pygame.time.wait(int((100-abs((width//10)*(height//10)-len(snake))**1.5)/1.5)+15)
		else:
			pygame.time.wait(15)
	screen.fill(black)
	
	# cuerpo
	for i in range(1,len(snake)-1):
		pygame.draw.rect(screen,(0,255,0),pygame.Rect(snake[i][0]+1,snake[i][1]+1,8,8))
		pygame.draw.rect(screen,(0,255,0),pygame.Rect((snake[i][0]+1 + snake[i-1][0]+1)//2,(snake[i][1]+1 + snake[i-1][1]+1)//2,8,8))
	
	# cola
	pygame.draw.rect(screen,(0,255,0),pygame.Rect(snake[-1][0]+3,snake[-1][1]+3,4,4))
	pygame.draw.rect(screen,(0,255,0),pygame.Rect((snake[-1][0]+1+snake[-2][0]+1)//2+1,(snake[-1][1]+1+snake[-2][1]+1)//2+1,6,6))
	
	# cabeza
	#pygame.draw.rect(screen,(0,200,0),pygame.Rect(snake[0][0],snake[0][1],10,10))
	pygame.draw.circle(screen,(0,150,0),(snake[0][0]+5,snake[0][1]+5),6)
	
	#dibujar comida
	#pygame.draw.rect(screen,(255,0,0),pygame.Rect(comida[-1][0],comida[-1][1],10,10))
	pygame.draw.circle(screen,(255,0,0),(comida[-1][0]+5,comida[-1][1]+5),5)
    
	pygame.display.flip()
