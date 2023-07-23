class Scalar:

    __value: dict

    def __init__(self, value: any) -> None:
        if self.__validate(value) == False:
            raise Exception("Invalid scalar") 
        self.__value = value

    def __validate(self, value: any):
        if not isinstance(value, dict):
            return False
        
        if "min" not in value or "max" not in value or "scalar" not in value:
            return False
        
        return True

    @property
    def min(self) -> float:
        return self.__value["min"]
    
    @min.setter
    def min(self, value: float) -> None:
        self.__value["min"] = value

    @property
    def max(self) -> float:
        return self.__value["max"]
    
    @max.setter
    def max(self, value: float) -> None:
        self.__value["max"] = value

    @property
    def scalar(self) -> float:
        return self.__value["scalar"]
    
    @scalar.setter
    def scalar(self, value: float) -> None:
        self.__value["scalar"] = value


class Color:

    __value: dict

    def __init__(self, value: any) -> None:
        if self.__validate(value) == False:
            raise Exception("Invalid color") 
        self.__value = value

    def __validate(self, value: any):
        if not isinstance(value, dict):
            return False
        
        if "red" not in value or value["red"] < 0 or value["red"] > 255:
            return False
        
        if "green" not in value or value["green"] < 0 or value["green"] > 255:
            return False
        
        if "blue" not in value or value["blue"] < 0 or value["blue"] > 255:
            return False
        
        if "alpha" not in value or value["alpha"] < 0 or value["alpha"] > 255:
            return False
        
        return True

    @property
    def red(self) -> int:
        return self.__value["red"]
    
    @red.setter
    def red(self, value: int) -> None:
        if value < 0 or value > 255:
            raise Exception("Invalid value")
        self.__value["red"] = value

    @property
    def green(self) -> int:
        return self.__value["green"]
    
    @green.setter
    def green(self, value: int) -> None:
        if value < 0 or value > 255:
            raise Exception("Invalid value")
        self.__value["green"] = value

    @property
    def blue(self) -> int:
        return self.__value["blue"]
    
    @blue.setter
    def blue(self, value: int) -> None:
        if value < 0 or value > 255:
            raise Exception("Invalid value")
        self.__value["blue"] = value

    @property
    def alpha(self) -> int:
        return self.__value["alpha"]
    
    @alpha.setter
    def alpha(self, value: int) -> None:
        if value < 0 or value > 255:
            raise Exception("Invalid value")
        self.__value["alpha"] = value


class Vector:

    __value: dict

    def __init__(self, value: any) -> None:
        if self.__validate(value) == False:
            raise Exception("Invalid vector") 
        self.__value = value

    def __validate(self, value: any):
        if not isinstance(value, dict):
            return False
        
        if "x" not in value or "y" not in value or "z" not in value or "w" not in value:
            return False
        
        return True

    @property
    def x(self) -> float:
        return self.__value["x"]
    
    @x.setter
    def x(self, value: float) -> None:
        self.__value["x"] = value

    @property
    def y(self) -> float:
        return self.__value["y"]
    
    @y.setter
    def y(self, value: float) -> None:
        self.__value["y"] = value

    @property
    def z(self) -> float:
        return self.__value["z"]
    
    @z.setter
    def z(self, value: float) -> None:
        self.__value["z"] = value

    @property
    def w(self) -> float:
        return self.__value["w"]
    
    @w.setter
    def w(self, value: float) -> None:
        self.__value["w"] = value