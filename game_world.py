objects = [[] for _ in range(5)]

# fill here
collision_pairs = {} # {'boy:ball' : [[boy], [balls]]}

def move_depth(o, depth):
    for i in objects:
        if o in i:
            i.remove(o)
    objects[depth].append(o)
    objects[depth].sort(key=lambda obj:obj.y)
    pass

def add_object(o, depth = 0):
    objects[depth].append(o)

def add_objects(ol, depth = 0):
    objects[depth] += ol

def update():
    for layer in objects:
        for o in layer:
            if type(o) == list:
                o[0].update()
                o[1].update()
            else:
                o.update()


def render():
    for layer in objects:
        for o in layer:
            if type(o) == list:
                o[0].draw()
                o[1].draw()
            else:
                o.draw()

# fill here
def add_collision_pair(group, a = None, b = None): # a와 b 사이에 충돌 검사가 필요하다
    if group not in collision_pairs:
        print(f'new group {group} added...')
        collision_pairs[group] = [ [], [] ]
    if a:
        collision_pairs[group][0].append(a)
    if b:
        collision_pairs[group][1].append(b)


def remove_collision_object(o):
    for pairs in collision_pairs.values():
        if o in pairs[0]:
            pairs[0].remove(o)
        if o in pairs[1]:
            pairs[1].remove(o)

def clear_collision_object():
    collision_pairs.clear()

def remove_object(o):
    for layer in objects:
        if o in layer:
            layer.remove(o)
            remove_collision_object(o)
            del o # 메모리도 날려 주도록
            return
    raise ValueError('Cannot delete non existing object')


def clear():
    clear_collision_object()
    for layer in objects:
        for o in layer:
            remove_collision_object(o)
        layer.clear()


def collide(a, b):

    if type(a) == list:
        la, ba, ra, ta = a[0].get_bb()
    else:
        la, ba, ra, ta = a.get_bb()

    if type(b) == list:
        lb, bb, rb, tb = b[0].get_bb()
    else:
        lb, bb, rb, tb = b.get_bb()

    if la > rb: return False
    if ra < lb: return False
    if ta < bb: return False
    if ba > tb: return False

    return True

def init_collide(a, b):
    if a == b: return False

    if type(a) == list:
        la, ba, ra, ta = a[0].get_init_bb()
    else :
        la, ba, ra, ta = a.get_init_bb()

    if type(b) == list:
        lb, bb, rb, tb = b[0].get_init_bb()
    else:
        lb, bb, rb, tb = b.get_init_bb()

    if la > rb: return False
    if ra < lb: return False
    if ta < bb: return False
    if ba > tb: return False
    return True

def obs_collide(a, b):
    if b.get_obs_bb() == None:
        return (False, None)
    la, ba, ra, ta = a.get_bb()
    coll_list_b = b.get_obs_bb()

    for lb, bb, rb, tb in coll_list_b:
        if la <= rb and ra >= lb and ta >= bb and ba <= tb:
            overlap_left = ra - lb
            overlap_right = rb - la
            overlap_bottom = ta - bb
            overlap_top = tb - ba

            min_overlap = min(overlap_left, overlap_right, overlap_bottom, overlap_top)

            if min_overlap == overlap_left:
                return (True, 'left')
            elif min_overlap == overlap_right:
                return (True, 'right')
            elif min_overlap == overlap_bottom:
                return (True, 'bottom')
            elif min_overlap == overlap_top:
                return (True, 'top')

    return (False, None)  # 모든 객체와의 충돌을 확인한 후에 충돌이 없으면 False 반환



def handle_init_collisions(group):
    flag = True
    for a in collision_pairs[group][0]:
        for b in collision_pairs[group][1]:
            if a is not b and init_collide(a, b):
                flag = False
                if type(a) == list and type(b) == list:
                    a[0].handle_collision(group, b[0])
                else:
                    a.handle_collision(group, b)
    return flag

def handle_collisions(group = None):
    if group == None:
        for g, pairs in collision_pairs.items():
            for a in pairs[0]:
                for b in pairs[1]:
                    if collide(a, b):
                        a.handle_collision(g, b)
                        b.handle_collision(g, a)
    else:
        for a in collision_pairs[group][0]:
            for b in collision_pairs[group][1]:
                if collide(a, b): # a와 b에게 충돌 처리 알아서 하라고 알려줌
                    a.handle_collision(group, b)
                    b.handle_collision(group, a)
    return None

def handle_obs_collisions(group = None):
    if group == None:
        for g, pairs in collision_pairs.items():
            for a in pairs[0]:
                for b in pairs[1]:
                    q = obs_collide(a, b)
                    if q[0]:
                        a.handle_obs_collision(g, b, q[1])
    else:
        for a in collision_pairs[group][0]:
            for b in collision_pairs[group][1]:
                q = obs_collide(a, b)
                if q[0]: # a와 b에게 충돌 처리 알아서 하라고 알려줌
                    a.handle_obs_collision(group, b, q[1])
        return None
