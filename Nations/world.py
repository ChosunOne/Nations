from tile import tile
import pygame
import random
import math
from nation import nation
import time

class world():
    """This is the world in which the simulation takes place"""
    def __init__(self, width=100, 
                 height=100, 
                 tiles=None, 
                 nations=None, 
                 biomes=None, 
                 biomeStrength = .5,
                 viewMode = 0,
                 unclaimed = None,
                 year = 0,
                 WATER_VAL = 2,
                 WOOD_VAL = 200,
                 FOOD_VAL = 10,
                 ORE_VAL = 130,
                 ARMY_COST = 1000,
                 NAVY_COST = 100000,
                 AIR_COST = 10000,
                 TECH_FACTOR = .001,
                 ECON_FACTOR = .001,
                 waterlevel = 0):

        self.width = width
        self.height = height

        if not tiles:
            self.tiles = {}
        else:
            self.tiles = tiles

        if not nations:
            self.nations = []
        else:
            self.nations = nations

        if not biomes:
            self.biomes = {}
        else:
            self.biomes = biomes

        self.biomeStrength = biomeStrength
        self.viewMode = viewMode

        if not unclaimed:
            self.unclaimed = []
        else:
            self.unclaimed = unclaimed

        self.year = year
        self.WATER_VAL = WATER_VAL
        self.WOOD_VAL = WOOD_VAL
        self.FOOD_VAL = FOOD_VAL
        self.ORE_VAL = ORE_VAL
        self.TECH_FACTOR = TECH_FACTOR
        self.ECON_FACTOR = ECON_FACTOR
        self.ARMY_COST = ARMY_COST
        self.NAVY_COST = NAVY_COST
        self.AIR_COST = AIR_COST
        self.waterlevel = waterlevel
        self.createWorld()

    def createWorld(self):
        print('Generating Heightmap')
        heightmap = self.generateHeightmap(.5)
        print('Creating tiles')
        generateTile = self.generateTile
        generateTileTerrain = self.generateTileTerrain

        for x in range(0, self.width + 1):
            for y in range(0, self.height + 1):
                height = heightmap[x][y]
                generateTile(x, y, height)
                self.waterlevel += height

        self.waterlevel = self.waterlevel / (self.width * self.height)
        for x in range(0, self.width + 1):
            for y in range(0, self.height + 1):
                generateTileTerrain(x, y, self.waterlevel)
        
            
        print('Generating Resources')
        self.generateResources()
        print('Finding Nations')
        self.findNations()
        print('Initializing Nations')
        self.updateYears(2)
        print('World Generation Complete')

    def generateTile(self, xC, yC, height):
        """Creates a generic tile"""
        t = tile(xCoor = xC, yCoor = yC)
        self.tiles[(xC, yC)] = t
        t.jobs = []
        t.connectedCities = []
        t.improvements = []
        t.height = height
        t.world = self

    def generateTileTerrain(self, xC, yC, waterlevel):
        """Determines the terrain type for a tile"""

        if waterlevel < 0:
            waterlevel = .01

        t = self.tiles[(xC, yC)]
        if t.height < waterlevel:
            t.biome = 1
            t.terrain = 4 # Water
        elif t.height < waterlevel + .07 * waterlevel:
            t.biome = 3
            t.terrain = 1 # Desert
        elif t.height < waterlevel + .15 * waterlevel:
            t.biome = 2
            t.terrain = 0 # Grasslands
        elif t.height < waterlevel + .25 * waterlevel:
            t.biome = 4
            t.terrain = 2 # Forests
        else:
            t.biome = 5
            t.terrain = 3 # Mountains
        t.calcTileColor()
        t.neighbors = self.findNeighbors(xC, yC)   

    def findNeighbors(self, xC, yC):
        """Finds the neighbors of a tile"""
        neighbors = {}
        for x in range(xC - 1, xC + 2):
            for y in range(yC - 1, yC + 2):
                if(x == xC and y == yC):
                    pass
                else:
                   if(x > self.width):
                       x = 0
                   elif(x < 0):
                       x = self.width
                   if(y > self.height):
                       y = 0
                   elif(y < 0):
                       y = self.height
                    
                   neighbors[(x, y)] = self.tiles[(x, y)]

        return neighbors

    def determineTerrain(self, t):
        terrain = random.random()
        #Ungenerated Biome effect
        if(t.biome == -1):
            grass = .01 
            forest = .01 
            desert = .01 
            mountain = .01 
            water = .01 
        #Land biome effect
        elif(t.biome == 0):
            grass = .0005 
            forest = .0004 
            desert = .0001 
            mountain = .0002 
            water = .0001 
        #Water biome effect 
        elif(t.biome == 1):
            grass = .00001 
            forest = .00001 
            desert = .00001 
            mountain = .00001 
            water = .01 
        #Grass biome effect
        elif(t.biome == 2):
            grass = .01 
            forest = .001 
            desert = .001 
            mountain = .001 
            water = .001 
        #Desert biome effect
        elif(t.biome == 3):
            grass = .0001 
            forest = .000001 
            desert = .01 
            mountain = .0005 
            water = .000001 
        #Forest biome effect
        elif(t.biome == 4):
            grass = .005 
            forest = .01 
            desert = .0000001 
            mountain = .0005 
            water = .0001 

        #Mountain biome effect
        elif(t.biome == 5):
            grass = .000001 
            forest = .005 
            desert = .001 
            mountain = .01 
            water = .000001

        #Lake biome effect
        elif(t.biome == 6):
            grass = .005 
            forest = .005 
            desert = .00000001 
            mountain = .0001 
            water = .01 

        else:
            #print(t.biome)
            grass = .1 
            forest = .1
            desert = .1
            mountain = .1 
            water = .1 

        grass = grass * self.biomeStrength
        forest = forest * self.biomeStrength
        desert = desert * self.biomeStrength
        mountain = mountain * self.biomeStrength
        water = water * self.biomeStrength

        for adj in t.neighbors.values():
            if adj.terrain == -1:
                pass
            else:
                #Grass effect
                if adj.terrain == 0:
                    grass += 84.49
                    desert += .5
                    forest += 4.5
                    mountain += 1
                    water += .01
                #Desert effect
                elif adj.terrain == 1:
                    grass += 10
                    desert += 70
                    mountain += 20
                #Forest effect
                elif adj.terrain == 2:
                    grass += 4.5
                    forest += 94.415
                    mountain += .975
                    water += .01
                #Mountain effect
                elif adj.terrain == 3:
                    grass += 1
                    desert += 20
                    forest += .975
                    mountain += 78.015
                    water += .01
                #Water effect
                elif adj.terrain == 4:
                    grass += .01
                    forest += .01
                    mountain += .01
                    water += 99.97

        total = grass + forest + desert + mountain + water
        if total == 0:
            pass
        grassP = grass / total
        desertP = desert / total + grassP
        forestP = forest / total + desertP
        mountainP = mountain / total + forestP
        waterP = water / total + mountainP

        if(terrain <= grassP):
            terrain = 0
        elif(terrain <= desertP and terrain > grassP):
            terrain = 1
        elif(terrain <= forestP and terrain > desertP):
            terrain = 2
        elif(terrain <= mountainP and terrain > forestP):
            terrain = 3
        elif(terrain <= waterP and terrain > mountainP):
            terrain = 4
        else:
            terrain = 4

        return terrain

    def generateHeightmap(self, h):
        """Creates a square heightmap for use in generating terrain.  Uses diamond square algorithm"""

        def square(grid, h, center, size, iteration):
            size = int(size / 2)
            #print(size)
            #print(center)
            #print(iteration)
            top = grid[center[0]][center[1] - size]
            bottom = grid[center[0]][center[1] + size]
            left = grid[center[0] - size][center[1]]
            right = grid[center[0] + size][center[1]]

            tl = grid[center[0] - size][center[1] - size]
            tr = grid[center[0] + size][center[1] - size]
            bl = grid[center[0] - size][center[1] + size]
            br = grid[center[0] + size][center[1] + size]
            ce = grid[center[0]][center[1]]

            grid[int(center[0] - size / 2)][int(center[1] - size / 2)] = (tl + top + left + ce) / 4 + h * (random.random() * 2 - 1) / iteration #Top left of the square
            grid[int(center[0] + size / 2)][int(center[1] - size / 2)] = (tr + top + right + ce) / 4 + h * (random.random() * 2 - 1) / iteration #Top right of the square
            grid[int(center[0] - size / 2)][int(center[1] + size / 2)] = (bl + bottom + left + ce) / 4 + h * (random.random() * 2 - 1) / iteration #Bottom left of the sqaure
            grid[int(center[0] + size / 2)][int(center[1] + size / 2)] = (br + bottom + right + ce) / 4 + h * (random.random() * 2 - 1) / iteration #Bottom right of the square

            newCenters = []
            newCenters.append((int(center[0] - size / 2), int(center[1] - size / 2)))
            newCenters.append((int(center[0] + size / 2), int(center[1] - size / 2)))
            newCenters.append((int(center[0] - size / 2), int(center[1] + size / 2)))
            newCenters.append((int(center[0] + size / 2), int(center[1] + size / 2)))

            return newCenters

        def diamond(grid, h, center, size, iteration):
            size = int(size / 2)
            #print(size)
            #print(center)
            #print(iteration)
            top = (center[0], center[1] - size)
            bottom = (center[0], center[1] + size)
            left = (center[0] - size, center[1])
            right = (center[0] + size, center[1])
            

            tl = grid[center[0] - size][center[1] - size]
            tr = grid[center[0] + size][center[1] - size]
            bl = grid[center[0] - size][center[1] + size]
            br = grid[center[0] + size][center[1] + size]
            ce = grid[center[0]][center[1]]

            #print((center[0] - size, center[1] - size), tl)
            #print((center[0] + size, center[1] - size), tr)
            #print((center[0] - size, center[1] + size), bl)
            #print((center[0] + size, center[1] + size), br)
            #print((center[0], center[1]), ce)

            if grid[top[0]][top[1]] == None:
                grid[top[0]][top[1]] = (tl + tr + ce) / 3 + h * (random.random() * 2 - 1) / iteration
            if grid[bottom[0]][bottom[1]] == None:
                grid[bottom[0]][bottom[1]] = (bl + br + ce) / 3 + h * (random.random() * 2 - 1) / iteration
            if grid[left[0]][left[1]] == None:
                grid[left[0]][left[1]] = (tl + bl + ce) / 3 + h * (random.random() * 2 - 1) / iteration
            if grid[right[0]][right[1]] == None:
                grid[right[0]][right[1]] = (tr + br + ce) / 3 + h * (random.random() * 2 - 1) / iteration

        def recursiveSquare(grid, h, center, size, iteration):
            if size < 1:
                return
            diamond(grid, h, center, size, iteration)
            centers = square(grid, h, center, size, iteration)
            size = int(size / 2)
            iteration += 1
            for c in centers:
                recursiveSquare(grid, h, c, size, iteration)

        rectsize = 0

        if self.width > self.height:
            rectsize = self.width
        else:
            rectsize = self.height

        rectsize = int(pow(2, math.ceil(math.log(rectsize, 2)))) # find the next highest power of two

        if rectsize % 2 != 1:
            rectsize += 1


        grid = [[None for x in range(0, rectsize)] for x in range(0, rectsize)]
        rectsize -= 1

        tl = 1
        tr = 1
        bl = 1
        br = 1

        grid[0][0] = tl
        grid[0][rectsize] = tr
        grid[rectsize][0] = bl
        grid[rectsize][rectsize] = br

        grid[int(rectsize/2)][int(rectsize/2)] = (tl + tr + bl + br) / 4 + h * random.random() * 2
        iteration = 1

        #rectsize = int(rectsize / 2)
        recursiveSquare(grid, h, (int(rectsize / 2), int(rectsize / 2)), rectsize, iteration)
        
        return grid

    def generateResources(self):
        generateTileResources = self.generateTileResources

        for t in self.tiles.values():
            generateTileResources(t)

    def generateTileResources(self, t):
        if t.terrain == 4:
            #Water effect
            t.population = 0
            t.food = 100
            t.water = 100

        elif t.terrain == 0:
            #Grasslands effect
            roll = 2*random.random()
            t.population = int(20 * roll)
            roll = 2*random.random()
            t.food = 1000 * roll
            roll = 2*random.random()
            t.ore = 100 * roll
            roll = 2*random.random()
            t.water = 1000 * roll
            roll = 2*random.random()
            t.wood = 50 * roll
            roll = 2*random.random()
            t.roughness = 5 * roll

        elif t.terrain == 1:
            #Desert Effect
            roll = 2*random.random()
            t.population = int(10 * roll)
            roll = 2*random.random()
            t.food = int(.5 * roll)
            roll = 2*random.random()
            t.ore = 150 * roll
            roll = 2*random.random()
            t.water = 10 * roll
            roll = 2*random.random()
            t.wood = 10 * roll
            t.roughness = 30 * roll

        elif t.terrain == 2:
            #Forest Effect
            roll = 2*random.random()
            t.population = int(5 * roll)
            roll = 2*random.random()
            t.food = 750 * roll
            roll = 2*random.random()
            t.ore = 50 * roll
            roll = 2*random.random()
            t.water = 1500 * roll
            roll = 2*random.random()
            t.wood = 1800 * roll
            roll = 2*random.random()
            t.roughness = 40 * roll

        elif t.terrain == 3:
            #Mountain Effect
            roll = 2*random.random()
            t.population = int(3 * roll)
            roll = 2*random.random()
            t.food = 300 * roll
            roll = 2*random.random()
            t.ore = 3000 * roll
            roll = 2*random.random()
            t.water = 500 * roll
            roll = 2*random.random()
            t.wood = 600 * roll
            roll = 2*random.random()
            t.roughness = 50 * roll

    def changeViewMode(self, mode):
        for t in self.tiles.values():
            t.calcTileColor(mode)

    def findNations(self):
        for t in self.tiles.values():
            if t.population >= 39 and t.owner == None:
                r = int(random.random() * 255)
                g = int(random.random() * 255)
                b = int(random.random() * 255)
                n = nation(world = self,
                           name = (t.xCoor, t.yCoor),
                           color = (r, g, b),
                           tiles = [],
                           cities = [],
                           roads = set(),
                           borders = [],
                           consQueue = [],
                           enemies = [],
                           offers = []
                           )
                n.claimTile(t)
                self.nations.append(n)
                for nb in t.neighbors.values():
                    if nb.owner == None:
                        n.claimTile(nb)
                                    
    def updateUnclaimedLand(self):
        for t in self.tiles.values():
            if t.owner != None:
                pass
            elif t.terrain == 4:
                pass
            else:
                for n in t.neighbors.values():
                    if n.owner == None:
                        pass
                    else:
                        roll = random.random()
                        posMod = n.infra + n.population + n.owner.tech * self.TECH_FACTOR
                        negMod = n.roughness + 1
                        total = posMod + negMod
                        chance = posMod / total
                        if roll < chance:
                            n.owner.claimTile(t)

    def updateBorders(self):
        for t in self.tiles.values():
            if t.owner == None:
                pass
            elif t.terrain == 4:
                pass
            else:
                border = False
                for n in t.neighbors:
                    neighbor = self.tiles[n]
                    if neighbor.owner == None or neighbor.owner != t.owner:
                        border = True
                        break
                if border:
                    t.owner.borders.append(t)
                elif t in t.owner.borders and border == False:
                    t.owner.borders.remove(t)

    def updateTiles(self):
        for t in self.tiles.values():
            if t.terrain == 4:
                pass
            else:
                t.updateTileReadout()
                t.updateResources()
                t.updatePopulation()
                t.updateMilitaryProjection()

    def checkNation(self, country):
        
        if country.population < 1 or country.cities == []:
            print('Nation', str(country.name), 'was destroyed by famine')
            for t in country.tiles:
                t.owner = None
                country.tiles.remove(t)
            self.nations.remove(country)

        country.updateReadout()

    def updateNations(self):
        checkNation = self.checkNation
        for n in self.nations:
            n.findCities()
            n.updatePopulation()
            n.updateResources()
            n.buildResources()
            #n.queueRoads()
            n.buildMilitary()
            n.research()
            n.trade()
            n.wageWar()
            checkNation(n)

    def updateJobs(self):
        for t in self.tiles.values():
            t.doJobs()

    def famine(self, country):
        if country.population < country.foodStorage:
            return
        else:
            count = 0
            while(count < len(country.tiles) and country.food < country.population):
                t = country.tiles[count]
                if t.food < t.population and t.foodStorage <= 0:
                    t.population -= 1
                    country.population -= 1
                count += 1
            if country.population == 0:
                print('Nation', str(country.name), 'was destroyed by famine')
                for t in country.tiles:
                    t.owner = None
                    country.tiles.remove(t)
                self.nations.remove(country)

    def updateWorld(self):
        t0 = time.clock()
        print('')
        print('Updating year', self.year)
        self.year += 1
        print('Updating unclaimed land')
        self.updateUnclaimedLand()
        print('Updating borders')
        self.updateBorders()
        print('Updating tiles')
        self.updateTiles()
        print('Updating nations')
        self.updateNations()
        print('Updating jobs')
        self.updateJobs()
        print('Update complete in ', time.clock() - t0, 'seconds')

    def updateYears(self, years):
        updateWorld = self.updateWorld
        for x in range(0, years):
            updateWorld()
