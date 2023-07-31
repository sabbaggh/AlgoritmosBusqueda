## 0 es Muro     1 es Road     2 es Swamp     3 es Snow
## 4 es grass    5 es Water    6 es Mountain

## Poner los pesos en ese orden, si no puede pasar, solo dejalo como Null yo que se xd

class Humano:
    nombre = 'Humano'
    img_Path = 'menu_items\humano.png'
    terr_disp = ["1", "2", "3", "4", "5"]
    pesos = [0, 1, 4, 4, 2, 3, 0]


class Monkey:
    nombre = 'Mono'
    img_Path = 'menu_items\mono.png'
    terr_disp = ["1", "2", "3", "4"]
    pesos = [0, 2, 3, 5, 1, 0, 0]


class Octopus:
    nombre = 'Pulpo'
    img_Path = 'menu_items\pulpo.png'
    terr_disp = ["1", "2", "3", "5"]
    pesos = [0, 4, 2, 3, 0, 1, 0]


class Sasquatch:
    nombre = 'Pie Grande'
    img_Path = 'menu_items\pie_grande.png'
    terr_disp = ["1", "2", "3", "6"]
    pesos = [0, 15, 2, 2, 0, 0, 5]


