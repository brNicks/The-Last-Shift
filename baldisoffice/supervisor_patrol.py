"""Patrulha nao hostil do supervisor, independente da IA de perseguicao.

A rota respeita paredes e moveis. Funciona com Pygame Rects, mas o algoritmo
nao precisa do Pygame, o que permite testar os caminhos separadamente.
"""
from heapq import heappush, heappop
from math import hypot, sqrt


class SupervisorPatrol:
    CELL = 10
    MARGIN = 3

    def __init__(self, rect, waypoints, blockers, bounds, speed=58.0):
        self.rect = rect
        self.waypoints = tuple((int(x), int(y)) for x, y in waypoints)
        self.blockers = tuple((b.x, b.y, b.width, b.height) for b in blockers)
        self.bounds = tuple(bounds)  # esquerda, cima, direita, baixo
        self.speed = float(speed)
        self.x, self.y = float(rect.x), float(rect.y)
        self.next_waypoint = 0
        self.path = []
        self.dwell = 0.0
        self.route_completions = 0
        self._failures = 0
        self._origin_x = self.bounds[0] + self.MARGIN
        self._origin_y = self.bounds[1] + self.MARGIN
        self._max_i = int((self.bounds[2] - self.MARGIN - rect.width - self._origin_x) // self.CELL)
        self._max_j = int((self.bounds[3] - self.MARGIN - rect.height - self._origin_y) // self.CELL)
        self._free_cache = {}

    def reset(self, x=None, y=None):
        if x is not None:
            self.x = float(x)
            self.rect.x = int(x)
        if y is not None:
            self.y = float(y)
            self.rect.y = int(y)
        self.next_waypoint = 0
        self.path = []
        self.dwell = 0.0
        self.route_completions = 0
        self._failures = 0

    def _free_at(self, x, y):
        l, t, r, b = self.bounds
        w, h = self.rect.width, self.rect.height
        gap = self.MARGIN
        if x < l + gap or y < t + gap or x + w > r - gap or y + h > b - gap:
            return False
        for bx, by, bw, bh in self.blockers:
            if (x < bx + bw + gap and x + w > bx - gap and
                    y < by + bh + gap and y + h > by - gap):
                return False
        return True

    def _grid_xy(self, node):
        return (self._origin_x + node[0]*self.CELL,
                self._origin_y + node[1]*self.CELL)

    def _grid_free(self, node):
        i, j = node
        if not (0 <= i <= self._max_i and 0 <= j <= self._max_j):
            return False
        if node not in self._free_cache:
            self._free_cache[node] = self._free_at(*self._grid_xy(node))
        return self._free_cache[node]

    def _nearest_free(self, x, y):
        ci = round((x-self._origin_x)/self.CELL)
        cj = round((y-self._origin_y)/self.CELL)
        for radius in range(0, 12):
            options = []
            for di in range(-radius, radius+1):
                for dj in range(-radius, radius+1):
                    if max(abs(di), abs(dj)) != radius:
                        continue
                    node = (ci+di,cj+dj)
                    if self._grid_free(node):
                        gx, gy = self._grid_xy(node)
                        options.append(((gx-x)**2+(gy-y)**2,node))
            if options:
                return min(options)[1]
        return None

    def _plan(self, target):
        start = self._nearest_free(self.x, self.y)
        goal = self._nearest_free(*target)
        if start is None or goal is None:
            return []
        open_heap = [(0,0,start)]
        came = {}
        best_cost = {start:0.0}
        counter=0
        neighbors = ((1,0),(-1,0),(0,1),(0,-1),
                     (1,1),(1,-1),(-1,1),(-1,-1))
        def heuristic(node):
            return hypot(node[0]-goal[0], node[1]-goal[1])
        visited=0
        while open_heap and visited < 12000:
            _,_,cur = heappop(open_heap)
            visited+=1
            if cur == goal:
                nodes=[]
                while cur != start:
                    nodes.append(cur)
                    cur=came[cur]
                nodes.reverse()
                # Adiciona primeiro ponto da grade para sair suavemente da
                # posicao inicial, mesmo quando ela nao coincide com a grade.
                return [self._grid_xy(start)] + [self._grid_xy(n) for n in nodes]
            for di,dj in neighbors:
                other=(cur[0]+di,cur[1]+dj)
                if not self._grid_free(other): continue
                # Nao permite atalhos diagonais atravessando quinas.
                if di and dj and (not self._grid_free((cur[0]+di,cur[1])) or
                                   not self._grid_free((cur[0],cur[1]+dj))):
                    continue
                new_cost=best_cost[cur]+(sqrt(2) if di and dj else 1)
                if new_cost < best_cost.get(other, float('inf')):
                    came[other]=cur
                    best_cost[other]=new_cost
                    counter+=1
                    heappush(open_heap,(new_cost+heuristic(other),counter,other))
        return []

    def _finish_waypoint(self):
        self.path.clear()
        self.next_waypoint = (self.next_waypoint+1) % len(self.waypoints)
        if self.next_waypoint == 0:
            self.route_completions += 1
        # Pequena parada de fiscal olhando a sala; tempo deterministico.
        self.dwell = 0.35 + 0.18 * (self.next_waypoint % 4)

    def update(self, dt, paused=False):
        if paused or dt <= 0 or not self.waypoints:
            return
        dt = min(float(dt), 0.05)
        if self.dwell > 0:
            self.dwell=max(0,self.dwell-dt)
            return
        if not self.path:
            self.path=self._plan(self.waypoints[self.next_waypoint])
            if not self.path:
                self._finish_waypoint()
                return
        # Evita saltos longos e atravessamento dos moveis por lag na janela.
        remaining=self.speed*dt
        while remaining > 0.0001 and self.path:
            tx,ty = self.path[0]
            dx,dy=tx-self.x,ty-self.y
            distance=hypot(dx,dy)
            if distance < 0.75:
                self.x,self.y=float(tx),float(ty)
                self.path.pop(0)
                continue
            step=min(remaining,distance)
            nx=self.x+dx/distance*step
            ny=self.y+dy/distance*step
            if not self._free_at(nx,ny):
                self._failures += 1
                self.path.clear()
                if self._failures >= 3:
                    self._failures=0
                    self._finish_waypoint()
                break
            self.x,self.y=nx,ny
            remaining-=step
        self.rect.x=int(round(self.x))
        self.rect.y=int(round(self.y))
        if not self.path:
            self._failures=0
            self._finish_waypoint()
