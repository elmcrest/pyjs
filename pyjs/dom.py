import re
from pyjs import js, js_str, js_object


class TagNameSetterMetaclass(type):
    def __new__(mcls, name, bases, namespace, /, **kwargs):
        tag = re.sub(r'([a-z0-9])([A-Z])', r'\1-\2', name)
        tag = re.sub(r'([A-Z]+)([A-Z][a-z])', r'\1-\2', tag)
        namespace = {"tagName": js_str(tag.lower()), **namespace}
        cls = super().__new__(mcls, name, bases, namespace, **kwargs)
        return cls


@js(builtin=True)
class Event:

    def __init__(self, name: str, bubbles=False, cancelable=False, composed=False):
        self.name = name
        self.bubbles = bubbles
        self.cancelable = cancelable
        self.composed = composed
        self.target = Element()

    def preventDefault(self):
        pass


@js(builtin=True)
class UIEvent(Event):
    pass


@js(builtin=True)
class KeyboardEvent(UIEvent):
    def __init__(self, name: str, bubbles=False, cancelable=False, composed=False):
        super().__init__(name, bubbles=bubbles, cancelable=cancelable, composed=composed)
        self.key = ""
        self.target = HTMLInputElement()


@js(builtin=True)
class CustomEvent(Event):

    def __init__(self, name: str, detail: object=None, bubbles=False, cancelable=False, composed=False):
        super().__init__(name, bubbles=bubbles, cancelable=cancelable, composed=composed)
        self.detail = detail


@js(builtin=True)
class DOMTokenList:

    def __init__(self):
        self.tokens: list[str] = []

    def add(self, *tokens: tuple[str]):
        self.tokens.extend(tokens)

    def remove(self, *tokens: tuple[str]):
        for token in tokens:
            self.tokens.remove(token)


@js(builtin=True)
class EventTarget:

    def addEventListener(self, event: str, listener: callable):
        pass

    def removeEventListener(self, event: str, listener: callable):
        pass

    def dispatchEvent(self, event: Event):
        pass


@js(builtin=True)
class Node(EventTarget):

    def __init__(self):
        super().__init__()
        self.textContent = ""


@js(builtin=True)
class Element(Node):
    tagName = ""

    def __init__(self):
        super().__init__()
        self.children: list[Element] = []
        self.attributes: dict[str,str|int] = {}
        self.classList = DOMTokenList()

    def setAttribute(self, name: str, value: str):
        self.attributes[name] = value

    def append(self, *child: Node):
        self.children.extend(child)

    def remove(self):
        pass

    def querySelector(self, selector: str):
        return self

    def querySelectorAll(self, selector: str):
        return [self]


@js(builtin=True)
class CSSStyleDeclaration:
    def __init__(self):
        self.display = "block"


@js(builtin=True)
class DOMStringMap:

    def __init__(self):
        self.map: dict[str,str] = {}

    @js(inline="{self}[{key}]")
    def __getitem__(self, key: str) -> str:
        return self.map[key]

    @js(inline="{self}[{key}] = {value}")
    def __setitem__(self, key: str, value: str) -> str:
        self.map[key] = value
        return value


@js(builtin=True)
class HTMLElement(Element):

    def __init__(self):
        super().__init__()
        self.style = CSSStyleDeclaration()
        self.dataset = DOMStringMap()

    def focus(self):
        pass

    def blur(self):
        pass


@js(builtin=True)
class HTMLInputElement(HTMLElement):
    def __init__(self):
        super().__init__()
        self.value = ""
        self.checked = False


@js(builtin=True)
class Document:

    @js(analyze=False)
    def createElement(self, name: str) -> HTMLElement:
        e = HTMLElement()
        e.tagName = name
        return e

document = Document()
js_object(document, builtin=True)


@js(builtin=True)
class CustomElementsRegistry:

    def define(self, name: str, element: HTMLElement):
        pass

customElements = CustomElementsRegistry()
js_object(customElements, builtin=True)