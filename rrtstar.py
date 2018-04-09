
import sys, random, math, pygame
from pygame.locals import *
from math import sqrt,cos,sin,atan2
from lineIntersect import *
import copy
import pdb

#constants
XDIM = 640
YDIM = 480
WINSIZE = [XDIM, YDIM]
EPSILON = 7.0
NUMNODES = 2000
RADIUS=15
OBS=[(500,150,100,50),(300,80,100,50),(150,220,100,50)]

def obsDraw(pygame,screen):
    blue=(0,0,255)
    for o in OBS: 
      pygame.draw.rect(screen,blue,o)

def dist(p1,p2):
    return sqrt((p1[0]-p2[0])*(p1[0]-p2[0])+(p1[1]-p2[1])*(p1[1]-p2[1]))

def step_from_to(p1,p2):
    if dist(p1,p2) < EPSILON:
        return p2
    else:
        theta = atan2(p2[1]-p1[1],p2[0]-p1[0])
        return p1[0] + EPSILON*cos(theta), p1[1] + EPSILON*sin(theta)

def chooseParent(nn,newnode,nodes):
        for p in nodes:
         if checkIntersect(p,newnode,OBS) and dist([p.x,p.y],[newnode.x,newnode.y]) <RADIUS and p.cost+dist([p.x,p.y],[newnode.x,newnode.y]) < nn.cost+dist([nn.x,nn.y],[newnode.x,newnode.y]):
          nn = p
        newnode.cost=nn.cost+dist([nn.x,nn.y],[newnode.x,newnode.y])
        newnode.parent=nn
        return newnode,nn

def reWire(nodes,newnode,pygame,screen):
        white = 255, 240, 200
        black = 20, 20, 40
        for i in range(len(nodes)):
           p = nodes[i]
           if checkIntersect(p,newnode,OBS) and p!=newnode.parent and dist([p.x,p.y],[newnode.x,newnode.y]) <RADIUS and newnode.cost+dist([p.x,p.y],[newnode.x,newnode.y]) < p.cost:
              pygame.draw.line(screen,white,[p.x,p.y],[p.parent.x,p.parent.y])  
              p.parent = newnode
              p.cost=newnode.cost+dist([p.x,p.y],[newnode.x,newnode.y]) 
              nodes[i]=p  
              pygame.draw.line(screen,black,[p.x,p.y],[newnode.x,newnode.y])                    
        return nodes

def drawSolutionPath(start,goal,nodes,pygame,screen):
	pink = 200, 20, 240
	nn = nodes[0]
  print nn.x, nn.y
	for p in nodes:
	   if dist([p.x,p.y],[goal.x,goal.y]) < dist([nn.x,nn.y],[goal.x,goal.y]):
	      nn = p
	while (nn.x, nn.y)!=(start.x, start.y):
		pygame.draw.line(screen,pink,[nn.x,nn.y],[nn.parent.x,nn.parent.y],5)  
		nn=nn.parent

'''class Cost:
    x = 0
    y = 0
    cost=0  
    parent=None
    def __init__(self,xcoord, ycoord):
         self.x = xcoord
         self.y = ycoord'''

class Node:
    x = 0
    y = 0
    cost=0  
    parent=None
    def __init__(self,xcoord, ycoord):
         self.x = xcoord
         self.y = ycoord

def extend(nodes, screen, black):

  rand = Node(random.random()* XDIM, random.random()*YDIM)
  nn= nodes[0]
  for p in nodes:
    if dist([p.x, p.y], [rand.x, rand.y]) < dist([nn.x, nn.y],[rand.x, rand.y]):
      nn = p
  interpolatedNode = step_from_to([nn.x, nn.y],[rand.x, rand.y])

  newnode = Node(interpolatedNode[0], interpolatedNode[1])

  if checkInterest(nn, newnode, OBS):

    [newnode, nn] = chooseParent(nn, newnode, nodes)
    nodes.append(newnode)
    pygame.draw.line(screen, black, [nn.x, nn.y], [newnode.x, newnode.y])
    pygame.display.update()

    for e in pygame.event.get():
      if e.type == QUIT or (e.type == KEYUP and e.key == K_ESCAPE):
        sys.exit("Leaving because you requested it.")
  return nodes

def find_q_nearest(nodes, target):
  ret_nodes = []
  nn=nodes[0]
  for p in nodes:
    if dist([p.x, p.y],[goal.x, goal.y]) < dist([nn.x, nn.y], [goal.x, goal.y]):
      nn = p
  while nn!=start:
    ret_nodes.append(nn)
    nn=nn.parent
  return ret_nodes

def reverse_path(parent, nodes):
  ret_nodes = []
  cur_parent = parent
  cur_node = nodes[0]

  while cur_node!=None:
    newnode = Node(cur_node.x, cur_node.y)
    newnode.parent = cur_parent
    cur_node = cur_node.parent
    cur_parent = newnode
    ret_nodes.append(newnode)
  return ret_nodes

	
def main():
    #initialize and prepare screen
    #a=checkIntersect()
    #print(a)
    pygame.init()
    screen = pygame.display.set_mode(WINSIZE)
    pygame.display.set_caption('Bi Directional RRTstar')
    white = 255, 255, 255
    black = 20, 20, 40
    screen.fill(white)
    obsDraw(pygame,screen)
    nodes_start = []
    nodes_goal = []
    
    nodes_start.append(Node(0.0,0.0)) # Start in the Top Left Corner
    nodes_goal.append(Node(630.0,470.0)) #End in the Bottom Right Corner
    
    start_begin = nodes_start[0]
    start_finish = nodes_goal[0]

    goal_begin = Node(630.0, 470.0)
    goal_finish = Node(0.0, 0.0)

    q_near = None
    q_tar = nodes_goal[0]

    for i in range(NUMNODES):
      if (i%2):
        nodes_start = extend(nodes_start, screen, black)

      else:
        nodes_goal = extend(nodes_goal, screen, black)
        q_tar = nodes_goal[len(nodes_goal)-1]
      q_near = find_q_nearest(nodes_start, q_tar)
      if(dist([q_tar.x, q_tar.y], [q_near.x, q_near.y]) < RADIUS):
        if checkIntersect(q_near, q_tar, OBS):
          newnode = Node(q_tar.x, q_tar.y)
          newnode.parent = q_near
          nodes_start.append(newnode)
          pygame.draw.line(screen, black, [q_near.x, q_near.y], [newnode.x, newnode.y])
        break



        
# if python says run, then we should run
if __name__ == '__main__':
    main()
    running = True
    while running:
       for event in pygame.event.get():
           if event.type == pygame.QUIT:
                 running = False



