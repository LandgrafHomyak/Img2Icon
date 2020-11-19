"""
Template classes interface for python like in c++
in C++: any_class<any>
in Python: any_class[any]
"""

from typing import Iterable, Type, Tuple, Union, NoReturn, Any, Dict, TypeVar

BC = TypeVar("BC")


class template(type):  # Template class interface creates classes, not objects
    def __new__(mcs, c: Type[BC], patterns: Union[Iterable[str], Tuple[str], str]) -> Any:
        return super().__new__(mcs, c.__name__, tuple(), dict())

    def __init__(cls, c: Type, patterns: Union[Iterable[str], Tuple[str], str]) -> NoReturn:
        super().__init__(c.__name__, tuple(), dict())
        cls.__cls: Type[BC] = c

        cls.__patterns: Tuple[str] = patterns
        if not isinstance(patterns, tuple):
            if not isinstance(patterns, Iterable) or isinstance(patterns, (bytes, str)):
                cls.__patterns = (patterns,)
            else:
                cls.__patterns = tuple(patterns)

        cls.__cache: Dict[Tuple[str], Type[BC]] = dict()

        cls.__mcs: Type = type(c.__name__, (type,), {
            # "__class_getitem__": lambda __cls, __p: cls.__getitem__(__p),
            "__class__": property(fget=lambda __cls: cls),  # makes possible 'any_class[any].__class__[not_any]'
            **{
                patterns[i]: property(fget=lambda __cls: getattr(__cls, "__" + patterns[i]))
                for i in range(len(patterns))
                # makes possible 'any_class[any].TEMP_TYPE', without it only 'any_class[any]().TEMP_TYPE'
            }
        })

    def __getitem__(cls, patterns: Union[Iterable[Type[Any]], Tuple[Type[Any]], str]) -> Type[BC]:
        if not isinstance(patterns, tuple):
            if not isinstance(patterns, Iterable):
                patterns = (patterns,)
            else:
                patterns = tuple(patterns)

        if len(patterns) != len(cls.__patterns):
            raise TypeError

        if patterns not in cls.__cache:
            cls.__cache[patterns] = cls.__mcs(
                f"{cls.__cls.__name__}[{', '.join(map(lambda t: t.__name__, patterns))}]",  # beautiful name
                (cls.__cls,),  # coping methods from the target class
                {
                    **{cls.__patterns[i]: property(fget=cls.__mk_mtd(patterns[i])) for i in range(len(patterns))},
                    # makes possible 'any_class[any]().TEMP_TYPE'
                    **{"__" + cls.__patterns[i]: patterns[i] for i in range(len(patterns))},
                    # data for metaclass properties
                }
            )

        return cls.__cache[patterns]

    @staticmethod
    def __mk_mtd(v):
        """
        makes method with values created in inline loop
        """
        return lambda self: v

    @classmethod
    def decorator(mcs, patterns):
        def class_template_decorator(cls):
            return mcs(cls, patterns)

        return class_template_decorator


if __name__ == "__main__":
    class HelloWorld:
        def hello_name(self):
            print("Hello", self.PERSON.name)


    class Vasya:
        name = "Vasya"


    class Petya:
        name = "Petya"


    HelloWorld = template(HelloWorld, "PERSON")

    vasya_class = HelloWorld[Vasya]()
    vasya_class.hello_name()  # Hello Vasya

    petya_class = HelloWorld[Petya]()
    petya_class.hello_name()  # Hello Petya


    @template.decorator(("KT", "VT"))  # other way to set interface
    class DictWithTypeCheck(dict):
        def __setitem__(self, key, value):
            if not isinstance(key, self.KT):
                raise TypeError
            if not isinstance(value, self.VT):
                raise TypeError
            super().__setitem__(key, value)


    int_str_dict = DictWithTypeCheck[int, str]()

    try:
        int_str_dict[1] = "1"  # succesful
    except:
        pass

    try:
        int_str_dict[True] = "true"  # error
    except:
        pass

    try:
        int_str_dict[1] = True  # error
    except:
        pass

    print(int_str_dict)  # {1: 'true'}

    print(DictWithTypeCheck[int, int].__name__)  # DictWithTypeCheck[int, int]