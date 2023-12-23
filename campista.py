class campista:
    def __init__(self,nombre, apellido, equipo, versiculo,capitulo_pequeno,capitulo_grande):
        self.__nombre=nombre,
        self.__apellido = apellido,
        self.__equipo = equipo,
        self.__versiculo = versiculo,
        self.__capitulo_pequeno = capitulo_pequeno,
        self.__capitulo_grande = capitulo_grande

    @property
    def nombre(self):
        return self.__nombre

    @nombre.setter
    def nombre(self, new_value):
        self.__nombre = new_value



    @property
    def apellido(self):
        return self.__nombre

    @apellido.setter
    def apellido(self, new_value):
        self.__apellido = new_value

    @property
    def equipo(self):
        return self.__equipo

    @equipo.setter
    def equipo(self, new_value):
        self.__equipo = new_value

    @property
    def versiculo(self):
        return self.__versiculo

    @versiculo.setter
    def versiculo(self, new_value):
        self.__versiculo = new_value

    @property
    def capitulo_pequeno(self):
        return self.__capitulo_pequeno

    @versiculo.setter
    def capitulo_pequeno(self, new_value):
        self.__capitulo_pequeno= new_value

    @property
    def capitulo_grande(self):
        return self.__capitulo_grande

    @capitulo_grande.setter
    def capitulo_pequeno(self, new_value):
        self.__capitulo_grande = new_value


campista1=campista("Eunice","Portilla","Rojo",0,0,0)